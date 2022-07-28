import requests


geocase_endpoint = "https://geocase.eu/api"
facet_field_constant = 'facet.field'


def gather_data() -> dict:
    """ Questions the GeoCASe API
        Collects data about total specimens and record basis per country
        Saves the data in the global 'data' dict
        :return: Returns the dict as geocase_data
    """

    # Defining global data variable
    geocase_data: dict = {
        'total': {},
        'countries': {}
    }

    # Search for all specimens in GeoCASe, facet on provider country
    query: dict = {
        'q': '*',
        'rows': 0,
        facet_field_constant: [
            'providercountry'
        ],
        'facet': 'on'
    }
    response = requests.get(geocase_endpoint, params=query).json()

    # Set total amount of specimens
    geocase_data['total']['specimens'] = response['response']['numFound']

    # Set total amount of specimens per provider country
    provider_countries = response['facet_counts']['facet_fields']['providercountry']
    country_names = [provider_countries[i] for i in range(0, len(provider_countries), 2)]
    record_basis = ['Fossil', 'Meteorite', 'Mineral', 'Rock', 'Other']

    # Iterate through provider countries
    i = 0
    for provider_country in range(1, len(provider_countries), 2):
        country_name = country_names[i]

        geocase_data['countries'][country_name] = {
            'total': provider_countries[provider_country]
        }

        # Query API by provider country and facet on basis of record
        query = {
            'q': '*',
            'fq': '{!tag=providercountry}providercountry:(\"' + country_name + '\")',
            'rows': 0,
            facet_field_constant: [
                'recordbasis'
            ],
            'facet': 'on'
        }
        response = requests.get(geocase_endpoint, params=query).json()
        provider_record_basis = response['facet_counts']['facet_fields']['recordbasis']

        # Set record basis values
        for rb in record_basis:
            rb_amount = provider_record_basis[provider_record_basis.index(rb) + 1]

            # Check if record basis is other
            if rb == 'Other':
                rb = 'Other_geological'

            geocase_data['countries'][country_name][rb] = rb_amount

            # Add to record basis total
            if not geocase_data['total'].get(rb):
                geocase_data['total'][rb] = rb_amount
            else:
                geocase_data['total'][rb] += rb_amount

        # Plus one for the overlapping loop
        i += 1

    return geocase_data


def gather_publishers() -> dict:
    """ Questions the GeoCASe API
        Collects data about total specimens and record basis per publisher (provider)
        Saves the data in the global 'publishers' dict
        :return: Returns the dict as publishers
    """

    # Defining global data variable
    publishers: dict = {
        'total': {},
        'providers': {}
    }

    # Search for all specimens in GeoCASe, facet on publisher
    query: dict = {
        'q': '*',
        'rows': 0,
        facet_field_constant: [
            'providername'
        ],
        'facet': 'on'
    }
    response = requests.get(geocase_endpoint, params=query).json()

    # Set total amount of specimens
    publishers['total']['specimens'] = response['response']['numFound']

    # Set total amount of specimens per provider
    providers = response['facet_counts']['facet_fields']['providername']
    provider_names = [providers[i] for i in range(0, len(providers), 2)]
    record_basis = ['Fossil', 'Meteorite', 'Mineral', 'Rock', 'Other']

    # Iterate through providers
    i = 0
    for provider in range(1, len(providers), 2):
        provider_name = provider_names[i]

        publishers['providers'][provider_name] = {
            'total': providers[provider]
        }

        # Query API by provider and facet on record basis
        publishers = query_on_record_basis(provider_name, publishers, record_basis)

        # Plus one for the overlapping loop
        i += 1

    return publishers


def query_on_record_basis(provider_name: str, publishers: dict, record_basis: list) -> dict:
    """ Internal function of gather_publishers()
        Request record basis data from GeoCASe API per individual provider
        :return: Returns the updated publishers dict
    """

    query: dict = {
        'q': '*',
        'fq': '{!tag=providername}providername:(\"' + provider_name + '\")',
        'rows': 0,
        facet_field_constant: [
            'recordbasis'
        ],
        'facet': 'on'
    }
    response = requests.get(geocase_endpoint, params=query).json()
    provider_record_basis = response['facet_counts']['facet_fields']['recordbasis']

    # Set record basis values
    for rb in record_basis:
        rb_amount = provider_record_basis[provider_record_basis.index(rb) + 1]

        # Check if record basis is other
        if rb == 'Other':
            rb = 'Other_geological'

        publishers['providers'][provider_name][rb] = rb_amount

        # Add to record basis total
        if not publishers['total'].get(rb):
            publishers['total'][rb] = rb_amount
        else:
            publishers['total'][rb] += rb_amount

    return publishers
