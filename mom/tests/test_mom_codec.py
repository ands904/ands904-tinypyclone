#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
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
from mom.builtins import b
from mom.security.random import \
    generate_random_bytes, generate_random_uint_between
from mom.codec import \
    base64_encode, \
    base64_decode, \
    hex_decode, \
    hex_encode, \
    decimal_decode, \
    decimal_encode, \
    bin_encode, \
    bin_decode, \
    base85_encode, base85_decode, base58_encode, base58_decode, \
    base64_urlsafe_encode, base64_urlsafe_decode
from mom.codec._alt_integer import \
    uint_to_bytes_naive_array_based, \
    uint_to_bytes_naive, \
    uint_to_bytes_pycrypto, \
    uint_to_bytes_array_based, \
    bytes_to_uint_naive
from mom.codec.integer import \
    bytes_to_uint, \
    uint_to_bytes
from mom.prime_sieve import sieve
from mom.tests.test_mom_builtins import unicode_string

# Generates a 1024-bit strength random byte string.
random_bytes_1024 = generate_random_bytes(1024 >> 3)
# Generates a 2048-bit strength random byte string.
random_bytes_2048 = generate_random_bytes(2048 >> 3)
# Generates a 4093 byte length random byte string.
random_bytes_len_4093 = generate_random_bytes(4093)

zero_bytes = b('\x00\x00\x00\x00')
one_zero_byte = b('\x00')

random_long_value = generate_random_uint_between(0, 99999999999999999)
zero_long = 0
negative_long_value = -1

long_value = 71671831749689734735896910666236152091910950933161125188784836897624039426313152092699961904060141667369
expected_blocksize_bytes = b('''\
\x00\x01\xff\xff\xff\xff\xff\xff\xff\xff\x000 0\x0c\x06\x08*\x86H\x86\
\xf7\r\x02\x05\x05\x00\x04\x10\xd6\xc7\xde\x19\xf6}\xb3#\xbdhI\xafDL\x04)''')
long_value_blocksize = 45
expected_bytes = b('''\
\x01\xff\xff\xff\xff\xff\xff\xff\xff\x000 0\x0c\x06\x08*\x86H\x86\
\xf7\r\x02\x05\x05\x00\x04\x10\xd6\xc7\xde\x19\xf6}\xb3#\xbdhI\xafDL\x04)''')


base85_raw = b("""Man is distinguished, not only by his reason, but by this
singular passion from other animals, which is a lust of the
mind, that by a perseverance of delight in the continued and
indefatigable generation of knowledge, exceeds the short
vehemence of any carnal pleasure.""").replace(b('\n'), b(' '))

base85_encoded = b("""\
9jqo^BlbD-BleB1DJ+*+F(f,q/0JhKF<GL>Cj@.4Gp$d7F!,L7@<6@)/0JDEF<G%<+EV:2F!,\
O<DJ+*.@<*K0@<6L(Df-\\0Ec5e;DffZ(EZee.Bl.9pF"AGXBPCsi+DGm>@3BB/F*&OCAfu2/AKY\
i(DIb:@FD,*)+C]U=@3BN#EcYf8ATD3s@q?d$AftVqCh[NqF<G:8+EV:.+Cf>-FD5W8ARlolDIa\
l(DId<j@<?3r@:F%a+D58'ATD4$Bl@l3De:,-DJs`8ARoFb/0JMK@qB4^F!,R<AKZ&-DfTqBG%G\
>uD.RTpAKYo'+CT/5+Cei#DII?(E,9)oF*2M7/c""")


# Base64 encoding this sequence of bytes using the standard Base-64 alphabet
# produces a "/", "+", and "=" in the encoded sequence.
url_safety_test_bytes = b('''\
G\x81Y\x9aK\x9d\xf2\xe9\x81\x06\xc6\xbe6\xa5\x0e\xc0k\x91I\x05\xde\xd8\
\xdc\xd6\xa7\xf2\x9f\t\x8c\xa1\xa6\xf3\x19\xc7\x0b\xfd=z\x02Z\xbeR\xc0\
\xc6~`\xddfzA''')
url_safety_test_standard_encoded = \
    b('R4FZmkud8umBBsa+NqUOwGuRSQXe2NzWp/KfCYyhpvMZxwv9PXoCWr5SwMZ+YN1mekE=')
url_safety_test_safe_encoded = \
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
        self.assertEqual(base58_decode(base58_encode(random_bytes_1024)),
                         random_bytes_1024)
        self.assertEqual(base58_decode(base58_encode(random_bytes_len_4093)),
                         random_bytes_len_4093)

    def test_raises_TypeError_when_invalid_argument(self):
        self.assertRaises(TypeError, base58_encode, unicode_string)
        self.assertRaises(TypeError, base58_encode, None)
        self.assertRaises(TypeError, base58_decode, unicode_string)
        self.assertRaises(TypeError, base58_decode, None)

