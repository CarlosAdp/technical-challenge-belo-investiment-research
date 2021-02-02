import os
from datetime import datetime

from flask import Flask, jsonify, request, make_response
from ptax_client import PTAXClient


application = Flask(__name__)


@application.route('/')
def hello():
    return jsonify(todo='Documentation')


@application.route('/ptax_data')
def get_ptax_data():
    c = PTAXClient()
    parameters = ('start', 'end', 'currency')

    if any(parameter not in request.args for parameter in parameters):
        return jsonify(
            message='Required parameters: '
            + ', '.join(parameters[:-1]) + ' and ' + parameters[-1]
        )

    data_frame = c.get(
        start_date=datetime.strptime(request.args.get('start'), '%d/%m/%Y'),
        end_date=datetime.strptime(request.args.get('end'), '%d/%m/%Y'),
        currency=request.args.get('currency')
    )

    response = make_response(data_frame.to_csv())
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    response.headers["Content-Type"] = "text/csv"

    return response


if __name__ == '__main__':
    application.run(
        host='0.0.0.0',
        port=8080,
        debug=os.environ.get('FLASK_DEBUG', True)
    )
