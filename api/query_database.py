from sqlalchemy import create_engine, extract, and_

from configparser import ConfigParser
from itertools import islice
from datetime import datetime as dt, timedelta
from typing import Union

# Import database models
import model.countries
import model.organisations


# Setting current month
current_month = dt.now().strftime('%B')

# Sonar constant
sonar_constant_datasets = 'Total datasets'

# Temporary mapping between GBIF and GeoCASe
country_mapping = {
    'DE': 'Germany',
    'GB': 'UK',
    'EE': 'Estonia',
    'AT': 'Austria',
    'FI': 'Finland',
    'NL': 'The Netherlands'
}

# Temporary mapping between GBIF and GeoCASe
organisation_mapping = {
    'Museum für Naturkunde': 'Museum für Naturkunde',
    'Natural History Museum': 'Natural History Museum, England',
    'Tallinn University of Technology': 'SARV',
    'Naturhistorisches Museum': 'Museum of Natural History Vienna',
    'Finnish Museum of Natural History': 'FMNH',
    'Naturalis Biodiversity Center': 'Naturalis'
}


def database_config(filename: str = 'database.ini', section: str = 'postgresql'):
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

    database_config = create_engine('postgresql+psycopg2://' + db['user'] + ':' + db['password'] + '@' + db['host'] + '/' + db['database'], echo=False)

    return database_config


def prepare_country(global_data: dict, country: list, country_code: str) -> dict:
    """ Prepares the country data that was found by the database query
        Sets all different values regarding the GBIF and GeoCASe data
        :return: Returns the global dict with the added country data
    """

    global_data[country_code] = {}

    # Add GBIF datasets
    global_data[country_code][sonar_constant_datasets] = country[4]['gbif']

    # General totals
    global_data['Total'] += int(country[5]['gbif']['total'])
    global_data[country_code]['Total'] = int(country[5]['gbif']['total'])

    # Add GBIF basis of record
    global_data[country_code]['FOSSIL_SPECIMEN'] = country[5]['gbif']['FOSSIL_SPECIMEN']
    global_data[country_code]['LIVING_SPECIMEN'] = country[5]['gbif']['LIVING_SPECIMEN']
    global_data[country_code]['MATERIAL_SAMPLE'] = country[5]['gbif']['MATERIAL_SAMPLE']
    global_data[country_code]['PRESERVED_SPECIMEN'] = country[5]['gbif']['PRESERVED_SPECIMEN']

    # Check if country has overlapping data between GeoCASe and GBIF
    if country_code in country_mapping:
        # Add GeoCASe numbers to GBIF total
        global_data['Total'] += int(country[5]['geocase']['total'])
        global_data[country_code]['Total'] += int(country[5]['geocase']['total'])

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

    # Add month
    global_data[country_code]['month'] = dt.strftime(country[7], '%B')

    return global_data


def prepare_countries(global_data: dict, country: list, country_code: str) -> dict:
    """ Prepares the multiple countries' data that was found by the database query
        Sets all different values regarding the GBIF and GeoCASe data
         :return: Returns the global dict with the added countries' data
    """

    month_save = global_data[country_code]
    global_data[country_code] = {}
    global_data[country_code][month_save['month']] = month_save

    month = dt.strftime(country[7], '%B')
    global_data[country_code][month] = {}

    # Add GBIF datasets
    global_data[country_code][month][sonar_constant_datasets] = country[4]['gbif']

    # Add GBIF basis of record
    global_data[country_code][month]['FOSSIL_SPECIMEN'] = country[5]['gbif']['FOSSIL_SPECIMEN']
    global_data[country_code][month]['LIVING_SPECIMEN'] = country[5]['gbif']['LIVING_SPECIMEN']
    global_data[country_code][month]['MATERIAL_SAMPLE'] = country[5]['gbif']['MATERIAL_SAMPLE']
    global_data[country_code][month]['PRESERVED_SPECIMEN'] = country[5]['gbif']['PRESERVED_SPECIMEN']

    # Check if country has overlapping data between GeoCASe and GBIF
    if country_code in country_mapping:
        # Add GeoCASe numbers to GBIF total
        global_data['Total'] += (int(country[5]['geocase']['total']) + int(country[5]['gbif']['total']))
        global_data[country_code][month]['Total'] = (
                int(country[5]['geocase']['total']) + int(country[5]['gbif']['total']))

        # Check if country has fossil specimens in GeoCASe
        if int(country[5]['geocase']['Fossil']) > 0:
            # Check if country also has fossil specimens in GBIF
            if int(country[5]['gbif']['FOSSIL_SPECIMEN']) > 0:
                # Set fossil to data from GeoCASe
                global_data[country_code][month]['FOSSIL_SPECIMEN'] = \
                    country[5]['geocase']['Fossil']

                # Remove GBIF fossil records from grand total
                global_data[country_code][month]['Total'] -= int(country[5]['gbif']['FOSSIL_SPECIMEN'])
                global_data['Total'] -= int(country[5]['gbif']['FOSSIL_SPECIMEN'])

        # Update with other record basis
        global_data[country_code][month]['METEORITE'] = country[5]['geocase']['Meteorite']
        global_data[country_code][month]['MINERAL'] = country[5]['geocase']['Mineral']
        global_data[country_code][month]['ROCK'] = country[5]['geocase']['Rock']
        global_data[country_code][month]['OTHER_GEOLOGICAL'] = country[5]['geocase']['Other_geological']

        # Add record basis to totals
        for value in islice(country[5]['geocase'].values(), 1, 6):
            global_data[country_code][month]['Total'] += int(value)
            global_data['Total'] += int(value)
    else:
        # Update countries out of GeoCASe
        global_data[country_code][month]['METEORITE'] = 0
        global_data[country_code][month]['MINERAL'] = 0
        global_data[country_code][month]['ROCK'] = 0
        global_data[country_code][month]['OTHER_GEOLOGICAL'] = 0

    # Add GBIF issues and flags
    global_data[country_code][month]['issues_and_flags'] = country[6]

    # Add month
    global_data[country_code][month]['month'] = country[7]

    return global_data


