import logging

from com.qaconsultants.classifyit.exceptions.error_exceptions import InvalidParameter, \
    MissingParameter, MethodUnsupported
from com.qaconsultants.classifyit.request_data import RequestData
from com.qaconsultants.classifyit.utils.common import process_post_request
from flask import current_app
from flask import request, jsonify, make_response, Blueprint

from com.qaconsultants.classifyit.utils.string_utilities import is_list_of_strings, is_valid_url

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

blueprint_classifyit = Blueprint(name="classifyit", import_name=__name__)


@blueprint_classifyit.route('/classifyit', methods=HTTP_METHODS)
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
          description: Image URL is not a valid URL or cannot be reached;
                        image texts is not a list of strings.
          content:
            application/json:
              schema: ErrorSchema
        '422':
          description: Image URL (image_url) or image texts list (image texts) parameter is missing
          content:
            application/json:
              schema: ErrorSchema
        '500':
          description: Internal server error
          content:
            application/json:
              schema: ErrorSchema
      tags:
        - classifyit
     """
    if request.method == 'POST':
        req = request.get_json()
        if req is None:
            logging.error('Request body is missing')
            raise MissingParameter('Request body')
        if req.get('image_url') is None:
            logging.error('Parameter image_url is missing')
            raise MissingParameter('image_url')
        if req.get('image_texts') is None:
            logging.error('Parameter image_texts is missing')
            raise MissingParameter('image_texts')
        image_texts = req['image_texts']
        if not is_list_of_strings(image_texts):
            logging.error("Parameter 'image_texts' is not a list of strings " + str(image_texts))
            raise InvalidParameter("Parameter 'image_texts' is not a list of strings")
        image_url = req['image_url']
        if not is_valid_url(image_url):
            logging.error('Given image_url [' + image_url + '] is not a valid URL')
            raise InvalidParameter('Given image_url [' + image_url + '] is not a valid URL')

        response = process_post_request(current_app, RequestData(image_url, image_texts))
        if response:
            return make_response(jsonify(response.body), response.status)
        else:
            return make_response(jsonify({"message": "An internal error has happened"}), 500)
    else:
        logging.warn('Method is unsupported:' + request.method)
        raise MethodUnsupported(request.method)
