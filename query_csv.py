import csv
import copy
from itertools import islice
from datetime import datetime as dt


current_month = dt.now().strftime('%B')


# General functions for returning requested data

def read_country_data(month: str = current_month) -> dict:
    """ Reads the GBIF and GeoCASe csv files for countries and prepares the data for usage
        Combines the GBIF and GeoCASe data and filters on fossil
        :rule GeoCASe fossil numbers replace GBIF numbers if country has fossils in GeoCASe
        :return global_data:
    """

    # Temporary country mapping (to be replaced when GeoCASe supports country codes)
    # First term is GBIF, second is country code from GeoCASe
    country_mapping = {
        'DE': 'Germany',
        'GB': 'UK',
        'EE': 'Estonia',
        'AT': 'Austria',
        'FI': 'Finland',
        'NL': 'The Netherlands'
    }

    # Reading country data from GeoCASe csv
    geocase_csv = f'csv_files/storage/{month}/geocase_specimens.csv'
    geocase_data = read_geocase_specimens(geocase_csv)

    # Reading country data from GBIF csv
    gbif_csv = f'csv_files/storage/{month}/gbif_specimens.csv'
    gbif_data = read_gbif_specimens(gbif_csv)

    # Reading and adding issues and flags from GBIF
    issues_and_flags_csv = f'csv_files/storage/{month}/gbif_issues_and_flags.csv'
    gbif_data = read_gbif_issues_flags(issues_and_flags_csv, gbif_data)

    # Run through GBIF countries and check if GeoCASe contains fossil data,
    # if so disable fossil data from GBIF and merge data
    global_data = copy.deepcopy(gbif_data)
    gbif_data.pop('Total')

    for country in gbif_data:
        # Check if country has data in GeoCASe
        if country in country_mapping:
            # Add GeoCASe numbers to GBIF total
            global_data['Total'] += int(geocase_data[country_mapping[country]]['Total'])
            global_data[country]['Total'] = int(global_data[country]['Total'])

            # Check if country has fossil specimens in GeoCASe
            if int(geocase_data[country_mapping[country]]['Fossil']) > 0:
                # Check if country also has fossil specimens in GBIF
                if int(gbif_data[country]['FOSSIL_SPECIMEN']) > 0:
                    # Set fossil to data from GeoCASe
                    global_data[country]['FOSSIL_SPECIMEN'] =\
                        geocase_data[country_mapping[country]]['Fossil']

                    # Remove GBIF fossil records from grand total
                    global_data[country]['Total'] -= int(gbif_data[country]['FOSSIL_SPECIMEN'])
                    global_data['Total'] -= int(gbif_data[country]['FOSSIL_SPECIMEN'])

            # Update with other record basis
            global_data[country]['METEORITE'] = geocase_data[country_mapping[country]]['Meteorite']
            global_data[country]['MINERAL'] = geocase_data[country_mapping[country]]['Mineral']
            global_data[country]['ROCK'] = geocase_data[country_mapping[country]]['Rock']
            global_data[country]['OTHER_GEOLOGICAL'] = geocase_data[country_mapping[country]]['Other_geological']

            # Add record basis to totals
            for value in islice(geocase_data[country_mapping[country]].values(), 1, 6):
                global_data[country]['Total'] += int(value)
                global_data['Total'] += int(value)
        else:
            # Update countries out of GeoCASe
            global_data[country]['METEORITE'] = 0
            global_data[country]['MINERAL'] = 0
            global_data[country]['ROCK'] = 0
            global_data[country]['OTHER_GEOLOGICAL'] = 0

    # Add datasets total to country data
    datasets_csv = f'csv_files/storage/{month}/gbif_datasets.csv'
    global_data = read_gbif_datasets(datasets_csv, global_data)

    return global_data


