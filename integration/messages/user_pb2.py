# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: user.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nuser.proto\x12\x06userpb\"\x19\n\x0bUserRequest\x12\n\n\x02id\x18\x01 \x01(\t\"\x18\n\x08RoleList\x12\x0c\n\x04role\x18\x01 \x03(\t\"2\n\x10RoleListResponse\x12\x1e\n\x04role\x18\x01 \x03(\x0b\x32\x10.userpb.RoleList2:\n\x04User\x12\x32\n\x07GetUser\x12\x13.userpb.UserRequest\x1a\x10.userpb.RoleList\"\x00\x62\x06proto3')



_USERREQUEST = DESCRIPTOR.message_types_by_name['UserRequest']
_ROLELIST = DESCRIPTOR.message_types_by_name['RoleList']
_ROLELISTRESPONSE = DESCRIPTOR.message_types_by_name['RoleListResponse']
UserRequest = _reflection.GeneratedProtocolMessageType('UserRequest', (_message.Message,), {
  'DESCRIPTOR' : _USERREQUEST,
  '__module__' : 'user_pb2'
  # @@protoc_insertion_point(class_scope:userpb.UserRequest)
  })
_sym_db.RegisterMessage(UserRequest)

RoleList = _reflection.GeneratedProtocolMessageType('RoleList', (_message.Message,), {
  'DESCRIPTOR' : _ROLELIST,
  '__module__' : 'user_pb2'
  # @@protoc_insertion_point(class_scope:userpb.RoleList)
  })
_sym_db.RegisterMessage(RoleList)

RoleListResponse = _reflection.GeneratedProtocolMessageType('RoleListResponse', (_message.Message,), {
  'DESCRIPTOR' : _ROLELISTRESPONSE,
  '__module__' : 'user_pb2'
  # @@protoc_insertion_point(class_scope:userpb.RoleListResponse)
  })
_sym_db.RegisterMessage(RoleListResponse)

_USER = DESCRIPTOR.services_by_name['User']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _USERREQUEST._serialized_start=22
  _USERREQUEST._serialized_end=47
  _ROLELIST._serialized_start=49
  _ROLELIST._serialized_end=73
  _ROLELISTRESPONSE._serialized_start=75
  _ROLELISTRESPONSE._serialized_end=125
  _USER._serialized_start=127
  _USER._serialized_end=185
# @@protoc_insertion_point(module_scope)