class Test_base64_codec(unittest2.TestCase):
    def test_encodes_without_trailing_newline(self):
        self.assertFalse(base64_encode(zero_bytes).endswith(b("\n")))
        self.assertFalse(base64_encode(random_bytes_1024).endswith(b("\n")))
        self.assertFalse(base64_encode(random_bytes_2048).endswith(b("\n")))
        self.assertFalse(base64_encode(random_bytes_len_4093).endswith(
            b("\n")))

    def test_codec_identity(self):
        # Not zero-destructive.
        self.assertEqual(base64_decode(base64_encode(zero_bytes)), zero_bytes)
        self.assertEqual(base64_decode(base64_encode(random_bytes_1024)),
                         random_bytes_1024)
        self.assertEqual(base64_decode(base64_encode(random_bytes_2048)),
                         random_bytes_2048)
        self.assertEqual(base64_decode(base64_encode(random_bytes_len_4093)),
                         random_bytes_len_4093)

    def test_TypeError_non_bytes_argument(self):
        self.assertRaises(TypeError, base64_encode, unicode_string)
        self.assertRaises(TypeError, base64_encode, None)

        self.assertRaises(TypeError, base64_decode, unicode_string)
        self.assertRaises(TypeError, base64_decode, None)

        
class Test_base64_urlsafe_codec(unittest2.TestCase):
    def test_encodes_without_trailing_newline(self):
        self.assertFalse(base64_urlsafe_encode(zero_bytes).endswith(b("\n")))
        self.assertFalse(
            base64_urlsafe_encode(random_bytes_1024).endswith(b("\n")))


    def test_codec_identity(self):
        # Not zero-destructive.
        self.assertEqual(
            base64_urlsafe_decode(base64_urlsafe_encode(zero_bytes)),
            zero_bytes
        )
        self.assertEqual(
            base64_urlsafe_decode(base64_urlsafe_encode(random_bytes_1024)),
            random_bytes_1024
        )

    def test_correctness(self):
        self.assertEqual(base64_urlsafe_encode(url_safety_test_bytes),
                         url_safety_test_safe_encoded)
        self.assertEqual(base64_encode(url_safety_test_bytes),
                         url_safety_test_standard_encoded)
        self.assertEqual(base64_urlsafe_decode(url_safety_test_safe_encoded),
                         url_safety_test_bytes)
        self.assertEqual(base64_decode(url_safety_test_standard_encoded),
                         url_safety_test_bytes)

        # Tests whether this decoder can decode standard encoded base64
        # representation too.
        self.assertEqual(
            base64_urlsafe_decode(url_safety_test_standard_encoded),
            url_safety_test_bytes
        )
        
    def test_TypeError_non_bytes_argument(self):
        self.assertRaises(TypeError, base64_urlsafe_encode, unicode_string)
        self.assertRaises(TypeError, base64_urlsafe_encode, None)

        self.assertRaises(TypeError, base64_urlsafe_decode, unicode_string)
        self.assertRaises(TypeError, base64_urlsafe_decode, None)


class Test_hex_codec(unittest2.TestCase):
    def test_codec_identity(self):
        # Not zero-destructive
        self.assertEqual(hex_decode(hex_encode(zero_bytes)), zero_bytes)
        self.assertEqual(hex_decode(hex_encode(random_bytes_1024)),
                         random_bytes_1024)
        self.assertEqual(hex_decode(hex_encode(random_bytes_2048)),
                         random_bytes_2048)
        self.assertEqual(
            hex_decode(hex_encode(random_bytes_len_4093)),
                         random_bytes_len_4093)

    def test_TypeError_non_bytes_argument(self):
        self.assertRaises(TypeError, hex_encode, unicode_string)
        self.assertRaises(TypeError, hex_encode, None)

        self.assertRaises(TypeError, hex_decode, unicode_string)
        self.assertRaises(TypeError, hex_decode, None)


class Test_decimal_codec(unittest2.TestCase):
    def test_codec_identity(self):
        self.assertEqual(
            decimal_decode(decimal_encode(zero_bytes)),
            zero_bytes)
        self.assertEqual(
            decimal_decode(decimal_encode(random_bytes_1024)),
            random_bytes_1024)
        self.assertEqual(
            decimal_decode(decimal_encode(random_bytes_2048)),
            random_bytes_2048)
        self.assertEqual(
            decimal_decode(decimal_encode(random_bytes_len_4093)),
            random_bytes_len_4093)

    def test_TypeError_non_bytes_argument(self):
        self.assertRaises(TypeError, decimal_encode, unicode_string)
        self.assertRaises(TypeError, decimal_encode, None)

        self.assertRaises(TypeError, decimal_decode, unicode_string)
        self.assertRaises(TypeError, decimal_decode, None)


