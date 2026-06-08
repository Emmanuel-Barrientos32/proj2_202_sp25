import unittest
from typing import Optional, Union
from proj22 import (Row, Node, read_csv_lines, listlen, filter_rows, parse_row)


class TestStructureBasics(unittest.TestCase):

    def test_row_instantiation(self):
        row = Row(
            country="United States",
            year=2002,
            electricity_and_heat_co2_emissions=2679.75,
            electricity_and_heat_co2_emissions_per_capita=9.3,
            energy_co2_emissions=5549.8,
            energy_co2_emissions_per_capita=19.2,
            total_co2_emissions_excluding_luc=5593.0,
            total_co2_emissions_excluding_lucf_per_capita=19.4
        )
        self.assertEqual(row.country, "United States")
        self.assertEqual(row.year, 2002)



    def test_node_instantiation(self):
        row = Row("United Kingdom", 2002, 1000.0, 15.0, 8000.0, 30.0, 5000.0, 75.0)
        n = Node(value=row, next=None)
        self.assertEqual(n.value.country, "United Kingdom")
        self.assertIsNone(n.next)

    def test_node_chain(self):
        row1 = Row("A", 2000, 1.0, 0.1, 2.0, 0.2, 3.0, 0.3)
        row2 = Row("B", 2001, 1.1, 0.2, 2.1, 0.3, 3.1, 0.4)
        n2 = Node(value=row2, next=None)
        n1 = Node(value=row1, next=n2)
        self.assertEqual(n1.value.country, "A")
        self.assertEqual(n1.next.value.country, "B")


class TestFunctionSignatures(unittest.TestCase):

    def test_parse_row_type(self):
        row = parse_row([
            "United States", "2002", "200.0", "3.0", "100.0", "4.5", "100.0", "2.5"
        ])
        self.assertIsInstance(row, Row)
        self.assertEqual(row.country, "United States")

    def test_read_csv_lines_type(self):
        result = read_csv_lines("some-ghg-emissions.csv")  # Ensure this file exists or mock it
        self.assertTrue(result is None or isinstance(result, Node))

    def test_listlen_none(self):
        self.assertEqual(listlen(None), 0)





    def test_listlen_chain(self):
        row1 = Row("United States", 2000, None, None, None, None, None, None)
        row2 = Row("Mexico", 2002, None, None, None, None, None, None)
        lst = Node(row1, Node(row2, None))
        self.assertEqual(listlen(lst), 2)

    def test_filter_rows_returns_node_or_none(self):
        row = Row("United States", 2002, 200.0, 3.0, 100.0, 4.5, 100.0, 2.5)
        lst = Node(row, None)
        result = filter_rows(lst, "country", "equal", "United States")
        self.assertTrue(result is None or isinstance(result, Node))


if __name__ == "__main__":
    unittest.main()

