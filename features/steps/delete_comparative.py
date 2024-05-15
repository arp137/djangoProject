from behave import *


@given("Exists a user {username}")
def step_impl(context, username):
    from django.contrib.auth.models import User
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
    from dataGoal.models import Comparacio, EstadistiquesEquip, Temporada
    remove_link = context.browser.find_by_text('REMOVE')
    remove_link.first.click()
    context.browser.comparatives_before = Comparacio.objects.all().count()
    context.browser.statistics_before = EstadistiquesEquip.objects.all().count()
    context.browser.seasons_before = Temporada.objects.all().count()
    confirm_button = context.browser.find_by_xpath("//button[@class='delete']")
    confirm_button.click()
    assert context.browser.url == "http://127.0.0.1:8000/dashboard/"


@then('There is one less comparative')
def step_impl(context):
    from dataGoal.models import Comparacio
    current_comparative = Comparacio.objects.all().count()
    assert current_comparative + 1 == context.browser.comparatives_before


@then('There are two less Team Statistics')
def step_impl(context):
    from dataGoal.models import EstadistiquesEquip
    current_statistics = EstadistiquesEquip.objects.all().count()
    assert current_statistics + 2 == context.browser.statistics_before


@then('There is one Season less')
def step_impl(context):
    from dataGoal.models import Temporada
    current_season = Temporada.objects.all().count()
    assert current_season + 1 == context.browser.seasons_before
