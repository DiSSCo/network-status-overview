import plotly.graph_objects as go
import calendar
import os
from datetime import datetime as dt

# Internal functions
import query_csv


no_mode_message = 'No valid mode is selected'
current_month = dt.now().strftime('%B')


def draw_datasets(mode: str, request_list: list):
    """ Calls on the data belonging to the requested publishing countries / publishers
        Transforms the data to a usable format for Plotly
        :return: Draws a graph based on the amount of datasets
    """

    x: list = []
    y: list = []

    # Check which mode is being called
    if mode == 'publishing_country':
        # Prepare publishing country data
        publishing_countries = query_csv.request_publishing_country(request_list)
        graph_title = 'Number of datasets per DiSSCo publishing country'

        for country in publishing_countries:
            x.append(country)
            y.append(int(publishing_countries[country]['Total datasets']))
    elif mode == 'publisher':
        # Prepare publisher data
        publishers = query_csv.request_publishers(request_list)
        graph_title = 'Number of datasets per DiSSCo publisher'

        for publisher in publishers:
            x.append(publishers[publisher]['Publisher'])
            y.append(int(publishers[publisher]['Total datasets']))
    else:
        print(no_mode_message)
        return False

    fig = go.Figure(
        data=[go.Bar(
            x=x,
            y=y
        )],
        layout=go.Layout(
            title=go.layout.Title(text=graph_title)
        )
    )

    fig.show()


def draw_specimens(mode: str, request_list: list):
    """ Calls on the data belonging to the requested publishing countries / publishers
        Transforms the data to a usable format for Plotly
        :return: Draws a graph based on the amount of specimens
    """

    x: list = []
    y: list
    plot_data: list = []

    basis_of_record = [
        'PRESERVED_SPECIMEN',
        'FOSSIL_SPECIMEN',
        'LIVING_SPECIMEN',
        'MATERIAL_SAMPLE',
        'METEORITE',
        'MINERAL',
        'ROCK',
        'OTHER_GEOLOGICAL'
    ]

    # Check which mode is being called
    if mode == 'publishing_country':
        # Prepare publishing country data
        publishing_countries = query_csv.request_publishing_country(request_list)

        # Prepare graph
        graph_title = 'Number of specimens per DiSSCo publishing country'

        # Setting x and y values
        for country in publishing_countries:
            y = []

            for bor in basis_of_record:
                x.append(bor)
                y.append(int(publishing_countries[country][bor]))

            plot_data.append(
                go.Bar(
                    name=country,
                    x=x,
                    y=y
                )
            )
    elif mode == 'publisher':
        # Prepare publisher data
        publishers = query_csv.request_publishers(request_list)

        # Prepare graph
        graph_title = 'Number of datasets per DiSSCo publisher'

        # Setting x and y values
        for publisher in publishers:
            y = []

            for bor in basis_of_record:
                x.append(bor)
                y.append(int(publishers[publisher][bor]))

            plot_data.append(
                go.Bar(
                    name=publishers[publisher]['Publisher'],
                    x=x,
                    y=y
                )
            )
    else:
        print(no_mode_message)
        return False

    fig = go.Figure(
        data=plot_data,
        layout=go.Layout(
            title=go.layout.Title(text=graph_title)
        )
    )

    fig.show()


