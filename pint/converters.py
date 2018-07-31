# -*- coding: utf-8 -*-
"""
    pint.converters
    ~~~~~~~~~

    Functions and classes related to unit conversions.

    :copyright: 2016 by Pint Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import (division, unicode_literals, print_function,
                        absolute_import)
from math import log, pow

class Converter(object):
    """Base class for value converters.
    """

    is_multiplicative = True

    def to_reference(self, value, inplace=False):
        return value

    def from_reference(self, value, inplace=False):
        return value


class ScaleConverter(Converter):
    """A linear transformation
    """

    is_multiplicative = True

    def __init__(self, scale):
        self.scale = scale

    def to_reference(self, value, inplace=False):
        if inplace:
            value *= self.scale
        else:
            value = value * self.scale

        return value

    def from_reference(self, value, inplace=False):
        if inplace:
            value /= self.scale
        else:
            value = value / self.scale

        return value


class OffsetConverter(Converter):
    """An affine transformation
    """

    def __init__(self, scale, offset):
        self.scale = scale
        self.offset = offset

    @property
    def is_multiplicative(self):
        return self.offset == 0

    def to_reference(self, value, inplace=False):
        if inplace:
            value *= self.scale
            value += self.offset
        else:
            value = value * self.scale + self.offset

        return value

    def from_reference(self, value, inplace=False):
        if inplace:
            value -= self.offset
            value /= self.scale
        else:
            value = (value - self.offset) / self.scale

        return value


class LogarithmicConverter(Converter):
    """ A converter for logarithmic units

    """
    def __init__(self, scale, logbase, factor):
        self.scale = scale
        self.logbase = logbase
        self.factor = factor

    @property
    def is_multiplicative(self):
        return False

    def to_reference(self, value, inplace=False):
        if inplace:
            value /= self.factor
            # TODO: not sure how to make it inplace
            value = self.scale * pow(self.logbase, value)
        else:
            value = self.scale * pow(self.logbase, value / self.factor)

        return value

    def from_reference(self, value, inplace=False):
        if inplace:
            value /= self.scale
            # TODO: not sure how to make it inplace
            value = self.factor * log(value, self.logbase)
        else:
            value = self.factor * log(value / self.scale, self.logbase)

        return value

    def __repr__(self):
        return('<LogarithmicConverter (scale: {}, logbase: {}, factor: {})>'
               .format(self.scale, self.logbase, self.factor))
