# f value unit test
import unittest

from f_value import f1f2Value


class TestFValue(unittest.TestCase):

    def setUp(self):
        self._v = f1f2Value()

    def test_RegionTest(self):

        test_patterns = [
            ('Type1', 'Cooling', 'region1', 'N', 0.0, 0.139),
            ('Type1', 'Cooling', 'region2', 'N', 0.0, 0.134),
            ('Type1', 'Cooling', 'region3', 'N', 0.0, 0.136),
            ('Type1', 'Cooling', 'region4', 'N', 0.0, 0.142),
            ('Type1', 'Cooling', 'region5', 'N', 0.0, 0.122),
            ('Type1', 'Cooling', 'region6', 'N', 0.0, 0.134),
            ('Type1', 'Cooling', 'region7', 'N', 0.0, 0.148),
            ('Type1', 'Cooling', 'region8', 'N', 0.0, 0.141),
            ('Type1', 'Heating', 'region1', 'N', 0.0, 0.175),
            ('Type1', 'Heating', 'region2', 'N', 0.0, 0.173),
            ('Type1', 'Heating', 'region3', 'N', 0.0, 0.160),
            ('Type1', 'Heating', 'region4', 'N', 0.0, 0.178),
            ('Type1', 'Heating', 'region5', 'N', 0.0, 0.191),
            ('Type1', 'Heating', 'region6', 'N', 0.0, 0.174),
            ('Type1', 'Heating', 'region7', 'N', 0.0, 0.200),
        ]
        for glassType, season, region, direction, lValue, expected in test_patterns:
            with self.subTest(gt=glassType, s=season, r=region, d=direction, l=lValue):
                actual = self._v.getValue(glassType, season, region, direction, lValue)
                self.assertAlmostEqual(actual, expected, delta=0.000001)

    def test_TypeTest(self):

        test_patterns = [
            ('Type1', 'Cooling', 'region1', 'N', 0.0, 0.139),
            ('Type2', 'Cooling', 'region1', 'N', 0.0, 0.132),
            ('Type3', 'Cooling', 'region1', 'N', 0.0, 0.130),
            ('Type4', 'Cooling', 'region1', 'N', 0.0, 0.132),
            ('Type5', 'Cooling', 'region1', 'N', 0.0, 0.128),
            ('Type6', 'Cooling', 'region1', 'N', 0.0, 0.129),
            ('Type7', 'Cooling', 'region1', 'N', 0.0, 0.126),
            ('Type1', 'Heating', 'region1', 'N', 0.0, 0.175),
            ('Type2', 'Heating', 'region1', 'N', 0.0, 0.167),
            ('Type3', 'Heating', 'region1', 'N', 0.0, 0.164),
            ('Type4', 'Heating', 'region1', 'N', 0.0, 0.167),
            ('Type5', 'Heating', 'region1', 'N', 0.0, 0.162),
            ('Type6', 'Heating', 'region1', 'N', 0.0, 0.162),
            ('Type7', 'Heating', 'region1', 'N', 0.0, 0.159),
        ]
        for glassType, season, region, direction, lValue, expected in test_patterns:
            with self.subTest(gt=glassType, s=season, r=region, d=direction, l=lValue):
                actual = self._v.getValue(glassType, season, region, direction, lValue)
                self.assertAlmostEqual(actual, expected, delta=0.000001)

    def test_DirectionTest(self):

        test_patterns = [
            ('Type1', 'Cooling', 'region1', 'N', 0.0, 0.139),
            ('Type1', 'Cooling', 'region1', 'NE', 0.0, 0.106),
            ('Type1', 'Cooling', 'region1', 'E', 0.0, 0.084),
            ('Type1', 'Cooling', 'region1', 'SE', 0.0, 0.081),
            ('Type1', 'Cooling', 'region1', 'S', 0.0, 0.091),
            ('Type1', 'Cooling', 'region1', 'SW', 0.0, 0.087),
            ('Type1', 'Cooling', 'region1', 'W', 0.0, 0.090),
            ('Type1', 'Cooling', 'region1', 'NW', 0.0, 0.111),
            ('Type1', 'Heating', 'region1', 'N', 0.0, 0.175),
            ('Type1', 'Heating', 'region1', 'NE', 0.0, 0.137),
            ('Type1', 'Heating', 'region1', 'E', 0.0, 0.081),
            ('Type1', 'Heating', 'region1', 'SE', 0.0, 0.055),
            ('Type1', 'Heating', 'region1', 'S', 0.0, 0.049),
            ('Type1', 'Heating', 'region1', 'SW', 0.0, 0.058),
            ('Type1', 'Heating', 'region1', 'W', 0.0, 0.085),
            ('Type1', 'Heating', 'region1', 'NW', 0.0, 0.140),
        ]
        for glassType, season, region, direction, lValue, expected in test_patterns:
            with self.subTest(gt=glassType, s=season, r=region, d=direction, l=lValue):
                actual = self._v.getValue(glassType, season, region, direction, lValue)
                self.assertAlmostEqual(actual, expected, delta=0.000001)

    def test_InterpolateTest(self):

        test_patterns = [
            ('Type1', 'Cooling', 'region1', 'N', 0.0, 0.139),
            ('Type1', 'Cooling', 'region1', 'N', 0.4, 0.260),
            ('Type1', 'Cooling', 'region1', 'N', 0.2, 0.1995),
        ]
        for glassType, season, region, direction, lValue, expected in test_patterns:
            with self.subTest(gt=glassType, s=season, r=region, d=direction, l=lValue):
                actual = self._v.getValue(glassType, season, region, direction, lValue)
                self.assertAlmostEqual(actual, expected, delta=0.000001)

    def test_Over20Test(self):

        test_patterns = [
            ('Type1', 'Cooling', 'region1', 'N', 20.0, 0.853),
            ('Type1', 'Cooling', 'region1', 'N', 25.0, 0.853),
        ]
        for glassType, season, region, direction, lValue, expected in test_patterns:
            with self.subTest(gt=glassType, s=season, r=region, d=direction, l=lValue):
                actual = self._v.getValue(glassType, season, region, direction, lValue)
                self.assertAlmostEqual(actual, expected, delta=0.000001)


if __name__ == "__main__":
    unittest.main()
