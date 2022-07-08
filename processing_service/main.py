import logging


# GBIF and GeoCASe API functionality
import GBIF_functions
import GeoCASe_functions
# Database functionality
import insert_to_database


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

    insert_to_database.insert_countries_data(gbif_datasets, gbif_specimens, gbif_issues_flags, geocase_data)


def process_organisations():
    logging.info('Receiving organisations datasets data from GBIF...')
    gbif_organisations_data = GBIF_functions.gather_institutions()

    logging.info('Receiving organisations data from GeoCASe...')
    geocase_data = GeoCASe_functions.gather_publishers()

    insert_to_database.insert_organisations_data(gbif_organisations_data, geocase_data)


def main():
    process_countries()
    process_organisations()


main()
