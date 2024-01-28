from cassandra.cluster import Cluster
import os
import time

time.sleep(120)

cluster = Cluster([os.getenv('SCY_HOST')], port=os.getenv('SCY_PORT'))
session = cluster.connect()

session.execute('''CREATE KEYSPACE test_db
                    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
                ''')
session.execute('use test_db;')
session.execute('''CREATE TABLE fin_t_a (
                    transaction_id uuid,
                    year int,
                    month int,
                    day int,
                    customer_id int,
                    amount decimal,
                    transaction_type int,
                    description varchar,
                    is_archived boolean,
                    PRIMARY KEY ((year), transaction_id)
                );
                ''')
session.execute('CREATE INDEX is_archived_index ON fin_t_a (is_archived);')

session.shutdown()
cluster.shutdown()
print('Таблица создана')
