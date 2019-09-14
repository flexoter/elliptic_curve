"""
    Module contains unit tests for simplicityTests module

"""

import unittest
import simplicityTests


class root_test(unittest.TestCase):

    def test_root_computation(self):
        self.assertEqual(simplicityTests.root_computation(10, 53), tuple([13, 40]))
        self.assertEqual(simplicityTests.root_computation(11, 37), tuple([23, 14]))
        self.assertEqual(simplicityTests.root_computation(14, 193), tuple([173, 20]))

    def test_dcg(self):
        self.assertEqual(simplicityTests.gcd(3, 5), 1)
        self.assertEqual(simplicityTests.gcd(3, 137), 1)
        self.assertEqual(simplicityTests.gcd(7, 137), 1)
        self.assertEqual(simplicityTests.gcd(5, 7), 1)


if __name__ == '__main__':
    unittest.main()