import plotly.graph_objects as go
from datetime import datetime as dt


# Internal functions
import query_database
import draw_functions.draw_specimens as prep_draw_specimens
import draw_functions.draw_issues_flags_progress as prep_draw_issues_flags_progress
import draw_functions.draw_issues_flags as prep_draw_issues_flags
import draw_functions.draw_specimens_progress as prep_draw_specimens_progress


no_mode_message = 'No valid mode is selected'
current_month = dt.now().strftime('%B')

# SonarLint: define constant instead of literal
total_datasets_str = 'Total datasets'

colors = [
    '#cc0000',
    '#39ac39',
    '#e68a00',
    '#aa80ff',
    '#0099cc',
    '#e6e600',
    '#ffbf00',
    '#ffccff'
]


def draw_infrastructures_total() -> go:
    """ Calls on the data belonging to the relative infrastructures (GBIF and GeoCASe)
        Transforms the data to a usable format for Plotly
        :return: Draws a graph based on the amount of datasets
    """

    # Search for total GBIF datasets via
    publishing_countries = query_database.select_countries_data([])
    publishing_countries.pop('Total')

    # Count for total amount of datasets
    total_datasets = 0

    for country in publishing_countries:
        total_datasets += publishing_countries[country][total_datasets_str]

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=['Infrastructure', 'Count', 'Percent'],
                    fill_color='#205692',
                    font=dict(
                        size=13,
                        color='white'
                    )
                ),
                cells=dict(
                    values=[['GBIF', 'GeoCASe'], total_datasets, '100%'],
                    fill_color='#ffffff',
                    line_color='#d9d9d9',
                    font=dict(
                        size=12,
                        color='#333333'
                    ),
                    height=30
                )
            )
        ],
        layout=go.Layout(
            plot_bgcolor="#FFF",
            height=90,
            uniformtext_mode='hide',
            margin=go.layout.Margin(
                l=0,
                r=0,
                b=0,
                t=0
            )
        ))

    return fig


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
            y.append(int(publishing_countries[publisher][total_datasets_str]))
    elif mode == 'publisher':
        # Prepare publisher data
        publishers = query_database.select_organisations_data(request_list)
        publishers.pop('Total')

        for publisher in publishers:
            x.append(publishers[publisher]['organisation_name'])
            y.append(int(publishers[publisher][total_datasets_str]))
    else:
        print(no_mode_message)
        return False

    fig = go.Figure(
        data=[go.Bar(
            x=y,
            y=x,
            orientation='h',
            marker=dict(
                color=colors
            ),
            text=x,
            textposition='inside',
            insidetextanchor='start',
            width=0.5
        )],
        layout=go.Layout(
            plot_bgcolor="#FFF",
            bargap=0,
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

    # Check calling method
    if method == 'bar':
        # Check which mode is being called
        if mode == 'publishing_country':
            # Prepare publishing country data
            publishing_countries = query_database.select_countries_data(request_list)
            publishing_countries.pop('Total')

            # Preparing plot data
            plot_data = prep_draw_specimens.prepare_draw_specimens_bar_country(publishing_countries)
        elif mode == 'publisher':
            # Prepare publisher data
            publishers = query_database.select_organisations_data(request_list)
            publishers.pop('Total')

            plot_data = prep_draw_specimens.prepare_draw_specimens_bar_organisation(publishers)
        else:
            print(no_mode_message)
            return False

        fig = go.Figure(
            data=plot_data,
            layout=go.Layout(
                plot_bgcolor="#FFF",
                barmode='stack',
                showlegend=False,
                bargap=0.3,
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

            plot_data = prep_draw_specimens.prepare_draw_specimens_pie_country(publishing_countries)
        elif mode == 'publisher':
            # Prepare publisher data
            publishers = query_database.select_organisations_data(request_list)
            publishers.pop('Total')

            plot_data = prep_draw_specimens.prepare_draw_specimens_pie_organisation(publishers)
        else:
            print(no_mode_message)
            return False

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=plot_data[0],
                    values=plot_data[1],
                    textposition='inside',
                    marker=dict(
                        colors=colors
                    )
                )
            ],
            layout=go.Layout(
                plot_bgcolor="#FFF",
                uniformtext_mode='hide',
                showlegend=False,
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
    # Prepare quarter months
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

        plot_data = prep_draw_issues_flags_progress.prepare_draw_issues_flags_progress_country(quarter_months, country_code, issue_flag)
    elif mode == 'publisher':
        ror_id = request_list[0]

        plot_data = prep_draw_issues_flags_progress.prepare_draw_issues_flags_progress_organisation(quarter_months, ror_id, issue_flag)

    # Draw graph
    fig = go.Figure(
        data=[
            go.Scatter(
                x=plot_data[0],
                y=plot_data[1],
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

    # Check which mode is being called
    if mode == 'publishing_country' and len(request_list) == 1:
        publishing_countries = query_database.select_countries_data(request_list)
        publishing_countries.pop('Total')

        country_code = request_list[0]
        publishing_country = publishing_countries[country_code]

        # Remove total value
        del publishing_country['issues_and_flags']['total']

        plot_data = prep_draw_issues_flags.prepare_draw_issues_flags_countries(publishing_country, return_length)
    elif mode == 'publisher' and len(request_list) == 1:
        publishers = query_database.select_organisations_data(request_list)
        publishers.pop('Total')

        ror_id = request_list[0]
        publisher = publishers[ror_id]

        plot_data = prep_draw_issues_flags.prepare_draw_issues_flags_organisation(publisher, return_length)
    else:
        print(no_mode_message)
        return False

    # Setting sub graphs
    sub_graphs: list = []

    for issue_flag in plot_data[0]:
        sub_graphs.append(draw_issue_flag_progress(mode, request_list, issue_flag))

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=['No. ISSUE FLAGS', 'Count'],
                    fill_color='#205692',
                    font=dict(
                        size=13,
                        color='white'
                    )
                ),
                cells=dict(
                    values=[plot_data[0], plot_data[1]],
                    fill_color=[['white'],
                                ['#E74C3C' if int(val) > 5000 else '#F7A112' if int(val) > 2500 else '#ffdb4d' for val in plot_data[1]],
                                ['white']],
                    line_color='#d9d9d9',
                    font=dict(
                        size=12,
                        color='#333333'
                    ),
                    height=40
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

    # Check which mode is being called
    if mode == 'publishing_country':
        # Prepare publishing country data
        country_code = request_list[0]

        plot_data = prep_draw_specimens_progress.prepare_specimens_progress_country(country_code)
    elif mode == 'publisher':
        # Prepare publishing country data
        ror_id = request_list[0]

        plot_data = prep_draw_specimens_progress.prepare_specimens_progress_organisation(ror_id)
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
