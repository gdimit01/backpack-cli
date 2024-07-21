import unittest
from collection import get_pie_data, format_weight

class TestGetPieData(unittest.TestCase):
    def test1(self):
        data = {
            'Shelter': 3300.0,
            'Sleep': 960.0
        }
        expected_result = [
            {"name": 'Shelter    3.3 kg', "value": 3300},
            {"name": 'Sleep      960 g', "value": 960}
        ]
        self.assertEqual(get_pie_data(data), expected_result)

class TestFormatWeight(unittest.TestCase):
    def test_kg(self):
        self.assertEqual(format_weight(1500), "1.5 kg")
        self.assertEqual(format_weight(1000), "1.0 kg")
        self.assertEqual(format_weight(12345.67), "12.3 kg")

    def test_gram(self):
        self.assertEqual(format_weight(500), "500 g")
        self.assertEqual(format_weight(999.99), "999 g")

if __name__ == '__main__':
    unittest.main()