class Test_bin_codec(unittest2.TestCase):
    def test_codec_identity(self):
        self.assertEqual(bin_decode(bin_encode(zero_bytes)), zero_bytes)
        self.assertEqual(
            bin_decode(bin_encode(random_bytes_1024)), random_bytes_1024)
        self.assertEqual(
            bin_decode(bin_encode(random_bytes_2048)), random_bytes_2048)
        self.assertEqual(
            bin_decode(bin_encode(random_bytes_len_4093)),
            random_bytes_len_4093)

    def test_TypeError_non_bytes_argument(self):
        self.assertRaises(TypeError, bin_encode, unicode_string)
        self.assertRaises(TypeError, bin_encode, None)

        self.assertRaises(TypeError, bin_decode, unicode_string)
        self.assertRaises(TypeError, bin_decode, None)


class Test_bytes_uint_codec(unittest2.TestCase):
    def test_codec_equivalence(self):
        # Padding bytes are not preserved (it is acceptable here).
        random_bytes = b("\x00\xbcE\x9a\xda]")
        expected_bytes = b("\xbcE\x9a\xda]")
        self.assertEqual(uint_to_bytes(bytes_to_uint(zero_bytes)),
                         one_zero_byte)
        self.assertEqual(uint_to_bytes(bytes_to_uint(random_bytes)),
                         expected_bytes)

        self.assertEqual(uint_to_bytes(bytes_to_uint_naive(zero_bytes)),
                         one_zero_byte)
        self.assertEqual(uint_to_bytes(bytes_to_uint_naive(random_bytes)),
                         expected_bytes)

    def test_TypeError_non_bytes_argument(self):
        self.assertRaises(TypeError, bytes_to_uint, unicode_string)
        self.assertRaises(TypeError, bytes_to_uint, None)

        self.assertRaises(TypeError, bytes_to_uint_naive, unicode_string)
        self.assertRaises(TypeError, bytes_to_uint_naive, None)


