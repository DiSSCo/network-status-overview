from datetime import datetime as dt
import calendar as calendar

# Internal functions
import query_database
import api.draw_functions.draw_specimens as prep_draw_specimens
import api.draw_functions.draw_issues_flags_progress as prep_draw_issues_flags_progress
import api.draw_functions.draw_issues_flags as prep_draw_issues_flags
import api.draw_functions.draw_specimens_progress as prep_draw_specimens_progress


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


def draw_infrastructures_total() -> list:
    """ Calls on the data belonging to the relative infrastructures (GBIF and GeoCASe)
        Transforms the data to a usable format for Plotly
        :return: Draws a graph based on the amount of datasets
    """

    # Search for total GBIF datasets via
    publishing_countries = query_database.select_countries_data([])
    publishing_countries.pop('Total')

    print(publishing_countries)

    # Count for total amount of datasets
    total_datasets = 0

    for country in publishing_countries:
        total_datasets += publishing_countries[country][total_datasets_str]

    graph_data = [{
        'type': 'table',
        'header': {
            'values': ['Infrastructure', 'Total count', 'Percent'],
            'fill': {
                'color': '#205692'
            },
            'font': {
                'size': 13,
                'color': 'white'
            }
        },
        'cells': {
            'values': [['GBIF', 'GeoCASe'], total_datasets, '100%'],
            'fill': {
                'color': '#ffffff'
            },
            'line': {
                'color': '#d9d9d9',
            },
            'font': {
                'size': 12,
                'color': '#333333'
            },
            'height': 30
        }
    }]

    graph_layout = {
        'plot_bgcolor': "#FFF",
        'height': 90,
        'uniformtext_mode': 'hide',
        'margin': {
            'l': 0,
            'r': 0,
            'b': 0,
            't': 0
        }
    }

    return [graph_data, graph_layout]


