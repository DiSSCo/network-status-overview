import csv


# GBIf functions
def create_issues_and_flags_list() -> list:
    """ Takes the csv containing the names of all issues and converts it to a list
        :return: Returns the issues and flags list
    """

    issues_file = 'csv_files/sources/GBIF_issues.csv'
    issues_and_flags_list = []

    with open(issues_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            issue_flag = row[1].lower().replace('_', ' ').capitalize()

            issues_and_flags_list.append(issue_flag)

    return issues_and_flags_list


def write_datasets_to_csv(total_datasets: dict):
    """ Takes the total datasets dict and writes it to csv
        :param total_datasets: Dict of global data variable containing total datasets per country
        :return: Writes a csv
    """

    # Preparing basic csv
    headers = ['Total']
    values = [total_datasets['total']]

    # And iterating through the countries to append headers/values
    for country in total_datasets['countries']:
        headers.append(country)
        values.append(total_datasets['countries'][country])

    # Write to datasets.csv
    csv_file = 'csv_files/written/datasets.csv'

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerows([headers, values])

    return csv_file


def write_specimens_to_csv(total_specimens: dict):
    """ Takes the total specimens dict and writes it to csv
        :param total_specimens: Dict of global data variable containing total specimens per country
        :return: Writes a csv
    """

    basis_of_record = ['PRESERVED_SPECIMEN', 'FOSSIL_SPECIMEN', 'LIVING_SPECIMEN', 'MATERIAL_SAMPLE']

    # Preparing basic csv
    headers = ['Origin', 'Total'] + basis_of_record
    values = {
        'Total': ['Total']
    }

    # Insert values
    total_general = 0

    for t in total_specimens['total']:
        values['Total'].append(total_specimens['total'][t])
        total_general += total_specimens['total'][t]

    values['Total'].insert(1, str(total_general))

    # And iterating through the countries to append values
    for country in total_specimens['countries']:
        values[country] = [country]
        country_total = 0

        for bor in basis_of_record:
            values[country].append(total_specimens['countries'][country][bor])
            country_total += total_specimens['countries'][country][bor]

        values[country].insert(1, str(country_total))

    # Write to specimens.csv
    csv_file = 'csv_files/written/specimens.csv'

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(headers)

        for v in values.values():
            writer.writerow(v)

    return csv_file


def write_issues_and_flags_to_csv(issues_and_flags: dict):
    """ Takes the total datasets dict and writes it to csv
        :param issues_and_flags: Dict of global data variable containing total issues and flags per country
        :return: Writes a csv
    """

    # Receiving issues and flags
    issues_and_flags_list = create_issues_and_flags_list()

    # Preparing basic csv
    headers = ['Origin', 'Total']
    values = {
        'Total': ['Total', issues_and_flags['total']]
    }
    issue_totals = {}

    # Iterating through countries
    for country in issues_and_flags['countries']:
        # Defining total of country
        country_total = 0
        values[country] = [country]

        # Iterating through issues and flags
        for issue_flag in issues_and_flags_list:
            # Checking if headers (issues and flags) are present
            if issue_flag not in headers:
                headers.append(issue_flag)
                issue_totals[issue_flag] = 0

            # If issue exists for country, add up to values and total
            if issues_and_flags['countries'][country].get(issue_flag):
                # Issue add up to total
                issue_totals[issue_flag] += issues_and_flags['countries'][country][issue_flag]['total']

                # Add up to country total
                country_total += issues_and_flags['countries'][country][issue_flag]['total']

                # Add to issues and flags values
                values[country].append(issues_and_flags['countries'][country][issue_flag]['total'])
            else:
                values[country].append(0)

        # Append country total
        values[country].insert(1, country_total)

    # Append general total per issues and flags
    for issue_total in issue_totals:
        values['Total'].append(issue_totals[issue_total])

    # Write to issues_and_flags.csv
    csv_file = 'csv_files/written/issues_and_flags.csv'

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(headers)

        for v in values.values():
            writer.writerow(v)

    return csv_file


def write_issues_and_flags_monthly_to_csv(issues_and_flags: dict):
    """ Let's the user choose a country code and writes the monthly progress of issues and flags to csv
        :param issues_and_flags: Dict of global data variable containing total issues and flags per country
        :return: Writes a csv
    """

    # Choose country code (later to be automized)
    country = ""

    while country not in issues_and_flags['countries']:
        country = input("Please insert a valid country code: ")

    country_data = issues_and_flags['countries'][country]

    # Receiving issues and flags
    issues_and_flags_list = create_issues_and_flags_list()

    # Setting months and basic csv
    months = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
    ]
    headers = ['Origin', 'Total'] + months
    values = {
        'Total': ['Total', country_data['total']]
    }

    # Preparing monthly count
    month_count: dict = {}

    # Iterate through issues and flags
    for issue_flag in issues_and_flags_list:
        values[issue_flag] = [issue_flag]

        # If country has issue / flag add total to values
        if country_data.get(issue_flag):
            # Total
            values[issue_flag].append(country_data[issue_flag]['total'])

            # Per month
            i = 1
            for _ in months:
                values[issue_flag].append(country_data[issue_flag]['monthly_progress'][i])

                # Updating month total
                if i in month_count:
                    month_count[i] += country_data[issue_flag]['monthly_progress'][i]
                else:
                    month_count[i] = country_data[issue_flag]['monthly_progress'][i]

                i += 1

    # Set overall monthly totals
    for i in range(12):
        i += 1
        values['Total'].append(month_count[i])

    # Write to issues_and_flags_monthly.csv
    csv_file = 'csv_files/written/issues_and_flags_monthly.csv'

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(headers)

        for v in values.values():
            writer.writerow(v)

    return csv_file


