from faker import Faker
import uuid


def generate_row():
    fake = Faker()
    description = ' '.join([fake.word() for i in range(6)])
    description = description.capitalize() + '.'
    customer_id = fake.random_int(min=1, max=1000)
    dt = fake.date_between('-5y', 'today')
    year, month, day = dt.year, dt.month, dt.day
    amount = fake.random_number(digits=7, fix_len=False) / 100
    transaction_type = fake.random_element([0, 1, 2])
    transaction_id = uuid.uuid4()
    row_for_insert = (transaction_id, year, month, day, customer_id, amount, transaction_type, description)
    return row_for_insert
