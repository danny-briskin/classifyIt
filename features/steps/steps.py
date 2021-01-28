from behave import *

from pageobject import *

global page_object


@given('I open "{url}"')
def step_impl(context, url):
    global page_object
    page_object.open_page(url)


@given('I load webdriver')
def step_impl(context):
    global page_object
    page_object = PageObject(
        webdriver.Firefox(executable_path='/home/dbriskin/WORK/geckodriver/geckodriver'))


@when('I find all images on the page')
def step_impl(context):
    global page_object
    page_object.find_all_images()


@step('I close webdriver')
def step_impl(context):
    global page_object
    try:
        if page_object is not None:
            page_object.close_webdriver()
        del page_object
    except NameError:
        pass
