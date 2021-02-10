from flask import Flask, request, jsonify, make_response
from com.qaconsultants.classifyit.request_data import RequestData
from com.qaconsultants.classifyit.utils.common import process_post_request, load_clip_model

app = Flask(__name__)


@app.route('/classifyit', methods=['GET', 'POST'])
def text():
    if request.method == 'GET':
        return jsonify({'message': 'Hello world!'})
    if request.method == 'POST':
        req = request.get_json()
        response_body = process_post_request(app, RequestData(req['image_url'], req['image_texts']))
        if response_body and response_body != '':
            return make_response(jsonify(response_body), 200)
        else:
            return make_response(jsonify({"message": "Sorry"}), 500)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '404 Not Found'}), 404


@app.before_first_request
def load_model():
    load_clip_model(app)


if __name__ == '__main__':
    app.run(debug=True)
