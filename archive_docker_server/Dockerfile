FROM python:3.11

WORKDIR /flskap

COPY requirements.txt .
COPY ./archive_docker_client/archivers/archive_pb2.py ./archivers/archive_pb2.py
COPY ./archive_docker_client/archivers/archive_pb2_grpc.py ./archivers/archive_pb2_grpc.py
COPY archive_server.py ./archivers/archive_server.py
COPY scylla_setup.py .
RUN pip install -r requirements.txt
ENV SCY_PORT=9042
ENV MAX_WORKERS=2
ENV GRPC_PORT='localhost:50051'

CMD python scylla_setup.py && python ./archivers/archive_server.py