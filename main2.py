import logging


# GBIF API functionality
import GBIF_functions
# GeoCASe API functionality
import GeoCASe_functions
import query_database


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def process_countries():
    logging.info('Receiving countries datasets data from GBIF...')
    gbif_datasets = GBIF_functions.gather_datasets()

    logging.info('Receiving countries specimens data from GBIF...')
    gbif_specimens = GBIF_functions.gather_specimens()

    logging.info('Receiving countries issues and flags data from GBIF...')
    gbif_issues_flags = GBIF_functions.gather_issues_flags()

    logging.info('Receiving countries data from GeoCASe...')
    geocase_data = GeoCASe_functions.gather_data()

    query_database.insert_countries_data(gbif_datasets, gbif_specimens, gbif_issues_flags, geocase_data)


def process_organisations():
    logging.info('Receiving organisations datasets data from GBIF...')
    gbif_organisations_data = GBIF_functions.gather_institutions()

    logging.info('Receiving organisations data from GeoCASe...')
    geocase_data = GeoCASe_functions.gather_publishers()

    query_database.insert_organisations_data(gbif_organisations_data, geocase_data)


def main2():
    process_countries()
    process_organisations()


main2()