def read_publishers_data(month: str = current_month) -> dict:
    """ Reads the GBIF and GeoCASe csv files for publishers and prepares the data for usage
        Combines the GBIF and GeoCASe data and filters on fossil
        :rule GeoCASe fossil numbers replace GBIF numbers if country has fossils in GeoCASe
        :return global_data:
    """

    # Temporary publisher mapping (to be replaced when GeoCASe supports relevant publisher id like ROR)
    # First term is GBIF, second is name from ROR
    publisher_mapping = {
        'Museum für Naturkunde': 'Museum für Naturkunde',
        'Natural History Museum': 'Natural History Museum, England',
        'Tallinn University of Technology': 'SARV',
        'Naturhistorisches Museum': 'Museum of Natural History Vienna',
        'Finnish Museum of Natural History': 'FMNH',
        'Naturalis Biodiversity Center': 'Naturalis'
    }

    # Reading publisher data from GeoCASe csv and add to geocase_data
    geocase_csv = f'csv_files/storage/{month}/geocase_publishers.csv'
    geocase_data = read_geocase_publishers(geocase_csv)

    # Reading publisher data from GBIF csv
    gbif_csv = f'csv_files/storage/{month}/gbif_publishers.csv'
    gbif_data = read_gbif_publishers(gbif_csv)

    # Run through GBIF publishers and check if GeoCASe contains fossil data,
    # if so disable fossil data from GBIF and merge data
    global_data = copy.deepcopy(gbif_data)
    gbif_data.pop('Total')

    for publisher in gbif_data:
        publisher_name = gbif_data[publisher]['Publisher']

        # Check if publisher has data in GeoCASe
        if publisher_name in publisher_mapping:
            # Add GeoCASe numbers to GBIF total
            global_data['Total'] += int(geocase_data[publisher_mapping[publisher_name]]['Total'])

            # Check if publisher has fossil specimens in GeoCASe
            if int(geocase_data[publisher_mapping[publisher_name]]['Fossil']) > 0:
                # Check if publisher also has fossil specimens in GBIF
                if int(gbif_data[publisher]['FOSSIL_SPECIMEN']) > 0:
                    # Set fossil to data from GeoCASe
                    global_data[publisher]['FOSSIL_SPECIMEN'] =\
                        geocase_data[publisher_mapping[publisher_name]]['Fossil']

                    # Remove GBIF fossil records from grand total
                    global_data[publisher]['Total'] -= int(gbif_data[publisher]['FOSSIL_SPECIMEN'])
                    global_data['Total'] -= int(gbif_data[publisher]['FOSSIL_SPECIMEN'])

            # Update with other record basis
            global_data[publisher]['METEORITE'] = geocase_data[publisher_mapping[publisher_name]]['Meteorite']
            global_data[publisher]['MINERAL'] = geocase_data[publisher_mapping[publisher_name]]['Mineral']
            global_data[publisher]['ROCK'] = geocase_data[publisher_mapping[publisher_name]]['Rock']
            global_data[publisher]['OTHER_GEOLOGICAL'] = geocase_data[publisher_mapping[publisher_name]]['Other_geological']

            # Add record basis to totals
            for value in islice(geocase_data[publisher_mapping[publisher_name]].values(), 1, 6):
                global_data[publisher]['Total'] += int(value)
                global_data['Total'] += int(value)
        else:
            # Update countries out of GeoCASe
            global_data[publisher]['METEORITE'] = 0
            global_data[publisher]['MINERAL'] = 0
            global_data[publisher]['ROCK'] = 0
            global_data[publisher]['OTHER_GEOLOGICAL'] = 0

    # Read and add publisher issues and flags
    issues_and_flags_csv = f'csv_files/storage/{month}/gbif_publishers_issues_flags.csv'
    global_data = read_gbif_publishers_issues_flags(issues_and_flags_csv, global_data)

    return global_data