# Currently, for a single publishing country or publisher
# Takes top 10 of the highest issues and flags and draws graph
def draw_issues_and_flags(mode: str, request_list: list):
    """ Calls on the data belonging to the requested publishing countries / publishers
        Transforms the data to a usable format for Plotly
        :return: Draws a graph based on the amount of issues and flags
    """

    x: list = []
    y: list = []

    # Check which mode is being called
    if mode == 'publishing_country' and len(request_list) == 1:
        publishing_countries = query_csv.request_publishing_country(request_list)
        country_code = request_list[0]
        publishing_country = publishing_countries[country_code]

        # Remove total value
        del publishing_country['issues_and_flags']['Total']

        # Preparing graph
        graph_title = f'Number of issues and flags for: {country_code}'

        # Set y values
        y_values: dict = {}

        for issue_flag in publishing_country['issues_and_flags']:
            # Check if issue flag number is high enough
            if len(y_values) < 10:
                y_values[issue_flag] = int(publishing_country['issues_and_flags'][issue_flag])
            else:
                # Check if some value in y is lower, if true remove and add new one
                i = 0
                difference = {}

                for value in y_values:
                    if y_values[value] < int(publishing_country['issues_and_flags'][issue_flag]):
                        difference[value] = int(y_values[value]) - int(publishing_country['issues_and_flags'][issue_flag])

                # Check if any issue or flag is greater than existing value
                if len(difference) != 0:
                    smallest = 0
                    smallest_issue_flag = ''

                    for value in difference:
                        if smallest == 0 or smallest > difference[value]:
                            smallest = difference[value]
                            smallest_issue_flag = value

                    del y_values[smallest_issue_flag]
                    y_values[issue_flag] = int(publishing_country['issues_and_flags'][issue_flag])

        # Refactoring y values to list and setting x values
        for issue_flag in y_values:
            x.append(issue_flag)
            y.append(y_values[issue_flag])

    elif mode == 'publisher' and len(request_list) == 1:
        publishers = query_csv.request_publishers(request_list)
        ror_id = request_list[0]
        publisher = publishers[ror_id]

        # Remove total value
        del publisher['issues_and_flags']['Total']

        # Preparing graph
        graph_title = f'Number of issues and flags for: {publisher["Publisher"]}'

        # Set y values
        y_values = {}

        for issue_flag in publisher['issues_and_flags']:
            # Check if issue flag number is high enough
            if len(y_values) < 10:
                y_values[issue_flag] = int(publisher['issues_and_flags'][issue_flag])
            else:
                # Check if some value in y is lower, if true remove and add new one
                i = 0
                difference = {}

                for value in y_values:
                    if y_values[value] < int(publisher['issues_and_flags'][issue_flag]):
                        difference[value] = int(y_values[value]) - int(
                            publisher['issues_and_flags'][issue_flag])

                # Check if any issue or flag is greater than existing value
                if len(difference) != 0:
                    smallest = 0
                    smallest_issue_flag = ''

                    for value in difference:
                        if smallest == 0 or smallest > difference[value]:
                            smallest = difference[value]
                            smallest_issue_flag = value

                    del y_values[smallest_issue_flag]
                    y_values[issue_flag] = int(publisher['issues_and_flags'][issue_flag])

        # Refactoring y values to list and setting x values
        for issue_flag in y_values:
            x.append(issue_flag)
            y.append(y_values[issue_flag])
    else:
        print(no_mode_message)
        return False

    fig = go.Figure(
        data=[go.Bar(
            x=x,
            y=y
        )],
        layout=go.Layout(
            title=go.layout.Title(text=graph_title)
        )
    )

    fig.show()


