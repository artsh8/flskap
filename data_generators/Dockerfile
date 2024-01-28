FROM python:3.11

WORKDIR /data_generators

COPY requirements.txt .
COPY generator.py .
COPY generator_0.py .
RUN pip install -r requirements.txt
ENV SCY_HOST='127.0.0.1'
ENV SCY_PORT=9042
ENV KAFKA_BOOTSTRAP_SERVERS='localhost:9094'
ENV KAFKA_PARTITION=0

CMD ["python", "./generator_0.py"]