def select_countries_data(request_list: list, month: Union[str, list] = current_month) -> dict:
    """ Calls on data belonging to requested countries out of database
        Transforms the data to a usable format
        :return: global_data: dictionary that possesses the reformed data
    """

    # Prepare database connection
    db_config = database_config()

    # Set date range
    current_date = dt.now().date() + timedelta(days=1)
    last_date = dt.now().date() - timedelta(days=360)

    countries = model.countries.countries_model()

    # Check if entity already exists (for same month)
    if request_list:
        if type(month) == list:
            query = countries.select().where(and_(
                countries.c.country_code.in_(tuple(request_list)),
                countries.c.static_date >= last_date,
                countries.c.static_date <= current_date
            ))
        else:
            current_year = dt.now().year
            query = countries.select().where(
                extract('year', countries.c.static_date) == current_year,
                extract('month', countries.c.static_date) == dt.strptime(month, '%B').month,
                countries.c.country_code.in_(tuple(request_list))
            )
    else:
        query = countries.select().where(
            countries.c.static_date >= last_date,
            countries.c.static_date <= current_date,
            extract('month', countries.c.static_date) == dt.strptime(month, '%B').month
        )

    with db_config.connect() as conn:
        countries_data = conn.execute(query).fetchall()

    # Set up basic response element
    global_data: dict = {
        'Total': 0
    }

    # For each country, set data properties out of database
    for country in countries_data:
        country_code = country[1]

        if country_code in global_data:
            global_data = prepare_countries(global_data, country, country_code)
        else:
            global_data = prepare_country(global_data, country, country_code)

    return global_data


def prepare_organisation(global_data: dict, organisation: list, ror_id: str, organisation_name: str) -> dict:
    """ Prepares the organisation data that was found by the database query
        Sets all different values regarding the GBIF and GeoCASe data
        :return: Returns the global dict with the added organisation data
    """

    global_data[ror_id] = {}

    # Add GBIF datasets
    global_data[ror_id][sonar_constant_datasets] = organisation[4]['gbif']
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

    # Add month
    global_data[ror_id]['month'] = dt.strftime(organisation[7], '%B')

    return global_data


