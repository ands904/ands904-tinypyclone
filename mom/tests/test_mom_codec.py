#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
# Copyright 2012 Google, Inc.
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

from mom.tests.test_mom_builtins import UNICODE_STRING
from mom.builtins import b
from mom.security.random import\
  generate_random_bytes, generate_random_uint_between
from mom.codec import\
  base64_encode,\
  base64_decode,\
  hex_decode,\
  hex_encode,\
  decimal_decode,\
  decimal_encode,\
  bin_encode,\
  bin_decode,\
  base85_encode, base85_decode, base58_encode, base58_decode,\
  base64_urlsafe_encode, base64_urlsafe_decode
from mom.tests.test_mom_codec_base85 import RAW as base85_raw,\
  ENCODED as base85_encoded

# Generates a 1024-bit strength random byte string.
RANDOM_BYTES_1024 = generate_random_bytes(1024 >> 3)
# Generates a 2048-bit strength random byte string.
RANDOM_BYTES_2048 = generate_random_bytes(2048 >> 3)
# Generates a 4093 byte length random byte string.
RANDOM_BYTES_4093 = generate_random_bytes(4093)

ZERO_BYTES = b('\x00\x00\x00\x00')
ONE_ZERO_BYTE = b('\x00')

RANDOM_LONG_VALUE = generate_random_uint_between(0, 99999999999999999)
ZERO_LONG = 0
NEGATIVE_LONG_VALUE = -1

LONG_VALUE = 71671831749689734735896910666236152091910950933161125188784836897624039426313152092699961904060141667369
EXPECTED_BLOCKSIZE_BYTES = b('''\
\x00\x01\xff\xff\xff\xff\xff\xff\xff\xff\x000 0\x0c\x06\x08*\x86H\x86\
\xf7\r\x02\x05\x05\x00\x04\x10\xd6\xc7\xde\x19\xf6}\xb3#\xbdhI\xafDL\x04)''')
LONG_VALUE_BLOCKSIZE = 45
EXPECTED_BYTES = b('''\
\x01\xff\xff\xff\xff\xff\xff\xff\xff\x000 0\x0c\x06\x08*\x86H\x86\
\xf7\r\x02\x05\x05\x00\x04\x10\xd6\xc7\xde\x19\xf6}\xb3#\xbdhI\xafDL\x04)''')


# Base64 encoding this sequence of bytes using the standard Base-64 alphabet
# produces a "/", "+", and "=" in the encoded sequence.
URL_SAFETY_TEST_BYTES = b('''\
G\x81Y\x9aK\x9d\xf2\xe9\x81\x06\xc6\xbe6\xa5\x0e\xc0k\x91I\x05\xde\xd8\
\xdc\xd6\xa7\xf2\x9f\t\x8c\xa1\xa6\xf3\x19\xc7\x0b\xfd=z\x02Z\xbeR\xc0\
\xc6~`\xddfzA''')
URL_SAFETY_TEST_STANDARD_ENCODED =\
b('R4FZmkud8umBBsa+NqUOwGuRSQXe2NzWp/KfCYyhpvMZxwv9PXoCWr5SwMZ+YN1mekE=')
URL_SAFETY_TEST_SAFE_ENCODED =\
b('R4FZmkud8umBBsa-NqUOwGuRSQXe2NzWp_KfCYyhpvMZxwv9PXoCWr5SwMZ-YN1mekE')


class Test_base85_codec(unittest2.TestCase):
  def test_codec_identity(self):
    self.assertEqual(base85_decode(base85_encode(base85_raw)), base85_raw)

  def test_encoding_and_decoding(self):
    self.assertEqual(base85_encode(base85_raw), base85_encoded)
    self.assertEqual(base85_decode(base85_encoded), base85_raw)

  def test_raises_KeyError_when_invalid_charset(self):
    self.assertRaises(ValueError,
                      base85_encode, base85_raw, "BADCHARSET")
    self.assertRaises(ValueError,
                      base85_decode, base85_encoded, "BADCHARSET")


class Test_base58_codec(unittest2.TestCase):
  def test_codec_identity(self):
    self.assertEqual(base58_decode(base58_encode(RANDOM_BYTES_1024)),
                     RANDOM_BYTES_1024)
    self.assertEqual(base58_decode(base58_encode(RANDOM_BYTES_4093)),
                     RANDOM_BYTES_4093)

  def test_raises_TypeError_when_invalid_argument(self):
    self.assertRaises(TypeError, base58_encode, UNICODE_STRING)
    self.assertRaises(TypeError, base58_encode, None)
    self.assertRaises(TypeError, base58_decode, UNICODE_STRING)
    self.assertRaises(TypeError, base58_decode, None)


class Test_base64_codec(unittest2.TestCase):
  def test_encodes_without_trailing_newline(self):
    self.assertFalse(base64_encode(ZERO_BYTES).endswith(b("\n")))
    self.assertFalse(base64_encode(RANDOM_BYTES_1024).endswith(b("\n")))
    self.assertFalse(base64_encode(RANDOM_BYTES_2048).endswith(b("\n")))
    self.assertFalse(base64_encode(RANDOM_BYTES_4093).endswith(
      b("\n")))

  def test_codec_identity(self):
    # Not zero-destructive.
    self.assertEqual(base64_decode(base64_encode(ZERO_BYTES)), ZERO_BYTES)
    self.assertEqual(base64_decode(base64_encode(RANDOM_BYTES_1024)),
                     RANDOM_BYTES_1024)
    self.assertEqual(base64_decode(base64_encode(RANDOM_BYTES_2048)),
                     RANDOM_BYTES_2048)
    self.assertEqual(base64_decode(base64_encode(RANDOM_BYTES_4093)),
                     RANDOM_BYTES_4093)

  def test_TypeError_non_bytes_argument(self):
    self.assertRaises(TypeError, base64_encode, UNICODE_STRING)
    self.assertRaises(TypeError, base64_encode, None)

    self.assertRaises(TypeError, base64_decode, UNICODE_STRING)
    self.assertRaises(TypeError, base64_decode, None)


