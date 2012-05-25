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

from mom.builtins import is_bytes, is_unicode, b
from mom.codec.text import utf8_encode_if_unicode,\
  to_unicode_if_bytes, bytes_to_unicode, utf8_encode,\
  utf8_encode_recursive, bytes_to_unicode_recursive,\
  utf8_decode, utf8_decode_if_bytes
from mom.tests.constants import *


class Test_to_utf8_if_unicode(unittest2.TestCase):
  def test_encodes_unicode_strings(self):
    self.assertEqual(utf8_encode_if_unicode(UNICODE_STRING), UTF8_BYTES)
    self.assertTrue(is_bytes(utf8_encode_if_unicode(UNICODE_STRING)))

    self.assertEqual(utf8_encode_if_unicode(UNICODE_STRING2), UTF8_BYTES2)
    self.assertTrue(is_bytes(utf8_encode_if_unicode(UNICODE_STRING2)))

  def test_does_not_encode_else_to_utf8(self):
    self.assertEqual(utf8_encode_if_unicode(UTF8_BYTES), UTF8_BYTES)
    self.assertTrue(is_bytes(utf8_encode_if_unicode(UTF8_BYTES)))

    self.assertEqual(utf8_encode_if_unicode(UTF8_BYTES2), UTF8_BYTES2)
    self.assertTrue(is_bytes(utf8_encode_if_unicode(UTF8_BYTES2)))

    self.assertEqual(utf8_encode_if_unicode(None), None)
    self.assertEqual(utf8_encode_if_unicode(False), False)
    self.assertEqual(utf8_encode_if_unicode(5), 5)
    self.assertEqual(utf8_encode_if_unicode([]), [])
    self.assertEqual(utf8_encode_if_unicode(()), ())
    self.assertEqual(utf8_encode_if_unicode({}), {})
    self.assertEqual(utf8_encode_if_unicode(object), object)


class Test_to_unicode_if_bytes(unittest2.TestCase):
  def test_encodes_bytes_to_unicode(self):
    self.assertEqual(to_unicode_if_bytes(UTF8_BYTES), UNICODE_STRING)
    self.assertTrue(is_unicode(to_unicode_if_bytes(UTF8_BYTES)))

    self.assertEqual(to_unicode_if_bytes(UTF8_BYTES2), UNICODE_STRING2)
    self.assertTrue(is_unicode(to_unicode_if_bytes(UTF8_BYTES2)))

  def test_does_not_encode_else_to_unicode(self):
    self.assertEqual(to_unicode_if_bytes(UNICODE_STRING), UNICODE_STRING)
    self.assertTrue(is_unicode(to_unicode_if_bytes(UNICODE_STRING)))

    self.assertEqual(to_unicode_if_bytes(UNICODE_STRING2), UNICODE_STRING2)
    self.assertTrue(is_unicode(to_unicode_if_bytes(UNICODE_STRING2)))

    self.assertEqual(to_unicode_if_bytes(None), None)
    self.assertEqual(to_unicode_if_bytes(False), False)
    self.assertEqual(to_unicode_if_bytes(5), 5)
    self.assertEqual(to_unicode_if_bytes([]), [])
    self.assertEqual(to_unicode_if_bytes(()), ())
    self.assertEqual(to_unicode_if_bytes({}), {})
    self.assertEqual(to_unicode_if_bytes(object), object)


class Test_utf8_decode_if_bytes(unittest2.TestCase):
  def test_encodes_bytes_to_unicode(self):
    self.assertEqual(utf8_decode_if_bytes(UTF8_BYTES), UNICODE_STRING)
    self.assertTrue(is_unicode(utf8_decode_if_bytes(UTF8_BYTES)))

    self.assertEqual(utf8_decode_if_bytes(UTF8_BYTES2), UNICODE_STRING2)
    self.assertTrue(is_unicode(utf8_decode_if_bytes(UTF8_BYTES2)))

  def test_does_not_encode_else_to_unicode(self):
    self.assertEqual(utf8_decode_if_bytes(UNICODE_STRING), UNICODE_STRING)
    self.assertTrue(is_unicode(utf8_decode_if_bytes(UNICODE_STRING)))

    self.assertEqual(utf8_decode_if_bytes(UNICODE_STRING2), UNICODE_STRING2)
    self.assertTrue(is_unicode(utf8_decode_if_bytes(UNICODE_STRING2)))

    self.assertEqual(utf8_decode_if_bytes(None), None)
    self.assertEqual(utf8_decode_if_bytes(False), False)
    self.assertEqual(utf8_decode_if_bytes(5), 5)
    self.assertEqual(utf8_decode_if_bytes([]), [])
    self.assertEqual(utf8_decode_if_bytes(()), ())
    self.assertEqual(utf8_decode_if_bytes({}), {})
    self.assertEqual(utf8_decode_if_bytes(object), object)


class Test_bytes_to_unicode(unittest2.TestCase):
  def test_converts_bytes_to_unicode(self):
    self.assertEqual(bytes_to_unicode(UTF8_BYTES), UNICODE_STRING)
    self.assertTrue(is_unicode(bytes_to_unicode(UTF8_BYTES)))

    self.assertEqual(bytes_to_unicode(UTF8_BYTES2), UNICODE_STRING2)
    self.assertTrue(is_unicode(bytes_to_unicode(UTF8_BYTES2)))

  def test_does_not_encode_unicode_and_None_to_unicode(self):
    self.assertEqual(bytes_to_unicode(UNICODE_STRING), UNICODE_STRING)
    self.assertTrue(is_unicode(bytes_to_unicode(UNICODE_STRING)))

    self.assertEqual(bytes_to_unicode(UNICODE_STRING2), UNICODE_STRING2)
    self.assertTrue(is_unicode(bytes_to_unicode(UNICODE_STRING2)))

    self.assertEqual(bytes_to_unicode(None), None)

  def test_raises_TypeError_when_not_string_or_None(self):
    self.assertRaises(TypeError, bytes_to_unicode, 5)
    self.assertRaises(TypeError, bytes_to_unicode, False)
    self.assertRaises(TypeError, bytes_to_unicode, True)
    self.assertRaises(TypeError, bytes_to_unicode, [])
    self.assertRaises(TypeError, bytes_to_unicode, ())
    self.assertRaises(TypeError, bytes_to_unicode, {})
    self.assertRaises(TypeError, bytes_to_unicode, object)

  def test_raises_UnicodeDecodeError_when_latin1_bytes(self):
    self.assertRaises(UnicodeDecodeError, bytes_to_unicode, LATIN1_BYTES)


