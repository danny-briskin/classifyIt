from behave import *


@given('we have behave installed')
def step_impl(context):
    pass


@when('we implement a test')
def step_impl(context):
    print('Hi there!')
    assert True is True


@then('behave will test it for us!')
def step_impl(context):
    assert context.failed is False