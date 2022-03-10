from flask import Flask, jsonify, request
from authlib.integrations.flask_oauth2 import ResourceProtector, current_token
from authlib.oauth2.rfc7662 import IntrospectTokenValidator
import requests


class MyIntrospectTokenValidator(IntrospectTokenValidator):
    def introspect_token(self, token_string):
        url = 'http://keycloak:8080/auth/realms/demo/protocol/openid-connect/token/introspect'
        data = {'token': token_string, 'token_type_hint': 'access_token'}
        auth = ('demo', 'm8CKzuCSXVvelweUrKzzRQIFuglZat51')
        resp = requests.post(url, data=data, auth=auth)
        resp.raise_for_status()
        return resp.json()


require_oauth = ResourceProtector()
require_oauth.register_token_validator(MyIntrospectTokenValidator())


app = Flask(__name__)


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")


@app.route('/')
@app.route('/<path>')
@require_oauth()
def handle(path):
    return jsonify({
        "path": '/' + (path or ''),
        'headers': request.headers,
        'token': current_token
    })
