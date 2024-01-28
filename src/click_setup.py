import os
import clickhouse_connect
import time

# time.sleep(10)
click = clickhouse_connect.get_client(
    host=os.getenv('CLICK_HOST'),
    port=os.getenv('CLICK_PORT'),
    username=os.getenv('CLICK_USR'),
    password=os.getenv('CLICK_PASS')
)

click.query('CREATE DATABASE test_db;')
click.query(
    '''
    CREATE TABLE test_db.fin_t_a
    (
        `transaction_id` UUID,
        `date` Date,
        `customer_id` UInt32,
        `amount` Decimal32(2),
        `type` Enum('credit' = 0, 'debit' = 1, 'transfer' = 3),
        `description` String
    )
    ENGINE = MergeTree
    PRIMARY KEY (date, customer_id);
    '''
)
click.close()
print('Таблица создана')