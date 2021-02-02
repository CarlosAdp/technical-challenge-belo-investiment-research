import os

from flask import Flask, jsonify


application = Flask(__name__)


@application.route('/')
def hello():
    return jsonify(message='Hi there')


if __name__ == '__main__':
    application.run(
        host='0.0.0.0',
        port=8080,
        debug=os.environ.get('FLASK_DEBUG', True)
    )