class Test_utf8_decode(unittest2.TestCase):
  def test_converts_utf8_decode(self):
    self.assertEqual(utf8_decode(UTF8_BYTES), UNICODE_STRING)
    self.assertTrue(is_unicode(utf8_decode(UTF8_BYTES)))

    self.assertEqual(utf8_decode(UTF8_BYTES2), UNICODE_STRING2)
    self.assertTrue(is_unicode(utf8_decode(UTF8_BYTES2)))

  def test_does_not_encode_unicode_and_None_to_unicode(self):
    self.assertEqual(utf8_decode(UNICODE_STRING), UNICODE_STRING)
    self.assertTrue(is_unicode(utf8_decode(UNICODE_STRING)))

    self.assertEqual(utf8_decode(UNICODE_STRING2), UNICODE_STRING2)
    self.assertTrue(is_unicode(utf8_decode(UNICODE_STRING2)))

    self.assertEqual(utf8_decode(None), None)

  def test_raises_TypeError_when_not_string_or_None(self):
    self.assertRaises(TypeError, utf8_decode, 5)
    self.assertRaises(TypeError, utf8_decode, False)
    self.assertRaises(TypeError, utf8_decode, True)
    self.assertRaises(TypeError, utf8_decode, [])
    self.assertRaises(TypeError, utf8_decode, ())
    self.assertRaises(TypeError, utf8_decode, {})
    self.assertRaises(TypeError, utf8_decode, object)

  def test_raises_UnicodeDecodeError_when_latin1_bytes(self):
    self.assertRaises(UnicodeDecodeError, utf8_decode, LATIN1_BYTES)


class Test_unicode_to_utf8(unittest2.TestCase):
  def test_encodes_only_unicode_to_utf8(self):
    self.assertEqual(utf8_encode(UNICODE_STRING), UTF8_BYTES)
    self.assertTrue(is_bytes(utf8_encode(UNICODE_STRING)))

    self.assertEqual(utf8_encode(UNICODE_STRING2), UTF8_BYTES2)
    self.assertTrue(is_bytes(utf8_encode(UNICODE_STRING2)))

  def test_does_not_encode_bytes_or_None_to_utf8(self):
    self.assertEqual(utf8_encode(None), None)
    self.assertEqual(utf8_encode(UTF8_BYTES), UTF8_BYTES)
    self.assertTrue(is_bytes(utf8_encode(UTF8_BYTES)))

    self.assertEqual(utf8_encode(LATIN1_BYTES), LATIN1_BYTES)
    self.assertTrue(is_bytes(utf8_encode(LATIN1_BYTES)))

    self.assertEqual(utf8_encode(UTF8_BYTES2), UTF8_BYTES2)
    self.assertTrue(is_bytes(utf8_encode(UTF8_BYTES2)))

  def test_raises_TypeError_when_not_string_or_None(self):
    self.assertRaises(TypeError, utf8_encode, 5)
    self.assertRaises(TypeError, utf8_encode, False)
    self.assertRaises(TypeError, utf8_encode, True)
    self.assertRaises(TypeError, utf8_encode, [])
    self.assertRaises(TypeError, utf8_encode, ())
    self.assertRaises(TypeError, utf8_encode, {})
    self.assertRaises(TypeError, utf8_encode, object)


class Test_bytes_to_unicode_recursive(unittest2.TestCase):
  def test_converts_all_bytes_to_unicode_recursively(self):
    p = {
      "l": [UTF8_BYTES2, UTF8_BYTES],
      "t": (UTF8_BYTES2, UTF8_BYTES),
      "d": dict(another=[UTF8_BYTES, UTF8_BYTES2]),
      "b": UTF8_BYTES,
      "n": None,
      }
    e = {
      "l": [UNICODE_STRING2, UNICODE_STRING],
      "t": (UNICODE_STRING2, UNICODE_STRING),
      "d": dict(another=[UNICODE_STRING, UNICODE_STRING2]),
      "b": UNICODE_STRING,
      "n": None,
      }
    self.assertDictEqual(bytes_to_unicode_recursive(p), e)


class Test_unicode_to_utf8_recursive(unittest2.TestCase):
  def test_converts_all_unicode_to_utf8_bytes_recursively(self):
    e = {
      b("l"): [UTF8_BYTES2, UTF8_BYTES],
      b("t"): (UTF8_BYTES2, UTF8_BYTES),
      b("d"): {b('another'): [UTF8_BYTES, UTF8_BYTES2]},
      b("b"): UTF8_BYTES,
      b("n"): None,
      }
    p = {
      "l": [UNICODE_STRING2, UNICODE_STRING],
      "t": (UNICODE_STRING2, UNICODE_STRING),
      "d": dict(another=[UNICODE_STRING, UNICODE_STRING2]),
      "b": UNICODE_STRING,
      "n": None,
      }
    self.assertDictEqual(utf8_encode_recursive(p), e)