class Test_base64_urlsafe_codec(unittest2.TestCase):
  def test_encodes_without_trailing_newline(self):
    self.assertFalse(base64_urlsafe_encode(ZERO_BYTES).endswith(b("\n")))
    self.assertFalse(
      base64_urlsafe_encode(RANDOM_BYTES_1024).endswith(b("\n")))

  def test_codec_identity(self):
    # Not zero-destructive.
    self.assertEqual(
      base64_urlsafe_decode(base64_urlsafe_encode(ZERO_BYTES)),
      ZERO_BYTES
    )
    self.assertEqual(
      base64_urlsafe_decode(base64_urlsafe_encode(RANDOM_BYTES_1024)),
      RANDOM_BYTES_1024
    )

  def test_correctness(self):
    self.assertEqual(base64_urlsafe_encode(URL_SAFETY_TEST_BYTES),
                     URL_SAFETY_TEST_SAFE_ENCODED)
    self.assertEqual(base64_encode(URL_SAFETY_TEST_BYTES),
                     URL_SAFETY_TEST_STANDARD_ENCODED)
    self.assertEqual(base64_urlsafe_decode(URL_SAFETY_TEST_SAFE_ENCODED),
                     URL_SAFETY_TEST_BYTES)
    self.assertEqual(base64_decode(URL_SAFETY_TEST_STANDARD_ENCODED),
                     URL_SAFETY_TEST_BYTES)

    # Tests whether this decoder can decode standard encoded base64
    # representation too.
    self.assertEqual(
      base64_urlsafe_decode(URL_SAFETY_TEST_STANDARD_ENCODED),
      URL_SAFETY_TEST_BYTES
    )

  def test_TypeError_non_bytes_argument(self):
    self.assertRaises(TypeError, base64_urlsafe_encode, UNICODE_STRING)
    self.assertRaises(TypeError, base64_urlsafe_encode, None)

    self.assertRaises(TypeError, base64_urlsafe_decode, UNICODE_STRING)
    self.assertRaises(TypeError, base64_urlsafe_decode, None)


class Test_hex_codec(unittest2.TestCase):
  def test_codec_identity(self):
    # Not zero-destructive
    self.assertEqual(hex_decode(hex_encode(ZERO_BYTES)), ZERO_BYTES)
    self.assertEqual(hex_decode(hex_encode(RANDOM_BYTES_1024)),
                     RANDOM_BYTES_1024)
    self.assertEqual(hex_decode(hex_encode(RANDOM_BYTES_2048)),
                     RANDOM_BYTES_2048)
    self.assertEqual(
      hex_decode(hex_encode(RANDOM_BYTES_4093)),
      RANDOM_BYTES_4093)

  def test_TypeError_non_bytes_argument(self):
    self.assertRaises(TypeError, hex_encode, UNICODE_STRING)
    self.assertRaises(TypeError, hex_encode, None)

    self.assertRaises(TypeError, hex_decode, UNICODE_STRING)
    self.assertRaises(TypeError, hex_decode, None)


class Test_decimal_codec(unittest2.TestCase):
  def test_codec_identity(self):
    self.assertEqual(
      decimal_decode(decimal_encode(ZERO_BYTES)),
      ZERO_BYTES)
    self.assertEqual(
      decimal_decode(decimal_encode(RANDOM_BYTES_1024)),
      RANDOM_BYTES_1024)
    self.assertEqual(
      decimal_decode(decimal_encode(RANDOM_BYTES_2048)),
      RANDOM_BYTES_2048)
    self.assertEqual(
      decimal_decode(decimal_encode(RANDOM_BYTES_4093)),
      RANDOM_BYTES_4093)

  def test_TypeError_non_bytes_argument(self):
    self.assertRaises(TypeError, decimal_encode, UNICODE_STRING)
    self.assertRaises(TypeError, decimal_encode, None)

    self.assertRaises(TypeError, decimal_decode, UNICODE_STRING)
    self.assertRaises(TypeError, decimal_decode, None)


class Test_bin_codec(unittest2.TestCase):
  def test_codec_identity(self):
    self.assertEqual(bin_decode(bin_encode(ZERO_BYTES)), ZERO_BYTES)
    self.assertEqual(
      bin_decode(bin_encode(RANDOM_BYTES_1024)), RANDOM_BYTES_1024)
    self.assertEqual(
      bin_decode(bin_encode(RANDOM_BYTES_2048)), RANDOM_BYTES_2048)
    self.assertEqual(
      bin_decode(bin_encode(RANDOM_BYTES_4093)),
      RANDOM_BYTES_4093)

  def test_TypeError_non_bytes_argument(self):
    self.assertRaises(TypeError, bin_encode, UNICODE_STRING)
    self.assertRaises(TypeError, bin_encode, None)

    self.assertRaises(TypeError, bin_decode, UNICODE_STRING)
    self.assertRaises(TypeError, bin_decode, None)
