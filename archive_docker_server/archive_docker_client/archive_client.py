import archive_pb2, archive_pb2_grpc
import grpc
from kafka import KafkaConsumer
import json
import clickhouse_connect
from enum import Enum
import uuid
from datetime import datetime
import os
import time

time.sleep(30)

class TransactionType(Enum):
    CREDIT = 0
    DEBIT = 1
    TRANSFER = 2


group_id = 'group2'
topic_name = 'archive_tasks'
consumer = KafkaConsumer(
    client_id='client1',
    group_id=group_id,
    bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
    security_protocol='PLAINTEXT',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    key_deserializer=lambda v: json.loads(v.decode('utf-8')),
    max_poll_records=10
)
consumer.subscribe(topics=[topic_name])

click = clickhouse_connect.get_client(
    host=os.getenv('CLICK_HOST'),
    port=int(os.getenv('CLICK_PORT')),
    username=os.getenv('CLICK_USR'),
    password=os.getenv('CLICK_PASS')
)


def run():
    with grpc.insecure_channel(os.getenv('GRPC_PORT')) as channel:
        stub = archive_pb2_grpc.ArchiverStub(channel)
        for message in consumer:
            print("%d:%d: k=%s v=%s" % (message.partition,
                                        message.offset,
                                        message.key,
                                        message.value))
            print(message.value['create_task'])
            archive_request = archive_pb2.ArchiveRequest(request_string=message.value['create_task'])
            archive_reply = stub.Archive(archive_request)
            ti_list = archive_reply.transaction_info
            if not ti_list:
                print('Нет данных к архивации')
            else:
                # print(archive_reply)
                data_for_insert = []
                for ti in ti_list:
                    row_for_insert = [
                        uuid.UUID(ti.transaction_id),
                        datetime.strptime(ti.date, '%Y-%m-%d').date(),
                        ti.customer_id,
                        ti.amount,
                        TransactionType(ti.transaction_type).name.lower(),
                        ti.description
                    ]
                    data_for_insert.append(row_for_insert)
                print(data_for_insert)
                transaction_id_list = [str(i[0]) for i in data_for_insert]
                print(transaction_id_list)
                click.insert(
                    'test_db.fin_t_a', data_for_insert,
                    ['transaction_id', 'date', 'customer_id', 'amount', 'type', 'description']
                )
                ack_request = archive_pb2.AckRequest(
                    request_string='archived_successfully',
                    year=int(message.value['create_task'])
                )
                ack_request.transaction_id.extend(transaction_id_list)
                ack_reply = stub.Ack(ack_request)
                print(ack_reply)

print('Сервис запущен успешно')
run()
