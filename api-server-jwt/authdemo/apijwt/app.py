import requests
from flask import Flask, jsonify
from authlib.integrations.flask_oauth2 import ResourceProtector, current_token
from authlib.oauth2.rfc6750 import BearerTokenValidator
from authlib.integrations.sqla_oauth2 import OAuth2TokenMixin


class MyBearerTokenValidator(BearerTokenValidator):
    def authenticate_token(self, token_string):
        print('token_string: ' + token_string)

require_oauth = ResourceProtector()
require_oauth.register_token_validator(MyBearerTokenValidator())

app = Flask(__name__)


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")


@app.route('/')
@app.route('/<path>')
@require_oauth()
def handle(path):
    return jsonify({"path": '/' + (path or '')})
