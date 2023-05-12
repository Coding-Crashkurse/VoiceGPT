from flask import Flask, render_template, request, redirect, url_for, session, make_response
from elevenlabslib import ElevenLabsUser
from io import BytesIO
import openai
import os

openai.api_key = os.environ.get("OPENAI_KEY")

user = ElevenLabsUser(os.environ.get("ELEVENLABS_KEY"))

app = Flask(__name__)
app.secret_key = 'your secret key'

@app.before_request
def require_login():
    if not 'logged_in' in session and request.endpoint != 'login':
        return redirect(url_for('login'))


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'test' or request.form['password'] != 'test':
            error = 'Ungültige Anmeldeinformationen. Bitte versuchen Sie es erneut.'
        else:
            session['logged_in'] = True
            return redirect(url_for('index'))
    return render_template('login.html', error=error)



@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    audio_file  = request.files.get('audio')
    voice = request.form.get('voice')

    if not audio_file:
        return 'Keine Audiodatei im Request gefunden', 400

    audio_data = audio_file.read()


    with open('audio.mp4', 'wb') as file:
        file.write(audio_data)

    new_file = open("./audio.mp4", "rb")
    transcript = openai.Audio.transcribe("whisper-1", new_file)
    print(transcript.text)

    output = openai.Completion.create(
    model="text-davinci-003",
    prompt=transcript.text,
    max_tokens=250,
    temperature=0.7
    )

    print(output['choices'][0]['text'])
    voice = user.get_voices_by_name(voice)[0]
    audio_output = voice.generate_audio_bytes(output['choices'][0]['text'], model_id="eleven_multilingual_v1")

    response = make_response(audio_output)
    response.headers.set('Content-Type', 'audio/mpeg')
    response.headers.set('Content-Disposition', 'attachment', filename='output.mp3')

    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=4000, debug=True)