def draw_datasets(mode: str, request_list: list) -> list:
    """ Calls on the data belonging to the requested publishing countries / publishers
        Transforms the data to a usable format for Plotly
        :return: Returns a set-up for a graph based on the amount of datasets
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
        return []

    graph_data = [{
        'x': y,
        'y': x,
        'type': 'bar',
        'orientation': 'h',
        'marker': {
            'color': colors
        },
        'text': x,
        'textposition': 'inside',
        'insidetextanchor': 'start',
        'width': 0.5
    }]
    graph_layout = {
        'plot_bgcolor': "#FFF",
        'xaxis': {
            'fixedrange': True
        },
        'yaxis': {
            'fixedrange': True,
            'showticklabels': False
        },
        'margin': {
            'l': 0,
            'r': 0,
            'b': 0,
            't': 0
        }
    }

    return [graph_data, graph_layout]


def draw_specimens(mode: str, request_list: list, method: str) -> list:
    """ Calls on the data belonging to the requested publishing countries / publishers
        Transforms the data to a usable format for Plotly
        :return: Draws a graph based on the amount of specimens
    """

    graph_data: list = []
    graph_layout: dict = {}

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
            return []

        graph_data = plot_data

        graph_layout = {
            'plot_bgcolor': "#FFF",
            'barmode': 'stack',
            'showlegend': False,
            'bargap': 0.3,
            'hovermode': False,
            'xaxis': {
                'fixedrange': True,
                # 'showticklabels': False
            },
            'yaxis': {
                'fixedrange': True,
                # 'showticklabels': False
            },
            'margin': {
                'l': 0,
                'r': 0,
                'b': 0,
                't': 0
            }
        }

        return [graph_data, graph_layout]
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
            return []

        graph_data = [{
            'values': plot_data[1],
            'labels': plot_data[0],
            'type': 'pie',
            'textposition': 'inside',
            'marker': {
                'colors': colors
            }
        }]

        graph_layout = {
            'plot_bgcolor': "#FFF",
            'uniformtext_mode': 'hide',
            'showlegend': False,
            'margin': {
                'l': 0,
                'r': 0,
                'b': 0,
                't': 0
            }
        }

    return [graph_data, graph_layout]


def draw_issue_flag_progress(mode: str, monthly_progress) -> list:
    # Prepare quarter months
    quarter_months: list = []
    check_month = dt.now().month
    counter = 0

    for _ in range(0, 4):
        if (check_month - counter) > 0:
            quarter_months.insert(0, calendar.month_name[(check_month - counter)])
        else:
            counter = 0
            check_month = 12
            quarter_months.insert(0, calendar.month_name[(check_month - counter)])

        counter += 1

    # Check which mode is being called
    if mode == 'publishing_country':
        # Prepare graph data
        plot_data = prep_draw_issues_flags_progress.prepare_draw_issues_flags_progress_country(quarter_months,
                                                                                               monthly_progress)
    elif mode == 'publisher':
        # Prepare graph data
        plot_data = prep_draw_issues_flags_progress.prepare_draw_issues_flags_progress_organisation(quarter_months,
                                                                                                    monthly_progress)
    # Set graph data
    graph_data = [{
        'x': plot_data[0],
        'y': plot_data[1],
        'mode': 'line',
        'text': quarter_months,
        'type': 'scatter'
    }]
    graph_layout = {
        'plot_bgcolor': "#FFF",
        'autosize': False,
        'width': 250,
        'height': 40,
        'xaxis': {
            'fixedrange': True,
            'showticklabels': False
        },
        'yaxis': {
            'fixedrange': True,
            'showticklabels': False,
            'color': '#333333'
        },
        'margin': {
            'l': 0,
            'r': 0,
            'b': 0,
            't': 0
        }
    }

    return [graph_data, graph_layout]


# Currently, for a single publishing country or publisher
# Takes top 10 of the highest issues and flags and draws graph
def draw_issues_and_flags(mode: str, request_list: list, return_length: int) -> list:
    """ Calls on the data belonging to the requested publishing countries / publishers
        Transforms the data to a usable format for Plotly
        :return: Draws a graph based on the amount of issues and flags
    """

    sub_graphs: list = []

    # Check which mode is being called
    if mode == 'publishing_country' and len(request_list) == 1:
        publishing_countries = query_database.select_countries_data(request_list)
        publishing_countries.pop('Total')

        country_code = request_list[0]
        publishing_country = publishing_countries[country_code]

        # Remove total value
        del publishing_country['issues_and_flags']['total']

        plot_data = prep_draw_issues_flags.prepare_draw_issues_flags_countries(publishing_country, return_length)

        # Setting sub graphs
        for issue_flag in plot_data[0]:
            sub_graphs.append(
                draw_issue_flag_progress(mode, publishing_countries[country_code]['issues_and_flags'][issue_flag]))
    elif mode == 'publisher' and len(request_list) == 1:
        publishers = query_database.select_organisations_data(request_list)
        publishers.pop('Total')

        ror_id = request_list[0]
        publisher = publishers[ror_id]

        plot_data = prep_draw_issues_flags.prepare_draw_issues_flags_organisation(publisher, return_length)

        # Setting sub graphs
        for issue_flag in plot_data[0]:
            sub_graphs.append(
                draw_issue_flag_progress(mode, publishers[ror_id]['issues_and_flags'][issue_flag]))
    else:
        print(no_mode_message)
        return []

    graph_data = [{
        'type': 'table',
        'header': {
            'values': ['Issue Flag', 'Total count'],
            'fill': {
                'color': '#205692'
            },
            'font': {
                'size': 13,
                'color': 'white'
            }
        },
        'cells': {
            'values': [plot_data[0], plot_data[2]],
            'fill': {
                'color': [['white'],
                          ['#E74C3C' if int(val) > 5000 else '#F7A112' if int(val) > 2500 else '#ffdb4d' for val
                           in plot_data[1]],
                          ['white']]
            },
            'line': {
                'color': '#d9d9d9'
            },
            'font': {
                'size': 12,
                'color': '#333333'
            },
            'height': 40
        }
    }]

    graph_layout = {
        'plot_bgcolor': "#FFF",
        'uniformtext_mode': 'hide',
        'margin': {
            'l': 0,
            'r': 0,
            'b': 0,
            't': 0
        }
    }

    return [graph_data, graph_layout, sub_graphs]


# Currently, for a single publishing country or publisher
def draw_specimens_progress(mode: str, request_list: list) -> list:
    """ Calls on the data belonging to the requested publishing countries / publishers
        Transforms the data to a usable format for Plotly
        :return: Draws a graph based on the amount of specimens per basis of record per month
    """

    months = list(calendar.month_name)[1:]

    # Check which mode is being called
    if mode == 'publishing_country':
        # Prepare publishing country data
        country_code = request_list[0]

        country_data = query_database.select_countries_data([country_code], months)
        country_data.pop('Total')

        plot_data = prep_draw_specimens_progress.prepare_specimens_progress_country(country_data)
    elif mode == 'publisher':
        # Prepare publishing country data
        ror_id = request_list[0]

        organisation_data = query_database.select_organisations_data([ror_id], months)
        organisation_data.pop('Total')

        plot_data = prep_draw_specimens_progress.prepare_specimens_progress_organisation(organisation_data)
    else:
        print(no_mode_message)
        return []

    graph_data: list = []

    for bor in plot_data[1]:
        graph_data.append({
            'x': plot_data[0],
            'y': plot_data[1][bor],
            'type': 'scatter',
            'mode': 'lines',
            'name': bor
        })

    graph_layout = {
        'plot_bgcolor': "#FFF",
        'xaxis': {
            'fixedrange': True,
        },
        'yaxis': {
            'fixedrange': True,
            'visible': False,
            # 'color': '#333333'
        },
        'margin': {
            'l': 6,
            'r': 0,
            'b': 20,
            't': 0
        }
    }

    return [graph_data, graph_layout]
