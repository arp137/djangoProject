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


@when('I create a comparative')
def step_impl(context):
    from dataGoal.models import Comparacio
    assert context.browser is not None
    context.browser.visit("http://127.0.0.1:8000/make-comp/")
    select_element = context.browser.find_by_xpath("//*[@id='temporades-select']")
    context.comparative_counter = Comparacio.objects.count()
    select_element.select('2024')

    context.browser.find_by_id('equip1-select').select('Real Madrid')
    context.browser.find_by_id('equip2-select').select('Barcelona')
    context.browser.find_by_id('accept-button').click()
    assert context.browser.url == "http://127.0.0.1:8000/dashboard/"


@then('There are {count:n} comparative')
def step_impl(context, count):
    from dataGoal.models import Comparacio
    print(context.comparative_counter)
    comparatives = Comparacio.objects.count() - context.comparative_counter
    print(comparatives)
    assert count == comparatives
