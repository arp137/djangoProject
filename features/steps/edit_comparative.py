from behave import *


@given('I click on the edit button and accept it')
def step_impl(context):
    from dataGoal.models import Comparacio, EstadistiquesEquip, Temporada
    edit_link = context.browser.find_by_text('EDIT')
    edit_link.first.click()
    select_element = context.browser.find_by_xpath("//*[@id='temporades-select']")
    context.browser.comparatives_before = Comparacio.objects.all().count()
    context.browser.statistics_before = EstadistiquesEquip.objects.all().count()
    context.browser.seasons_before = Temporada.objects.all().count()
    select_element.select('2024')

    context.browser.find_by_id('equip1-select').select('Real Madrid')
    context.browser.find_by_id('equip2-select').select('Getafe')
    context.browser.find_by_id('accept-button').click()
    assert context.browser.url == "http://127.0.0.1:8000/dashboard/"


@then('There is the same number of Comparatives, Seasons and Team Stadistics')
def step_impl(context):
    from dataGoal.models import Comparacio, EstadistiquesEquip, Temporada
    current_comparatives = Comparacio.objects.all().count()
    current_statistics = EstadistiquesEquip.objects.all().count()
    current_seasons = Temporada.objects.all().count()
    assert (current_comparatives == context.browser.comparatives_before
            and current_statistics == context.browser.statistics_before
            and current_seasons == context.browser.seasons_before)
