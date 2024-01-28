from kafka import KafkaConsumer, TopicPartition
import json
import os
from generator import generate_row
from cassandra.cluster import Cluster
import time

time.sleep(150)
cluster = Cluster([os.getenv('SCY_HOST')], port=os.getenv('SCY_PORT'))
session = cluster.connect('test_db')

group_id = 'group1'

topic_name = 'gen_tasks'
topic_name_partitioned = topic_name + '_partitioned'

consumer_partition_0 = KafkaConsumer(
    # client_id='client1',
    group_id=group_id + '_partitioned',
    bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
    security_protocol='PLAINTEXT',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    key_deserializer=lambda v: json.loads(v.decode('utf-8')),
    max_poll_records=10
)

# consumer.topics()
consumer_partition_0.assign([TopicPartition(topic_name_partitioned, int(os.getenv('KAFKA_PARTITION')))])
# consumer.subscription()
print('Контейнер запущен успешно')

for message in consumer_partition_0:
    print("%d:%d: k=%s v=%s" % (message.partition,
                                 message.offset,
                                 message.key,
                                 message.value))
    print(message.value)
    generated_row = generate_row()
    print(generated_row)
    session.execute(
        """
        INSERT INTO fin_t_a (transaction_id, year, month, day, customer_id, amount, transaction_type, description, is_archived)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """,
        (generated_row[0], generated_row[1], generated_row[2], generated_row[3], generated_row[4], generated_row[5], generated_row[6], generated_row[7], False)
    )
