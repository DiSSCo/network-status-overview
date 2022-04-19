import csv
import main


def create_issues_and_flags_list() -> list:
    """ Takes the csv containing the names of all issues and converts it to a list
        :return: Returns the issues and flags list
    """

    issues_file = 'csv_files/GBIF_issues.csv'
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
    csv_file = 'csv_files/datasets.csv'

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerows([headers, values])


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
    csv_file = 'csv_files/specimens.csv'

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(headers)

        for v in values.values():
            writer.writerow(v)


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
    csv_file = 'csv_files/issues_and_flags.csv'

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(headers)

        for v in values.values():
            writer.writerow(v)


def write_issues_and_flags_monthly(issues_and_flags: dict):
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
    csv_file = 'csv_files/issues_and_flags_monthly.csv'

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(headers)

        for v in values.values():
            writer.writerow(v)


# Call on functions
# write_datasets_to_csv(main.gather_datasets())
# write_specimens_to_csv(main.gather_specimens())
# write_issues_and_flags_to_csv(main.gather_issues_flags())
write_issues_and_flags_monthly(main.gather_issues_flags())
