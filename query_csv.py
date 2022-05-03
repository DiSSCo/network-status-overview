import csv
import copy
from itertools import islice


def read_country_data():
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
    geocase_csv = 'csv_files/written/geocase_data.csv'

    with open(geocase_csv, 'r', newline='', encoding='utf-8') as file:
        geocase_data = {
            'Total': 0
        }
        reader = csv.reader(file)

        # Saving headers of csv
        geocase_mapping = next(reader)
        next(reader)

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

    # Reading country data from GBIF csv
    gbif_csv = 'csv_files/written/specimens.csv'

    with open(gbif_csv, 'r', newline='', encoding='utf-8') as file:
        gbif_data = {
            'Total': 0
        }
        reader = csv.reader(file)

        # Saving headers of csv
        gbif_mapping = next(reader)
        next(reader)

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

    # Reading and adding issues and flags
    issues_and_flags_csv = 'csv_files/written/issues_and_flags.csv'

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

            gbif_data[country]['issues_and_flags'] = row_issues_and_flags

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
    datasets_csv = 'csv_files/written/datasets.csv'

    with open(datasets_csv, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        datasets_mapping = next(reader)

        for row in reader:
            row.remove(row[0])
            i = 1

            for value in row:
                # Set dataset total of country
                global_data[datasets_mapping[i]]['Total datasets'] = value

                i += 1

    return global_data


def read_publishers_data():
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

    # Reading publisher data from GeoCASe csv
    geocase_csv = 'csv_files/written/geocase_publishers.csv'

    with open(geocase_csv, 'r', newline='', encoding='utf-8') as file:
        geocase_data = {
            'Total': 0
        }
        reader = csv.reader(file)

        # Saving headers of csv
        geocase_mapping = next(reader)
        next(reader)

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

    # Reading publisher data from GBIF csv
    gbif_csv = 'csv_files/written/publishers.csv'

    with open(gbif_csv, 'r', newline='', encoding='utf-8') as file:
        gbif_data = {
            'Total': 0
        }
        reader = csv.reader(file)

        # Saving headers of csv
        gbif_mapping = next(reader)

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
    issues_and_flags_csv = 'csv_files/written/publishers_issues_flags.csv'

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

            global_data[publisher]['issues_and_flags'] = row_issues_and_flags

    return global_data


def request_publishing_country(country_codes: list):
    # Receive publishing countries data
    publishing_countries = read_country_data()

    # Create response
    response: dict = {}

    for country in country_codes:
        response[country] = publishing_countries[country]

    return response


def request_publishers(ror_ids: list):
    # Receive publishers ROR id data
    publishers = read_publishers_data()

    # Create response
    response: dict = {}

    for publisher in ror_ids:
        response[publisher] = publishers[publisher]

    return response


# countries = ['NL', 'DE', 'EE']
# print(request_publishing_country(countries))

# ror_ids = ['05natt857', '0566bfb96', '05th1v540']
# print(request_publishers(ror_ids))
