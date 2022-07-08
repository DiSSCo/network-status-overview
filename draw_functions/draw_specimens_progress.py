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


def prepare_specimens_progress_country(country_code) -> list:
    x: list = []
    y: dict = {}
    plot_data: list = []

    # Setting x and y values, x = months, y = monthly numbers (out of stored csvs)
    for month in months:
        x.append(month)

        # Convert month name to number
        datetime_object = dt.strptime(month, "%B")
        month_number = datetime_object.month

        month_data = query_database.select_countries_data([country_code], month_number)
        month_data.pop('Total')

        # Check if month directory is empty
        for bor in basis_of_record:
            if bor not in y:
                y[bor] = []

            if country_code in month_data:
                y[bor].append(month_data[country_code][bor])
            else:
                y[bor].append(0)

    # Append to plot data
    for bor in basis_of_record:
        plot_data.append(
            go.Scatter(
                name=bor,
                x=x,
                y=y[bor]
            )
        )

    return plot_data


def prepare_specimens_progress_organisation(ror_id):
    x: list = []
    y: dict = {}
    plot_data: list = []

    # Setting x and y values, x = months, y = monthly numbers (out of stored csvs)
    for month in months:
        x.append(month)

        # Convert month name to number
        datetime_object = dt.strptime(month, "%B")
        month_number = datetime_object.month

        month_data = query_database.select_organisations_data([ror_id], month_number)
        month_data.pop('Total')

        # Check if month directory is empty
        for bor in basis_of_record:
            if bor not in y:
                y[bor] = []

            if ror_id in month_data:
                y[bor].append(month_data[ror_id][bor])
            else:
                y[bor].append(0)

    # Append to plot data
    for bor in basis_of_record:
        plot_data.append(
            go.Scatter(
                name=bor,
                x=x,
                y=y[bor]
            )
        )

    return plot_data
