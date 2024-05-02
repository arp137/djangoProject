from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template import loader

from . import api
from django.http import JsonResponse, HttpResponse
from django.views import generic

class dashboardClass(generic.TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        years = api.get_years()
        context['years'] = years
        return context


def equips(request):
    equip_list = api.get_teams2()
    template = '../../dataGoal/templates/equips.html'
    context = {'equip_list': []}
    for team in equip_list['teams']:
        context['equip_list'].append(team)
    return render(request, template, context)


def equip(request, equip_id):
    equip_info = api.get_equip_info(equip_id)
    template = '../../dataGoal/templates/equip.html'
    context = {'equip_info': equip_info}
    return render(request, template, context)

def make_comparative(request):
    selected_year = request.GET.get('Seasons')
    selected_team1 = request.GET.get('Team1')
    teams = api.get_teams(selected_year) if selected_year else None
    teams_without = api.get_teams_without_selected(teams, selected_team1) if selected_team1 and teams else None

    context = {
        "years": api.get_years(),
        "selected_year": selected_year,
        "teams": teams,
        "selected_team1": selected_team1,
        "teams_without": teams_without
    }
    template = '../../dataGoal/templates/make-comparative.html'
    return render(request, template, context)
