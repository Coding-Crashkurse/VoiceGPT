
FROM python:3.10-slim-buster

WORKDIR /app


RUN apt-get update && apt-get install -y ffmpeg

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py
ENV ELEVENLABS_KEY=<api_key>
ENV OPENAI_KEY=<api_key>

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
