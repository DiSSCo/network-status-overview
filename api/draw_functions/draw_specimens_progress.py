import query_database
from datetime import datetime as dt
import calendar
import plotly.graph_objects as go

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


def prepare_specimens_progress_country(country_data) -> list:
    x: list = []
    y: dict = {}

    country = country_data[list(country_data.keys())[0]]

    # Setting x and y values, x = months, y = monthly numbers
    for month in months:
        if month in country:
            x.append(dt.strptime(month, '%B').strftime('%b'))

            for bor in basis_of_record:
                if bor not in y:
                    y[bor] = []

                y[bor].append(country[month][bor])

    plot_data = [x, y]

    return plot_data


def prepare_specimens_progress_organisation(organisation_data):
    x: list = []
    y: dict = {}

    organisation = organisation_data[list(organisation_data.keys())[0]]

    # Setting x and y values, x = months, y = monthly numbers
    for month in months:
        if month in organisation:
            x.append(dt.strptime(month, '%B').strftime('%b'))

            for bor in basis_of_record:
                if bor not in y:
                    y[bor] = []

                y[bor].append(organisation[month][bor])

    plot_data = [x, y]

    return plot_data
