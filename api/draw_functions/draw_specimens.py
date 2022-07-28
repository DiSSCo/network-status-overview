import sys
sys.path.append("../constants.py")
import constants


colors = constants.colors
basis_of_record = constants.basis_of_record


def prepare_draw_specimens_bar_country(publishing_countries: dict) -> list:
    """ Sub function for drawing the specimens country bar graph
        Function prepares the graphical data and sets the x and y values
        :return: Returns the graphical values
    """

    x: list = []
    y: dict = {}

    # Setting x and y values
    for country in publishing_countries:
        x.append(country)

        for bor in basis_of_record:
            if bor not in y:
                y[bor] = []

            y[bor].append(int(publishing_countries[country][bor]))

    # Set bar stacks
    plot_data = []
    i = 0

    for bor in basis_of_record:
        plot_data.append({
            'x': y[bor],
            'y': x,
            'type': 'bar',
            'orientation': 'h',
            'marker': {
                'color': colors[i]
            },
            'text': bor,
            'textposition': 'inside',
            'insidetextanchor': 'start',
            'hovertemplate': f"<b>{y[bor]}</b><extra></extra>"
        })

        i += 1

    return plot_data


def prepare_draw_specimens_bar_organisation(publishers: dict) -> list:
    """ Sub function for drawing the specimens organisation bar graph
        Function prepares the graphical data and sets the x and y values
        :return: Returns the graphical values
    """

    y: dict = {}
    x: list = []

    # Setting x and y values
    for publisher in publishers:
        x.append(publisher)

        for bor in basis_of_record:
            if bor not in y:
                y[bor] = []

            y[bor].append(int(publishers[publisher][bor]))

    # Set bar stacks
    plot_data = []
    i = 0

    for bor in basis_of_record:
        plot_data.append({
            'x': y[bor],
            'y': x,
            'type': 'bar',
            'orientation': 'h',
            'marker': {
                'color': colors[i]
            },
            'text': bor,
            'textposition': 'inside',
            'insidetextanchor': 'start',
            'hovertemplate': f"<b>{y[bor]}</b><extra>"
        })

        i += 1

    return plot_data


def prepare_draw_specimens_pie_country(publishing_countries: dict) -> list:
    """ Sub function for drawing the specimens country pie graph
        Function prepares the graphical data and sets the x and y values
        :return: Returns the graphical values
    """

    x: list = []
    y: list = []

    # Setting x and y values
    for country in publishing_countries:
        y = []

        for bor in basis_of_record:
            x.append(bor)
            y.append(int(publishing_countries[country][bor]))

    return [x, y]


def prepare_draw_specimens_pie_organisation(publishers: dict) -> list:
    """ Sub function for drawing the specimens organisation pie graph
        Function prepares the graphical data and sets the x and y values
        :return: Returns the graphical values
    """

    x: list = []
    y: list = []

    # Setting x and y values
    for publisher in publishers:
        y = []

        for bor in basis_of_record:
            x.append(bor)
            y.append(int(publishers[publisher][bor]))

    return [x, y]