class Test_uint_to_bytes(unittest2.TestCase):
    def test_accuracy(self):
        self.assertEqual(uint_to_bytes(123456789), b('\x07[\xcd\x15'))
        self.assertEqual(uint_to_bytes_pycrypto(123456789),
                         b('\x07[\xcd\x15'))
        self.assertEqual(uint_to_bytes_array_based(123456789),
                         b('\x07[\xcd\x15'))
        self.assertEqual(uint_to_bytes_naive(123456789), b('\x07[\xcd\x15'))
        self.assertEqual(uint_to_bytes_naive_array_based(123456789),
                         b('\x07[\xcd\x15'))

        self.assertEqual(uint_to_bytes(long_value),
                         expected_bytes)
        self.assertEqual(uint_to_bytes_pycrypto(long_value),
                         expected_bytes)
        self.assertEqual(uint_to_bytes_array_based(long_value),
                         expected_bytes)
        self.assertEqual(uint_to_bytes_naive(long_value),
                         expected_bytes)
        self.assertEqual(uint_to_bytes_naive_array_based(long_value),
                         expected_bytes)

    def test_chunk_size(self):
        self.assertEqual(uint_to_bytes(long_value,
                                       long_value_blocksize),
                         expected_blocksize_bytes)
        self.assertEqual(uint_to_bytes_pycrypto(long_value,
                                                long_value_blocksize),
                         expected_blocksize_bytes)
        self.assertEqual(uint_to_bytes_array_based(long_value,
                                                   long_value_blocksize),
                         expected_blocksize_bytes)
        self.assertEqual(uint_to_bytes_naive(long_value,
                                             long_value_blocksize),
                         expected_blocksize_bytes)
        self.assertEqual(uint_to_bytes_naive_array_based(long_value,
                                                         long_value_blocksize),
                         expected_blocksize_bytes)


        self.assertEqual(uint_to_bytes(123456789, 6),
                         b('\x00\x00\x07[\xcd\x15'))
        self.assertEqual(uint_to_bytes(123456789, 7),
                         b('\x00\x00\x00\x07[\xcd\x15'))

        self.assertEqual(uint_to_bytes_pycrypto(123456789, 6),
                         b('\x00\x00\x07[\xcd\x15'))
        self.assertEqual(uint_to_bytes_pycrypto(123456789, 7),
                         b('\x00\x00\x00\x07[\xcd\x15'))
        
        self.assertEqual(uint_to_bytes_array_based(123456789, 6),
                         b('\x00\x00\x07[\xcd\x15'))
        self.assertEqual(uint_to_bytes_array_based(123456789, 7),
                         b('\x00\x00\x00\x07[\xcd\x15'))

        self.assertEqual(uint_to_bytes_naive(123456789, 6),
                         b('\x00\x00\x07[\xcd\x15'))
        self.assertEqual(uint_to_bytes_naive(123456789, 7),
                         b('\x00\x00\x00\x07[\xcd\x15'))

        self.assertEqual(uint_to_bytes_naive_array_based(123456789, 6),
                         b('\x00\x00\x07[\xcd\x15'))
        self.assertEqual(uint_to_bytes_naive_array_based(123456789, 7),
                         b('\x00\x00\x00\x07[\xcd\x15'))

    def test_zero(self):
        self.assertEqual(uint_to_bytes(0, 4), b('\x00') * 4)
        self.assertEqual(uint_to_bytes_array_based(0, 4), b('\x00') * 4)
        self.assertEqual(uint_to_bytes_naive(0, 4), b('\x00') * 4)
        self.assertEqual(uint_to_bytes_naive_array_based(0, 4), b('\x00') * 4)
        self.assertEqual(uint_to_bytes_pycrypto(0, 4), b('\x00') * 4)

        self.assertEqual(uint_to_bytes(0, 7), b('\x00') * 7)
        self.assertEqual(uint_to_bytes_naive(0, 7), b('\x00') * 7)
        self.assertEqual(uint_to_bytes_array_based(0, 7), b('\x00') * 7)
        self.assertEqual(uint_to_bytes_naive_array_based(0, 7), b('\x00') * 7)
        self.assertEqual(uint_to_bytes_pycrypto(0, 7), b('\x00') * 7)

        self.assertEqual(uint_to_bytes(0), b('\x00'))
        self.assertEqual(uint_to_bytes_naive(0), b('\x00'))
        self.assertEqual(uint_to_bytes_array_based(0), b('\x00'))
        self.assertEqual(uint_to_bytes_naive_array_based(0), b('\x00'))
        self.assertEqual(uint_to_bytes_pycrypto(0), b('\x00'))

    def test_correctness_against_base_implementation(self):
        # Slow test.
        values = [
            1 << 512,
            1 << 8192,
            1 << 77,
        ]
        for value in values:
            self.assertEqual(uint_to_bytes(value), uint_to_bytes_naive(value),
                             "Boom %d" % value)
            self.assertEqual(uint_to_bytes_array_based(value),
                             uint_to_bytes_naive(value),
                             "Boom %d" % value)
            self.assertEqual(uint_to_bytes(value),
                             uint_to_bytes_naive_array_based(value),
                             "Boom %d" % value)
            self.assertEqual(uint_to_bytes_pycrypto(value),
                             uint_to_bytes_naive(value),
                             "Boom %d" % value)
            self.assertEqual(bytes_to_uint(uint_to_bytes(value)),
                             value,
                             "Boom %d" % value)

    def test_correctness_for_primes(self):
        for prime in sieve:
            self.assertEqual(uint_to_bytes(prime), uint_to_bytes_naive(prime),
                             "Boom %d" % prime)
            self.assertEqual(uint_to_bytes_array_based(prime),
                             uint_to_bytes_naive(prime),
                             "Boom %d" % prime)
            self.assertEqual(uint_to_bytes_pycrypto(prime),
                             uint_to_bytes_naive(prime),
                             "Boom %d" % prime)

    def test_raises_OverflowError_when_chunk_size_is_insufficient(self):
        self.assertRaises(OverflowError, uint_to_bytes, 123456789, 3)
        self.assertRaises(OverflowError, uint_to_bytes, 299999999999, 4)

        self.assertRaises(OverflowError,
                          uint_to_bytes_array_based, 123456789, 3)
        self.assertRaises(OverflowError,
                          uint_to_bytes_array_based, 299999999999, 4)

        self.assertRaises(OverflowError, uint_to_bytes_naive, 123456789, 3)
        self.assertRaises(OverflowError, uint_to_bytes_naive, 299999999999, 4)

        self.assertRaises(OverflowError,
                          uint_to_bytes_naive_array_based, 123456789, 3)
        self.assertRaises(OverflowError,
                          uint_to_bytes_naive_array_based, 299999999999, 4)

    def test_raises_ValueError_when_negative_integer(self):
        self.assertRaises(ValueError, uint_to_bytes, -1)
        self.assertRaises(ValueError, uint_to_bytes_array_based, -1)
        self.assertRaises(ValueError, uint_to_bytes_naive, -1)
        self.assertRaises(ValueError, uint_to_bytes_naive_array_based, -1)

    def test_raises_TypeError_when_not_integer(self):
        self.assertRaises(TypeError, uint_to_bytes, None)
        self.assertRaises(TypeError, uint_to_bytes_array_based, None)
        self.assertRaises(TypeError, uint_to_bytes_naive, None)
        self.assertRaises(TypeError, uint_to_bytes_naive_array_based, None)