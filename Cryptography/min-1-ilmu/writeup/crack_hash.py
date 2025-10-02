#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Oranav <contact@oranav.me>
#
# Distributed under terms of the GPLv3 license.
# Based on: https://gist.github.com/HoLyVieR/11e464a91b290e33b38e

from binascii import hexlify, unhexlify
import struct

DIGEST_SIZE = 16
BLOCK_SIZE = 64

# Constants for compression function.
S11 = 7
S12 = 12
S13 = 17
S14 = 22
S21 = 5
S22 = 9
S23 = 14
S24 = 20
S31 = 4
S32 = 11
S33 = 16
S34 = 23
S41 = 6
S42 = 10
S43 = 15
S44 = 21

PADDING = b"\x80" + 63*b"\0"


def F(x, y, z): return (((x) & (y)) | ((~x) & (z)))

def G(x, y, z): return (((x) & (z)) | ((y) & (~z)))

def H(x, y, z): return ((x) ^ (y) ^ (z))

def I(x, y, z): return((y) ^ ((x) | (~z)))

def ROTATE_LEFT(x, n):
    x = x & 0xffffffff   # make shift unsigned
    return (((x) << (n)) | ((x) >> (32-(n)))) & 0xffffffff


def ROTATE_RIGHT(x, n):
    return ROTATE_LEFT(x, 32-n)


def FF(a, b, c, d, x, s, ac):
    a = a + F ((b), (c), (d)) + (x) + (ac)
    a = ROTATE_LEFT ((a), (s))
    a = a + b
    return a # must assign this to a

def GG(a, b, c, d, x, s, ac):
    a = a + G ((b), (c), (d)) + (x) + (ac)
    a = ROTATE_LEFT ((a), (s))
    a = a + b
    return a # must assign this to a

def HH(a, b, c, d, x, s, ac):
    a = a + H ((b), (c), (d)) + (x) + (ac)
    a = ROTATE_LEFT ((a), (s))
    a = a + b
    return a # must assign this to a

def II(a, b, c, d, x, s, ac):
    a = a + I ((b), (c), (d)) + (x) + (ac)
    a = ROTATE_LEFT ((a), (s))
    a = a + b
    return a # must assign this to a

def InvFF(res, b, c, d, x, s, ac):
    # This is just FF in reverese, given that only a is unknown.
    res = res - b
    res = ROTATE_RIGHT ((res), (s))
    res = res - F ((b), (c), (d)) - (x) - (ac)
    return res & 0xffffffff

def InvGG(res,b,c,d,x,s,ac):
    # This is just GG in reverse, given that only a is unknown.
    res = res - b
    res = ROTATE_RIGHT ((res), (s))
    res = res - G ((b), (c), (d)) - (x) - (ac)
    return res & 0xffffffff

def InvHH(res, b, c, d, x, s, ac):
    # This is just HH in reverse, given that only a is unknown.
    res = res - b
    res = ROTATE_RIGHT ((res), (s))
    res = res - H ((b), (c), (d)) - (x) - (ac)
    return res & 0xffffffff

def InvII(res, b, c, d, x, s, ac):
    # This is just II in reverse, given that only a is unknown.
    res = res - b
    res = ROTATE_RIGHT ((res), (s))
    res = res - I ((b), (c), (d)) - (x) - (ac)
    return res & 0xffffffff

def PreimageFF(res, a, b, c, d, s, ac):
    # This is FF for when the result is known but the input block is unknown.
    res = res - b
    res = ROTATE_RIGHT ((res), (s))
    res = res - F ((b), (c), (d)) - (ac)
    return (res - a) & 0xffffffff, a


def padding(msg_bits):
    """padding(msg_bits) - Generates the padding that should be
    appended to the end of a message of the given size to reach
    a multiple of the block size."""

    index = int((msg_bits >> 3) & 0x3f)
    if index < 56:
        padLen = (56 - index)
    else:
        padLen = (120 - index)

    # (the last 8 bytes store the number of bits in the message)
    return PADDING[:padLen] + _encode((msg_bits & 0xffffffff, msg_bits>>32), 8)


