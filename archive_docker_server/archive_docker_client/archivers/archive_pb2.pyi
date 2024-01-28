from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TransactionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CREDIT: _ClassVar[TransactionType]
    DEBIT: _ClassVar[TransactionType]
    TRANSFER: _ClassVar[TransactionType]
CREDIT: TransactionType
DEBIT: TransactionType
TRANSFER: TransactionType

class ArchiveRequest(_message.Message):
    __slots__ = ("request_string",)
    REQUEST_STRING_FIELD_NUMBER: _ClassVar[int]
    request_string: str
    def __init__(self, request_string: _Optional[str] = ...) -> None: ...

class TransactionInfo(_message.Message):
    __slots__ = ("transaction_id", "date", "customer_id", "amount", "transaction_type", "description")
    TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    transaction_id: str
    date: str
    customer_id: int
    amount: float
    transaction_type: TransactionType
    description: str
    def __init__(self, transaction_id: _Optional[str] = ..., date: _Optional[str] = ..., customer_id: _Optional[int] = ..., amount: _Optional[float] = ..., transaction_type: _Optional[_Union[TransactionType, str]] = ..., description: _Optional[str] = ...) -> None: ...

class ArchiveReply(_message.Message):
    __slots__ = ("transaction_info",)
    TRANSACTION_INFO_FIELD_NUMBER: _ClassVar[int]
    transaction_info: _containers.RepeatedCompositeFieldContainer[TransactionInfo]
    def __init__(self, transaction_info: _Optional[_Iterable[_Union[TransactionInfo, _Mapping]]] = ...) -> None: ...

class AckRequest(_message.Message):
    __slots__ = ("request_string", "year", "transaction_id")
    REQUEST_STRING_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    request_string: str
    year: int
    transaction_id: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, request_string: _Optional[str] = ..., year: _Optional[int] = ..., transaction_id: _Optional[_Iterable[str]] = ...) -> None: ...

class AckReply(_message.Message):
    __slots__ = ("reply",)
    REPLY_FIELD_NUMBER: _ClassVar[int]
    reply: str
    def __init__(self, reply: _Optional[str] = ...) -> None: ...
