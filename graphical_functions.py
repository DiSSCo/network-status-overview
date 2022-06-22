import plotly.graph_objects as go
import calendar
from datetime import datetime as dt


# Internal functions
import query_database


no_mode_message = 'No valid mode is selected'
current_month = dt.now().strftime('%B')

colors = [
    'red',
    'green',
    'blue',
    'yellow',
    'orange',
    'purple',
    'brown',
    'pink'
]


def draw_datasets(mode: str, request_list: list) -> go:
    """ Calls on the data belonging to the requested publishing countries / publishers
        Transforms the data to a usable format for Plotly
        :return: Draws a graph based on the amount of datasets
    """

    x: list = []
    y: list = []

    # Check which mode is being called
    if mode == 'publishing_country':
        # Prepare publishing country data
        publishing_countries = query_database.select_countries_data(request_list)
        publishing_countries.pop('Total')

        for publisher in publishing_countries:
            x.append(publisher)
            y.append(int(publishing_countries[publisher]['Total datasets']))
    elif mode == 'publisher':
        # Prepare publisher data
        publishers = query_database.select_organisations_data(request_list)
        publishers.pop('Total')

        for publisher in publishers:
            x.append(publishers[publisher]['organisation_name'])
            y.append(int(publishers[publisher]['Total datasets']))
    else:
        print(no_mode_message)
        return False

    fig = go.Figure(
        data=[go.Bar(
            x=y,
            y=x,
            orientation='h',
            marker=dict(
                color='#33cc33'
            ),
            text=x,
            textposition='inside',
            insidetextanchor='start'
        )],
        layout=go.Layout(
            plot_bgcolor="#FFF",
            bargap=0.6,
            xaxis={
                'fixedrange': True
            },
            yaxis={
                'fixedrange': True,
                'showticklabels': False
            },
            margin=go.layout.Margin(
                l=0,
                r=0,
                b=0,
                t=0
            )
        )
    )

    return fig


def draw_specimens(mode: str, request_list: list, method: str) -> go:
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

    # Check calling method
    if method == 'bar':
        # Check which mode is being called
        if mode == 'publishing_country':
            # Prepare publishing country data
            publishing_countries = query_database.select_countries_data(request_list)
            publishing_countries.pop('Total')

            # Setting x and y values
            for country in publishing_countries:
                y = []
                i = 0

                for bor in basis_of_record:
                    x.append(bor)
                    y.append(int(publishing_countries[country][bor]))

                    plot_data.append(
                        go.Bar(
                            name=country,
                            x=[int(publishing_countries[country][bor])],
                            y=[country],
                            orientation='h',
                            marker=dict(
                                color=colors[i]
                            ),
                            text=bor,
                            textposition='inside',
                            insidetextanchor='start'
                        )
                    )

                    i += 1
        elif mode == 'publisher':
            # Prepare publisher data
            publishers = query_database.select_organisations_data(request_list)
            publishers.pop('Total')

            # Setting x and y values
            for publisher in publishers:
                y = []
                i = 0

                for bor in basis_of_record:
                    x.append(bor)
                    y.append(int(publishers[publisher][bor]))

                    plot_data.append(
                        go.Bar(
                            name=publishers[publisher]['organisation_name'],
                            x=[int(publishers[publisher][bor])],
                            y=[publishers[publisher]['organisation_name']],
                            orientation='h',
                            marker=dict(
                                color=colors[i]
                            ),
                            text=bor,
                            textposition='inside',
                            insidetextanchor='start'
                        )
                    )

                    i += 1
        else:
            print(no_mode_message)
            return False

        fig = go.Figure(
            data=plot_data,
            layout=go.Layout(
                plot_bgcolor="#FFF",
                barmode='stack',
                showlegend=False,
                bargap=0.6,
                xaxis={
                    'fixedrange': True,
                    # 'showticklabels': False
                },
                yaxis={
                    'fixedrange': True,
                    # 'showticklabels': False
                },
                margin=go.layout.Margin(
                    l=0,
                    r=0,
                    b=0,
                    t=0
                )
            )
        )

        return fig
    elif method == 'pie':
        # Check which mode is being called
        if mode == 'publishing_country':
            # Prepare publishing country data
            publishing_countries = query_database.select_countries_data(request_list)
            publishing_countries.pop('Total')

            # Setting x and y values
            for country in publishing_countries:
                y = []

                for bor in basis_of_record:
                    x.append(bor)
                    y.append(int(publishing_countries[country][bor]))
        elif mode == 'publisher':
            # Prepare publisher data
            publishers = query_database.select_organisations_data(request_list)
            publishers.pop('Total')

            # Setting x and y values
            for publisher in publishers:
                y = []

                for bor in basis_of_record:
                    x.append(bor)
                    y.append(int(publishers[publisher][bor]))
        else:
            print(no_mode_message)
            return False

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=x,
                    values=y,
                    textposition='inside',
                    marker=dict(
                        colors=colors
                    )
                )
            ],
            layout=go.Layout(
                plot_bgcolor="#FFF",
                uniformtext_mode='hide',
                margin=go.layout.Margin(
                    l=0,
                    r=0,
                    b=0,
                    t=0
                )
            )
        )

        return fig


