import psycopg2
from configparser import ConfigParser
import json
from itertools import islice
from datetime import datetime as dt


current_num_month = dt.now().month


def config(filename='database.ini', section='postgresql'):
    """ Sets up the basic database connection rules fur further usage
        :return: db: instance of the database's properties
    """

    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]

    return db


def insert_countries_data(gbif_datasets, gbif_specimens, gbif_issues_flags, geocase_data):
    """ Transforms the received countries' data to a standardised format
        Saves the formatted data in the database by insert or update
    """

    # Temporary mapping between GBIF and GeoCASe
    country_mapping = {
        'DE': 'Germany',
        'GB': 'UK',
        'EE': 'Estonia',
        'AT': 'Austria',
        'FI': 'Finland',
        'NL': 'The Netherlands'
    }

    # For each organisation, prepare and save data to database
    for country in gbif_datasets['countries']:
        # Check if GeoCASe data from country is present
        geocase_dummy: dict

        if country in country_mapping:
            geocase_dummy = geocase_data['countries'][country_mapping[country]]
        else:
            geocase_dummy = {}

        # Initiate basic entity for database
        country_entity = {
            'country_code': country,
            'country_name': 'test',
            'datasets_count': json.dumps({
                'gbif': gbif_datasets['countries'][country]
            }),
            'specimens_count': json.dumps({
                'gbif': gbif_specimens['countries'][country],
                'geocase': geocase_dummy
            }),
            'issues_flags': json.dumps(gbif_issues_flags['countries'][country])
        }

        # Create database connection
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # Check if entity already exists (for same month)
        query = f"SELECT * FROM countries WHERE EXTRACT(MONTH from datetime) = {current_num_month} AND country_code = '{country}'"
        cur.execute(query)
        row = cur.fetchone()

        if row:
            # Update existing record
            column_values: str = ''

            for key in country_entity:
                column_values += f"{key} = '{country_entity[key]}', "

            query = f"UPDATE countries SET {column_values[:-2]} WHERE id = {row[0]}"
        else:
            # Insert new record
            columns: str = ''
            values: str = ''

            for key in country_entity.keys():
                if len(columns) == 0:
                    columns += key
                else:
                    columns += ', ' + key

            for value in country_entity.values():
                if len(values) == 0:
                    values += "'" + str(value) + "'"
                else:
                    values += ", '" + str(value) + "'"

            query = f"INSERT INTO countries ({columns}) VALUES ({values})"

        # Execute query
        cur.execute(query)

        # Save and close database connection
        conn.commit()
        cur.close()


def insert_organisations_data(gbif_data, geocase_data):
    """ Transforms the received organisations' data to a standardised format
        Saves the formatted data in the database by insert or update
    """

    # Temporary mapping between GBIF and GeoCASe
    organisation_mapping = {
        'Museum für Naturkunde': 'Museum für Naturkunde',
        'Natural History Museum': 'Natural History Museum, England',
        'Tallinn University of Technology': 'SARV',
        'Naturhistorisches Museum': 'Museum of Natural History Vienna',
        'Finnish Museum of Natural History': 'FMNH',
        'Naturalis Biodiversity Center': 'Naturalis'
    }

    # For each organisation, prepare and save data to database
    for organisation in gbif_data:
        # Check if GeoCASe data from organisation is present
        geocase_dummy: dict
        organisation_name = gbif_data[organisation]['name']

        if organisation_name in organisation_mapping:
            geocase_dummy = geocase_data['providers'][organisation_mapping[organisation_name]]
        else:
            geocase_dummy = {}

        # Initiate basic entity for database
        organisation_entity = {
            'ror_id': gbif_data[organisation]['ror_id'],
            'organisation_name': organisation_name,
            'datasets_count': json.dumps({
                'gbif': gbif_data[organisation]['totals']['datasets']
            }),
            'specimens_count': json.dumps({
                'gbif': gbif_data[organisation]['totals'],
                'geocase': geocase_dummy
            }),
            'issues_flags': json.dumps(gbif_data[organisation]['issues_and_flags'])
        }

        # Create database connection
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # Check if entity already exists (for same month)
        query = f"SELECT * FROM organisations WHERE EXTRACT(MONTH from datetime) = {current_num_month} AND ror_id = '{gbif_data[organisation]['ror_id']}'"
        cur.execute(query)
        row = cur.fetchone()

        if row:
            # Update existing record
            column_values: str = ''

            for key in organisation_entity:
                if organisation_entity[key].__contains__("'"):
                    organisation_entity[key] = organisation_entity[key].replace("'", "''")

                column_values += f"{key} = '{organisation_entity[key]}', "

            query = f"UPDATE organisations SET {column_values[:-2]} WHERE id = {row[0]}"
        else:
            # Inserting new record
            columns: str = ''
            values: str = ''

            for key in organisation_entity.keys():
                if len(columns) == 0:
                    columns += key
                else:
                    columns += ', ' + key

            for value in organisation_entity.values():
                if value.__contains__("'"):
                    value = value.replace("'", "''")

                if len(values) == 0:
                    values += "'" + str(value) + "'"
                else:
                    values += ", '" + str(value) + "'"

            query = f"INSERT INTO organisations ({columns}) VALUES ({values})"

        # Execute query
        cur.execute(query)

        # Save and close database connection
        conn.commit()
        cur.close()


