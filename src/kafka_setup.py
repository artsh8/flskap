from kafka.admin import KafkaAdminClient, NewTopic
import os
import time

time.sleep(30)
topic_name = 'gen_tasks'
topic_name_partitioned = topic_name + '_partitioned'


admin = KafkaAdminClient(
    client_id='admin',
    bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
    security_protocol='PLAINTEXT'
)


topic = NewTopic(name=topic_name_partitioned, num_partitions=2, replication_factor=1)
admin.create_topics([topic], timeout_ms=int(5000))
print('Топик создан')
