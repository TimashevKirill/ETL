import unittest
from ETL import multiplexor as m


class TestMultiplexor(unittest.TestCase):

    def test_empty_file(self):
        self.assertEqual(m.get_convert_data(m.CSVDataManager, "asd.xml"), [])
        self.assertEqual(m.get_convert_data(m.JsonDataManager, "asd.xml"), [])
        self.assertEqual(m.get_convert_data(m.XMLDataManager, "asd.xml"), [])

    def test_error_list(self):
        error_viewer = m.ErrorManager()
        combine = m.Combine(error_viewer)

        csv_data_1 = m.get_convert_data(m.CSVDataManager, "Input_data/csv_data_1.csv")
        csv_data_1_for_headers = m.get_convert_data(
            m.CSVDataManager, "Input_data/csv_data_1.csv")

        combine.max_len_headers_load(csv_data_1_for_headers)
        combine.load_data("csv_data_1.csv", csv_data_1)
        combine.create_headers()

        combine_basic_data = combine.combine_to_basic_data()
        self.assertEqual(error_viewer.get_errors(),
                         ["File csv_data_1.csv has an error(elem not int) of the M2 element on the 2th line."])

if __name__ == "__main__":
    unittest.main()