def select_countries_data(request_list: list, month=current_num_month):
    """ Calls on data belonging to requested countries out of database
        Transforms the data to an usable format
        :return: global_data: dictionary that possesses the reformed data
    """

    # Temporary mapping between GBIF and GeoCASe
    country_mapping = {
        'DE': 'Germany',
        'GB': 'UK',
        'EE': 'Estonia',
        'AT': 'Austria',
        'FI': 'Finland',
        'NL': 'The Netherlands'
    }

    # Create database connection
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    # Check if entity already exists (for same month)
    query = f"SELECT * FROM countries WHERE EXTRACT(MONTH from datetime) = {month} AND country_code IN {tuple(request_list)}".replace(',)', ')')
    cur.execute(query)
    data = cur.fetchall()

    # Set up basic response element
    global_data: dict = {
        'Total': 0
    }

    # For each country, set data properties out of database
    for country in data:
        country_code = country[1]
        global_data[country_code] = {}

        # Add GBIF datasets
        global_data[country_code]['Total datasets'] = country[4]['gbif']

        # Add GBIF basis of record
        global_data[country_code]['FOSSIL_SPECIMEN'] = country[5]['gbif']['FOSSIL_SPECIMEN']
        global_data[country_code]['LIVING_SPECIMEN'] = country[5]['gbif']['LIVING_SPECIMEN']
        global_data[country_code]['MATERIAL_SAMPLE'] = country[5]['gbif']['MATERIAL_SAMPLE']
        global_data[country_code]['PRESERVED_SPECIMEN'] = country[5]['gbif']['PRESERVED_SPECIMEN']

        # Check if country has overlapping data between GeoCASe and GBIF
        if country_code in country_mapping:
            # Add GeoCASe numbers to GBIF total
            global_data['Total'] += (int(country[5]['geocase']['total']) + int(country[5]['gbif']['total']))
            global_data[country_code]['Total'] = (
                    int(country[5]['geocase']['total']) + int(country[5]['gbif']['total']))

            # Check if country has fossil specimens in GeoCASe
            if int(country[5]['geocase']['Fossil']) > 0:
                # Check if country also has fossil specimens in GBIF
                if int(country[5]['gbif']['FOSSIL_SPECIMEN']) > 0:
                    # Set fossil to data from GeoCASe
                    global_data[country_code]['FOSSIL_SPECIMEN'] = \
                        country[5]['geocase']['Fossil']

                    # Remove GBIF fossil records from grand total
                    global_data[country_code]['Total'] -= int(country[5]['gbif']['FOSSIL_SPECIMEN'])
                    global_data['Total'] -= int(country[5]['gbif']['FOSSIL_SPECIMEN'])

            # Update with other record basis
            global_data[country_code]['METEORITE'] = country[5]['geocase']['Meteorite']
            global_data[country_code]['MINERAL'] = country[5]['geocase']['Mineral']
            global_data[country_code]['ROCK'] = country[5]['geocase']['Rock']
            global_data[country_code]['OTHER_GEOLOGICAL'] = country[5]['geocase']['Other_geological']

            # Add record basis to totals
            for value in islice(country[5]['geocase'].values(), 1, 6):
                global_data[country_code]['Total'] += int(value)
                global_data['Total'] += int(value)
        else:
            # Update countries out of GeoCASe
            global_data[country_code]['METEORITE'] = 0
            global_data[country_code]['MINERAL'] = 0
            global_data[country_code]['ROCK'] = 0
            global_data[country_code]['OTHER_GEOLOGICAL'] = 0

        # Add GBIF issues and flags
        global_data[country_code]['issues_and_flags'] = country[6]

    return global_data