# Currently, for a single publishing country or publisher
def draw_specimens_progress(mode: str, request_list: list):
    """ Calls on the data belonging to the requested publishing countries / publishers
        Transforms the data to a usable format for Plotly
        :return: Draws a graph based on the amount of specimens per basis of record per month
    """

    x: list = []
    y: dict = {}
    plot_data: list = []

    basis_of_record = [
        'PRESERVED_SPECIMEN',
        'FOSSIL_SPECIMEN',
        'LIVING_SPECIMEN',
        'MATERIAL_SAMPLE',
        'METEORITE',
        'MINERAL',
        'ROCK',
        'OTHER_GEOLOGICAL'
    ]
    months = list(calendar.month_name)[1:]

    # Check which mode is being called
    if mode == 'publishing_country':
        # Prepare publishing country data
        country_code = request_list[0]

        # Prepare graph
        graph_title = f'Progress of digitised specimens of: {country_code}'

        # Setting x and y values, x = months, y = monthly numbers (out of stored csvs)
        for month in months:
            x.append(month)

            # Check if month directory is empty
            if len(os.listdir(f'csv_files/storage/{month}')) == 0:
                # Set values to zero
                for bor in basis_of_record:
                    if y.get(bor):
                        y[bor].append(0)
                    else:
                        y[bor] = [0]
            else:
                # Read csv from month and set values
                month_data = query_csv.request_publishing_country([country_code], month)

                for bor in basis_of_record:
                    if y.get(bor):
                        y[bor].append(int(month_data[country_code][bor]))
                    else:
                        y[bor] = [int(month_data[country_code][bor])]

        # Append to plot data
        for bor in basis_of_record:
            plot_data.append(
                go.Scatter(
                    name=bor,
                    x=x,
                    y=y[bor]
                )
            )

    elif mode == 'publisher':
        # Prepare publishing country data
        ror_id = request_list[0]
        publishers = query_csv.request_publishers([ror_id])

        # Prepare graph
        graph_title = f'Progress of digitised specimens of: {publishers[ror_id]["Publisher"]}'

        # Setting x and y values, x = months, y = monthly numbers (out of stored csvs)
        for month in months:
            x.append(month)

            # Check if month directory is empty
            if len(os.listdir(f'csv_files/storage/{month}')) == 0:
                # Set values to zero
                for bor in basis_of_record:
                    if y.get(bor):
                        y[bor].append(0)
                    else:
                        y[bor] = [0]
            else:
                # Read csv from month and set values
                month_data = query_csv.request_publishers([ror_id], month)

                for bor in basis_of_record:
                    if y.get(bor):
                        y[bor].append(int(month_data[ror_id][bor]))
                    else:
                        y[bor] = [int(month_data[ror_id][bor])]

        # Append to plot data
        for bor in basis_of_record:
            plot_data.append(
                go.Scatter(
                    name=bor,
                    x=x,
                    y=y[bor]
                )
            )
    else:
        print(no_mode_message)
        return False

    # Draw graph
    fig = go.Figure(
        data=plot_data,
        layout=go.Layout(
            title=go.layout.Title(text=graph_title)
        )
    )

    fig.show()


