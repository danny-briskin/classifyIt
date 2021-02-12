from flask import Flask, request, jsonify, make_response
from com.qaconsultants.classifyit.request_data import RequestData
from com.qaconsultants.classifyit.utils.common import process_post_request, load_clip_model

app = Flask(__name__)


@app.route('/classifyit', methods=['GET', 'POST'])
def text():
    if request.method == 'GET':
        str = [{'usage': 'Please use the next request to get the values you are looking for'},
               {'request': 'POST /classifyit HTTP/1.1 '
                           + 'Host: 127.0.0.1:5000 '
                           + 'Content-Type: application/json '},
               {'body': "{ 'image_url' : 'your-url/image.jpg', "
                        + " 'image_texts' : ["
                        + "'text1', 'text2', 'text3', 'text4']"},
               {'response body': "[{ 'probability' : 0.0101, 'text':'text2' } ,"
                                 + "{ 'probability' : 0.2101, 'text':'text1' } ,"
                                 + " { 'probability' : 0.0011, 'text':'text3' } ,"
                                 + "{ 'probability' : 0.6202, 'text':'text3' } "
                                 + " ]"}]
        return jsonify(str)
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
    from waitress import serve
    serve(app, url_scheme='https', port=5000)
