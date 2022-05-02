import csv
import copy
from itertools import islice


def request_country_data():
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

    return global_data


def request_publishers_data():
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
            # Check if name is not empty, else set GBIF id
            if row[0] == '':
                publisher = str(row[1])
            else:
                publisher = row[0]
            row.remove(row[0])

            gbif_data[publisher] = {}

            # Calculating totals of GBIF publishers
            gbif_data[publisher]['Total'] = 0

            for value in islice(row, 3, 7):
                gbif_data[publisher]['Total'] += int(value)
                gbif_data['Total'] += int(value)

            # Adding values
            i = 1
            for value in row:
                gbif_data[publisher][gbif_mapping[i]] = value

                i += 1

    # Run through GBIF publishers and check if GeoCASe contains fossil data,
    # if so disable fossil data from GBIF and merge data
    global_data = copy.deepcopy(gbif_data)
    gbif_data.pop('Total')

    for publisher in gbif_data:
        # Check if publisher has data in GeoCASe
        if publisher in publisher_mapping:
            # Add GeoCASe numbers to GBIF total
            global_data['Total'] += int(geocase_data[publisher_mapping[publisher]]['Total'])

            # Check if publisher has fossil specimens in GeoCASe
            if int(geocase_data[publisher_mapping[publisher]]['Fossil']) > 0:
                # Check if publisher also has fossil specimens in GBIF
                if int(gbif_data[publisher]['FOSSIL_SPECIMEN']) > 0:
                    # Set fossil to data from GeoCASe
                    global_data[publisher]['FOSSIL_SPECIMEN'] =\
                        geocase_data[publisher_mapping[publisher]]['Fossil']

                    # Remove GBIF fossil records from grand total
                    global_data[publisher]['Total'] -= int(gbif_data[publisher]['FOSSIL_SPECIMEN'])
                    global_data['Total'] -= int(gbif_data[publisher]['FOSSIL_SPECIMEN'])

            # Update with other record basis
            global_data[publisher]['METEORITE'] = geocase_data[publisher_mapping[publisher]]['Meteorite']
            global_data[publisher]['MINERAL'] = geocase_data[publisher_mapping[publisher]]['Mineral']
            global_data[publisher]['ROCK'] = geocase_data[publisher_mapping[publisher]]['Rock']
            global_data[publisher]['OTHER_GEOLOGICAL'] = geocase_data[publisher_mapping[publisher]]['Other_geological']

            # Add record basis to totals
            for value in islice(geocase_data[publisher_mapping[publisher]].values(), 1, 6):
                global_data[publisher]['Total'] += int(value)
                global_data['Total'] += int(value)
        else:
            # Update countries out of GeoCASe
            global_data[publisher]['METEORITE'] = 0
            global_data[publisher]['MINERAL'] = 0
            global_data[publisher]['ROCK'] = 0
            global_data[publisher]['OTHER_GEOLOGICAL'] = 0

    return global_data


def request_publishing_country():
    print('test')


request_publishers_data()
request_country_data()