def draw_issue_flag_progress(mode: str, request_list, issue_flag):
    x: list = []
    y: list = []

    # Prepare quarter months
    months = list(calendar.month_name)[1:]
    quarter_months: list = []
    check_month = dt.now().month
    counter = 0

    for _ in range(0, 4):
        if (check_month - counter) > 0:
            quarter_months.insert(0, check_month - counter)
        else:
            counter = 0
            check_month = 12
            quarter_months.insert(0, (check_month - counter))

        counter += 1

    # Check which mode is being called
    if mode == 'publishing_country':
        # Prepare graph data
        country_code = request_list[0]

        for month in quarter_months:
            x.append(months[month - 1])
            month_data = query_database.select_countries_data([country_code], month)

            if country_code in month_data:
                # Read csv from month and set values
                y.append(month_data[country_code]['issues_and_flags'][issue_flag]['total'])
            else:
                # Set values to zero
                y.append(0)

    elif mode == 'publisher':
        ror_id = request_list[0]

        for month in quarter_months:
            x.append(months[month - 1])
            month_data = query_database.select_organisations_data([ror_id], month)

            if ror_id in month_data:
                # Read csv from month and set values
                y.append(month_data[ror_id]['issues_and_flags'][issue_flag]['total'])
            else:
                # Set values to zero
                y.append(0)

    # Draw graph
    fig = go.Figure(
        data=[
            go.Scatter(
                x=x,
                y=y,
                orientation='h',
            )
        ],
        layout=go.Layout(
            plot_bgcolor="#FFF",
            autosize=False,
            width=200,
            height=40,
            xaxis={
                'fixedrange': True,
                'showticklabels': False
            },
            yaxis={
                'fixedrange': True,
                'showticklabels': False,
                'color': '#333333'
            },
            margin=go.layout.Margin(
                l=0,
                r=0,
                b=0,
                t=0
            )
        )
    )

    return fig