# Currently, for a single publishing country or publisher
def draw_issues_and_flags_progress(mode: str, request_list: list):
    """ Calls on the data belonging to the requested publishing countries / publishers
        Transforms the data to a usable format for Plotly
        :return: Draws a graph based on the amount of issues and flags per month
    """

    x: list = []
    y: dict = {}
    plot_data: list = []

    months = list(calendar.month_name)[1:]
    issues_and_flags_list = query_csv.create_issues_and_flags_list()
    hottest_issues_and_flags: list

    # Check which mode is being called
    if mode == 'publishing_country':
        # Prepare publishing country data
        publishing_countries = query_csv.request_publishing_country(request_list)
        country_code = request_list[0]
        publishing_country = publishing_countries[country_code]

        # Prepare graph
        graph_title = f'Progress of hottest issues and flags of: {country_code}'

        hottest_issues_and_flags = []

        for issue_flag in issues_and_flags_list:
            if len(hottest_issues_and_flags) < 10:
                hottest_issues_and_flags.append(issue_flag)
            else:
                # Check if current issue flag value is higher than one in the hottest list
                difference: dict = {}

                # Replace the smallest issue flag value with current issue flag
                for hot_issue_flag in hottest_issues_and_flags:
                    if int(publishing_country['issues_and_flags'][issue_flag]) > int(publishing_country['issues_and_flags'][hot_issue_flag]):
                        difference[hot_issue_flag] = int(publishing_country['issues_and_flags'][hot_issue_flag]) - \
                            int(publishing_country['issues_and_flags'][issue_flag])

                # Check if any issue or flag is greater than existing value
                if len(difference) != 0:
                    smallest = 0
                    smallest_issue_flag = ''

                    for value in difference:
                        if smallest == 0 or smallest > difference[value]:
                            smallest = difference[value]
                            smallest_issue_flag = value

                    hottest_issues_and_flags.remove(smallest_issue_flag)
                    hottest_issues_and_flags.append(issue_flag)

        # Setting x and y values, x = months, y = monthly numbers (out of stored csvs)
        for month in months:
            x.append(month)

            # Check if month directory is empty
            if len(os.listdir(f'csv_files/storage/{month}')) == 0:
                # Set values to zero
                for hot_issue_flag in hottest_issues_and_flags:
                    if y.get(hot_issue_flag):
                        y[hot_issue_flag].append(0)
                    else:
                        y[hot_issue_flag] = [0]
            else:
                # Read csv from month and set values
                month_data = query_csv.request_publishing_country([country_code], month)

                for hot_issue_flag in hottest_issues_and_flags:
                    if y.get(hot_issue_flag):
                        y[hot_issue_flag].append(int(month_data[country_code]['issues_and_flags'][hot_issue_flag]))
                    else:
                        y[hot_issue_flag] = [int(month_data[country_code]['issues_and_flags'][hot_issue_flag])]

        # Append to plot data
        for hot_issue_flag in hottest_issues_and_flags:
            plot_data.append(
                go.Scatter(
                    name=hot_issue_flag,
                    x=x,
                    y=y[hot_issue_flag]
                )
            )
    elif mode == 'publisher':
        # Prepare publisher data
        publishers = query_csv.request_publishers(request_list)
        ror_id = request_list[0]
        publisher = publishers[ror_id]

        # Prepare graph
        graph_title = f'Progress of hottest issues and flags of: {publisher["Publisher"]}'

        hottest_issues_and_flags = []

        for issue_flag in issues_and_flags_list:
            if len(hottest_issues_and_flags) < 10:
                hottest_issues_and_flags.append(issue_flag)
            else:
                # Check if current issue flag value is higher than one in the hottest list
                difference = {}

                # Replace the smallest issue flag value with current issue flag
                for hot_issue_flag in hottest_issues_and_flags:
                    if int(publisher['issues_and_flags'][issue_flag]) > int(
                            publisher['issues_and_flags'][hot_issue_flag]):
                        difference[hot_issue_flag] = int(publisher['issues_and_flags'][hot_issue_flag]) - \
                                                     int(publisher['issues_and_flags'][issue_flag])

                # Check if any issue or flag is greater than existing value
                if len(difference) != 0:
                    smallest = 0
                    smallest_issue_flag = ''

                    for value in difference:
                        if smallest == 0 or smallest > difference[value]:
                            smallest = difference[value]
                            smallest_issue_flag = value

                    hottest_issues_and_flags.remove(smallest_issue_flag)
                    hottest_issues_and_flags.append(issue_flag)

        # Setting x and y values, x = months, y = monthly numbers (out of stored csvs)
        for month in months:
            x.append(month)

            # Check if month directory is empty
            if len(os.listdir(f'csv_files/storage/{month}')) == 0:
                # Set values to zero
                for hot_issue_flag in hottest_issues_and_flags:
                    if y.get(hot_issue_flag):
                        y[hot_issue_flag].append(0)
                    else:
                        y[hot_issue_flag] = [0]
            else:
                # Read csv from month and set values
                month_data = query_csv.request_publishers([publisher['ROR id']], month)

                for hot_issue_flag in hottest_issues_and_flags:
                    if y.get(hot_issue_flag):
                        y[hot_issue_flag].append(int(month_data[publisher['ROR id']]['issues_and_flags'][hot_issue_flag]))
                    else:
                        y[hot_issue_flag] = [int(month_data[publisher['ROR id']]['issues_and_flags'][hot_issue_flag])]

        # Append to plot data
        for hot_issue_flag in hottest_issues_and_flags:
            plot_data.append(
                go.Scatter(
                    name=hot_issue_flag,
                    x=x,
                    y=y[hot_issue_flag]
                )
            )
    else:
        print(no_mode_message)
        return False

    # Draw graph
    fig = go.Figure(
        data=plot_data,
        layout=go.Layout(
            title=go.layout.Title(text=graph_title)
        )
    )

    fig.show()
