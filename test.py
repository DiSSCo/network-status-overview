import csv
import main


# Possible list for indexing issues and flags
# Needs to be extracted from GBIF instead of hard coded
issues_and_flags_list = [
    'Institution match fuzzy',
    'Collection match none',
    'Geodetic datum assumed WGS84',
    'Coordinate rounded',
    'Taxon match higherrank',
    'Recorded date invalid',
    'Country derived from coordinates',
    'Institution match none',
    'Institution collection mismatch',
    'Collection match fuzzy',
    'Taxon match none',
    'Taxon match fuzzy',
    'Country invalid',
    'Country coordinate mismatch',
    'Ambiguous institution',
    'Type status invalid',
    'Multimedia URI invalid',
    'Geodetic datum invalid',
    'Presumed negated longitude',
    'Presumed swapped coordinate',
    'Recorded date unlikely',
    'Presumed negated latitude',
    'Zero coordinate',
    'Coordinate uncertainty metres invalid',
    'Elevation non numeric',
    'Elevation min/max swapped',
    'Coordinate out of range',
    'Basis of record invalid',
    'Identified date unlikely',
    'Coordinate reprojected',
    'Coordinate precision invalid',
    'Occurrence status inferred from individual count',
    'Occurrence status unparsable',
    'Individual count invalid',
    'Coordinate invalid',
    'Continent invalid',
    'Depth min/max swapped',
    'Multimedia date invalid',
    'Country mismatch',
    'Occurrence status inferred from basis of record',
    'Individual count conflicts with occurrence status',
    'Depth unlikely',
    'Recorded date mismatch',
    'Modified date unlikely',
    'Elevation not metric',
    'Different owner institution',
    'Footprint SRS invalid',
    'Coordinate reprojection failed',
    'Footprint WKT invalid'
]


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


# Call on functions
# write_datasets_to_csv(main.gather_datasets())
# write_specimens_to_csv(main.gather_specimens())
# write_issues_and_flags_to_csv(main.gather_issues_flags())
