from ETL.multiplexor import get_convert_data
from ETL.multiplexor import save_data
from ETL.multiplexor import Combine
from ETL.multiplexor import CSVDataManager, JsonDataManager, XMLDataManager
from ETL.multiplexor import TSVSaver
from ETL.multiplexor import ErrorManager
import time


def timmer(func):
    def wrapper():
        start_search = time.time()
        func()
        print(time.time() - start_search)
    return wrapper


@timmer
def main():
    """
    Logic start function

    """
    error_viewer = ErrorManager()
    combine = Combine(error_viewer)

    csv_data_1 = get_convert_data(CSVDataManager, "Input_data/csv_data_1.csv")
    csv_data_1_for_headers = get_convert_data(
        CSVDataManager, "Input_data/csv_data_1.csv")
    combine.max_len_headers_load(csv_data_1_for_headers)
    combine.load_data("csv_data_1.csv", csv_data_1)

    csv_data_3 = get_convert_data(CSVDataManager, "Input_data/test.csv")
    csv_data_3_for_headers = get_convert_data(
        CSVDataManager, "Input_data/test.csv")
    combine.max_len_headers_load(csv_data_3_for_headers)
    combine.load_data("csv_data_3.csv", csv_data_3)

    csv_data_2 = get_convert_data(CSVDataManager, "Input_data/csv_data_2.csv")
    csv_data_2_for_headers = get_convert_data(
        CSVDataManager, "Input_data/csv_data_2.csv")
    combine.max_len_headers_load(csv_data_2_for_headers)
    combine.load_data("csv_data_2.csv", csv_data_2)

    json_data = get_convert_data(JsonDataManager, "Input_data/json_data.json")
    json_data_for_headers = get_convert_data(
        JsonDataManager, "Input_data/json_data.json")
    combine.max_len_headers_load(json_data_for_headers)
    combine.load_data("json_data.json", json_data)

    xml_data = get_convert_data(XMLDataManager, "Input_data/xml_data.xml")
    xml_data_for_headers = get_convert_data(
        XMLDataManager, "Input_data/xml_data.xml")
    combine.max_len_headers_load(xml_data_for_headers)
    combine.load_data("xml_data.xml", xml_data)

    combine.create_headers()

    combine_basic_data = combine.combine_to_basic_data()

    save_data(TSVSaver, 'Output_data/basic_results.tsv', combine_basic_data)

    adv = input("Create advanced data file? y/n")
    if adv == "y":
        csv_data_1 = get_convert_data(
            CSVDataManager, "Input_data/csv_data_1.csv")
        combine.load_data("csv_data_1.csv", csv_data_1)

        csv_data_2 = get_convert_data(
            CSVDataManager, "Input_data/csv_data_2.csv")
        combine.load_data("csv_data_2.csv", csv_data_2)

        json_data = get_convert_data(
            JsonDataManager, "Input_data/json_data.json")
        combine.load_data("json_data.json", json_data)

        xml_data = get_convert_data(XMLDataManager, "Input_data/xml_data.xml")
        combine.load_data("xml_data.xml", xml_data)

        combine_advanced_data = combine.combine_to_advanced_data()

        save_data(
            TSVSaver,
            'Output_data/advanced_results.tsv',
            combine_advanced_data)

    er = input("View errors? y/n")
    if er == "y":
        error_viewer.view_errors()


if __name__ == "__main__":
    main()
