from flask import Flask, render_template, request, flash, redirect
import io
import os
import base64
import numpy as np
import matplotlib
matplotlib.use('agg')  # нужно для использования матплотлиба в api-режиме
import matplotlib.pyplot as plt
from kafka import KafkaProducer
import json
from connections import DbClick


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLSK_SECRET_KEY')
click = DbClick(
    host=os.getenv('CLICK_HOST'),
    port=os.getenv('CLICK_PORT'),
    username=os.getenv('CLICK_USR'),
    password=os.getenv('CLICK_PASS')
)


@app.teardown_appcontext
def close_db(error):
    click.close_connection(error)


def get_metric(date_from, date_to):
    sql = f'''SELECT customer_id, ROUND(AVG(amount),2)
            FROM test_db.fin_t_a 
            WHERE  date > '{date_from}' AND date < '{date_to}'
            GROUP BY customer_id
            ORDER BY AVG(amount) DESC
            LIMIT 10'''
    return click.query_db(sql)


def get_sum_by_type(date_from, date_to):
    sql = f'''SELECT type, SUM(amount)
            FROM test_db.fin_t_a
            WHERE  date > '{date_from}' AND date < '{date_to}'
            GROUP BY type'''
    return click.query_db(sql)


def get_transactions_by_date(date_from, date_to):
    sql = f'''SELECT date, medianExact(amount)
            FROM test_db.fin_t_a
            WHERE date IN (
                SELECT date
                FROM test_db.fin_t_a
                WHERE date > '{date_from}' AND date < '{date_to}'
                GROUP BY date
                ORDER BY COUNT(transaction_id) DESC
                LIMIT 10
            )
            GROUP BY date
            ORDER BY date'''
    return click.query_db(sql)


def row_to_list(rows, index):
    return [row[index] for row in rows]


def pie_chart(rows):
    y = np.array(row_to_list(rows, 1))
    lables = row_to_list(rows, 0)
    fig, ax = plt.subplots(figsize=(6, 6))
    plt.pie(y, labels=lables)
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url


def line_chart(rows):
    xpoints = np.array(row_to_list(rows, 0))
    ypoints = np.array(row_to_list(rows, 1))
    fig, ax = plt.subplots(figsize=(9, 9))
    plt.plot(xpoints, ypoints, marker='o')
    plt.xlabel('Даты')
    plt.ylabel('Медианная стоимость покупки')
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url


@app.route('/count_data', methods=['POST'])
def count_data():
    sql = """SELECT COUNT(*) FROM test_db.fin_t_a"""
    result = click.query_db(sql)
    response = f"""<input type="number" id="count_viewer" value="{result[0][0]}" disabled>"""
    return response


def create_tasks(rows_num):
    producer = KafkaProducer(
        bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
        security_protocol='PLAINTEXT',
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    topic_name = 'gen_tasks'
    topic_name_partitioned = topic_name + '_partitioned'
    for i in range(1, rows_num + 1):
        if i % 2 == 0:  # если четное, то партиция 0
            producer.send(
                topic_name_partitioned,
                key={'id': 0},
                value={'create_task': 'true'}
            )
        else:  # иначе партиция 1
            producer.send(
                topic_name_partitioned,
                key={'id': 1},
                value={'create_task': 'true'}
            )
    producer.flush()


@app.route('/generate_data', methods=['POST', 'GET'])
def generate_data():
    if request.method == 'POST':
        rows_num = int(request.form['rows_num'])
        try:
            create_tasks(rows_num)
            flash('Задача на генерацию поставлена', category='success')
        except:
            flash('Ошибка при постановке задачи', category='error')
        finally:
            return redirect('/')
    return redirect('/')


@app.route('/add_archive_task', methods=['POST', 'GET'])
def add_archive_task():
    producer = KafkaProducer(
        bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
        security_protocol='PLAINTEXT',
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    if request.method == 'POST':
        topic_name = 'archive_tasks'
        try:
            producer.send(
                topic_name,
                key={'id': 0},
                value={'create_task': request.form['archive_year']}
            )
            producer.flush()
            flash('Задача на архивирование поставлена', category='success')
        except:
            flash('Ошибка при постановке задачи', category='error')
        finally:
            return redirect('/')
    return redirect('/')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/show_metric', methods=['POST', 'GET'])
def show_metric():
    if request.method == 'POST':
        data_header = 'Данные'
        date_from = request.form['date_from']
        date_to = request.form['date_to']
        headings = ('Покупатель', 'Средняя сумма покупки')
        try:
            metric = get_metric(date_from, date_to)
            img_pie = None if not metric else pie_chart(get_sum_by_type(date_from, date_to))
            img_line = None if not metric else line_chart(get_transactions_by_date(date_from, date_to))
            plt.close('all')
        except:
            flash('Ошибка при подключении к БД', category='error')
            return redirect('/')
    else:
        data_header = 'Запросите данные'
        metric = []
        img_pie, img_line, headings = None, None, None
    return render_template(
        'metric.html',
        data_header=data_header,
        headings=headings,
        metric=metric,
        img_pie=img_pie,
        img_line=img_line
    )


if __name__ == "__main__":
    app.run(
        debug=os.getenv('FLSK_DEBUG'),
        host=os.getenv('FLSK_HOST'),
        port=os.getenv('FLSK_PORT')
    )
