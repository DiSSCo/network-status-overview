import plotly.graph_objects as go

# Internal functions
import query_csv


def draw_datasets(mode: str, request_list: list):
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
        print('No valid mode is selected')
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
        print('No valid mode is selected')
        return False

    fig = go.Figure(
        data=plot_data,
        layout=go.Layout(
            title=go.layout.Title(text=graph_title)
        )
    )

    fig.show()


# Currently, single publishing country or publisher
# Takes top 10 of the highest issues and flags and draws graph
def draw_issues_and_flags(mode: str, request: list):
    x: list = []
    y: list = []

    # Check which mode is being called
    if mode == 'publishing_country' and len(request) == 1:
        publishing_countries = query_csv.request_publishing_country(request)
        country_code = request[0]
        publishing_country = publishing_countries[country_code]

        # Remove total value
        del publishing_country['issues_and_flags']['Total']

        # Preparing graph
        graph_title = f'Number of issues and flags for: {country_code}'

        # Set x and y values
        for issue_flag in publishing_country['issues_and_flags']:
            # Check if issue flag number is high enough
            if len(y) < 10:
                y.append(int(publishing_country['issues_and_flags'][issue_flag]))
                x.append(issue_flag)
            else:
                # Check if some value in y is lower, if true remove and add new one
                i = 0

                for value in y:
                    if value < int(publishing_country['issues_and_flags'][issue_flag]):
                        # Remove value from x and y
                        del y[i]
                        del x[i]

                        # Add new value
                        y.append(int(publishing_country['issues_and_flags'][issue_flag]))
                        x.append(issue_flag)

                        break

                    i += 1

    elif mode == 'publisher' and len(request) == 1:
        publishers = query_csv.request_publishers(request)
        ror_id = request[0]
        publisher = publishers[ror_id]

        # Remove total value
        del publisher['issues_and_flags']['Total']

        # Preparing graph
        graph_title = f'Number of issues and flags for: {publisher["Publisher"]}'

        # Set x and y values
        for issue_flag in publisher['issues_and_flags']:
            # Check if issue flag number is high enough
            if len(y) < 10:
                y.append(int(publisher['issues_and_flags'][issue_flag]))
                x.append(issue_flag)
            else:
                # Check if some value in y is lower, if true remove and add new one
                i = 0

                for value in y:
                    if value < int(publisher['issues_and_flags'][issue_flag]):
                        # Remove value from x and y
                        del y[i]
                        del x[i]

                        # Add new value
                        y.append(int(publisher['issues_and_flags'][issue_flag]))
                        x.append(issue_flag)

                        break

                    i += 1
    else:
        print('No valid mode is selected')

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


# countries = ['NL']
# draw_issues_and_flags('publishing_country', countries)

# ror_ids = ['052d1a351']
# draw_issues_and_flags('publisher', ror_ids)