def md15_compress(msg):
    state = (0x67452301,
             0xefcdab89,
             0x98badcfe,
             0x10325476,)
    a, b, c, d = state
    block = msg + padding(len(msg) * 8)
    x = _decode(block, BLOCK_SIZE)

    #  Round
    a = FF (a, b, c, d, x[ 0], S11, 0xd76aa478) # 1
    d = FF (d, a, b, c, x[ 1], S12, 0xe8c7b756) # 2
    c = FF (c, d, a, b, x[ 2], S13, 0x242070db) # 3
    b = FF (b, c, d, a, x[ 3], S14, 0xc1bdceee) # 4
    a = FF (a, b, c, d, x[ 4], S11, 0xf57c0faf) # 5
    d = FF (d, a, b, c, x[ 5], S12, 0x4787c62a) # 6
    c = FF (c, d, a, b, x[ 6], S13, 0xa8304613) # 7
    b = FF (b, c, d, a, x[ 7], S14, 0xfd469501) # 8
    a = FF (a, b, c, d, x[ 8], S11, 0x698098d8) # 9
    d = FF (d, a, b, c, x[ 9], S12, 0x8b44f7af) # 10
    c = FF (c, d, a, b, x[10], S13, 0xffff5bb1) # 11
    b = FF (b, c, d, a, x[11], S14, 0x895cd7be) # 12
    a = FF (a, b, c, d, x[12], S11, 0x6b901122) # 13
    d = FF (d, a, b, c, x[13], S12, 0xfd987193) # 14
    c = FF (c, d, a, b, x[14], S13, 0xa679438e) # 15
    b = FF (b, c, d, a, x[15], S14, 0x49b40821) # 16
    d = GG (d, a, b, c, x[ 6], S22, 0xc040b340) # 18
    c = GG (c, d, a, b, x[11], S23, 0x265e5a51) # 19
    a = GG (a, b, c, d, x[ 5], S21, 0xd62f105d) # 21
    d = GG (d, a, b, c, x[10], S22,  0x2441453) # 22
    c = GG (c, d, a, b, x[15], S23, 0xd8a1e681) # 23
    b = GG (b, c, d, a, x[ 4], S24, 0xe7d3fbc8) # 24
    a = GG (a, b, c, d, x[ 9], S21, 0x21e1cde6) # 25
    d = GG (d, a, b, c, x[14], S22, 0xc33707d6) # 26
    b = GG (b, c, d, a, x[ 8], S24, 0x455a14ed) # 28
    a = GG (a, b, c, d, x[13], S21, 0xa9e3e905) # 29
    c = GG (c, d, a, b, x[ 7], S23, 0x676f02d9) # 31
    b = GG (b, c, d, a, x[12], S24, 0x8d2a4c8a) # 32
    a = HH (a, b, c, d, x[ 5], S31, 0xfffa3942) # 33
    d = HH (d, a, b, c, x[ 8], S32, 0x8771f681) # 34
    c = HH (c, d, a, b, x[11], S33, 0x6d9d6122) # 35
    b = HH (b, c, d, a, x[14], S34, 0xfde5380c) # 36
    d = HH (d, a, b, c, x[ 4], S32, 0x4bdecfa9) # 38
    c = HH (c, d, a, b, x[ 7], S33, 0xf6bb4b60) # 39
    b = HH (b, c, d, a, x[10], S34, 0xbebfbc70) # 40
    a = HH (a, b, c, d, x[13], S31, 0x289b7ec6) # 41
    b = HH (b, c, d, a, x[ 6], S34,  0x4881d05) # 44
    a = HH (a, b, c, d, x[ 9], S31, 0xd9d4d039) # 45
    d = HH (d, a, b, c, x[12], S32, 0xe6db99e5) # 46
    c = HH (c, d, a, b, x[15], S33, 0x1fa27cf8) # 47
    d = II (d, a, b, c, x[ 7], S42, 0x432aff97) # 50
    c = II (c, d, a, b, x[14], S43, 0xab9423a7) # 51
    b = II (b, c, d, a, x[ 5], S44, 0xfc93a039) # 52
    a = II (a, b, c, d, x[12], S41, 0x655b59c3) # 53
    c = II (c, d, a, b, x[10], S43, 0xffeff47d) # 55
    a = II (a, b, c, d, x[ 8], S41, 0x6fa87e4f) # 57
    d = II (d, a, b, c, x[15], S42, 0xfe2ce6e0) # 58
    c = II (c, d, a, b, x[ 6], S43, 0xa3014314) # 59
    b = II (b, c, d, a, x[13], S44, 0x4e0811a1) # 60
    a = II (a, b, c, d, x[ 4], S41, 0xf7537e82) # 61
    d = II (d, a, b, c, x[11], S42, 0xbd3af235) # 62
    b = II (b, c, d, a, x[ 9], S44, 0xeb86d391) # 64

    state = (0xffffffff & (state[0] + a),
             0xffffffff & (state[1] + b),
             0xffffffff & (state[2] + c),
             0xffffffff & (state[3] + d),)
    return _encode(state, DIGEST_SIZE)


