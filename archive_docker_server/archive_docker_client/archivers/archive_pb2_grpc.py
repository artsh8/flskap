# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import archive_pb2 as archive__pb2


class ArchiverStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Archive = channel.unary_unary(
                '/archive.Archiver/Archive',
                request_serializer=archive__pb2.ArchiveRequest.SerializeToString,
                response_deserializer=archive__pb2.ArchiveReply.FromString,
                )
        self.Ack = channel.unary_unary(
                '/archive.Archiver/Ack',
                request_serializer=archive__pb2.AckRequest.SerializeToString,
                response_deserializer=archive__pb2.AckReply.FromString,
                )


class ArchiverServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Archive(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Ack(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ArchiverServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Archive': grpc.unary_unary_rpc_method_handler(
                    servicer.Archive,
                    request_deserializer=archive__pb2.ArchiveRequest.FromString,
                    response_serializer=archive__pb2.ArchiveReply.SerializeToString,
            ),
            'Ack': grpc.unary_unary_rpc_method_handler(
                    servicer.Ack,
                    request_deserializer=archive__pb2.AckRequest.FromString,
                    response_serializer=archive__pb2.AckReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'archive.Archiver', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Archiver(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Archive(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/archive.Archiver/Archive',
            archive__pb2.ArchiveRequest.SerializeToString,
            archive__pb2.ArchiveReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Ack(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/archive.Archiver/Ack',
            archive__pb2.AckRequest.SerializeToString,
            archive__pb2.AckReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
