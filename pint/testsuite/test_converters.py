# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals, print_function, absolute_import

import itertools

from pint.compat import np
from pint.converters import (ScaleConverter, OffsetConverter, Converter)
from pint.converters import LogarithmicConverter
from pint.testsuite import helpers, BaseTestCase

class TestConverter(BaseTestCase):

    def test_converter(self):
        c = Converter()
        self.assertTrue(c.is_multiplicative)
        self.assertTrue(c.to_reference(8))
        self.assertTrue(c.from_reference(8))

    def test_multiplicative_converter(self):
        c = ScaleConverter(20.)
        self.assertEqual(c.from_reference(c.to_reference(100)), 100)
        self.assertEqual(c.to_reference(c.from_reference(100)), 100)

    def test_offset_converter(self):
        c = OffsetConverter(20., 2)
        self.assertEqual(c.from_reference(c.to_reference(100)), 100)
        self.assertEqual(c.to_reference(c.from_reference(100)), 100)

    @helpers.requires_numpy()
    def test_converter_inplace(self):
        for c in (ScaleConverter(20.), OffsetConverter(20., 2)):
            fun1 = lambda x, y: c.from_reference(c.to_reference(x, y), y)
            fun2 = lambda x, y: c.to_reference(c.from_reference(x, y), y)
            for fun, (inplace, comp) in itertools.product((fun1, fun2),
                                                          ((True, self.assertIs), (False, self.assertIsNot))):
                a = np.ones((1, 10))
                ac = np.ones((1, 10))
                r = fun(a, inplace)
                np.testing.assert_allclose(r, ac)
                comp(a, r)

    def test_logarithmic_converter(self):
        c = LogarithmicConverter(0.001, 10, 10)
        self.assertEqual(c.from_reference(c.to_reference(100)), 100)
        self.assertEqual(c.to_reference(c.from_reference(100)), 100)

        # converter for dBm
        c = LogarithmicConverter(logreference=0.001, logbase=10, scale=10)
        self.assertAlmostEqual(c.from_reference(1e-3), 0)  # 1 mW is 0 dBm
        self.assertAlmostEqual(c.from_reference(10 * 1e-3), 10)  # 10 mW is 10 dBm
        self.assertAlmostEqual(c.from_reference(0.1 * 1e-3), -10)  # 0.1 mW is -10 dBm
        self.assertAlmostEqual(c.to_reference(0), 1e-3)  # 0 dBm is 1 mW
        self.assertAlmostEqual(c.to_reference(-20), 0.01 * 1e-3)  # -20 dBm is 0.01 mW
        self.assertAlmostEqual(c.to_reference(20), 100 * 1e-3)  # 20 dBm is 100 mW

        # converter for dBW
        c = LogarithmicConverter(1, 10, 10)
        self.assertAlmostEqual(c.from_reference(1), 0)  # 1 W is 0 dBW
        self.assertAlmostEqual(c.from_reference(10), 10)  # 10 W is 10 dBW
        self.assertAlmostEqual(c.from_reference(0.1), -10)  # 0.1 W is -10 dBW
        self.assertAlmostEqual(c.to_reference(0), 1)  # 0 dBW is 1 W
        self.assertAlmostEqual(c.to_reference(-20), 0.01)  # -20 dBW is 0.01 W
        self.assertAlmostEqual(c.to_reference(20), 100)  # 20 dBW is 100 W
        self.assertAlmostEqual(c.to_reference(3), 1.995, places=2)  # 3 dBW is 2 W

        # converter for dBV
        c = LogarithmicConverter(1, 10, 20)
        self.assertAlmostEqual(c.from_reference(2), 6.02, places=2)  # 2 V is 6 dBW
        self.assertAlmostEqual(c.to_reference(0), 1)  # 0 dBV is 1 V
        self.assertAlmostEqual(c.to_reference(6), 1.995, places=2)  # 6 dBV is 2 V

        # converter for dBSPL
        c = LogarithmicConverter(20e-6, 10, 20)
        self.assertAlmostEqual(c.to_reference(0), 20e-6)  # 0 dBSPL  is 20 uPa
