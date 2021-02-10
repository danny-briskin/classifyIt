import os
from logging.config import dictConfig

import typing
from flask import Flask

from com.qaconsultants.classifyit.clip_processing.clip_image_text_processor import \
    ClipImageTextProcessor
from com.qaconsultants.classifyit.request_data import RequestData
from com.qaconsultants.classifyit.utils.file_utilities import find_images_in_folder, clean_folder
from com.qaconsultants.classifyit.utils.images_utilities import download_image

global clip_image_text_processor, dummy_categories

dummy_categories = [
    "Orange boy is riding a blue horse and talking to a squirrel",
    "President of the Moon has banned meat from restaurant menu",
    "Seahorses don't like when racoons are eating schnitzel on bone",
    "A cowboy is passing through prairie",
    "An abstract picture with something big"]

BASE_DIR = os.path.dirname(os.getcwd() + '/flaskProject')

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


def get_list_of_images() -> list:
    # find all downloaded images
    _list_of_images = find_images_in_folder(BASE_DIR + '/tmpImagesFolder/', '*.webp')
    _list_of_images.extend(find_images_in_folder(BASE_DIR + '/tmpImagesFolder/', '*.png'))
    _list_of_images.extend(find_images_in_folder(BASE_DIR + '/tmpImagesFolder/', '*.jpg'))
    _list_of_images.extend(find_images_in_folder(BASE_DIR + '/tmpImagesFolder/', '*.jpeg'))
    return _list_of_images


def process(app: Flask, initial_categories_list: typing.List[str]):
    list_of_images = get_list_of_images()

    app.logger.info('%s', 'Searching for text on page....')
    app.logger.info('%s', 'Prepare text.....' + ' found ' + str(
        len(initial_categories_list)) + ' texts')
    initial_categories_list = add_dummy_categories(initial_categories_list)

    clip_image_text_processor.format_texts(initial_categories_list, 45)
    # format_categories(initial_categories_list, 45)

    app.logger.info('%s', 'Starting to classify.....')
    for file_image in list_of_images:
        file_image_str = str(file_image)
        app.logger.info('%s', ' Classifying image file [file://' + file_image_str + ']')

        clip_image_text_processor.image_holder.set_image(file_image_str)

        clip_image_text_processor.calculate_probabilities()
        preprocessed_probabilities = clip_image_text_processor \
            .preprocess_probabilities(clip_image_text_processor.image_holder.probabilities)
        print_probabilities(app, initial_categories_list, preprocessed_probabilities)
        clip_image_text_processor.reset_split_categories_numbers()
        return json_probabilities(app, initial_categories_list, preprocessed_probabilities)


def print_probabilities(app: Flask, initial_texts_list: typing.List[str],
                        preprocessed_probabilities: typing.List[
                            typing.Tuple[int, float]]) -> None:
    """
    Prints probability per initial text
    :param app:
    :param preprocessed_probabilities: preprocessed_probabilities [(1,0.34),(2,0.78)]
    :param initial_texts_list: initial texts
    """
    for index in range(len(preprocessed_probabilities)):
        log_str = "{:<26}".format(
            initial_texts_list[index][:40].replace("\n", "") + ' <...> '
            + initial_texts_list[index][-20:].replace("\n", "")) + " : " + "{:.2%}" \
                      .format(preprocessed_probabilities[index][1])
        app.logger.info('%s', log_str)


def json_probabilities(app: Flask, initial_texts_list: typing.List[str],
                       preprocessed_probabilities: typing.List[
                           typing.Tuple[int, float]]):
    """
    Prints probability per initial text
    :param app:
    :param preprocessed_probabilities: preprocessed_probabilities [(1,0.34),(2,0.78)]
    :param initial_texts_list: initial texts
    """
    global dummy_categories

    json_list = {}
    for index in range(len(preprocessed_probabilities)):
        if initial_texts_list[index] not in dummy_categories:
            json_list[
                initial_texts_list[index][:40].replace("\n", "") + ' <...> '
                + initial_texts_list[index][-20:].replace("\n", "")] = \
                float(preprocessed_probabilities[index][1])

        app.logger.info('%s', str(json_list))

    return json_list


def process_post_request(app: Flask, request_data: RequestData):
    app.logger.info('URL [%s], \n Text [%s]', request_data.image_url,
                    str(request_data.image_texts))
    clean_folder(BASE_DIR + '/tmpImagesFolder/')
    download_image(request_data.image_url, BASE_DIR + '/tmpImagesFolder/')
    return process(app, request_data.image_texts)


def load_clip_model(app: Flask):
    global clip_image_text_processor
    app.logger.info('%s', 'Loading model...')
    clip_image_text_processor = ClipImageTextProcessor()
    clip_image_text_processor.load_model()


def add_dummy_categories(initial_texts_list: typing.List[str]) -> typing.List[str]:
    initial_texts_list.extend(dummy_categories)
    return initial_texts_list


def remove_dummy_categories(initial_texts_list: typing.List[str]) -> typing.List[str]:
    global dummy_categories
    for cat in dummy_categories:
        initial_texts_list.remove(cat)
    return initial_texts_list
