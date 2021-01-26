from Multiplexor import get_convert_data
from Multiplexor import create_test_file
from Multiplexor import Combine, CSVReader, JsonReader, XMLReader
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

    combine = Combine()
    csv_data_1 = get_convert_data(CSVReader, "Input_data/csv_data_1.csv")
    print("csv_data_1", csv_data_1)
    combine.load_data("csv_data_1.csv", csv_data_1)

    # csv_data_3 = get_convert_data(CSVReader, "Input_data/test.csv")
    # combine.load_data("csv_data_3.csv", csv_data_3)
    # print("csv_data_3", csv_data_3)

    csv_data_2 = get_convert_data(CSVReader, "Input_data/csv_data_2.csv")
    print("csv_data_2", csv_data_2)
    combine.load_data("csv_data_2.csv", csv_data_2)

    json_data = get_convert_data(JsonReader, "Input_data/json_data.json")
    combine.load_data("json_data.json", json_data)

    xml_data = get_convert_data(XMLReader, "Input_data/xml_data.xml")
    combine.load_data("xml_data.xml", xml_data)

    combine.create_headers()

    combine_basic_data = combine.combine_to_basic_data()
    combine.save('Output_data/basic_results.tsv', combine_basic_data)

    adv = input("Create advanced data file? y/n")
    if adv == "y":
        combine_advanced_data = combine.combine_to_advanced_data()
        combine.save('Output_data/advanced_results.tsv', combine_advanced_data)

    er = input("View errors? y/n")
    if er == "y":
        combine.view_errors()


if __name__ == "__main__":
    create_test_file(1000, 10000, 500)
    main()
