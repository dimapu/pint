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
from .compat import log, HAS_NUMPY


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
    def __init__(self, logreference, logbase, scale):
        """

        :param logreference: reference value in linear units
        :param logbase:  logarithm base
        :param scale:  scaling factor to obtain logarithmic units
        """

        if HAS_NUMPY is False:
            print("'numpy' package is not installed. Will use math.log() "
                  "for logarithmic units.")
        self.logreference = logreference
        self.logbase = logbase
        self.scale = scale

    @property
    def is_multiplicative(self):
        return False

    def to_reference(self, value, inplace=False):
        if inplace:
            value /= self.scale
            # TODO: not sure how to make it inplace
            value = self.logreference * pow(self.logbase, value)
        else:
            value = self.logreference * pow(self.logbase, value / self.scale)

        return value

    def from_reference(self, value, inplace=False):
        if inplace:
            value /= self.logreference
            # TODO: not sure how to make it inplace
            value = self.scale * log(value) / log(self.logbase)
        else:
            value = self.scale * log(value / self.logreference) / log(self.logbase)

        return value

    def __repr__(self):
        return('<LogarithmicConverter (logreference: {}, logbase: {}, scale: {})>'
               .format(self.logreference, self.logbase, self.scale))
