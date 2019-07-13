import requests
import sys


class TableReaderMixin:
    # Abstract class that provides methods for the
    # reading of tables on pages of Matricula Web
    # website.

    @staticmethod
    def readSimpleTableFromHTML(raw_html):
        # This method is capable of reading tables on
        # pages that use the common layout on Matricula
        # Web. It receives the raw_html element (returned from
        # BeautifulSoup) and process it.
        # It returns a list in which each element is a dictionarie
        # that has the following structure:
        # {
        #   'table_head_name': 'table_row_attribute',
        #   ...
        # }

        # Table head comment guide in table
        table_head_list = []
        extracted_data = []

        # Select all the th in html parser
        for table_head in raw_html.select('th'):
            table_head_list.append(str(table_head.text))

        # Select all the rows in html
        for table_row in raw_html.select('tr'):
            attributes = {}

            # In all rows we take the data
            for table_data in table_row.select('td'):

                if str(table_data.text) == '':
                    break

                # Creating the dictionary with the
                # first element in table head list
                # and data table text
                attributes[table_head_list[0]] = str(
                    table_data.text
                )

                # Take off the first element in list and adding
                # in final from the same list (queue)
                table_head_list.append(table_head_list.pop(0))

            # Verify if the current course attribute is empty,
            # if not append in list of course
            if attributes != {}:
                extracted_data.append(attributes)

        return extracted_data

    @staticmethod
    def readDatatableTableFromHTML(raw_html):
        # This method is capable of reading tables on
        # pages that use the datatable layout on Matricula
        # Web. It recieves the raw_html element (returned from
        # BeautifulSoup) and process it.
        # It returns a list in which each element is a dictionary
        # that has the following structure:
        # {
        #   'table_head_name': 'table_row_attribute',
        #   ...
        # }

        # Table head comment guide in table
        table_head_list = []
        extracted_data = []

        datatable_div = raw_html.select('#datatable')

        if len(datatable_div) == 0:
            return None

        # Select all the rows in html
        for table_row in datatable_div[0].select('tr'):

            if len(table_head_list) == 0:
                for th in table_row.select('th'):
                    table_head_list.append(str(th.text))
                continue

            attributes = {}

            # In all rows we take the data
            for table_data in table_row.select('td'):

                if str(table_data.text) == '':
                    break

                # Creating the dictionary with the
                # first element in table head list
                # and data table text
                attributes[table_head_list[0]] = str(
                    table_data.text
                )

                # Take off the first element in list and adding
                # in final from the same list (queue)
                table_head_list.append(table_head_list.pop(0))

            # Verify if the current course attribute is empty,
            # if not append in list of course
            if attributes != {}:
                extracted_data.append(attributes)

        return extracted_data


class UrlLoaderMixin:
    # This abstract class is a mixin for the act of loading a url,
    # its porpouse is to define a custom behaviour on the get method
    # without duplicating code

    def getFromUrl(self, url, fails=0):

        response = None

        try:
            response = requests.get(url=url)

        except requests.exceptions.Timeout:
            print("Request timeout for {}".format(url))

        except requests.exceptions.TooManyRedirects:
            print("Too many redirects on request for {}".format(url))

        except requests.exceptions.RequestException as e:
            print("Error making request for {} -- ERROR: ".format(url) + e)

        finally:
            if response is None:

                if fails >= 3:
                    print(
                        "Failed to get response for {} after retries, exiting...".format(url))
                    sys.exit(1)

                print("Failed to get response for {}, trying again... ({})".format(
                    url, fails+1))
                return self.getFromUrl(url, fails+1)

        return response