def write_institution_to_csv(publishers: dict):
    """ Receives data from the institution function in main.py
        Calls on related functions to write the data to csv
        :return: Calls on: write_institution_to_csv_totals and write_institution_to_csv_issues_and_flags
    """

    # Write csv files
    csv_file = ""

    csv_file += write_institutions_to_csv_totals(publishers)
    csv_file += 'and: ' + write_institutions_to_csv_issues_and_flags(publishers)

    return csv_file


def write_institutions_to_csv_totals(publishers: dict):
    """ Prepares data from publishers dictionary and writes this to csv
        Data handled are: total datasets and basis of record
        :param publishers: Dict of GBIF publishers from DiSSCo network and related data
        :return: Writes a csv
    """

    # Preparing basic csv
    basis_of_record = ['PRESERVED_SPECIMEN', 'FOSSIL_SPECIMEN', 'LIVING_SPECIMEN', 'MATERIAL_SAMPLE']
    headers = [
        'Publisher',
        'GBIF id',
        'ROR id',
        'Total datasets'
    ] + basis_of_record
    values: dict = {}

    for publisher in publishers:
        publisher = publishers[publisher]

        # Append meta data
        values[publisher['gbif_id']] = [
            publisher['name'],
            publisher['gbif_id'],
            publisher['ror_id'],
            publisher['totals']['datasets']
        ]

        for bor in basis_of_record:
            values[publisher['gbif_id']].append(publisher['totals'][bor])

    # Write to publishers_total.csv
    csv_file = "csv_files/written/publishers.csv"

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(headers)

        for v in values.values():
            writer.writerow(v)

    return csv_file


def write_institutions_to_csv_issues_and_flags(publishers: dict):
    """ Prepares data from publishers dictionary and writes this to csv
        Data handled are: issues and flags (total)
        :param publishers: Dict of GBIF publishers from DiSSCo network and related data
        :return: Writes a csv
    """

    # Receiving issues and flags
    issues_and_flags_list = create_issues_and_flags_list()

    # Preparing basic csv
    headers = ['Publisher', 'Total'] + issues_and_flags_list
    values: dict = {}

    for publisher in publishers:
        publisher = publishers[publisher]

        # Inserting values
        values[publisher['gbif_id']] = [
            publisher['name']
        ]

        # Issues and flags
        publisher_issue_flag_total = 0

        for issue_flag in issues_and_flags_list:
            if publisher['issues_and_flags'].get(issue_flag):
                values[publisher['gbif_id']].append(publisher['issues_and_flags'][issue_flag]['total'])

                publisher_issue_flag_total += publisher['issues_and_flags'][issue_flag]['total']
            else:
                values[publisher['gbif_id']].append(0)

        values[publisher['gbif_id']].insert(1, publisher_issue_flag_total)

    # Write to publishers_issues_flags.csv
    csv_file = "csv_files/written/publishers_issues_flags.csv"

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(headers)

        for v in values.values():
            writer.writerow(v)

    return csv_file


# GeoCASe functions
def write_geocase_data_to_csv(geocase_data: dict):
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

    return csv_file


def write_geocase_publishers_to_csv(geocase_publishers: dict):
    # Preparing basic csv
    headers = ['Origin', 'Total']
    values: dict = {
        'total': ['Total']
    }

    # Appending headers and total values
    for total in geocase_publishers['total']:
        if not total == "specimens":
            headers.append(total)

        values['total'].append(geocase_publishers['total'][total])

    # Appending country values
    for country in geocase_publishers['providers']:
        values[country] = [country]
        values[country] += [v for v in geocase_publishers['providers'][country].values()]

    # Write to publishers_issues_flags.csv
    csv_file = "csv_files/written/geocase_publishers.csv"

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(headers)

        for v in values.values():
            writer.writerow(v)

    return csv_file
