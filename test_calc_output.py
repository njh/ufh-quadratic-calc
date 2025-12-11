#!/usr/bin/env python3
import unittest

ERROR_TOLERANCE = 2  # Acceptable percentage error

def heat_output_100(r_value, flow_temp, room_temp):
    dT = flow_temp - room_temp
    m = 111.8353 * (r_value ** 2) - 39.5733 * r_value + 6.66364
    c = 558.6506 * (r_value ** 2) - 197.8043 * r_value + 33.31581
    return (m * dT) - c

def heat_output_150(r_value, flow_temp, room_temp):
    dT = flow_temp - room_temp
    m = 86.6934 * (r_value ** 2) - 31.5422 * r_value + 5.74376
    c = 424.6747 * (r_value ** 2) - 156.4000 * r_value + 28.70193
    return (m * dT) - c

def heat_output_200(r_value, flow_temp, room_temp):
    dT = flow_temp - room_temp
    m = 68.2878 * (r_value ** 2) - 25.3673 * r_value + 4.97757
    c = 341.2530 * (r_value ** 2) - 126.7552 * r_value + 24.89369
    return (m * dT) - c

def heat_output_300(r_value, flow_temp, room_temp):
    dT = flow_temp - room_temp
    m = 40.9224 * (r_value ** 2) - 16.0253 * r_value + 3.75131
    c = 204.8434 * (r_value ** 2) - 80.0533 * r_value + 18.74228
    return (m * dT) - c

class TestCalculations(unittest.TestCase):

    def assert_percent_error(self, actual, expected, threshold_percent=2):
        percent_error = abs(actual - expected) / expected * 100
        assert percent_error < threshold_percent, (
            f"Error {percent_error:.2f}% exceeds threshold of {threshold_percent}%: "
            f"expected={expected}, actual={actual}")

    def test_100_010_35_20(self):
        watts_m2 = heat_output_100(r_value=0.10, flow_temp=35, room_temp=20)
        self.assert_percent_error(watts_m2, 38.9, ERROR_TOLERANCE)

    def test_150_000_40_20(self):
        watts_m2 = heat_output_150(r_value=0.00, flow_temp=40, room_temp=20)
        self.assert_percent_error(watts_m2, 86.4, ERROR_TOLERANCE)

    def test_200_015_35_22(self):
        watts_m2 = heat_output_200(r_value=0.15, flow_temp=35, room_temp=22)
        self.assert_percent_error(watts_m2, 21.6, ERROR_TOLERANCE)

    def test_300_005_55_18(self):
        watts_m2 = heat_output_300(r_value=0.05, flow_temp=55, room_temp=18)
        self.assert_percent_error(watts_m2, 96.9, ERROR_TOLERANCE)

if __name__ == '__main__':
    unittest.main()

