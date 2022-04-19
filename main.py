import requests


# Defining GBIF endpoints
gbif_dataset = 'https://api.gbif.org/v1/dataset/search'
gbif_specimen = 'https://www.gbif.org/api/occurrence/breakdown'


def gather_datasets():
    """ Searches in GBIF for the number of datasets belonging to DiSSCo and saves this
        Uses the number to iterate through the datasets, adding up the total per country
        Saves the data in the global 'data' dict
    """

    # Data definition
    total_datasets = {
        'total': 0,
        'countries': {}
    }

    # Initial query for dataset count
    query = {'network_key': '17abcf75-2f1e-46dd-bf75-a5b21dd02655', 'limit': 1}
    response = requests.get(gbif_dataset, params=query).json()

    total_datasets['total'] = response['count']
    i = 0

    # Gather all datasets per 1000 (GBIF max)
    while i < total_datasets['total']:
        query = {'network_key': '17abcf75-2f1e-46dd-bf75-a5b21dd02655', 'limit': 1000, 'offset': i}
        response = requests.get(gbif_dataset, params=query).json()

        # Iterate through datasets and gather information
        for dataset in response['results']:
            # Count datasets per country
            if dataset['publishingCountry'] not in total_datasets['countries']:
                total_datasets['countries'][dataset['publishingCountry']] = 0

            total_datasets['countries'][dataset['publishingCountry']] += 1
            i += 1

    return total_datasets


def gather_specimens():
    """ Searches in GBIF for the number of specimens belonging to DiSSCo and saves this
        Filters the results based on the basis of record property and orders by country
        Uses this data to iterate through the countries to calculate their specimen total
        Finally categorizes these totals using basis of record
        Saves the data in the global 'data' dict
    """

    # Data definition
    total_specimens = {
        'total': {},
        'countries': {}
    }

    # Gather number of specimens per publishing country and filtered on basis of record
    basis_of_record = ['PRESERVED_SPECIMEN', 'FOSSIL_SPECIMEN', 'LIVING_SPECIMEN', 'MATERIAL_SAMPLE']
    query = {
        'basis_of_record': basis_of_record,
        'network_key': '17abcf75-2f1e-46dd-bf75-a5b21dd02655',
        'advanced': True,
        'dimension': 'publishing_country',
        'secondDimension': 'basis_of_record',
        'limit': 1000,
        'offset': 0
    }
    response = requests.get(gbif_specimen, params=query).json()

    # Iterate through the countries to calculate the total amount of specimens
    for country in response['results']:
        total_specimens['countries'][country['filter']['publishing_country']] = {
            'total': country['count']
        }

        # Group the totals of countries by basis of record
        i = 0
        for bor in basis_of_record:
            if total_specimens['total'].get(bor) is None:
                total_specimens['total'][bor] = country['values'][i]
            else:
                total_specimens['total'][bor] += country['values'][i]

            total_specimens['countries'][country['filter']['publishing_country']][bor] = country['values'][i]
            i += 1

    return total_specimens


def gather_issues_flags():
    """ Searches in GBIF for the number of publishing countries belonging to DiSSCo
        Iterates through this data to call on the issues and flags belonging to each country
        Finally calculates the totals per issue or flag from a country
        Saves the data in the global 'data' dict
    """

    # Data definition
    issues_and_flags = {
        'total': 0, 'countries': {}
    }

    # Gather all publishing countries of DiSSCo
    query = {
        'network_key': '17abcf75-2f1e-46dd-bf75-a5b21dd02655',
        'advanced': True,
        'dimension': 'publishing_country',
        'limit': 1000,
        'offset': 0
    }
    response = requests.get(gbif_specimen, params=query).json()

    # Iterate through countries
    for country in response['results']:
        country_code = country['filter']['publishing_country']

        # Gather issues and flags per country
        query = {
            'network_key': '17abcf75-2f1e-46dd-bf75-a5b21dd02655',
            'publishing_country': country_code,
            'advanced': True,
            'dimension': 'issue',
            'secondDimension': 'month',
            'limit': 1000,
            'offset': 0
        }
        response = requests.get(gbif_specimen, params=query).json()

        issues_and_flags['countries'][country_code] = {
            'total': 0
        }

        # Store total issues and flags per country
        for issue_flag in response['results']:
            issues_and_flags['countries'][country_code]['total'] \
                += issue_flag['count']

            issues_and_flags['countries'][country_code][issue_flag['displayName']] = {
                'total': issue_flag['count'],
                'monthly_progress': {}
            }

            issues_and_flags['total'] += issue_flag['count']

            # Gather process over time (per month)
            m = 1

            while m <= 12:
                issues_and_flags['countries'][country_code][issue_flag['displayName']]['monthly_progress'][m] \
                    = issue_flag['values'][m - 1]
                m += 1

    return issues_and_flags
