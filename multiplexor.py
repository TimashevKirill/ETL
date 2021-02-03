import csv
import json
from xml.dom import minidom
import os.path
from operator import itemgetter
from itertools import zip_longest
import random



class FileDataManager:

    @classmethod
    def make_data_worker(Class):
        return Class.DataWorker()

    @classmethod
    def make_reader(Class):
        return Class.Reader()

    class Reader:
        def read_file(self, file):
            """Read function of the file
            :param file: File path
            :return Data from file
            """

    class DataWorker:
        def convert_data_to_gener(self, file_data):
            """Function for converting file data to an array of dictionaries
            :param file_data: Data from loaded file
            :return Dicts array
            """


class CSVDataManager(FileDataManager):
    """class reads and convert data from CSV format file"""

    class Reader:
        def read_file(self, file):
            """
            Read function of the file
            :param file: File path
            :return Data from file
            """

            if os.path.exists(file):
                f_data = open(file)
                return f_data
            else:
                return None

    class DataWorker:
        def convert_data_to_gener(self, file_data):
            """
            Function for converting file data to an array of dictionaries
            :param file_data: Data from loaded file
            :return Dicts array
            """
            generator_of_dicts = (i for i in [])
            # dicts_array = []
            try:
                dicts_array = list(csv.DictReader(file_data, delimiter=','))
                # Create new generator of dictionaries to close a CSV file
                generator_of_dicts = (i for i in dicts_array)
                file_data.close()
            except Exception as e:
                print(e)
            finally:
                return generator_of_dicts


class JsonDataManager(FileDataManager):
    """class reads and convert data from JSON format file"""

    class Reader:
        def read_file(self, file):
            """
            Read function of the file
            :param file: File path
            :return Data from file
            """

            if os.path.exists(file):
                with open(file, encoding="utf-8") as f_data:
                    return f_data.read()
            else:
                return None

    class DataWorker:
        def convert_data_to_gener(self, file_data):
            """
            Function for converting file data to an array of dictionaries
            :param file_data: Data from loaded file
            :return Dicts array
            """
            generator_of_dicts = (i for i in [])
            try:
                data = json.loads(file_data)
                dicts_array = data["fields"]
                generator_of_dicts = (i for i in dicts_array)
                del data
                del dicts_array
            except Exception as e:
                print(e)
            finally:
                return generator_of_dicts


class XMLDataManager(FileDataManager):
    """class reads and convert data from JSON format file"""

    class Reader:
        def read_file(self, file):
            """
            Read function of the file
            :param file: File path
            :return Data from file
            """

            if os.path.exists(file):
                f_data = minidom.parse(file)
                return f_data
            else:
                return None

    class DataWorker:
        def convert_data_to_gener(self, file_data):
            """
            Function for converting file data to an array of dictionaries
            :param file_data: Data from loaded file
            :return Dicts array
            """
            generator_of_dicts = (i for i in [])
            try:
                items = file_data.getElementsByTagName('object')
                dicts_array = {
                    elem.attributes['name'].value: elem.childNodes[1].firstChild.nodeValue for elem in items}
                generator_of_dicts = (i for i in [dicts_array])
                del dicts_array
            except Exception as e:
                print(e)
            finally:
                return generator_of_dicts


