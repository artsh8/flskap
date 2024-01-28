FROM python:3.11

WORKDIR /flskap

COPY requirements.txt .
COPY ./archivers/archive_pb2.py ./archivers/archive_pb2.py
COPY ./archivers/archive_pb2_grpc.py ./archivers/archive_pb2_grpc.py
COPY archive_client.py ./archivers/archive_client.py
RUN pip install -r requirements.txt
ENV KAFKA_BOOTSTRAP_SERVERS='localhost:9094'
ENV CLICK_PORT=8123
ENV CLICK_HOST='localhost'
ENV CLICK_USR='username'
ENV CLICK_PASS='password'
ENV GRPC_PORT='localhost:50051'

CMD ["python", "./archivers/archive_client.py"]