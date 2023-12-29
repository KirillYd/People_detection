FROM python:3.10

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /main

COPY . .

CMD ["python", "/main/main.py"]