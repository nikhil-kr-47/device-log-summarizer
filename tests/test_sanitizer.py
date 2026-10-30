import unittest
import sys
import os

# Add src directory to system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from sanitizer import clean_sensor_readings


class TestSensorDataSanitizer(unittest.TestCase):

    def test_mixed_inputs_and_filtering(self):
        """Test general case with valid floats, numeric strings, None, and negative error flags."""
        raw_readings = [23.5, "45.1", None, -1.0, "invalid_val", -99.9, 120]
        expected = [23.5, 45.1, 120.0]
        self.assertEqual(clean_sensor_readings(raw_readings), expected)

    def test_value_clipping(self):
        """Test that values exceeding 500.0 are capped at 500.0."""
        raw_readings = [499.9, 500.0, 500.1, "750", 1200.5]
        expected = [499.9, 500.0, 500.0, 500.0, 500.0]
        self.assertEqual(clean_sensor_readings(raw_readings), expected)

    def test_empty_and_entirely_invalid_inputs(self):
        """Test edge cases: empty list, None input, and list with only invalid entries."""
        self.assertEqual(clean_sensor_readings([]), [])
        self.assertEqual(clean_sensor_readings(None), [])
        self.assertEqual(clean_sensor_readings([None, "N/A", -10, "error"]), [])


if __name__ == "__main__":
    unittest.main()