# Currently, for a single publishing country or publisher
# Takes top 10 of the highest issues and flags and draws graph
def draw_issues_and_flags(mode: str, request_list: list, return_length: int) -> go:
    """ Calls on the data belonging to the requested publishing countries / publishers
        Transforms the data to a usable format for Plotly
        :return: Draws a graph based on the amount of issues and flags
    """

    x: list = []
    y: list = []

    # Check which mode is being called
    if mode == 'publishing_country' and len(request_list) == 1:
        publishing_countries = query_database.select_countries_data(request_list)
        publishing_countries.pop('Total')

        country_code = request_list[0]
        publishing_country = publishing_countries[country_code]

        # Remove total value
        del publishing_country['issues_and_flags']['total']

        # Set y values
        y_values: dict = {}

        for issue_flag in publishing_country['issues_and_flags']:
            # Check if issue flag number is high enough
            if len(y_values) < return_length:
                y_values[issue_flag] = int(
                    publishing_country['issues_and_flags'][issue_flag]['total'])
            else:
                # Check if some value in y is lower, if true remove and add new one
                difference = {}

                for value in y_values:
                    if y_values[value] < int(publishing_country['issues_and_flags'][issue_flag]['total']):
                        difference[value] = int(
                            y_values[value]) - int(publishing_country['issues_and_flags'][issue_flag]['total'])

                # Check if any issue or flag is greater than existing value
                if len(difference) != 0:
                    smallest = 0
                    smallest_issue_flag = ''

                    for value in difference:
                        if smallest == 0 or smallest > difference[value]:
                            smallest = difference[value]
                            smallest_issue_flag = value

                    del y_values[smallest_issue_flag]
                    y_values[issue_flag] = int(
                        publishing_country['issues_and_flags'][issue_flag]['total'])

        # Refactoring y values to list and setting x values
        for issue_flag in y_values:
            x.append(issue_flag)
            y.append(y_values[issue_flag])

    elif mode == 'publisher' and len(request_list) == 1:
        publishers = query_database.select_organisations_data(request_list)
        publishers.pop('Total')

        ror_id = request_list[0]
        publisher = publishers[ror_id]

        # Set y values
        y_values = {}

        for issue_flag in publisher['issues_and_flags']:
            # Check if issue flag number is high enough
            if len(y_values) < return_length:
                y_values[issue_flag] = int(
                    publisher['issues_and_flags'][issue_flag]['total'])
            else:
                # Check if some value in y is lower, if true remove and add new one
                difference = {}

                for value in y_values:
                    if y_values[value] < int(publisher['issues_and_flags'][issue_flag]['total']):
                        difference[value] = int(y_values[value]) - int(
                            publisher['issues_and_flags'][issue_flag]['total'])

                # Check if any issue or flag is greater than existing value
                if len(difference) != 0:
                    smallest = 0
                    smallest_issue_flag = ''

                    for value in difference:
                        if smallest == 0 or smallest > difference[value]:
                            smallest = difference[value]
                            smallest_issue_flag = value

                    del y_values[smallest_issue_flag]
                    y_values[issue_flag] = int(
                        publisher['issues_and_flags'][issue_flag]['total'])

        # Refactoring y values to list and setting x values
        for issue_flag in y_values:
            x.append(issue_flag)
            y.append(y_values[issue_flag])
    else:
        print(no_mode_message)
        return False

    # Setting sub graphs
    sub_graphs: list = []

    for issue_flag in x:
        sub_graphs.append(draw_issue_flag_progress(mode, request_list, issue_flag))

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=['No ISSUE FLAGS', 'Count']
                ),
                cells=dict(
                    values=[x, y],
                    fill_color=[['white'],
                                ['red' if int(val) > 5000 else 'orange' if int(val) > 2500 else 'yellow' for val in y],
                                ['white']]
                )
            )
        ],
        layout=go.Layout(
            plot_bgcolor="#FFF",
            uniformtext_mode='hide',
            margin=go.layout.Margin(
                l=0,
                r=0,
                b=0,
                t=0
            )
        ))

    return {'fig': fig, 'sub_graphs': sub_graphs}


