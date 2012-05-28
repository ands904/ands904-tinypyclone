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

"""
:module: mom.codec.integer
:synopsis: Routines for converting between integers and bytes.

Number-bytes conversion
-----------------------
These codecs are "lossy" as they don't preserve prefixed padding zero bytes.
In a more mathematical sense,

    ``g(f(x))`` is **almost** an identity function, but not exactly.

where ``g`` is the decoder and ``f`` is a encoder.

.. autofunction:: bytes_to_uint
.. autofunction:: uint_to_bytes
"""

# This module contains only the implementations that were bench-marked
# to be the fastest. See _alt_integer.py for alternative but slower
# implementations.

from __future__ import absolute_import
from __future__ import division

# pylint: disable-msg=R0801
try: #pragma: no cover
  import psyco

  psyco.full()
except ImportError: #pragma: no cover
  psyco = None
# pylint: enable-msg=R0801

import binascii
import struct

from mom import _compat
from mom import builtins


__author__ = "yesudeep@google.com (Yesudeep Mangalapilly)"


__all__ = [
  "bytes_to_uint",
  "uint_to_bytes",
  ]


ZERO_BYTE = _compat.ZERO_BYTE
EMPTY_BYTE = _compat.EMPTY_BYTE


def bytes_to_uint(raw_bytes):
  """
  Converts a series of bytes into an unsigned integer.

  :param raw_bytes:
      Raw bytes (base-256 representation).
  :returns:
      Unsigned integer.
  """
  if not builtins.is_bytes(raw_bytes):
    raise TypeError("argument must be raw bytes: got %r" %
                    type(raw_bytes).__name__)
    # binascii.b2a_hex is written in C as is int.
  return int(binascii.b2a_hex(raw_bytes), 16)


def uint_to_bytes(number, fill_size=0, chunk_size=0, overflow=False):
  """
  Convert an unsigned integer to bytes (base-256 representation).

  Leading zeros are not preserved for positive integers unless a
  chunk size or a fill size is specified. A single zero byte is
  returned if the number is 0 and no padding is specified.

  When a chunk size or a fill size is specified, the resulting bytes
  are prefix-padded with zero bytes to satisfy the size. The total
  size of the number in bytes is either the fill size or an integral
  multiple of the chunk size.

  .. NOTE:
      You cannot specify both the fill size and the chunk size.

  :param number:
      Integer value
  :param fill_size:
      The maxmimum number of bytes with which to represent the integer.
      Prefix zero padding is added as necessary to satisfy the size.
      If the number of bytes needed to represent the integer is greater
      than the fill size, an ``OverflowError`` is raised. To suppress
      this error and allow overflow, you may set the ``overfloww``
      argument to this function to ``True``.
  :param chunk_size:
      If optional chunk size is given and greater than zero, the
      resulting sequence of bytes is prefix-padded with zero bytes so
      that the total number of bytes is a multiple of ``chunk_size``.
  :param overflow:
      ``False`` (default). If this is ``True``, no ``OverflowError``
      will be raised when the fill_size is shorter than the length
      of the generated byte sequence. Instead the byte sequence will
      be returned as is.
  :returns:
      Raw bytes (base-256 representation).
  :raises:
      ``OverflowError`` when a fill size is given and the number takes up
      more bytes than fit into the block. This requires the ``overflow``
      argument to this function to be set to ``False`` otherwise, no
      error will be raised.
  """
  if number < 0:
    raise ValueError("Number must be an unsigned integer: %d" % number)

  if fill_size and chunk_size:
    raise ValueError("You can either fill or pad chunks, but not both")

  # Ensure these are integers.
  _ = number & 1 and chunk_size & 1 and fill_size & 1

  raw_bytes = EMPTY_BYTE

  # Pack the integer one machine word at a time into bytes.
  num = number
  word_bits, _, max_uint, pack_type = _compat.get_word_alignment(num)
  pack_format = ">%s" % pack_type
  while num > 0:
    raw_bytes = struct.pack(pack_format, num & max_uint) + raw_bytes
    num >>= word_bits
    # Obtain the index of the first non-zero byte.
  zero_leading = builtins.bytes_leading(raw_bytes)
  if number == 0:
    raw_bytes = ZERO_BYTE
    # De-padding.
  raw_bytes = raw_bytes[zero_leading:]

  length = len(raw_bytes)
  if fill_size > 0:
    if not overflow and length > fill_size:
      raise OverflowError(
        "Need %d bytes for number, but fill size is %d" %
        (length, fill_size)
      )
    raw_bytes = raw_bytes.rjust(fill_size, ZERO_BYTE)
  elif chunk_size > 0:
    remainder = length % chunk_size
    if remainder:
      padding_size = chunk_size - remainder
      raw_bytes = raw_bytes.rjust(length + padding_size, ZERO_BYTE)
  return raw_bytes
