import logging
import os
import shutil
import socket
from typing import List

import requests

import http.client

import typing
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from com.qaconsultants.classifyit.clip_processing.clip_image_text_processing import *
from com.qaconsultants.classifyit.clip_processing.clip_image_text_processor import \
    ClipImageTextProcessor
from com.qaconsultants.classifyit.utils.file_utilities import clean_folder, find_images_in_folder
from com.qaconsultants.classifyit.utils.html_utilities import *
from com.qaconsultants.classifyit.utils.images_utilities import convert_svg_to_png, download_image

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
# project homedir
BASE_DIR = os.path.dirname(os.getcwd())


def run_classification():
    load_model()
    image_path = "../tmpImagesFolder/TEST-AUTOMATION.webp"
    load_image(image_path)
    initial_categories_list = ['Test Automation', 'We are a Test Automation Leader',
                               'What happens when test automation goes wrong?'
        ,
                               'QA Consultants is at the forefront of test automation engineering techniques, technologies, and methodologies with our test automation services. We partner with clients across various industries to drive their automation innovation and QA optimization. Our expertise spans all test automation platforms and we have a vast knowledge base of best practices which we leverage for our clients. spans all test automation platforms and we have a  .']
    format_categories(initial_categories_list)
    load_categories()
    process_probabilities(initial_categories_list)


def print_probabilities(initial_texts_list: List[str],
                        preprocessed_probabilities: typing.List[
                            typing.Tuple[int, float]]) -> None:
    """
    Prints probability per initial text
    :param preprocessed_probabilities: preprocessed_probabilities [(1,0.34),(2,0.78)]
    :param initial_texts_list: initial texts
    """
    for index in range(len(preprocessed_probabilities)):
        log_str = "{:<26}".format(
            initial_texts_list[index][:40].replace("\n", "") + ' <...> '
            + initial_texts_list[index][-20:].replace("\n", "")) + " : " + "{:.2%}" \
                      .format(preprocessed_probabilities[index][1])
        logging.info(log_str)


class PageObject:
    def __init__(self, p_driver):
        self.driver = p_driver
        self.text_results = []
        self.text_results_string = ''

    def open_page(self, url):
        logging.info("Opening ... " + url)
        self.driver.get("https://qac.staging.wpengine.com/" + url)

        WebDriverWait(self.driver, 20).until(
            EC.invisibility_of_element_located((By.ID, "preloader")))
        logging.info("Spinner is not visible")
        # # wait 10 seconds before looking for element
        # element = WebDriverWait(self.driver, 20).until(
        #     EC.visibility_of_element_located((By.ID, "s")))
        # element.send_keys('home', Keys.ENTER)
        # self.driver.implicitly_wait(5)
        # WebDriverWait(self.driver, 20).until(
        #     EC.invisibility_of_element_located((By.ID, "preloader")))

    def close_webdriver(self):
        """Quits the driver and close every associated window."""
        global driver

        if self.get_status() == 'Alive':
            try:
                self.driver.quit()
            except (http.client.BadStatusLine, socket.error) as e:
                logging.critical(e)

    def get_status(self):
        if self.driver is not None:
            try:
                self.driver.execute(Command.STATUS)
                return "Alive"
            except (socket.error, http.client.CannotSendRequest):
                return "Dead"

    def find_all_images(self):
        all_images = self.driver.find_elements_by_xpath(
            "//img[not(contains(@style,'display: none')) and not(contains(@style,"
            "'displayed:false'))]")
        # + ((this.isHeaderChecked) ? " or contains(@class,'header-bar')" : "")        # + ((
        # this.isFooterChecked) ? " or contains(@class,'footer-sidebar')" : "")
        xpath_to_not_include = "./ancestor-or-self::*[@aria-hidden='true' or contains(@data-src," \
                               "'youtube.com') or contains(@class,'rpc-post-image') or contains(" \
                               "@class,'qac-img-wrap') or contains(@class,'testimonials-rotator') " \
                               "or contains(@class,'flip-card-pic') or contains(@data-animation," \
                               "'zoom')] "

        for image_element in all_images:
            try:
                # logging.info('Trying with '+ image.get_attribute("src"))

                image_element.find_element_by_xpath(xpath_to_not_include)
                all_images.remove(image_element)
            except NoSuchElementException:
                pass
        clean_folder(BASE_DIR + '/tmpImagesFolder/')

        for image_element in all_images:
            image_url = get_image_url_from_attributes(image_element)
            download_image(image_url, BASE_DIR + '/tmpImagesFolder/')

        # find all downloaded images
        list_of_images = find_images_in_folder(BASE_DIR + '/tmpImagesFolder/', '*.webp')
        list_of_images.extend(find_images_in_folder(BASE_DIR + '/tmpImagesFolder/', '*.png'))
        logging.info('Loading model...')

        clip_image_text_processor = ClipImageTextProcessor()
        clip_image_text_processor.load_model()

        # init()
        # load_model()
        logging.info('Searching for text on page....')
        self.find_all_text()
        logging.info('Prepare text.....' + ' found ' + str(
            len(self.text_results_string)) + ' characters of text')
        initial_categories_list = [self.text_results_string]

        clip_image_text_processor.format_texts(initial_categories_list, 45)
        # format_categories(initial_categories_list, 45)

        logging.info('Starting to classify.....')
        for file_image in list_of_images:
            file_image_str = str(file_image)
            logging.info(' Classifying image file [file://' + file_image_str + ']')

            clip_image_text_processor.image_holder.set_image(file_image_str)

            # load_image(file_image_str)
            clip_image_text_processor.calculate_probabilities()
            # load_categories()
            preprocessed_probabilities = clip_image_text_processor \
                .preprocess_probabilities(clip_image_text_processor.image_holder.probabilities)
            print_probabilities(initial_categories_list, preprocessed_probabilities)
            # process_probabilities(initial_categories_list)
            # clean()
            clip_image_text_processor.reset_split_categories_numbers()

    def find_all_text(self):
        # TODO consider remove img tags from the search
        all_texts = self.driver.find_elements_by_xpath(
            "//div[contains(@class,'entry-content')]/descendant::*[not(contains(@style,'display: "
            "none')) and not(contains(@style,'displayed:false'))]")
        for text_item in all_texts:
            if text_item.text != "":
                self.text_results.append(text_item.text)
        self.text_results_string = ' '.join(self.text_results)
        logging.info('Found web text : [' + self.text_results_string[:30] + '...'
                     + self.text_results_string[-20:] + ']')
