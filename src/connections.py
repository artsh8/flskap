from flask import g
import clickhouse_connect

class DbClick:

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def connect_db(self):
        return clickhouse_connect.get_client(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password
        )

    def get_db(self):
        if not hasattr(g, 'link_db'):
            g.link_db = self.connect_db()
        return g.link_db

    def query_db(self, sql):
        db = self.get_db()
        try:
            result = db.query(sql)
            if result:
                print(result.result_rows)
                return result.result_rows
        except:
            print('Ошибка чтения из БД')
        return []

    def close_connection(self, error):
        if hasattr(g, 'link_db'):
            g.link_db.close()
