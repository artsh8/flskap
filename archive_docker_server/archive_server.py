from concurrent import futures
import grpc
import archive_pb2, archive_pb2_grpc
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from datetime import date
import uuid
import os


cluster = Cluster([os.getenv('SCY_HOST')], port=os.getenv('SCY_PORT'))
session = cluster.connect('test_db')


class ArchiverServicer(archive_pb2_grpc.ArchiverServicer):
    def Archive(self, request, context):
        print('Создан запрос на архивирование')
        scy_result = session.execute(
            '''
            SELECT year, month, day, customer_id, transaction_id, amount, transaction_type, description
            FROM fin_t_a
            WHERE year = %s
            AND is_archived = false;
            ''', (int(request.request_string),)
        )
        scy_result_list = []
        for row in scy_result:
            ti = archive_pb2.TransactionInfo()
            ti.date = str(date(row.year, row.month, row.day))
            ti.customer_id = row.customer_id
            ti.transaction_id = str(row.transaction_id)
            ti.amount = row.amount
            ti.transaction_type = row.transaction_type
            ti.description = row.description
            scy_result_list.append(ti)
        archive_reply = archive_pb2.ArchiveReply()
        archive_reply.transaction_info.extend(scy_result_list)
        print(archive_reply)
        return archive_reply

    def Ack(self, request, context):
        print(request.request_string)
        transaction_id_list = request.transaction_id
        uuid_list = [uuid.UUID(i) for i in transaction_id_list]
        batch = BatchStatement()
        vals = []
        for i in uuid_list:
            vals.append((request.year, i))
        # print(vals)
        stmt = session.prepare(
            '''
            UPDATE fin_t_a
            SET is_archived = true
            WHERE year = ?
            AND transaction_id = ?;
            '''
        )
        for i in vals:
            batch.add(stmt, i)
        session.execute(batch)
        ack_reply = archive_pb2.AckReply()
        ack_reply.reply = 'success'
        print(ack_reply)
        return ack_reply


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=int(os.getenv('MAX_WORKERS'))))
    archive_pb2_grpc.add_ArchiverServicer_to_server(ArchiverServicer(), server)
    server.add_insecure_port(os.getenv('GRPC_PORT'))
    server.start()
    server.wait_for_termination()

print('Сервис запущен успешно')
serve()
