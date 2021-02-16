import json

from flask import Flask, jsonify

from com.qaconsultants.classifyit.doc.api_specs import get_apispec
from com.qaconsultants.classifyit.doc.flask_swagger import SWAGGER_URL, swagger_ui_blueprint
from com.qaconsultants.classifyit.endpoints.classifyit_endpoint import blueprint_classifyit
from com.qaconsultants.classifyit.utils.common import load_clip_model

app = Flask(__name__)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(blueprint_classifyit)


@app.route('/swagger')
def create_swagger_spec():
    return json.dumps(get_apispec(app).to_dict())


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '404 Not Found'}), 404


@app.before_first_request
def load_model():
    load_clip_model(app)


if __name__ == '__main__':
    from waitress import serve

    serve(app, url_scheme='https', port=5000)
