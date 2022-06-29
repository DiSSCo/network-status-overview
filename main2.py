import logging


# Import database logic
# import query_database
# GBIF API functionality
import GBIF_functions
# GeoCASe API functionality
import GeoCASe_functions
import query_database

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def process_countries():
    logging.info('\nReceiving countries datasets data from GBIF...')
    gbif_datasets = GBIF_functions.gather_datasets()

    logging.info('\nReceiving countries specimens data from GBIF...')
    gbif_specimens = GBIF_functions.gather_specimens()

    logging.info('\nReceiving countries issues and flags data from GBIF...')
    gbif_issues_flags = GBIF_functions.gather_issues_flags()

    logging.info('\nReceiving countries data from GeoCASe...')
    geocase_data = GeoCASe_functions.gather_data()

    query_database.insert_countries_data(gbif_datasets, gbif_specimens, gbif_issues_flags, geocase_data)


def process_organisations():
    logging.info('\nReceiving organisations datasets data from GBIF...')
    gbif_organisations_data = GBIF_functions.gather_institutions()

    logging.info('\nReceiving organisations data from GeoCASe...')
    geocase_data = GeoCASe_functions.gather_publishers()

    query_database.insert_organisations_data(gbif_organisations_data, geocase_data)


process_countries()
process_organisations()
