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

from mom import builtins
from mom import codec
from mom.net.scheme import data
from mom.tests import constants


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"

b = builtins.b

PNG_BIN = constants.PNG
PNG_DATA_URI = constants.PNG_DATA_URI
PNG_DATA_URI_QUOTED = constants.PNG_DATA_URI_QUOTED
SAMPLE_DATA_URI = constants.SAMPLE_DATA_URI
NO_META_DATA_URI = constants.NO_META_DATA_URI
RFC_BASE64_GIF = constants.RFC_BASE64_GIF
RFC_GIF = constants.RFC_GIF
RFC_GIF_DATA_URI = constants.RFC_GIF_DATA_URI
RFC_NOTE_DATA_URI = constants.RFC_NOTE_DATA_URI
RFC_NOTE_DECODED = constants.RFC_NOTE_DECODED


class Test_encoding(unittest2.TestCase):
  def test_encoding(self):
    self.assertEqual(data.data_uri_encode(PNG_BIN, b("image/png"), charset=None),
                     PNG_DATA_URI)
    self.assertEqual(data.data_uri_encode(PNG_BIN, b("image/png"),
                                          charset=None, encoder=None),
                     PNG_DATA_URI_QUOTED)

    self.assertEqual(data.data_uri_encode(RFC_GIF, b("image/gif"),
                                          charset=None),
                     RFC_GIF_DATA_URI)
    # self.assertEqual(data.data_uri_encode(RFC_GIF, b("image/gif"),
    #                                       charset=None),
    #                  RFC_GIF_DATA_URI_QUOTED)
    self.assertEqual(data.data_uri_encode(b("A brief note"),
                                          b(""),
                                          b(""), None), RFC_NOTE_DATA_URI)


  def test_raises_TypeError_when_not_raw_bytes(self):
    self.assertRaises(TypeError,
                      data.data_uri_encode,
                      constants.UNICODE_STRING,
                      b("text/plain"),
                      b("utf-8"))
    self.assertRaises(TypeError,
                      data.data_uri_encode, None, b("text/plain"), b("utf-8"))


class Test_identity(unittest2.TestCase):
  def test_identity(self):
    self.assertEqual(
        data.data_uri_parse(data.data_uri_encode(PNG_BIN, b("image/png"),
                                                 charset=None)),
        (PNG_BIN, (b("image"), b("png"), {}))
        )
    self.assertEqual(
        data.data_uri_parse(data.data_uri_encode(PNG_BIN, b("image/png"),
                                                 charset=None, encoder=None)),
        (PNG_BIN, (b("image"), b("png"), {}))
        )


class Test_parsing(unittest2.TestCase):
  def test_parsing(self):
    raw_bytes, mime_type = data.data_uri_parse(SAMPLE_DATA_URI)
    self.assertEqual(raw_bytes, PNG_BIN)
    self.assertEqual(mime_type[:2], (b("text"), b("css")))
    self.assertDictEqual(mime_type[2], {
        b("charset"): b("utf-8"),
        })
    raw_bytes, mime_type = data.data_uri_parse(RFC_NOTE_DATA_URI)
    self.assertEqual(raw_bytes, b("A brief note"))
    self.assertEqual(mime_type[:2], (b("text"), b("plain")))
    self.assertDictEqual(mime_type[2], {
        b("charset"): b("US-ASCII"),
        })


  def test_parsing_no_metadata(self):
    raw_bytes, mime_type = data.data_uri_parse(NO_META_DATA_URI)
    self.assertEqual(raw_bytes, PNG_BIN)
    self.assertEqual(mime_type[:2], (b("text"), b("plain")))
    self.assertDictEqual(mime_type[2], {
        b("charset"): b("US-ASCII"),
        })


  def test_raises_TypeError_when_not_raw_bytes(self):
    self.assertRaises(TypeError, data.data_uri_parse, constants.UNICODE_STRING)
    self.assertRaises(TypeError, data.data_uri_parse, None)
