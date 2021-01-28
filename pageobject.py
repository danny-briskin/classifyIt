import logging
import shutil
import socket

import http.client

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')


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
            "//img[not(contains(@style,'display: none')) and not(contains(@style,'displayed:false'))]")
        # + ((this.isHeaderChecked) ? " or contains(@class,'header-bar')" : "")        # + ((
        # this.isFooterChecked) ? " or contains(@class,'footer-sidebar')" : "")
        xpathToNotInclude = "./ancestor-or-self::*[@aria-hidden='true'" + " or contains(@data-src,'youtube.com')" + " or contains(@class,'rpc-post-image')" + " or contains(@class,'qac-img-wrap')" + " or contains(@class,'testimonials-rotator')" + " or contains(@class,'flip-card-pic')" + " or contains(@data-animation,'zoom')" + "]";

        for image in all_images:
            try:
                image.find_element_by_xpath(xpathToNotInclude)
                all_images.remove(image)
            except NoSuchElementException:
                pass
        for image in all_images:
            res = self.getImageUrlFromAttributes(image)
            logging.info(res)

    def getImageUrlFromAttributes(self, image):
        srcUrl = ""
        # try with srcset attribute for 1x or first available
        # TODO consider sorting by width desc
        srcset = image.get_attribute("srcset")
        if srcset != "":
            srcsetArr = srcset.split(",")
            if not srcsetArr:
                srcCandidate = srcsetArr[0].split(" ")[0]
                # srcUrl = Arrays.stream(srcsetArr)
                #         .filter(src -> src.contains(" 1x"))
                #         .map(src -> src.split(" ")[0])
                #         .findFirst()
                #         .orElse(srcCandidate);
                srcUrl = srcCandidate
        # if not found, let's try with regular src
        if srcUrl == "" or not srcUrl.startswith('http'):
            srcUrl = image.get_attribute("src")

        # the last chance - try with data-lazy-srcUrl (comes from WPRocket optimization)
        if srcUrl == "" or not srcUrl.startswith('http'):
            srcUrl = image.get_attribute("data-lazy-src")
        return srcUrl
