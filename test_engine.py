import unittest
from engine import calculate_supplement

class TestCalculateSupplement(unittest.TestCase):
    def test_single_no_children(self):
        input_data = {
            "id": "001",
            "numberOfChildren": 0,
            "familyComposition": "single",
            "familyUnitInPayForDecember": True
        }
        expected_output = {
            "id": "001",
            "isEligible": True,
            "baseAmount": 60.0,
            "childrenAmount": 0.0,
            "supplementAmount": 60.0
        }
        self.assertEqual(calculate_supplement(input_data), expected_output)

    def test_single_with_children(self):
        input_data = {
            "id": "002",
            "numberOfChildren": 1,
            "familyComposition": "single",
            "familyUnitInPayForDecember": True
        }
        expected_output = {
            "id": "002",
            "isEligible": True,
            "baseAmount": 120.0,
            "childrenAmount": 20.0,
            "supplementAmount": 140.0
        }
        self.assertEqual(calculate_supplement(input_data), expected_output)

    def test_couple_no_children(self):
        input_data = {
            "id": "003",
            "numberOfChildren": 0,
            "familyComposition": "couple",
            "familyUnitInPayForDecember": True
        }
        expected_output = {
            "id": "003",
            "isEligible": True,
            "baseAmount": 120.0,
            "childrenAmount": 0.0,
            "supplementAmount": 120.0
        }
        self.assertEqual(calculate_supplement(input_data), expected_output)

    def test_couple_with_children(self):
        input_data = {
            "id": "004",
            "numberOfChildren": 3,
            "familyComposition": "couple",
            "familyUnitInPayForDecember": True
        }
        expected_output = {
            "id": "004",
            "isEligible": True,
            "baseAmount": 120.0,
            "childrenAmount": 60.0,
            "supplementAmount": 180.0
        }
        self.assertEqual(calculate_supplement(input_data), expected_output)

    def test_ineligible(self):
        input_data = {
            "id": "005",
            "numberOfChildren": 0,
            "familyComposition": "single",
            "familyUnitInPayForDecember": False
        }
        expected_output = {
            "id": "005",
            "isEligible": False,
            "baseAmount": 0.0,
            "childrenAmount": 0.0,
            "supplementAmount": 0.0
        }
        self.assertEqual(calculate_supplement(input_data), expected_output)

if __name__ == "__main__":
    unittest.main()
