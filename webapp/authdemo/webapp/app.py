from flask import Flask, jsonify, escape, request
from authlib.integrations.flask_oauth2 import ResourceProtector, current_token
from authlib.oauth2.rfc7662 import IntrospectTokenValidator
import requests
import logging


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
app.logger.setLevel(logging.INFO)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")


@app.route('/')
@app.route("/<path:subpath>")
@require_oauth()
def handle(subpath = None):
    app.logger.info(f'type of current_token ... {type(current_token).__module__} . {type(current_token).__name__}')
    app.logger.info(f'type of request.headers ... {type(request.headers).__module__} . {type(request.headers).__name__}')

    return jsonify({
        "path": f'/{escape(subpath or "")}',
        'header': dict(request.headers),
        'token': dict(current_token)
    })