# Currently, for a single publishing country or publisher
def draw_specimens_progress(mode: str, request_list: list) -> go:
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

        # Setting x and y values, x = months, y = monthly numbers (out of stored csvs)
        for month in months:
            x.append(month)

            # Convert month name to number
            datetime_object = dt.strptime(month, "%B")
            month_number = datetime_object.month

            print(country_code)

            month_data = query_database.select_countries_data([country_code], month_number)
            month_data.pop('Total')

            # Check if month directory is empty
            if country_code in month_data:
                # Read csv from month and set values
                for bor in basis_of_record:
                    if y.get(bor):
                        y[bor].append(int(month_data[country_code][bor]))
                    else:
                        y[bor] = [int(month_data[country_code][bor])]
            else:
                # Set values to zero
                for bor in basis_of_record:
                    if y.get(bor):
                        y[bor].append(0)
                    else:
                        y[bor] = [0]

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

        # Setting x and y values, x = months, y = monthly numbers (out of stored csvs)
        for month in months:
            x.append(month)

            # Convert month name to number
            datetime_object = dt.strptime(month, "%B")
            month_number = datetime_object.month

            month_data = query_database.select_organisations_data([ror_id], month_number)
            month_data.pop('Total')

            # Check if month directory is empty
            if ror_id in month_data:
                for bor in basis_of_record:
                    if y.get(bor):
                        y[bor].append(int(month_data[ror_id][bor]))
                    else:
                        y[bor] = [int(month_data[ror_id][bor])]
            else:
                # Set values to zero
                for bor in basis_of_record:
                    if y.get(bor):
                        y[bor].append(0)
                    else:
                        y[bor] = [0]

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
            plot_bgcolor="#FFF",
            xaxis={
                'fixedrange': True
            },
            yaxis={
                'fixedrange': True,
                'color': '#333333'
            },
            margin=go.layout.Margin(
                l=0,
                r=0,
                b=0,
                t=0
            )
        )
    )

    return fig


