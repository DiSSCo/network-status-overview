import plotly.utils
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
# import requests

import graphical_functions

app = Flask(__name__)
CORS(app)


@app.route('/get_graph', methods=['POST', 'GET'])
def draw_graph():
    if request.method == 'POST':
        data = request.get_json()

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


def draw_functions_menu(method, mode, r, return_length, bar_type) -> list:
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


@app.route('/get_organisations', methods=['GET'])
def get_organisations():
    # response = requests.get('https://sandbox.dissco.tech/api/v1/organisation/tuples')

    organisations_list = [
        {
            'ror': '01tv5y993',
            'name': 'Natural History Museum Vienna'
        },
        {
            'ror': '0443cwa12',
            'name': 'Tallinn University of Technology'
        },
        {
            'ror': '052d1a351',
            'name': 'Museum für Naturkunde'
        }
    ]

    # return jsonify(response.json())
    return jsonify(organisations_list)


@app.route('/get_countries', methods=['GET'])
def get_countries():
    # List needs to be created from valid source
    countries_list = {'AT': 'Austria',
                      'BE': 'Belgium',
                      'BG': 'Bulgaria',
                      'CZ': 'Czech Republic',
                      'DK': 'Denmark',
                      'EE': 'Estonia',
                      'FI': 'Finland',
                      'FR': 'France',
                      'DE': 'Germany',
                      'EL': 'Greece',
                      'HU': 'Hungary',
                      'IT': 'Italy',
                      'LU': 'Luxembourg',
                      'NL': 'Netherlands',
                      'NO': 'Norway',
                      'PL': 'Poland',
                      'PT': 'Portugal',
                      'SK': 'Slovakia',
                      'ES': 'Spain',
                      'SE': 'Sweden',
                      'GB': 'United Kingdom'}

    return jsonify(countries_list)


if __name__ == '__main__':
    app.run()
