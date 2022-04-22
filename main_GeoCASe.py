import requests
import csv


geocase_endpoint = "https://geocase.eu/api"


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
        'facet.field': [
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
            'total': 0
        }

        geocase_data['countries'][country_name]['total'] = provider_countries[provider_country]

        # Query API by provider country and facet on basis of record
        query = {
            'q': '*',
            'fq': '{!tag=providercountry}providercountry:(\"' + country_name + '\")',
            'rows': 0,
            'facet.field': [
                'recordbasis'
            ],
            'facet': 'on'
        }
        response = requests.get(geocase_endpoint, params=query).json()
        provider_record_basis = response['facet_counts']['facet_fields']['recordbasis']

        # Set record basis values
        for rb in record_basis:
            rb_amount = provider_record_basis[provider_record_basis.index(rb) + 1]
            geocase_data['countries'][country_name][rb] = rb_amount

            # Add to record basis total
            if not geocase_data['total'].get(rb):
                geocase_data['total'][rb] = rb_amount
            else:
                geocase_data['total'][rb] += rb_amount

        # Plus one for the overlapping loop
        i += 1

    return geocase_data


def write_to_csv(geocase_data: dict):
    """ Takes the total geocase_data dict and writes it to csv
        :param geocase_data: Dict of global data variable containing total datasets per country
        and record basis
        :return: Writes a csv
    """

    # Preparing basic csv
    headers = ['Origin', 'Total']
    values: dict = {
        'total': ['Total']
    }

    # Appending headers and total values
    for total in geocase_data['total']:
        if not total == "specimens":
            headers.append(total)

        values['total'].append(geocase_data['total'][total])

    # Appending country values
    for country in geocase_data['countries']:
        values[country] = [country]
        values[country] += [v for v in geocase_data['countries'][country].values()]

    # Write to publishers_issues_flags.csv
    csv_file = "csv_files/written/geocase_data.csv"

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(headers)

        for v in values.values():
            writer.writerow(v)


# Call on function
write_to_csv(gather_data())