# Currently, for a single publishing country or publisher
# def draw_issues_and_flags_progress(mode: str, request_list: list, return_length=10) -> go:
#     """ Calls on the data belonging to the requested publishing countries / publishers
#         Transforms the data to a usable format for Plotly
#         :return: Draws a graph based on the amount of issues and flags per month
#     """
#
#     x: list = []
#     y: dict = {}
#     plot_data: list = []
#
#     months = list(calendar.month_name)[1:]
#     issues_and_flags_list = query_csv.create_issues_and_flags_list()
#     hottest_issues_and_flags: list
#
#     # Check which mode is being called
#     if mode == 'publishing_country':
#         # Prepare publishing country data
#         publishing_countries = query_csv.request_publishing_country(
#             request_list)
#         country_code = request_list[0]
#         publishing_country = publishing_countries[country_code]
#
#         # Prepare graph
#         graph_title = f'Progress of hottest issues and flags of: {country_code}'
#
#         hottest_issues_and_flags = []
#
#         for issue_flag in issues_and_flags_list:
#             if len(hottest_issues_and_flags) < return_length:
#                 hottest_issues_and_flags.append(issue_flag)
#             else:
#                 # Check if current issue flag value is higher than one in the hottest list
#                 difference: dict = {}
#
#                 # Replace the smallest issue flag value with current issue flag
#                 for hot_issue_flag in hottest_issues_and_flags:
#                     if int(publishing_country['issues_and_flags'][issue_flag]) > int(
#                             publishing_country['issues_and_flags'][hot_issue_flag]):
#                         difference[hot_issue_flag] = int(publishing_country['issues_and_flags'][hot_issue_flag]) - \
#                                                      int(publishing_country['issues_and_flags']
#                                                          [issue_flag])
#
#                 # Check if any issue or flag is greater than existing value
#                 if len(difference) != 0:
#                     smallest = 0
#                     smallest_issue_flag = ''
#
#                     for value in difference:
#                         if smallest == 0 or smallest > difference[value]:
#                             smallest = difference[value]
#                             smallest_issue_flag = value
#
#                     hottest_issues_and_flags.remove(smallest_issue_flag)
#                     hottest_issues_and_flags.append(issue_flag)
#
#         # Setting x and y values, x = months, y = monthly numbers (out of stored csvs)
#         for month in months:
#             x.append(month)
#
#             # Check if month directory is empty
#             if len(os.listdir(f'csv_files/storage/{month}')) == 0:
#                 # Set values to zero
#                 for hot_issue_flag in hottest_issues_and_flags:
#                     if y.get(hot_issue_flag):
#                         y[hot_issue_flag].append(0)
#                     else:
#                         y[hot_issue_flag] = [0]
#             else:
#                 # Read csv from month and set values
#                 month_data = query_csv.request_publishing_country(
#                     [country_code], month)
#
#                 for hot_issue_flag in hottest_issues_and_flags:
#                     if y.get(hot_issue_flag):
#                         y[hot_issue_flag].append(
#                             int(month_data[country_code]['issues_and_flags'][hot_issue_flag]))
#                     else:
#                         y[hot_issue_flag] = [
#                             int(month_data[country_code]['issues_and_flags'][hot_issue_flag])]
#
#         # Append to plot data
#         for hot_issue_flag in hottest_issues_and_flags:
#             plot_data.append(
#                 go.Scatter(
#                     name=hot_issue_flag,
#                     x=x,
#                     y=y[hot_issue_flag]
#                 )
#             )
#     elif mode == 'publisher':
#         # Prepare publisher data
#         publishers = query_csv.request_publishers(request_list)
#         ror_id = request_list[0]
#         publisher = publishers[ror_id]
#
#         # Prepare graph
#         graph_title = f'Progress of hottest issues and flags of: {publisher["Publisher"]}'
#
#         hottest_issues_and_flags = []
#
#         for issue_flag in issues_and_flags_list:
#             if len(hottest_issues_and_flags) < return_length:
#                 hottest_issues_and_flags.append(issue_flag)
#             else:
#                 # Check if current issue flag value is higher than one in the hottest list
#                 difference = {}
#
#                 # Replace the smallest issue flag value with current issue flag
#                 for hot_issue_flag in hottest_issues_and_flags:
#                     if int(publisher['issues_and_flags'][issue_flag]) > int(
#                             publisher['issues_and_flags'][hot_issue_flag]):
#                         difference[hot_issue_flag] = int(publisher['issues_and_flags'][hot_issue_flag]) - \
#                                                      int(publisher['issues_and_flags'][issue_flag])
#
#                 # Check if any issue or flag is greater than existing value
#                 if len(difference) != 0:
#                     smallest = 0
#                     smallest_issue_flag = ''
#
#                     for value in difference:
#                         if smallest == 0 or smallest > difference[value]:
#                             smallest = difference[value]
#                             smallest_issue_flag = value
#
#                     hottest_issues_and_flags.remove(smallest_issue_flag)
#                     hottest_issues_and_flags.append(issue_flag)
#
#         # Setting x and y values, x = months, y = monthly numbers (out of stored csvs)
#         for month in months:
#             x.append(month)
#
#             # Check if month directory is empty
#             if len(os.listdir(f'csv_files/storage/{month}')) == 0:
#                 # Set values to zero
#                 for hot_issue_flag in hottest_issues_and_flags:
#                     if y.get(hot_issue_flag):
#                         y[hot_issue_flag].append(0)
#                     else:
#                         y[hot_issue_flag] = [0]
#             else:
#                 # Read csv from month and set values
#                 month_data = query_csv.request_publishers(
#                     [publisher['ROR id']], month)
#
#                 for hot_issue_flag in hottest_issues_and_flags:
#                     if y.get(hot_issue_flag):
#                         y[hot_issue_flag].append(
#                             int(month_data[publisher['ROR id']]['issues_and_flags'][hot_issue_flag]))
#                     else:
#                         y[hot_issue_flag] = [
#                             int(month_data[publisher['ROR id']]['issues_and_flags'][hot_issue_flag])]
#
#         # Append to plot data
#         for hot_issue_flag in hottest_issues_and_flags:
#             plot_data.append(
#                 go.Scatter(
#                     name=hot_issue_flag,
#                     x=x,
#                     y=y[hot_issue_flag]
#                 )
#             )
#     else:
#         print(no_mode_message)
#         return False
#
#     # Draw graph
#     fig = go.Figure(
#         data=plot_data,
#         layout=go.Layout(
#             title=go.layout.Title(text=graph_title)
#         )
#     )
#
#     # fig.show()
#     return fig.to_image(format="png")