def prepare_organisations(global_data: dict, organisation: list, ror_id: str, organisation_name: str) -> dict:
    """ Prepares the organisation's data that was found by the database query
        Sets all different values regarding the GBIF and GeoCASe data
        :return: Returns the global dict with the added organisation's data
    """

    month_save = global_data[ror_id]
    global_data[ror_id] = {}
    global_data[ror_id][month_save['month']] = month_save

    month = dt.strftime(organisation[7], '%B')
    global_data[ror_id][month] = {}

    # Add GBIF datasets
    global_data[ror_id][month][sonar_constant_datasets] = organisation[4]['gbif']
    global_data[ror_id]['organisation_name'] = organisation_name

    # Add GBIF basis of record
    global_data[ror_id][month]['FOSSIL_SPECIMEN'] = organisation[5]['gbif']['FOSSIL_SPECIMEN']
    global_data[ror_id][month]['LIVING_SPECIMEN'] = organisation[5]['gbif']['LIVING_SPECIMEN']
    global_data[ror_id][month]['MATERIAL_SAMPLE'] = organisation[5]['gbif']['MATERIAL_SAMPLE']
    global_data[ror_id][month]['PRESERVED_SPECIMEN'] = organisation[5]['gbif']['PRESERVED_SPECIMEN']

    # Check if organisation has overlapping data between GeoCASe and GBIF
    if organisation_name in organisation_mapping:
        # Add totals
        gbif_total = global_data[ror_id][month]['FOSSIL_SPECIMEN'] + global_data[ror_id][month][
            'LIVING_SPECIMEN'] + global_data[ror_id][month]['PRESERVED_SPECIMEN'] + \
                     global_data[ror_id][month]['MATERIAL_SAMPLE']
        global_data['Total'] += (int(organisation[5]['geocase']['total']) + gbif_total)
        global_data[ror_id][month]['Total'] = (int(organisation[5]['geocase']['total']) + gbif_total)

        # Check if organisation has fossil specimens in GeoCASe
        if int(organisation[5]['geocase']['Fossil']) > 0:
            # Check if organisation also has fossil specimens in GBIF
            if int(organisation[5]['gbif']['FOSSIL_SPECIMEN']) > 0:
                # Set fossil to data from GeoCASe
                global_data[ror_id][month]['FOSSIL_SPECIMEN'] = \
                    organisation[5]['geocase']['Fossil']

                # Remove GBIF fossil records from grand total
                global_data[ror_id][month]['Total'] -= int(organisation[5]['gbif']['FOSSIL_SPECIMEN'])
                global_data['Total'] -= int(organisation[5]['gbif']['FOSSIL_SPECIMEN'])

        # Update with other record basis
        global_data[ror_id][month]['METEORITE'] = organisation[5]['geocase']['Meteorite']
        global_data[ror_id][month]['MINERAL'] = organisation[5]['geocase']['Mineral']
        global_data[ror_id][month]['ROCK'] = organisation[5]['geocase']['Rock']
        global_data[ror_id][month]['OTHER_GEOLOGICAL'] = organisation[5]['geocase']['Other_geological']

        # Add record basis to totals
        for value in islice(organisation[5]['geocase'].values(), 1, 6):
            global_data[ror_id][month]['Total'] += int(value)
            global_data['Total'] += int(value)
    else:
        # Add totals
        gbif_total = global_data[ror_id][month]['FOSSIL_SPECIMEN'] + global_data[ror_id][month][
            'LIVING_SPECIMEN'] + global_data[ror_id][month]['PRESERVED_SPECIMEN'] + \
                     global_data[ror_id][month]['MATERIAL_SAMPLE']
        global_data['Total'] += gbif_total
        global_data[ror_id][month]['Total'] = gbif_total

        # Update countries out of GeoCASe
        global_data[ror_id][month]['METEORITE'] = 0
        global_data[ror_id][month]['MINERAL'] = 0
        global_data[ror_id][month]['ROCK'] = 0
        global_data[ror_id][month]['OTHER_GEOLOGICAL'] = 0

    # Add GBIF issues and flags
    global_data[ror_id][month]['issues_and_flags'] = organisation[6]

    # Add month
    global_data[ror_id][month]['month'] = organisation[7]

    return global_data


def select_organisations_data(request_list: list, month: Union[str, list] = current_month) -> dict:
    """ Calls on data belonging to requested organisations out of database
        Transforms the data to an usable format
        :return: global_data: dictionary that possesses the reformed data
    """

    # Prepare database connection
    db_config = database_config()

    organisations = model.organisations.organisations_model()

    # Set date range
    current_date = dt.now().date() + timedelta(days=1)
    last_date = dt.now().date() - timedelta(days=360)

    # Check if entity already exists (for same month)
    if request_list:
        if type(month) == list:
            query = organisations.select().where(
                organisations.c.ror_id.in_(tuple(request_list)),
                organisations.c.static_date >= last_date,
                organisations.c.static_date <= current_date
            )
        else:
            current_year = dt.now().year

            query = organisations.select().where(
                extract('year', organisations.c.static_date) == current_year,
                extract('month', organisations.c.static_date) == dt.strptime(month, '%B').month,
                organisations.c.ror_id.in_(tuple(request_list))
            )
    else:
        query = organisations.select().where(
            organisations.c.static_date >= last_date,
            organisations.c.static_date <= current_date,
            extract('month', organisations.c.static_date) == dt.strptime(month, '%B').month
        )

    with db_config.connect() as conn:
        organisations_data = conn.execute(query).fetchall()

    # Set up basic response element
    global_data: dict = {
        'Total': 0
    }

    # For each organisation, set data properties out of database
    for organisation in organisations_data:
        ror_id = organisation[1]
        organisation_name = organisation[2]

        if ror_id in global_data:
            global_data = prepare_organisations(global_data, organisation, ror_id, organisation_name)
        else:
            global_data = prepare_organisation(global_data, organisation, ror_id, organisation_name)

    return global_data
