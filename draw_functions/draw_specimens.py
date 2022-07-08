import plotly.graph_objects as go


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


def prepare_draw_specimens_bar_country(publishing_countries) -> list:
    plot_data: list = []
    x: list = []

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

    return plot_data


def prepare_draw_specimens_bar_organisation(publishers) -> list:
    plot_data: list = []
    x: list = []

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

    return plot_data


def prepare_draw_specimens_pie_country(publishing_countries) -> list:
    x: list = []

    # Setting x and y values
    for country in publishing_countries:
        y = []

        for bor in basis_of_record:
            x.append(bor)
            y.append(int(publishing_countries[country][bor]))

    return [x, y]


def prepare_draw_specimens_pie_organisation(publishers) -> list:
    x: list = []

    # Setting x and y values
    for publisher in publishers:
        y = []

        for bor in basis_of_record:
            x.append(bor)
            y.append(int(publishers[publisher][bor]))

    return [x, y]
