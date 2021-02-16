from com.qaconsultants.classifyit.request_data import RequestData
from com.qaconsultants.classifyit.utils.common import process_post_request
from flask import current_app, json
from flask import request, jsonify, make_response, Blueprint

blueprint_classifyit = Blueprint(name="classifyit", import_name=__name__)


@blueprint_classifyit.route('/classifyit', methods=['GET'])
def classifyit_get():
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


@blueprint_classifyit.route('/classifyit', methods=['POST'])
def classifyit_post():
    """
    ---
    post:
      summary: Image and text classifier
      requestBody:
        content:
            application/json:
                schema: InputSchema
      responses:
        '200':
          description: Result of classification
          content:
            application/json:
              schema: OutputSchema
        '400':
          description: No image URL or image texts
          content:
            application/json:
              schema: ErrorSchema
      tags:
        - classifyit
     """
    if request.method == 'POST':
        req = request.get_json()
        if req.get('image_url') is None:
            return current_app.response_class(response=json.dumps(
                {'error': 'There was no "image_url" parameter'}),
                status=400, mimetype='application/json')
        if req.get('image_texts') is None:
            return current_app.response_class(response=json.dumps(
                {'error': 'There was no "image_texts" parameter'}),
                status=400, mimetype='application/json')
        response_body = process_post_request(current_app,
                                             RequestData(req['image_url'], req['image_texts']))
        if response_body and response_body != '':
            return make_response(jsonify(response_body), 200)
        else:
            return make_response(jsonify({"message": "Sorry"}), 500)