class Combine:
    """
    The class combines data from different unordered arrays into one,
    ordered array with the ability to save it in .tsv format.
    Also the ability to view errors that have occurred
    """

    def __init__(self, errormanager):
        self.array_data = {}
        self.max_len_headers_data = {}
        self.headers_d = []
        self.headers_m = []
        self.combine_data_array = []
        self.headers = []
        self.ErrorManager = errormanager

    def max_len_headers_load(self, data):
        """
        Search and select row with the largest number of data
        """
        for i in data:
            if len(i) > len(self.max_len_headers_data):
                self.max_len_headers_data = i

    def load_data(self, name_chunk, data):
        """
        :param name_chunk: Name directory for to specify the path when generating errors
        :param data: Convert data
        Loads data into a single shared array
        and calculates the longest sequence of headers
         """
        self.array_data[name_chunk] = data

    def create_headers(self):
        """
        Generates a sorted sequence of headers
        """
        d_count = 0
        m_count = 0
        for i in self.max_len_headers_data:
            if "D" in i:
                d_count += 1
            elif "M" in i:
                m_count += 1

        for i in range(d_count):
            self.headers_d.append("D" + str(i + 1))
        for i in range(m_count):
            self.headers_m.append("M" + str(i + 1))

        self.headers = [*self.headers_d, *self.headers_m]

    def combine_to_basic_data(self):
        """
        Combines data from different unordered arrays into one,
        ordered array
        """
        combine_data_array = []

        for data in self.array_data:
            for index_line, row in enumerate(self.array_data[data]):
                row_array = []

                for i in self.headers_d:
                    try:
                        elem = row[i]
                        if isinstance(elem, str):
                            row_array.append(elem)
                        else:
                            error = "File {} has an error(elem not str) of the {} element on the {}th line.".format(
                                data, i, index_line)
                            self.ErrorManager.append_error.append(error)
                    except KeyError:
                        pass
                        row_array.append(" ")

                for i in self.headers_m:
                    try:
                        try:
                            elem = int(row[i])
                            row_array.append(elem)
                        except ValueError:
                            row_array.append(0)
                            error = "File {} has an error(elem not int) of the {} element on the {}th line.".format(
                                data, i, index_line)
                            self.ErrorManager.append_error(error)

                    except KeyError:
                        pass
                combine_data_array.append(row_array)

        combine_data_array = sorted(
            combine_data_array, key=itemgetter(0))
        combine_data_array = [*[self.headers], *combine_data_array]
        generator_combine_data = (i for i in combine_data_array)
        return generator_combine_data

    def combine_to_advanced_data(self):
        """
        This logic combined data and adds strings to each other by a unique key,
         from all files in one comdine data array.
        :return: comdine data array
        """
        row_dict = {}
        combine_data_array = []
        for data in self.array_data:
            for index_line, row in enumerate(self.array_data[data]):
                row_d_array = []
                row_m_array = []
                for i in self.headers_d:
                    try:
                        elem = row[i]
                        if isinstance(elem, str):
                            row_d_array.append(elem)
                        else:
                            error = "File {} has an error(elem not str) of the {} element on the {}th line.".format(
                                data, i, index_line)
                            self.ErrorManager.append_error(error)
                    except KeyError:
                        row_d_array.append(' ')

                for i in self.headers_m:
                    try:
                        try:
                            elem = int(row[i])
                            row_m_array.append(elem)
                        except ValueError:
                            row_m_array.append(0)
                            error = "File {} has an error(elem not int) of the {} element on the {}th line.".format(
                                data, i, index_line)
                            self.ErrorManager.append_error(error)

                    except KeyError:
                        pass

                if str(row_d_array) in row_dict:
                    current_array = row_m_array
                    past_array = row_dict[str(row_d_array)]
                    sum_arrays = [
                        x + y for x, y in zip_longest(
                            current_array,
                            past_array,
                            fillvalue=0)]
                    row_dict[str(row_d_array)] = sum_arrays
                else:
                    row_dict[str(row_d_array)] = row_m_array

        for i in row_dict:
            combine_data_array.append([*eval(i), *row_dict[i]])
        combine_data_array = sorted(
            combine_data_array, key=itemgetter(0))
        combine_data_array = [*[self.headers], *combine_data_array]
        generator_combine_data = (i for i in combine_data_array)
        return generator_combine_data


class ErrorManager:
    """
    Class for aggregation and error output
    """

    def __init__(self):
        self.errors = []

    def append_error(self, error):

        if error not in self.errors:
            self.errors.append(error)

    def view_errors(self):
        if self.errors:
            for i in self.errors:
                print(i)
        else:
            print("there are no errors")

    def get_errors(self):
        return self.errors


class FileSaver:
    """
    Class for saving data to file
    """

    def save_data(self, file_name, data):
        """
        saving data to file
        """


class TSVSaver(FileSaver):
    """
    Class for saving TSV data to file
    """

    def save_data(self, file_name, data):
        if os.path.exists(file_name):
            file_name = file_name
        else:
            file_name = "../" + file_name
        data = list(data)
        with open(file_name, 'wt') as out_file:
            tsv_writer = csv.writer(out_file, delimiter='\t')
            for i in data:
                tsv_writer.writerow(i)


def save_data(saver, file, data):
    """
    This logic calls the save function of the passed class
    :param saver: Saver class
    :param file: Path to the file
    :data file: data for saving
    """
    saver().save_data(file, data)


def get_convert_data(manager, file):
    """
    This logic returns a an unordered array data
    :param manager: The appropriate class for reading the file
    :param file: Path to the file
    :return:Сonvert data
    """
    dataworker = manager.make_data_worker()
    reader = manager.make_reader()

    if os.path.exists(file):
        data = reader.read_file(file)
    else:
        file = "../" + file
        data = reader.read_file(file)

    if data is not None:
        convert_data = dataworker.convert_data_to_gener(data)
    else:
        convert_data = []
    return convert_data


def create_test_file(d_count, m_count, row_count):
    """
    This logic created a file with any amount of data to test the speed of the algorithm
    :param d_count: Number of D elements
    :param m_count: Number of M elements
    :param row_count: Number of rows
    """
    d = []
    m = []
    big_data = []
    bukv = ['a', 'b', 'c', 'd']

    d_count = d_count
    m_count = m_count
    for i in range(d_count):
        d.append("D" + str(i + 1))

    for i in range(row_count):
        m_data = []
        d_data = []
        for g in range(d_count):
            d_data.append(random.choice(bukv))

        for g in range(m_count):
            m_data.append(g + 1)

        big_data.append([*d_data, *m_data])

    for i in range(m_count):
        m.append("M" + str(i + 1))

    headers = [*d, *m]
    big_data = [*[headers], *big_data]
    with open('Input_data/test.csv', 'wt') as out_file:
        tsv_writer = csv.writer(out_file)
        for i in big_data:
            tsv_writer.writerow(i)
