import os
from datetime import datetime

from flask import Flask, jsonify, request, make_response
from ptax_client import PTAXClient, exceptions


application = Flask(__name__)


@application.route('/')
def hello():
    return jsonify(todo='Documentation')


@application.route('/ptax_data')
def get_ptax_data():
    client = PTAXClient()
    parameters = ('start', 'end', 'currencies')

    if any(parameter not in request.args for parameter in parameters):
        return jsonify(
            message='Required parameters: '
            + ', '.join(parameters[:-1]) + ' and ' + parameters[-1]
        ), 400

    try:
        start_date = datetime.strptime(request.args.get('start'), '%d/%m/%Y')
        end_date = datetime.strptime(request.args.get('end'), '%d/%m/%Y')
        currencies = request.args.get('currencies').split(',')

        dfs = []

        for currency in currencies:
            df = client.get(start_date, end_date, currency)
            df.drop(labels='currency', axis=1, inplace=True)
            df.columns = [f'{col}_{currency}' for col in df.columns]

            dfs.append(df)

        result = dfs[0]

        for df in dfs[1:]:
            result = result.merge(
                right=df,
                left_index=True,
                right_index=True,
            )

        response = make_response(result.to_csv())
        response.headers["Content-Disposition"] = \
            "attachment; filename=export.csv"
        response.headers["Content-Type"] = "text/csv"

        return response
    except (
        exceptions.InvalidIntervalError,
        KeyError,
        ValueError
    ) as e:
        return jsonify(
            error_msg=e.args[0] if len(e.args) else e.__class__.__name__
        ), 400
    except:     # noqa
        return jsonify(
            error_msg='Unknown error. Please report this to this '
            'application\'s administrator.'
        ), 500


if __name__ == '__main__':
    application.run(
        host='0.0.0.0',
        port=8080,
        debug=os.environ.get('FLASK_DEBUG', True)
    )
