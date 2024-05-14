from behave import *


@given("Exists a user {username}")
def step_impl(context, username):
    from django.contrib.auth.models import User
    print(username)
    assert User.objects.filter(username=username).exists()


@given("User {username} has created at least one comparative")
def step_impl(context, username):
    from django.contrib.auth.models import User
    from dataGoal.models import Comparacio
    user = User.objects.get(username=username)
    count = Comparacio.objects.filter(user=user).count()
    assert count > 0


@given("I click on the comparative")
def step_impl(context):
    context.browser.visit("http://127.0.0.1:8000/dashboard/")
    comparative_links = context.browser.find_by_css('.full-link')
    if len(comparative_links) >= 2:
        comparative_links[1].click()


@given("I click on the remove button and I accept to delete it")
def step_impl(context):
    from dataGoal.models import Comparacio
    remove_link = context.browser.find_by_text('REMOVE')
    remove_link.first.click()
    context.browser.before_deleting = Comparacio.objects.all().count()
    confirm_button = context.browser.find_by_xpath("//button[@class='delete']")
    confirm_button.click()
    assert context.browser.url == "http://127.0.0.1:8000/dashboard/"


@then('There is one less comparative')
def step_impl(context):
    from dataGoal.models import Comparacio
    current_comparative = Comparacio.objects.all().count()
    assert current_comparative + 1 == context.browser.before_deleting
