import unittest
from ETL import multiplexor as m


class TestMultiplexor(unittest.TestCase):

    def test_empty_file(self):
        self.assertEqual(m.get_convert_data(m.CSVDataManager, "asd.xml"), [])
        self.assertEqual(m.get_convert_data(m.JsonDataManager, "asd.xml"), [])
        self.assertEqual(m.get_convert_data(m.XMLDataManager, "asd.xml"), [])


if __name__ == "__main__":
    unittest.main()
