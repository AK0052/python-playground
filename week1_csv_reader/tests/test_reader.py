# tests/test_reader.py
import os, sys, unittest

# Make week1_csv_reader importable when running tests from repo root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "week1_csv_reader"))

from reader import filter_rows  # now available

class TestFilterRows(unittest.TestCase):
    def test_basic_filter_and_columns(self):
        rows = [
            {"id": "1", "name": "Alice", "age": "17"},
            {"id": "2", "name": "Bob", "age": "22"},
            {"id": "3", "name": "Charlie", "age": "19"},
        ]
        columns = ["id", "name", "age"]
        out = filter_rows(rows, columns, min_age=18)
        self.assertEqual(len(out), 2)
        self.assertEqual(out[0], {"id": "2", "name": "Bob", "age": "22"})
        self.assertEqual(out[1], {"id": "3", "name": "Charlie", "age": "19"})

    def test_invalid_age_skipped(self):
        rows = [
            {"id": "4", "name": "BadRow", "age": "oops"},
            {"id": "5", "name": "Eve", "age": "18"},
        ]
        columns = ["id", "name", "age"]
        out = filter_rows(rows, columns, min_age=18)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["id"], "5")

if __name__ == "__main__":
    unittest.main()
