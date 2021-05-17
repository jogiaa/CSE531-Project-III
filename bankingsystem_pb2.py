# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bankingsystem.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='bankingsystem.proto',
  package='bankingsystem',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x13\x62\x61nkingsystem.proto\x12\rbankingsystem\"b\n\ninputEvent\x12\n\n\x02id\x18\x01 \x01(\t\x12+\n\tinterface\x18\x02 \x01(\x0e\x32\x18.bankingsystem.operation\x12\r\n\x05money\x18\x03 \x01(\x05\x12\x0c\n\x04\x64\x65st\x18\x04 \x01(\x05\"{\n\x0b\x42\x61nkRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12#\n\x04type\x18\x03 \x01(\x0e\x32\x15.bankingsystem.entity\x12)\n\x06\x65vents\x18\x02 \x03(\x0b\x32\x19.bankingsystem.inputEvent\x12\x10\n\x08writeSet\x18\x04 \x03(\t\"t\n\x0boutputEvent\x12+\n\tinterface\x18\x01 \x01(\x0e\x32\x18.bankingsystem.operation\x12)\n\x06result\x18\x02 \x01(\x0e\x32\x19.bankingsystem.resultType\x12\r\n\x05money\x18\x03 \x01(\x05\"V\n\x0c\x42\x61nkResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12(\n\x04recv\x18\x02 \x03(\x0b\x32\x1a.bankingsystem.outputEvent\x12\x10\n\x08writeSet\x18\x03 \x03(\t*,\n\x06\x65ntity\x12\x0c\n\x08\x63ustomer\x10\x00\x12\n\n\x06\x62ranch\x10\x01\x12\x08\n\x04\x62\x61nk\x10\x02*o\n\toperation\x12\r\n\tpropagate\x10\x00\x12\x15\n\x11propagate_deposit\x10\x05\x12\x16\n\x12propagate_withdraw\x10\x01\x12\x0b\n\x07\x64\x65posit\x10\x02\x12\t\n\x05query\x10\x03\x12\x0c\n\x08withdraw\x10\x04*3\n\nresultType\x12\x0b\n\x07unknown\x10\x00\x12\x0b\n\x07\x66\x61ilure\x10\x01\x12\x0b\n\x07success\x10\x02\x32W\n\x0bTransaction\x12H\n\x0bMsgDelivery\x12\x1a.bankingsystem.BankRequest\x1a\x1b.bankingsystem.BankResponse\"\x00\x62\x06proto3'
)

_ENTITY = _descriptor.EnumDescriptor(
  name='entity',
  full_name='bankingsystem.entity',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='customer', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='branch', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='bank', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=469,
  serialized_end=513,
)
_sym_db.RegisterEnumDescriptor(_ENTITY)

entity = enum_type_wrapper.EnumTypeWrapper(_ENTITY)
_OPERATION = _descriptor.EnumDescriptor(
  name='operation',
  full_name='bankingsystem.operation',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='propagate', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='propagate_deposit', index=1, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='propagate_withdraw', index=2, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='deposit', index=3, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='query', index=4, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='withdraw', index=5, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=515,
  serialized_end=626,
)
_sym_db.RegisterEnumDescriptor(_OPERATION)

operation = enum_type_wrapper.EnumTypeWrapper(_OPERATION)
_RESULTTYPE = _descriptor.EnumDescriptor(
  name='resultType',
  full_name='bankingsystem.resultType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='unknown', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='failure', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='success', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=628,
  serialized_end=679,
)
_sym_db.RegisterEnumDescriptor(_RESULTTYPE)

resultType = enum_type_wrapper.EnumTypeWrapper(_RESULTTYPE)
customer = 0
branch = 1
bank = 2
propagate = 0
propagate_deposit = 5
propagate_withdraw = 1
deposit = 2
query = 3
withdraw = 4
unknown = 0
failure = 1
success = 2



_INPUTEVENT = _descriptor.Descriptor(
  name='inputEvent',
  full_name='bankingsystem.inputEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='bankingsystem.inputEvent.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='interface', full_name='bankingsystem.inputEvent.interface', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='money', full_name='bankingsystem.inputEvent.money', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dest', full_name='bankingsystem.inputEvent.dest', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=38,
  serialized_end=136,
)


