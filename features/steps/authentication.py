from behave import *
from splinter.browser import Browser

use_step_matcher("parse")


@given('I login as user "{username}" with password "{password}"')
def step_impl(context, username, password):
    context.browser = Browser('chrome', headless=True)
    context.browser.visit("http://127.0.0.1:8000/login/")  # Visit the correct URL based on the form action
    context.browser.fill('username', username)  # Fill the username field
    context.browser.fill('password', password)  # Fill the password field
    context.browser.find_by_value('LOGIN').first.click()  # Submit the form
    assert context.browser.is_element_present_by_id('add-league')
