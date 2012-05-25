#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
# Copyright 2012 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import unittest2
from mom._compat import ZERO_BYTE
from mom.builtins import b
from mom.codec import base58_decode, base58_encode
from mom.codec._alt_base import b58decode_naive, b58encode_naive
from mom.codec.base58 import b58encode, b58decode, ALT58_BYTES, ASCII58_BYTES
from mom.codec.integer import uint_to_bytes, bytes_to_uint
from mom.security.random import generate_random_bytes
from mom.tests.constants import UNICODE_STRING


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


RANDOM_BYTES = generate_random_bytes(384)

ZERO_BYTES_4 = ZERO_BYTE * 4
#raw_data = hex_decode(b('005cc87f4a3fdfe3a2346b6953267ca867282630d3f9b78e64'))
RAW_DATA = b('\x00\\\xc8\x7fJ?\xdf\xe3\xa24kiS&|\xa8g(&0\xd3\xf9\xb7\x8ed')
ENCODED = b('19TbMSWwHvnxAKy12iNm3KdbGfzfaMFViT')
ENCODED_WITH_WHITESPACE = b('''
19TbMSWwHvnxAKy12iN
m3KdbGfzfaMFViT
''')

PADDING_RAW = b('''\
\x00\x00\xa4\x97\xf2\x10\xfc\x9c]\x02\xfc}\xc7\xbd!\x1c\xb0\xc7M\xa0\xae\x16\
''')

class Test_base58_codec(unittest2.TestCase):
  def test_ensure_charset_length(self):
    self.assertEqual(len(ASCII58_BYTES), 58)
    self.assertEqual(len(ALT58_BYTES), 58)

  def test_codec_identity(self):
    self.assertEqual(b58decode(b58encode(RANDOM_BYTES)), RANDOM_BYTES)
    self.assertEqual(b58decode_naive(b58encode(RANDOM_BYTES)), RANDOM_BYTES)
    self.assertEqual(base58_decode(base58_encode(RANDOM_BYTES)),
                     RANDOM_BYTES)

  def test_encodes_zero_prefixed_padding(self):
    self.assertEqual(b58decode(b58encode(PADDING_RAW)), PADDING_RAW)
    self.assertEqual(b58decode_naive(b58encode(PADDING_RAW)), PADDING_RAW)
    self.assertEqual(base58_decode(base58_encode(PADDING_RAW)), PADDING_RAW)

  def test_zero_bytes(self):
    self.assertEqual(b58encode(ZERO_BYTES_4), b('1111'))
    self.assertEqual(b58decode(b('1111')), ZERO_BYTES_4)
    self.assertEqual(b58encode(ZERO_BYTE), b('1'))
    self.assertEqual(b58decode(b('1')), ZERO_BYTE)

    self.assertEqual(b58encode_naive(ZERO_BYTES_4), b('1111'))
    self.assertEqual(b58decode_naive(b('1111')), ZERO_BYTES_4)
    self.assertEqual(b58encode_naive(ZERO_BYTE), b('1'))
    self.assertEqual(b58decode_naive(b('1')), ZERO_BYTE)

    self.assertEqual(base58_encode(ZERO_BYTES_4), b('1111'))
    self.assertEqual(base58_decode(b('1111')), ZERO_BYTES_4)
    self.assertEqual(base58_encode(ZERO_BYTE), b('1'))
    self.assertEqual(base58_decode(b('1')), ZERO_BYTE)

  # The bitcoin implementation is a broken one. Do not use.
  #    def test_bitcoin_implementation(self):
  #        hello_world = b('\x48\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64')
  #        encoded_hello_world = b58encode(hello_world)
  #
  #        self.assertEqual(b58encode_bitcoin(raw_data), encoded)
  #        self.assertEqual(b58decode_bitcoin(encoded), raw_data)
  #        self.assertEqual(encoded_hello_world, b58encode_bitcoin(hello_world))
  #        self.assertEqual(b58decode_bitcoin(encoded_hello_world), hello_world)
  #
  #    def test_bitcoin_zero_encode(self):
  #        self.assertEqual(b58encode_bitcoin(zero_bytes_4), b('1111'))
  #        self.assertEqual(b58encode_bitcoin(ZERO_BYTE), b('1'))
  #
  #    def test_bitcoin_zero_decode(self):
  #        self.assertEqual(b58decode_bitcoin(b('1111')), zero_bytes_4)
  #        self.assertEqual(b58decode_bitcoin(b('1')), ZERO_BYTE)

  def test_encoding_and_decoding(self):
    hello_world = b('\x48\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64')
    encoded_hello_world = b58encode(hello_world)

    self.assertEqual(encoded_hello_world, b58encode_naive(hello_world))
    self.assertEqual(b58decode(encoded_hello_world), hello_world)

    self.assertEqual(bytes_to_uint(b58decode(b("16Ho7Hs"))), 3471844090)
    self.assertEqual(b58encode(uint_to_bytes(3471844090, 5)), b("16Ho7Hs"))

    self.assertEqual(b58encode(RAW_DATA), ENCODED)
    self.assertEqual(b58decode(ENCODED), RAW_DATA)
    self.assertEqual(b58decode(ENCODED_WITH_WHITESPACE), RAW_DATA)
    self.assertEqual(b58decode_naive(ENCODED), RAW_DATA)
    self.assertEqual(b58decode_naive(ENCODED_WITH_WHITESPACE), RAW_DATA)

    self.assertEqual(base58_encode(RAW_DATA), ENCODED)
    self.assertEqual(base58_decode(ENCODED), RAW_DATA)
    self.assertEqual(base58_decode(ENCODED_WITH_WHITESPACE), RAW_DATA)

  def test_TypeError_when_bad_type(self):
    self.assertRaises(TypeError, b58encode, UNICODE_STRING)
    self.assertRaises(TypeError, b58encode_naive, UNICODE_STRING)
    self.assertRaises(TypeError, b58decode, UNICODE_STRING)
    self.assertRaises(TypeError, b58decode_naive, UNICODE_STRING)