def md15_decompress(state):
    msg = b'A'*16
    block = msg + padding(len(msg) * 8)
    a, b, c, d = _decode(state, DIGEST_SIZE)
    x = _decode(block, BLOCK_SIZE)
    # x[0:4] are unknowns so we must not use them
    x[0:4] = [None] * 4
    initial_state = (0x67452301,
                     0xefcdab89,
                     0x98badcfe,
                     0x10325476,)

    # reverse final state calculation
    a = (a - initial_state[0]) & 0xffffffff
    b = (b - initial_state[1]) & 0xffffffff
    c = (c - initial_state[2]) & 0xffffffff
    d = (d - initial_state[3]) & 0xffffffff

    # reverse rounds 12...5
    b = InvII (b, c, d, a, x[ 9], S44, 0xeb86d391)
    d = InvII (d, a, b, c, x[11], S42, 0xbd3af235)
    a = InvII (a, b, c, d, x[ 4], S41, 0xf7537e82)
    b = InvII (b, c, d, a, x[13], S44, 0x4e0811a1)
    c = InvII (c, d, a, b, x[ 6], S43, 0xa3014314)
    d = InvII (d, a, b, c, x[15], S42, 0xfe2ce6e0)
    a = InvII (a, b, c, d, x[ 8], S41, 0x6fa87e4f)
    c = InvII (c, d, a, b, x[10], S43, 0xffeff47d)
    a = InvII (a, b, c, d, x[12], S41, 0x655b59c3)
    b = InvII (b, c, d, a, x[ 5], S44, 0xfc93a039)
    c = InvII (c, d, a, b, x[14], S43, 0xab9423a7)
    d = InvII (d, a, b, c, x[ 7], S42, 0x432aff97)
    c = InvHH (c, d, a, b, x[15], S33, 0x1fa27cf8)
    d = InvHH (d, a, b, c, x[12], S32, 0xe6db99e5)
    a = InvHH (a, b, c, d, x[ 9], S31, 0xd9d4d039)
    b = InvHH (b, c, d, a, x[ 6], S34,  0x4881d05)
    a = InvHH (a, b, c, d, x[13], S31, 0x289b7ec6)
    b = InvHH (b, c, d, a, x[10], S34, 0xbebfbc70)
    c = InvHH (c, d, a, b, x[ 7], S33, 0xf6bb4b60)
    d = InvHH (d, a, b, c, x[ 4], S32, 0x4bdecfa9)
    b = InvHH (b, c, d, a, x[14], S34, 0xfde5380c)
    c = InvHH (c, d, a, b, x[11], S33, 0x6d9d6122)
    d = InvHH (d, a, b, c, x[ 8], S32, 0x8771f681)
    a = InvHH (a, b, c, d, x[ 5], S31, 0xfffa3942)
    b = InvGG (b, c, d, a, x[12], S24, 0x8d2a4c8a)
    c = InvGG (c, d, a, b, x[ 7], S23, 0x676f02d9)
    a = InvGG (a, b, c, d, x[13], S21, 0xa9e3e905)
    b = InvGG (b, c, d, a, x[ 8], S24, 0x455a14ed)
    d = InvGG (d, a, b, c, x[14], S22, 0xc33707d6)
    a = InvGG (a, b, c, d, x[ 9], S21, 0x21e1cde6)
    b = InvGG (b, c, d, a, x[ 4], S24, 0xe7d3fbc8)
    c = InvGG (c, d, a, b, x[15], S23, 0xd8a1e681)
    d = InvGG (d, a, b, c, x[10], S22,  0x2441453)
    a = InvGG (a, b, c, d, x[ 5], S21, 0xd62f105d)
    c = InvGG (c, d, a, b, x[11], S23, 0x265e5a51)
    d = InvGG (d, a, b, c, x[ 6], S22, 0xc040b340)
    b = InvFF (b, c, d, a, x[15], S14, 0x49b40821) # 16
    c = InvFF (c, d, a, b, x[14], S13, 0xa679438e) # 15
    d = InvFF (d, a, b, c, x[13], S12, 0xfd987193) # 14
    a = InvFF (a, b, c, d, x[12], S11, 0x6b901122) # 13
    b = InvFF (b, c, d, a, x[11], S14, 0x895cd7be) # 12
    c = InvFF (c, d, a, b, x[10], S13, 0xffff5bb1) # 11
    d = InvFF (d, a, b, c, x[ 9], S12, 0x8b44f7af) # 10
    a = InvFF (a, b, c, d, x[ 8], S11, 0x698098d8) # 9
    b = InvFF (b, c, d, a, x[ 7], S14, 0xfd469501) # 8
    c = InvFF (c, d, a, b, x[ 6], S13, 0xa8304613) # 7
    d = InvFF (d, a, b, c, x[ 5], S12, 0x4787c62a) # 6
    a = InvFF (a, b, c, d, x[ 4], S11, 0xf57c0faf) # 5
    # reverse rounds 4...1 and restore block data
    x[3], b = PreimageFF (b, initial_state[1], c, d, a, S14, 0xc1bdceee) # 4
    x[2], c = PreimageFF (c, initial_state[2], d, a, b, S13, 0x242070db) # 3
    x[1], d = PreimageFF (d, initial_state[3], a, b, c, S12, 0xe8c7b756) # 2
    x[0], a = PreimageFF (a, initial_state[0], b, c, d, S11, 0xd76aa478) # 1

    block = _encode(x, BLOCK_SIZE)
    return block[:16]


def _encode(input, len):
    k = len >> 2
    res = struct.pack(*(("%iI" % k,) + tuple(input[:k])))
    return res


def _decode(input, len):
    k = len >> 2
    res = struct.unpack("%iI" % k, input[:len])
    return list(res)


def main():
    digest = unhexlify("0e834a4b35ee550b0be13c6bd03c48f9") 
    data = md15_decompress(digest)
    assert md15_compress(data) == digest
    print("Decompressed:", hexlify(data))


if __name__=="__main__":
    main()