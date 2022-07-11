import logging
import time


# GBIF and GeoCASe API functionality
import GBIF_functions
import GeoCASe_functions
# Database functionality
import insert_to_database


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def process_countries():
    """ Processes the data for each of the countries in GBIF and GeoCASe
        Saves the data in the 'countries' table of the database
    """

    tic = time.perf_counter()

    logging.info('Step 1/4: Receiving countries datasets data from GBIF...')
    gbif_datasets = GBIF_functions.gather_datasets()

    logging.info('Step 2/4: Receiving countries specimens data from GBIF...')
    gbif_specimens = GBIF_functions.gather_specimens()

    logging.info('Step 3/4: Receiving countries issues and flags data from GBIF...')
    gbif_issues_flags = GBIF_functions.gather_issues_flags()

    logging.info('Step 4/4: Receiving countries data from GeoCASe...')
    geocase_data = GeoCASe_functions.gather_data()

    logging.info('Fetching complete, now saving to database...')
    insert_to_database.insert_countries_data(gbif_datasets, gbif_specimens, gbif_issues_flags, geocase_data)

    toc = time.perf_counter()
    passed_time = round(toc - tic, 2)

    logging.info(f'Finished in {passed_time} seconds')


def process_organisations():
    """ Processes the data for each of the organisation in GBIF and GeoCASe
        Saves the data in the 'organisation' table of the database
    """

    tic = time.perf_counter()

    logging.info('Step 1/2: Receiving organisations data from GBIF...')
    gbif_organisations_data = GBIF_functions.gather_institutions()

    logging.info('Step 2/2: Receiving organisations data from GeoCASe...')
    geocase_data = GeoCASe_functions.gather_publishers()

    insert_to_database.insert_organisations_data(gbif_organisations_data, geocase_data)

    toc = time.perf_counter()
    passed_time = round(toc - tic, 2)

    logging.info(f'Finished in {passed_time} seconds')


def main():
    """ Main function for Network Status Overview: Processing Service
        Calls on functions for preparing and saving countries and organisations data of GBIF and GeoCASe
    """
    logging.info('NETWORK STATUS OVERVIEW: PROCESSING SERVICE')
    logging.info('Version: 0.5')
    logging.info('Now starting services...')

    logging.info('Fetching countries data and saving to database')
    process_countries()

    logging.info('Fetching organisations data and saving to database')
    process_organisations()

    logging.info('Both GBIF and GeoCASe processes complete, all processes finished!')


main()
