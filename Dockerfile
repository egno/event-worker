FROM python:3.6-slim-stretch

COPY . /app

RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

VOLUME ["/app", "/opt/data/queue"]

CMD ["python", "main.py"]
