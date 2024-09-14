# Reverse for HelloPython
from ctypes import * 
import sys
import operator
import contextlib


def encryption(v, k):
    y = c_uint32(v[0])
    z = c_uint32(v[1])
    sum = c_uint32(0)
    delta = 0x9e3779b9
    n = 32
    w = [0, 0]

    while(n>0):
        sum.value += delta
        y.value += ( z.value << 4 ) + k[0] ^ z.value + sum.value ^ ( z.value >> 5 ) + k[1]
        z.value += ( y.value << 4 ) + k[2] ^ y.value + sum.value ^ ( y.value >> 5 ) + k[3]
        n -= 1

    w[0] = y.value
    w[1] = z.value
    return w

def decription(v, k):
    y = c_uint32(v[0])
    z = c_uint32(v[1])
    sum = c_uint32(0xc6ef3720)
    delta = 0x9e3779b9
    n = 0
    w = [0, 0]

    while (n < 32):
        n += 1
        z.value -= (y.value << 4) + k[2] ^ y.value + sum.value ^ (y.value >> 5) + k[3]
        y.value -= (z.value << 4) + k[0] ^ z.value + sum.value ^ (z.value >> 5) + k[1]
        sum.value -= delta

    w[0] = y.value
    w[1] = z.value
    return w


if __name__ == '__main__':
    # sum=0
    # delta=0x9e3779b9
    # for _ in range(32):
    #     sum+=delta
    #     sum%=(2**32)
    # print(hex(sum))

    value = [0xf1f5d29b, 0x6e4414ec] 
    key = [3735928559, 590558003, 19088743, 4275878552]
    w = decription(value, key)
    print('flag{{{}}}'.format('_'.join(map(hex, w)).replace('0x', '').replace('L', '')))
