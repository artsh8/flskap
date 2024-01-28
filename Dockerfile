FROM python:3.11

WORKDIR /flskap

COPY requirements.txt .
COPY ./src ./src
RUN pip install -r requirements.txt
ENV CLICK_PORT=8123
ENV CLICK_HOST='localhost'
ENV CLICK_USR='username'
ENV CLICK_PASS='password'
ENV FLSK_SECRET_KEY='kjkj2~529%85tj*kbbj?hdfs!'
ENV FLSK_DEBUG=True
ENV FLSK_HOST='0.0.0.0'
ENV FLSK_PORT=5000
ENV KAFKA_BOOTSTRAP_SERVERS='localhost:9094'


CMD python ./src/kafka_setup.py && python ./src/click_setup.py && python ./src/flskapp.py