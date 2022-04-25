# GBIF API functionality
import GBIF_functions
# GeoCASe API functionality
import GeoCASe_functions
# CSV files functionality
import csv_functions


def main():
    options_list = [
        'all',
        'gbif_datasets',
        'gbif_specimens',
        'gbif_issues_flags',
        'gbif_issues_flags_monthly',
        'gbif_institutions',
        'geocase_data'
    ]

    print(*options_list, sep='\n')
    request = input('\nSelect an option: ')

    if request in options_list:
        # Check which function
        match request:
            case 'all':
                # Call on all functions
                execute_all()
            case 'gbif_datasets':
                # Call on GBIF datasets
                gbif_datasets()
            case 'gbif_specimens':
                # Call on GBIF specimens
                gbif_specimens()
            case 'gbif_issues_flags':
                # Call on GBIF issues and flags
                gbif_issues_flags()
            case 'gbif_issues_flags_monthly':
                # Call on GBIF issues and flags monthly progress
                gbif_issues_flags_monthly()
            case 'gbif_institutions':
                # Call on GBIF institutions
                gbif_institutions()
            case 'geocase_data':
                # Call on GeoCASe data
                geocase_data()


# Call on all functions, one at a time
def execute_all():
    print('Now executing all methods, one at a time')
    total_count = 6
    progress = 0

    # GBIF datasets
    gbif_datasets()
    progress += 1
    print(f'Completed: {progress} out of {total_count}')

    # GBIF specimens
    gbif_specimens()
    progress += 1
    print(f'Completed: {progress} out of {total_count}')

    # GBIF issues and flags
    gbif_issues_flags()
    progress += 1
    print(f'Completed: {progress} out of {total_count}')

    # GBIF issues and flags monthly
    gbif_issues_flags_monthly()
    progress += 1
    print(f'Completed: {progress} out of {total_count}')

    # GBIF institutions
    gbif_institutions()
    progress += 1
    print(f'Completed: {progress} out of {total_count}')

    # GeoCASe data
    geocase_data()
    progress += 1
    print(f'Completed: {progress} out of {total_count}')

    print('\nProcess done!')


# GBIF functions
def gbif_datasets():
    # First collect and prepare datasets data
    print('\nReceiving datasets data from GBIF...')
    data = GBIF_functions.gather_datasets()

    # Then write data to csv
    print('\nData fetched and prepared, now writing to CSV...')
    csv_file = csv_functions.write_datasets_to_csv(data)

    # Finishing statement
    print(f'\nProcess finished! CSV was saved in: "{csv_file}"')


def gbif_specimens():
    # First collect and prepare specimens data
    print('\nReceiving specimens data from GBIF...')
    data = GBIF_functions.gather_specimens()

    # Then write data to csv
    print('\nData fetched and prepared, now writing to CSV...')
    csv_file = csv_functions.write_specimens_to_csv(data)

    # Finishing statement
    print(f'\nProcess finished! CSV was saved in: "{csv_file}"')


def gbif_issues_flags():
    # First collect and prepare issues and flags data
    print('\nReceiving issues and flags data from GBIF...')
    data = GBIF_functions.gather_issues_flags()

    # Then write data to csv
    print('\nData fetched and prepared, now writing to CSV...')
    csv_file = csv_functions.write_issues_and_flags_to_csv(data)

    # Finishing statement
    print(f'\nProcess finished! CSV was saved in: "{csv_file}"')


def gbif_issues_flags_monthly():
    # First collect and prepare issues and flags data
    print('\nReceiving issues and flags data from GBIF...')
    data = GBIF_functions.gather_issues_flags()

    # Then write data to csv
    print('\nData fetched and prepared, now writing to CSV...')
    csv_file = csv_functions.write_issues_and_flags_monthly_to_csv(data)

    # Finishing statement
    print(f'\nProcess finished! CSV was saved in: "{csv_file}"')


def gbif_institutions():
    # First collect and prepare institutions data
    print('\nReceiving institutions data from GBIF...')
    data = GBIF_functions.gather_institutions()

    # Then write data to csv
    print('\nData fetched and prepared, now writing to CSV...')
    csv_file = csv_functions.write_institution_to_csv(data)

    # Finishing statement
    print(f'\nProcess finished! CSVs were saved in: "{csv_file}"')


# GeoCASe functions
def geocase_data():
    # First collect and prepare GeoCASe data
    print('\nReceiving data from GeoCASe...')
    data = GeoCASe_functions.gather_data()

    # Then write data to csv
    print('\nData fetched and prepared, now writing to CSV...')
    csv_file = csv_functions.write_geocase_data_to_csv(data)

    # Finishing statement
    print(f'\nProcess finished! CSVs was saved in: "{csv_file}"')


# Call on main function
main()
