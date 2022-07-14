from datetime import datetime as dt
import calendar


# List of used specimen types
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
# List the months of the year
months = list(calendar.month_name)[1:]


def prepare_specimens_progress_country(country_data: dict) -> list:
    """ Sub function for drawing the specimens progress country graph
        Function prepares the graphical data and sets the x and y values
        :return: Returns the graphical values
    """

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


def prepare_specimens_progress_organisation(organisation_data: dict):
    """ Sub function for drawing the specimens progress organisation graph
        Function prepares the graphical data and sets the x and y values
        :return: Returns the graphical values
    """

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
