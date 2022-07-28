import plotly.utils
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import requests


import graphical_functions


app = Flask(__name__)
CORS(app, allow_headers=['Content-Type'])


@app.route('/graph', methods=['GET'])
def draw_graph():
    """ Receives the data from the view and decides which graph needs to be drawn
        Send data to the draw_functions_menu function for further execution
        :return: The graph in string form to be rendered in the Javascript
    """

    data = json.loads(request.args.get('data'))

    method = data['method']

    mode = ''
    if 'mode' in data:
        mode = data['mode']

    r = ''
    if 'request' in data:
        r = data['request']

    return_length = ''
    if 'return_length' in data:
        return_length = data['return_length']

    bar_type = ''
    if 'type' in data:
        bar_type = data['type']

    fig = draw_functions_menu(method, mode, r, return_length, bar_type)

    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return jsonify(graph_json)


def draw_functions_menu(method: str, mode: str, r: list, return_length: int, bar_type: str) -> list:
    """ Receives the prepared data from the draw_graph function
        Based upon the chosen method, calls on the defined function for preparing the graphical data
        :return: The graphical data
    """

    fig: list = []

    if method == 'draw_datasets':
        fig = graphical_functions.draw_datasets(mode, r)
    elif method == 'draw_specimens':
        fig = graphical_functions.draw_specimens(mode, r, bar_type)
    elif method == 'draw_specimens_progress':
        fig = graphical_functions.draw_specimens_progress(mode, r)
    elif method == 'draw_issues_and_flags':
        fig = graphical_functions.draw_issues_and_flags(mode, r, return_length)
    elif method == 'draw_infrastructures_total':
        fig = graphical_functions.draw_infrastructures_total()

    return fig


@app.route('/organisations', methods=['GET'])
def get_organisations():
    """ Retrieves the list of organisations from the database
        :return: The organisations list
    """

    response = requests.get('https://sandbox.dissco.tech/api/v1/organisation/tuples')

    return jsonify(response.json())


@app.route('/countries', methods=['GET'])
def get_countries():
    """ Creates the list of countries
        :return: The organisations list
    """

    response = requests.get('https://sandbox.dissco.tech/api/v1/organisation/countries')
    countries_list: dict = {}

    for r in response.json():
        countries_list[r['countryCode']] = r['country']

    return jsonify(countries_list)
