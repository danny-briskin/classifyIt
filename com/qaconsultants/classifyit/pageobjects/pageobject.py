import logging
import os
import shutil
import socket
import requests

import http.client

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from com.qaconsultants.classifyit.clip_processing.clip_image_text_processing import *
from com.qaconsultants.classifyit.utils.file_utilities import clean_folder, find_images_in_folder
from com.qaconsultants.classifyit.utils.html_utilities import *
from com.qaconsultants.classifyit.utils.images_utilities import convert_svg_to_png

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
    load_categories(initial_categories_list)
    process_probabilities(initial_categories_list)


class PageObject:
    def __init__(self, p_driver):
        self.driver = p_driver

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
        # TODO all!!
        for image_element in all_images[:2]:
            image_url = get_image_url_from_attributes(image_element)
            first_pos = image_url.rfind("/")
            last_pos = len(image_url)
            image_file_name = image_url[first_pos + 1:last_pos]
            logging.info('Processing [' + image_url + ']')
            request = requests.get(image_url, allow_redirects=True)
            image_file_name_full = BASE_DIR + '/tmpImagesFolder/' + image_file_name
            open(image_file_name_full, 'wb').write(request.content)
            if image_url.endswith('.svg'):
                convert_svg_to_png(image_file_name, BASE_DIR + '/tmpImagesFolder/')

        # find all downloaded images
        list_of_images = find_images_in_folder(BASE_DIR + '/tmpImagesFolder/', '*.webp')
        list_of_images.extend(find_images_in_folder(BASE_DIR + '/tmpImagesFolder/', '*.png'))
        logging.info('Start to classify...')
        load_model()
        for file_image in list_of_images:
            file_image_str = str(file_image)
            logging.info(' Classification : ' + file_image_str)
            load_image(file_image_str)
            initial_categories_list = ['Test Automation', 'We are a Test Automation Leader',
                                       'What happens when test automation goes wrong?'
                ,
                                       'QA Consultants is at the forefront of test automation engineering techniques, technologies, and methodologies with our test automation services. We partner with clients across various industries to drive their automation innovation and QA optimization. Our expertise spans all test automation platforms and we have a vast knowledge base of best practices which we leverage for our clients. spans all test automation platforms and we have a  .']
            load_categories(initial_categories_list)
            process_probabilities(initial_categories_list)

    def find_all_text(self):
        text_results = set()
        # TODO consider remove img tags from the search
        all_texts = self.driver.find_elements_by_xpath(
            "//div[contains(@class,'entry-content')]/descendant::*[not(contains(@style,'display: none')) and not(contains(@style,'displayed:false'))]")
        for text_item in all_texts:
            if text_item.text != "":
                text_results.add(text_item.text)
        text_results_string = ' '.join(text_results)
        logging.info(text_results_string)
