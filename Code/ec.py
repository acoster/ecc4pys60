#! /usr/bin/env python
# -*- coding: utf8 -*-

"""Elliptic curve over a prime field implementation.

This module offers two classes, `EllipticCurvePrime`, that implements
an elliptic curve over a prime field, and `CECPoint`, which implements
a point of an elliptic curve.

"""

__version__ = "$Revision$"
# $Id$

from modular import mod_inverse

__all__ = ['leftmost_bit', 'EllipticCurvePrime', 'ECPoint', 'infinity']

def leftmost_bit(x):
    assert x > 0

    result = 1L
    while result <= x:
        result = 2 * result
    return result / 2

class EllipticCurvePrime(object):

    """
    """

    def __init__(self, a, b, modulus):
        self.__a = a
        self.__b = b
        self.__modulus = modulus

    def is_on_curve(self, point):
        return (point.y**2 - (point.x**3 + self.__a * point.x + self.__b)) % \
                self.__modulus == 0

    def a(self):
        return self.__a
    a = property(a)

    def b(self):
        return self.__b
    b = property(b)

    def modulus(self):
        return self.__modulus
    modulus = property(modulus)


class ECPoint(object):

    """Implementation of a point on an elliptic curve over a prime
    field. This class offers overloaded operators, so "elliptic curve"
    arithmetic can ben expressed as normal arithmetic.

    """

    def __init__(self, curve = None, x = None, y = None, order = None):
        self.__curve = curve
        self.__order = order
        self.__x = x
        self.__y = y

        if curve and x and y:
            assert curve.is_on_curve(self)

        if order:
            assert self * order == infinity

# UNARY OPERATORS #############################################################
    def __neg__(self):
        return ECPoint(self.__curve, self.__x, -self.__y, self.__order)

# BINARY OPERATORS ############################################################
    def __eq__(self, right):
        is_same_curve = False

        # For comparsions using infinity
        if self.__curve != None and right.__curve != None:
            is_same_curve = self.__curve == right.__curve
        else:
            is_same_curve = True

        return is_same_curve and self.__x == right.__x and \
                                 self.__y == right.__y

    def __add__(self, right):
        if right == infinity:
            return self

        if self == infinity:
            return right

        assert self.__curve == right.__curve

        if self.__x == right.__x:
            if (self.__y + right.__y) % self.__curve.modulus == 0:
                return infinity
            return self.double()

        modulus = self.__curve.modulus
        lambda_ = ((right.__y - self.__y) * mod_inverse(right.__x -
                    self.__x, modulus)) % modulus

        x3 = (lambda_**2 - self.__x - right.__x) % modulus
        y3 = (lambda_ * (self.__x - x3) - self.__y) % modulus

        return ECPoint(self.__curve, x3, y3)

    def __mul__(self, right):
        if self.__order:
            right = right % self.__order

        if right == 0 or self == infinity:
            return infinity

        assert right > 0

        if right == 2:
            return self.double()

        right3 = 3 * right
        i = leftmost_bit(right3) / 2
        minus_self = -self

        result = self # the initial result is not changed, hence it can be
                      # a pointer to self instead of a copy

        while i > 1:
            result = result.double()
            if (right3 & i) != 0 and (right & i) == 0:
                result = result + self
            if (right3 & i) == 0 and (right & i) != 0:
                result = result + minus_self
            i = i / 2

        return result

# REVERSE BINARY OPERATORS ####################################################
    def __rmul__(self, left):
        return self * left

# OTHER METHODS ###############################################################
    def double(self):
        if self == infinity:
            return infinity

        modulus = self.__curve.modulus
        a = self.__curve.a

        lambda_ = ((3 * self.__x**2 + a) *
                  mod_inverse(2 * self.__y, modulus)) % modulus
        x = (lambda_**2 - 2 * self.__x) % modulus
        y = (lambda_ * (self.__x - x) - self.__y) % modulus

        return ECPoint(self.__curve, x, y)

    # Returns self * k + oOtherPoint * l
    def MultiplyPoints(self, k, Q, l):
        """Shamir's trick implementation. Returns 
        self * k + Q * l

        """
        R = infinity
        PQ = self + Q
        i = max(leftmost_bit(k), leftmost_bit(l))

        while i > 0:
            R = R.double()

            if i & k == i:
                if i & l == i:
                    R = R + PQ
                else:
                    R = R + self
            elif i & l == i:
                R = R + Q
            i /= 2

        return R

# PROPERTIES ##################################################################
    def x(self):
        return self.__x
    x = property(x)

    def y(self):
        return self.__y
    y = property(y)

    def curve(self):
        return self.__curve
    curve = property(curve)

    def order(self):
        return self.__order
    order = property(order)

# Infinity point
infinity = ECPoint()
