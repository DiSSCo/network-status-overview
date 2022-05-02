import plotly.graph_objects as go
import GBIF_functions


def draw_gbif_datasets_country(gbif_datasets: dict):
    fig = go.Figure(
        data=[go.Bar(
            x=[country for country in gbif_datasets['countries'].keys()],
            y=[value for value in gbif_datasets['countries'].values()]
        )],
        layout=go.Layout(
            title=go.layout.Title(text="Number of datasets per DiSSCo Country")
        )
    )

    fig.show()


def draw_gbif_datasets_institution(gbif_publishers: dict):
    basis_of_record = ['PRESERVED_SPECIMEN', 'FOSSIL_SPECIMEN', 'LIVING_SPECIMEN', 'MATERIAL_SAMPLE']

    # Prepare X and Y lists
    x: list = []
    y: dict = {}

    # Setting x and y values
    for publisher in gbif_publishers:
        x.append(gbif_publishers[publisher]['name'])

        for bor in basis_of_record:
            if y.get(bor):
                y[bor].append(gbif_publishers[publisher]['totals'][bor])
            else:
                y[bor] = [gbif_publishers[publisher]['totals'][bor]]

    # Preparing graph
    plot_data = []

    for bor in basis_of_record:
        plot_data.append(
            go.Bar(
                name=bor,
                x=x,
                y=y[bor]
            )
        )

    # Draw graph
    fig = go.Figure(
        data=plot_data,
        layout=go.Layout(
            title=go.layout.Title(text="Number of specimens per DiSSCo country")
        )
    )

    fig.show()


def draw_gbif_specimens(gbif_specimens: dict):
    basis_of_record = ['PRESERVED_SPECIMEN', 'FOSSIL_SPECIMEN', 'LIVING_SPECIMEN', 'MATERIAL_SAMPLE']

    # Prepare X and Y lists
    x: list = []
    y: dict = {}

    # Setting x and y values
    for country in gbif_specimens['countries']:
        x.append(country)

        for bor in basis_of_record:
            if y.get(bor):
                y[bor].append(gbif_specimens['countries'][country][bor])
            else:
                y[bor] = [gbif_specimens['countries'][country][bor]]

    # Preparing graph
    plot_data = []

    for bor in basis_of_record:
        plot_data.append(
            go.Bar(
                name=bor,
                x=x,
                y=y[bor]
            )
        )

    # Draw graph
    fig = go.Figure(
        data=plot_data,
        layout=go.Layout(
            title=go.layout.Title(text="Number of specimens per DiSSCo country")
        )
    )

    fig.show()


draw_gbif_datasets_institution(GBIF_functions.gather_institutions())