def create_issues_and_flags_list() -> list:
    """ Takes the csv containing the names of all issues and converts it to a list
        :return: Returns the issues and flags list
    """

    issues_file = 'csv_files/sources/GBIF_issues.csv'
    issues_and_flags_list = []

    with open(issues_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            issue_flag = row[1].lower().replace('_', ' ').capitalize()

            issues_and_flags_list.append(issue_flag)

    return issues_and_flags_list


# Modules for reading stored csv files

def read_geocase_specimens(geocase_csv: str, geocase_data: dict = None) -> dict:
    """ Reads the geocase specimens csv and formats the data
        :params: geocase_csv: name of the csv file, geocase_data: base dictionary
        :return: Returns a dictionary of the formatted data
    """

    with open(geocase_csv, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        # Saving headers of csv
        geocase_mapping = next(reader)
        next(reader)

        # Check if geocase_data is None
        if geocase_data is None:
            geocase_data = {
                'Total': 0
            }

        for row in reader:
            country = row[0]
            row.remove(row[0])
            geocase_data[country] = {}

            i = 1
            for value in row:
                geocase_data[country][geocase_mapping[i]] = value

                i += 1

            # Adding to grand total
            geocase_data['Total'] += int(geocase_data[country]['Total'])

    return geocase_data


def read_gbif_specimens(gbif_csv: str, gbif_data: dict = None) -> dict:
    """ Reads the gbif specimens csv and formats the data
        :params: gbif_csv: name of the csv file, gbif_data: base dictionary
        :return: Returns a dictionary of the formatted data
    """

    with open(gbif_csv, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        # Saving headers of csv
        gbif_mapping = next(reader)
        next(reader)

        # Check if gbif_data is None
        if gbif_data is None:
            gbif_data = {
                'Total': 0
            }

        for row in reader:
            country = row[0]
            row.remove(row[0])
            gbif_data[country] = {}

            i = 1
            for value in row:
                gbif_data[country][gbif_mapping[i]] = value

                i += 1

            # Adding to grand total
            gbif_data['Total'] += int(gbif_data[country]['Total'])

    return gbif_data


def read_gbif_issues_flags(issues_and_flags_csv: str, data: dict) -> dict:
    """ Reads the gbif issues and flags csv and formats the data
        :params: issues_and_flags_csv: name of the csv file, data: base dictionary (required)
        :return: Returns a dictionary of the formatted data
    """

    with open(issues_and_flags_csv, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        issues_and_flags_mapping = next(reader)
        next(reader)

        for row in reader:
            # Get country code
            country = row[0]
            row.remove(row[0])

            row_issues_and_flags: dict = {}

            i = 1
            for value in row:
                row_issues_and_flags[issues_and_flags_mapping[i]] = value

                i += 1

            data[country]['issues_and_flags'] = row_issues_and_flags

    return data


def read_gbif_datasets(datasets_csv: str, data: dict) -> dict:
    """ Reads the gbif datasets csv and formats the data
        :params: datasets_csv: name of the csv file, data: base dictionary (required)
        :return: Returns a dictionary of the formatted data
    """

    with open(datasets_csv, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        datasets_mapping = next(reader)

        for row in reader:
            row.remove(row[0])
            i = 1

            for value in row:
                # Set dataset total of country
                data[datasets_mapping[i]]['Total datasets'] = value

                i += 1

    return data


def read_geocase_publishers(geocase_csv: str, geocase_data: dict = None) -> dict:
    """ Reads the geocase publishers csv and formats the data
        :params: geocase_csv: name of the csv file, geocase_data: base dictionary
        :return: Returns a dictionary of the formatted data
    """

    with open(geocase_csv, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        # Saving headers of csv
        geocase_mapping = next(reader)
        next(reader)

        # Checking if geocase_data is None
        if geocase_data is None:
            geocase_data = {
                'Total': 0
            }

        for row in reader:
            publisher = row[0]
            row.remove(row[0])
            geocase_data[publisher] = {}

            i = 1
            for value in row:
                geocase_data[publisher][geocase_mapping[i]] = value

                i += 1

            # Adding to grand total
            geocase_data['Total'] += int(geocase_data[publisher]['Total'])

    return geocase_data


def read_gbif_publishers(gbif_csv: str, gbif_data: dict = None) -> dict:
    """ Reads the gbif publishers csv and formats the data
        :params: gbif_csv: name of the csv file, gbif_data: base dictionary
        :return: Returns a dictionary of the formatted data
    """

    with open(gbif_csv, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        # Saving headers of csv
        gbif_mapping = next(reader)

        # Check if gbif_data is None
        if gbif_data is None:
            gbif_data = {
                'Total': 0
            }

        for row in reader:
            # Set ROR id, if not present set name
            if row[2] != '':
                publisher = str(row[2])
            else:
                publisher = row[0]

            gbif_data[publisher] = {}

            # Calculating totals of GBIF publishers
            gbif_data[publisher]['Total'] = 0

            for value in islice(row, 3, 7):
                gbif_data[publisher]['Total'] += int(value)
                gbif_data['Total'] += int(value)

            # Adding values
            i = 0
            for value in row:
                gbif_data[publisher][gbif_mapping[i]] = value

                i += 1

    return gbif_data


def read_gbif_publishers_issues_flags(issues_and_flags_csv: str, data: dict) -> dict:
    """ Reads the gbif publishers issues and flags csv and formats the data
        :params: issues_and_flags_csv: name of the csv file, data: base dictionary (required)
        :return: Returns a dictionary of the formatted data
    """

    with open(issues_and_flags_csv, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        issues_and_flags_mapping = next(reader)

        for row in reader:
            # Get publisher, as in ROR id
            publisher = row[0]
            # Remove ROR from values
            row.remove(row[0])
            # Remove name from values
            row.remove(row[0])

            row_issues_and_flags: dict = {}

            i = 2
            for value in row:
                row_issues_and_flags[issues_and_flags_mapping[i]] = value

                i += 1

            data[publisher]['issues_and_flags'] = row_issues_and_flags

    return data


# Functions for requesting data from interface

def request_publishing_country(country_codes: list, month=current_month) -> dict:
    """ Requests publishing countries data stored in csv files based upon the request
        :return: Returns the data of requested publishing countries
    """

    # Receive publishing countries data
    publishing_countries = read_country_data(month)

    # Create response
    response: dict = {}

    for country in country_codes:
        response[country] = publishing_countries[country]

    return response


def request_publishers(ror_ids: list, month=current_month) -> dict:
    """ Requests publishers data stored in csv files based upon the request
        :return: Returns the data of requested publishers
    """

    # Receive publishers ROR id data
    publishers = read_publishers_data(month)

    # Create response
    response: dict = {}

    for publisher in ror_ids:
        response[publisher] = publishers[publisher]

    return response