def select_organisations_data(request_list: list, month: int = current_num_month):
    """ Calls on data belonging to requested organisations out of database
        Transforms the data to an usable format
        :return: global_data: dictionary that possesses the reformed data
    """

    # Temporary mapping between GBIF and GeoCASe
    organisation_mapping = {
        'Museum für Naturkunde': 'Museum für Naturkunde',
        'Natural History Museum': 'Natural History Museum, England',
        'Tallinn University of Technology': 'SARV',
        'Naturhistorisches Museum': 'Museum of Natural History Vienna',
        'Finnish Museum of Natural History': 'FMNH',
        'Naturalis Biodiversity Center': 'Naturalis'
    }

    # Create database connection
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    # Check if entity already exists (for same month)
    query = f"SELECT * FROM organisations WHERE EXTRACT(MONTH from datetime) = {month} AND ror_id IN {tuple(request_list)}".replace(',)', ')')
    cur.execute(query)
    data = cur.fetchall()

    # Set up basic response element
    global_data: dict = {
        'Total': 0
    }

    # For each organisation, set data properties out of database
    for organisation in data:
        ror_id = organisation[1]
        organisation_name = organisation[2]
        global_data[ror_id] = {}

        # Add GBIF datasets
        global_data[ror_id]['Total datasets'] = organisation[4]['gbif']
        global_data[ror_id]['organisation_name'] = organisation_name

        # Add GBIF basis of record
        global_data[ror_id]['FOSSIL_SPECIMEN'] = organisation[5]['gbif']['FOSSIL_SPECIMEN']
        global_data[ror_id]['LIVING_SPECIMEN'] = organisation[5]['gbif']['LIVING_SPECIMEN']
        global_data[ror_id]['MATERIAL_SAMPLE'] = organisation[5]['gbif']['MATERIAL_SAMPLE']
        global_data[ror_id]['PRESERVED_SPECIMEN'] = organisation[5]['gbif']['PRESERVED_SPECIMEN']

        # Check if organisation has overlapping data between GeoCASe and GBIF
        if organisation_name in organisation_mapping:
            # Add totals
            gbif_total = global_data[ror_id]['FOSSIL_SPECIMEN'] + global_data[ror_id][
                'LIVING_SPECIMEN'] + global_data[ror_id]['PRESERVED_SPECIMEN'] + \
                         global_data[ror_id]['MATERIAL_SAMPLE']
            global_data['Total'] += (int(organisation[5]['geocase']['total']) + gbif_total)
            global_data[ror_id]['Total'] = (int(organisation[5]['geocase']['total']) + gbif_total)

            # Check if organisation has fossil specimens in GeoCASe
            if int(organisation[5]['geocase']['Fossil']) > 0:
                # Check if organisation also has fossil specimens in GBIF
                if int(organisation[5]['gbif']['FOSSIL_SPECIMEN']) > 0:
                    # Set fossil to data from GeoCASe
                    global_data[ror_id]['FOSSIL_SPECIMEN'] = \
                        organisation[5]['geocase']['Fossil']

                    # Remove GBIF fossil records from grand total
                    global_data[ror_id]['Total'] -= int(organisation[5]['gbif']['FOSSIL_SPECIMEN'])
                    global_data['Total'] -= int(organisation[5]['gbif']['FOSSIL_SPECIMEN'])

            # Update with other record basis
            global_data[ror_id]['METEORITE'] = organisation[5]['geocase']['Meteorite']
            global_data[ror_id]['MINERAL'] = organisation[5]['geocase']['Mineral']
            global_data[ror_id]['ROCK'] = organisation[5]['geocase']['Rock']
            global_data[ror_id]['OTHER_GEOLOGICAL'] = organisation[5]['geocase']['Other_geological']

            # Add record basis to totals
            for value in islice(organisation[5]['geocase'].values(), 1, 6):
                global_data[ror_id]['Total'] += int(value)
                global_data['Total'] += int(value)
        else:
            # Add totals
            gbif_total = global_data[ror_id]['FOSSIL_SPECIMEN'] + global_data[ror_id][
                'LIVING_SPECIMEN'] + global_data[ror_id]['PRESERVED_SPECIMEN'] + \
                         global_data[ror_id]['MATERIAL_SAMPLE']
            global_data['Total'] += gbif_total
            global_data[ror_id]['Total'] = gbif_total

            # Update countries out of GeoCASe
            global_data[ror_id]['METEORITE'] = 0
            global_data[ror_id]['MINERAL'] = 0
            global_data[ror_id]['ROCK'] = 0
            global_data[ror_id]['OTHER_GEOLOGICAL'] = 0

        # Add GBIF issues and flags
        global_data[ror_id]['issues_and_flags'] = organisation[6]

    return global_data