_BANKREQUEST = _descriptor.Descriptor(
  name='BankRequest',
  full_name='bankingsystem.BankRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='bankingsystem.BankRequest.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='bankingsystem.BankRequest.type', index=1,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='events', full_name='bankingsystem.BankRequest.events', index=2,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='writeSet', full_name='bankingsystem.BankRequest.writeSet', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=138,
  serialized_end=261,
)


_OUTPUTEVENT = _descriptor.Descriptor(
  name='outputEvent',
  full_name='bankingsystem.outputEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='interface', full_name='bankingsystem.outputEvent.interface', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='result', full_name='bankingsystem.outputEvent.result', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='money', full_name='bankingsystem.outputEvent.money', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=263,
  serialized_end=379,
)


_BANKRESPONSE = _descriptor.Descriptor(
  name='BankResponse',
  full_name='bankingsystem.BankResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='bankingsystem.BankResponse.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='recv', full_name='bankingsystem.BankResponse.recv', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='writeSet', full_name='bankingsystem.BankResponse.writeSet', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=381,
  serialized_end=467,
)

_INPUTEVENT.fields_by_name['interface'].enum_type = _OPERATION
_BANKREQUEST.fields_by_name['type'].enum_type = _ENTITY
_BANKREQUEST.fields_by_name['events'].message_type = _INPUTEVENT
_OUTPUTEVENT.fields_by_name['interface'].enum_type = _OPERATION
_OUTPUTEVENT.fields_by_name['result'].enum_type = _RESULTTYPE
_BANKRESPONSE.fields_by_name['recv'].message_type = _OUTPUTEVENT
DESCRIPTOR.message_types_by_name['inputEvent'] = _INPUTEVENT
DESCRIPTOR.message_types_by_name['BankRequest'] = _BANKREQUEST
DESCRIPTOR.message_types_by_name['outputEvent'] = _OUTPUTEVENT
DESCRIPTOR.message_types_by_name['BankResponse'] = _BANKRESPONSE
DESCRIPTOR.enum_types_by_name['entity'] = _ENTITY
DESCRIPTOR.enum_types_by_name['operation'] = _OPERATION
DESCRIPTOR.enum_types_by_name['resultType'] = _RESULTTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

inputEvent = _reflection.GeneratedProtocolMessageType('inputEvent', (_message.Message,), {
  'DESCRIPTOR' : _INPUTEVENT,
  '__module__' : 'bankingsystem_pb2'
  # @@protoc_insertion_point(class_scope:bankingsystem.inputEvent)
  })
_sym_db.RegisterMessage(inputEvent)

BankRequest = _reflection.GeneratedProtocolMessageType('BankRequest', (_message.Message,), {
  'DESCRIPTOR' : _BANKREQUEST,
  '__module__' : 'bankingsystem_pb2'
  # @@protoc_insertion_point(class_scope:bankingsystem.BankRequest)
  })
_sym_db.RegisterMessage(BankRequest)

outputEvent = _reflection.GeneratedProtocolMessageType('outputEvent', (_message.Message,), {
  'DESCRIPTOR' : _OUTPUTEVENT,
  '__module__' : 'bankingsystem_pb2'
  # @@protoc_insertion_point(class_scope:bankingsystem.outputEvent)
  })
_sym_db.RegisterMessage(outputEvent)

BankResponse = _reflection.GeneratedProtocolMessageType('BankResponse', (_message.Message,), {
  'DESCRIPTOR' : _BANKRESPONSE,
  '__module__' : 'bankingsystem_pb2'
  # @@protoc_insertion_point(class_scope:bankingsystem.BankResponse)
  })
_sym_db.RegisterMessage(BankResponse)



_TRANSACTION = _descriptor.ServiceDescriptor(
  name='Transaction',
  full_name='bankingsystem.Transaction',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=681,
  serialized_end=768,
  methods=[
  _descriptor.MethodDescriptor(
    name='MsgDelivery',
    full_name='bankingsystem.Transaction.MsgDelivery',
    index=0,
    containing_service=None,
    input_type=_BANKREQUEST,
    output_type=_BANKRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_TRANSACTION)

DESCRIPTOR.services_by_name['Transaction'] = _TRANSACTION

# @@protoc_insertion_point(module_scope)