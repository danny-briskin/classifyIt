from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields

DOCS_FILENAME = 'classifyIT.yaml'


class ErrorSchema(Schema):
    error = fields.Str(description="Error", required=True, example='An error was occurred')


class InputSchema(Schema):
    image_url = fields.Str(description="URL to existing image file",
                           required=True,
                           example='https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png')
    image_texts = fields.List(description="Possible descriptions of the image",
                              required=True,
                              cls_or_instance=fields.Str,
                              example=["a cow", "google", "a raccoon driving BMW"])


class TextProbability(Schema):
    probability = fields.Float(required=True,
                               description='Probability (from 0.0 to 1.0) that given text is a description of the image',
                               example=0.981261075957)
    text = fields.Str(required=True,
                      description='Input text, cut in the middle',
                      example='a raccoo<...>g BMW')


class OutputSchema(Schema):
    output = {"probability": 1.4406107595732465e-01,
              "text": "Candy Corn Dancin Tr <...> nimal With Motion 10"}
    result = fields.List(description="Results",
                         required=True,
                         example=output,
                         cls_or_instance=fields.Nested(TextProbability))


def load_docstrings(spec, app):
    """ API description load.

    :param spec: APISpec object
    :param app: Flask app
    """
    for fn_name in app.view_functions:
        if fn_name == 'static':
            continue
        print(f'Loading function description: {fn_name}')
        view_fn = app.view_functions[fn_name]
        spec.path(view=view_fn)


def get_apispec(app):
    """ Creation of APISpec

    :param app: Flask app
    """
    spec = APISpec(
        title="ClassifyIT",
        version="0.1.0",
        openapi_version="3.0.2",
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )

    spec.components.schema("Input", schema=InputSchema)
    spec.components.schema("Output", schema=OutputSchema)
    spec.components.schema("Error", schema=ErrorSchema)

    create_tags(spec)

    load_docstrings(spec, app)

    return spec


def create_tags(spec):
    """ Tags creation

    :param spec: APISpec object
    """
    tags = [{'name': 'classifyit', 'description': 'CLIP'}]

    for tag in tags:
        print(f"Adding tag: {tag['name']}")
        spec.tag(tag)


def write_yaml_file(spec: APISpec):
    """ Export APISpec to YAML file
    :param spec:  APISpec object
    """
    with open(DOCS_FILENAME, 'w') as file:
        file.write(spec.to_yaml())
    print(f'Saved into {DOCS_FILENAME}')
