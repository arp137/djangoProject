from behave import *


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
    comparatives = Comparacio.objects.count() - context.comparative_counter
    assert count == comparatives
