from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert

from configparser import ConfigParser
from datetime import datetime as dt

# Import database models
import model.countries
import model.organisations


# Setting the current month
current_month = dt.now().strftime('%B')

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

    database_config = create_engine(
        'postgresql+psycopg2://' + db['user'] + ':' + db['password'] + '@' + db['host'] + '/' + db['database'],
        echo=False)

    return database_config


def insert_countries_data(gbif_datasets: dict, gbif_specimens: dict, gbif_issues_flags: dict, geocase_data: dict):
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
        geocase_dummy: dict = {}

        if country in country_mapping:
            geocase_dummy = geocase_data['countries'][country_mapping[country]]

        # Set static date (first day, this month, this year)
        static_date = dt(dt.now().year, dt.now().month, 1).date()

        # Initiate basic entity for database
        country_entity = {
            'country_code': country,
            'country_name': 'test',
            'datasets_count': {
                'gbif': gbif_datasets['countries'][country]
            },
            'specimens_count': {
                'gbif': gbif_specimens['countries'][country],
                'geocase': geocase_dummy
            },
            'issues_flags': gbif_issues_flags['countries'][country],
            'static_date': static_date
        }

        # Prepare database connection
        db_config = database_config()

        countries = model.countries.countries_model()

        # Check if entity already exists (for same month) then upsert
        query = insert(countries).values(country_entity)
        query = query.on_conflict_do_update(
            constraint='countries_un',
            set_={
                countries.c.last_updated: dt.now(),
                countries.c.datasets_count: country_entity['datasets_count'],
                countries.c.specimens_count: country_entity['specimens_count'],
                countries.c.issues_flags: country_entity['issues_flags']
            }
        )

        # Execute query
        with db_config.connect() as conn:
            conn.execute(query)


def insert_organisations_data(gbif_data: dict, geocase_data: dict):
    """ Transforms the received organisations' data to a standardised format
        Saves the formatted data in the database by insert or update
    """

    # For each organisation, prepare and save data to database
    for organisation in gbif_data:
        # Check if GeoCASe data from organisation is present
        geocase_dummy: dict
        organisation_name = gbif_data[organisation]['name']

        if organisation_name in organisation_mapping:
            geocase_dummy = geocase_data['providers'][organisation_mapping[organisation_name]]
        else:
            geocase_dummy = {}

        # Set static date (first day, this month, this year)
        static_date = dt(dt.now().year, dt.now().month, 1).date()

        # Initiate basic entity for database
        organisation_entity = {
            'ror_id': gbif_data[organisation]['ror_id'],
            'organisation_name': organisation_name,
            'datasets_count': {
                'gbif': gbif_data[organisation]['totals']['datasets']
            },
            'specimens_count': {
                'gbif': gbif_data[organisation]['totals'],
                'geocase': geocase_dummy
            },
            'issues_flags': gbif_data[organisation]['issues_and_flags'],
            'static_date': static_date
        }

        # Prepare database connection
        db_config = database_config()

        organisations = model.organisations.organisations_model()

        # Check if entity already exists (for same month) then upsert
        query = insert(organisations).values(organisation_entity)
        query = query.on_conflict_do_update(
            constraint='organisations_un',
            set_={
                organisations.c.last_updated: dt.now(),
                organisations.c.datasets_count: organisation_entity['datasets_count'],
                organisations.c.specimens_count: organisation_entity['specimens_count'],
                organisations.c.issues_flags: organisation_entity['issues_flags']
            }
        )

        # Execute query
        with db_config.connect() as conn:
            conn.execute(query)
