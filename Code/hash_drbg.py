#! /usr/bin/env python
# -*- coding: utf8 -*-

__version__ = "$Revision$"
# $Id$

from math import ceil
import random
import time
import sys
import os

# platform dependant imports
if os.name == 'e32':
    import camera
    from pys60crypto import sha256

    sys.path.append('e:\ecc4pys60')
else:
    from hashlib import sha256

__all__ = ['HashDRBG', 'get_entropy']

if os.name == 'e32':
    def get_entropy(num_bytes = 125):
        size = max(camera.image_sizes())
        image = None
        samples = []
        num_samples = num_bytes / 3

        if num_bytes % 3 != 0:
            num_bytes += 1

        if 'forced' in camera.flash_modes():
            image = camera.take_photo('RGB', size, 3)
        else:
            image = camera.take_photo('RGB', size)

        while len(samples) < num_samples:
            pixels = image.getpixel((random.randint(0, size[0] - 1),
                                     random.randint(0, size[1] - 1)))
            for i in pixels[0]:
                samples.append("%.2x" % (i,))

        for i in xrange(num_bytes % 3):
            samples.pop()

        return long("".join(samples), 16)
else:
    def get_entropy(num_bytes = 125):
        entropy = os.urandom(num_bytes)
        result = 0

        for i in xrange(num_bytes):
            result += ord(entropy[i]) * 256**(num_bytes - (1 + i))

        return result

def _hash_df(input, number_of_bits):
    temp = ""
    length = int(ceil(float(number_of_bits) / 160))
    counter = 1

    for i in xrange(length):
        temp = temp + sha256("%.2x%.8x%s" % (counter, number_of_bits, input)).hexdigest()
        counter = (counter + 1) % 256

    return long(temp[:number_of_bits / 4], 16)

class HashDRBG(object):
    #initial nonce
    __initial_nonce = int(time.time())

    def __init__(self, seed = get_entropy(55)):
        entropy = get_entropy(125)
        nonce = HashDRBG.__initial_nonce
        HashDRBG.__initial_nonce += 1

        seed_material = "%x%x" % (entropy, nonce)

        self.__v = _hash_df(seed_material, 440)
        self.__c = _hash_df("00%x" % (self.__v,), 440)
        self.__reseed_counter = 1

    def __call__(self, num_bytes):
        if num_bytes > 625:
            raise ValueError("At most 625 bytes can be requested (%d requested)." %
                                (num_bytes))

        m = int(ceil(num_bytes / 20.0))
        modulus = 2**440
        data = self.__v
        W = ""

        for i in xrange(m):
            w = sha256("%x" % (data,)).hexdigest()
            W = W + w
            data = (data + 1) % modulus

        result = long(W[:num_bytes*2], 16)
        H = long(sha256("03%x" % (self.__v,)).hexdigest(), 16)
        self.__v = (self.__v + H + self.__reseed_counter) % modulus
        self.__reseed_counter += 1

        return result

a = HashDRBG()
print "%x" % (a(128),)
