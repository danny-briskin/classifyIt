import os

from behave import *
from selenium import webdriver

from com.qaconsultants.classifyit.pageobjects.pageobject import PageObject

global page_object


@given('I open "{url}"')
def step_impl(context, url):
    global page_object
    page_object.open_page(url)


@given('I load webdriver')
def step_impl(context):
    global page_object
    # driver = getattr(webdriver, driver_name)
    driver = webdriver.Firefox(service_log_path=os.path.devnull,
                               executable_path='/home/dbriskin/WORK/geckodriver/geckodriver')
    # driver.implicitly_wait(5)
    driver.set_window_size(1200, 800)

    page_object = PageObject(driver)


@when('I find all images on the page')
def step_impl(context):
    global page_object
    page_object.find_all_images()


@step('I grab all text from the page')
def step_impl(context):
    global page_object
    page_object.find_all_text()


@step('I run classification')
def step_impl(context):
    global page_object
    page_object.run_classification()


@step('I close webdriver')
def step_impl(context):
    global page_object
    try:
        if page_object is not None:
            page_object.close_webdriver()
        del page_object
    except NameError:
        pass
