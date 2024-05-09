from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template import loader

from . import api
from django.http import JsonResponse, HttpResponse
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from dataGoal.models import EstadistiquesEquip, Comparacio, Temporada



class dashboardClass(LoginRequiredMixin, generic.TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        usuario_actual = self.request.user
        comparaciones_ordenadas = Comparacio.objects.filter(user=usuario_actual).order_by('-last_save_date')
        context = {'user_id': usuario_actual.id}
        if comparaciones_ordenadas:
            print("Length: ", len(comparaciones_ordenadas))
            length = len(comparaciones_ordenadas) if len(comparaciones_ordenadas) < 5 else 5
            context['comps'] = comparaciones_ordenadas[:length]
        return context

class make_comparativeClass(LoginRequiredMixin, View):
    template_name = 'make-comparative.html'

    def get(self, request, *args, **kwargs):
        selected_year = request.GET.get('Seasons')
        selected_team1 = request.GET.get('Team1')
        selected_team2 = request.GET.get('Team2')

        teams = api.get_teams(selected_year) if selected_year else None
        teams_without = api.get_teams_without_selected(teams, selected_team1) if selected_team1 and teams else None

        context = {
            'user_id': request.user.id,
            "years": api.get_years(),
            "selected_year": selected_year,
            "teams": teams,
            "selected_team1": selected_team1,
            "teams_without": teams_without
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        selected_year = request.GET.get('Seasons')
        selected_team1 = request.GET.get('Team1')
        selected_team2 = request.GET.get('Team2')

        team1, team2 = api.get_data(selected_year, selected_team1, selected_team2)
        equip1 = EstadistiquesEquip()
        equip2 = EstadistiquesEquip()

        temporada = Temporada()
        temporada.user = request.user

        if selected_year is not None and isinstance(selected_year, str):
            temporada.any = selected_year
            temporada.titul = f"Season {int(selected_year) - 1}/{selected_year[-2:]}"
            temporada.save()
        else:
            temporada.save()

        equip1.temporada = temporada
        equip1.user = request.user
        equip2.temporada = temporada
        equip2.user = request.user

        copy_all(equip1, team1)
        copy_all(equip2, team2)

        equip1.save()
        equip2.save()

        comp = Comparacio()
        comp.user = request.user
        comp.temporada = temporada
        comp.estadistiquesEquip1 = equip1
        comp.estadistiquesEquip2 = equip2

        comp.save()

        context = {
            "team1": team1,
            "team2": team2
        }
        template_name = 'make-comparative-selection.html'
        return render(request, template_name, context)

def copy_all(equip, team):
    equip.nom = team.name
    equip.abreviacio = team.abreviation
    equip.estadi = team.estadi
    equip.escut_url = team.escut_url

    equip.gols_favor_local = team.stats['local']['goals_for']
    equip.gols_favor_visitant = team.stats['visitor']['goals_for']

    equip.gols_en_contra_local = team.stats['local']['goals_against']
    equip.gols_en_contra_visitant = team.stats['visitor']['goals_against']

    equip.victorias_local = team.stats['local']['victories']
    equip.victorias_visitant = team.stats['visitor']['victories']

    equip.empates_local = team.stats['local']['draws']
    equip.empates_visitant = team.stats['visitor']['draws']

    equip.derrotas_local = team.stats['local']['defeats']
    equip.derrotas_visitant = team.stats['visitor']['defeats']

