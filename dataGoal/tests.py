from django.test import TestCase
from django.utils import timezone
from .models import Temporada, EstadistiquesEquip, Comparacio
from django.contrib.auth.models import User


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.temporada = Temporada.objects.create(any='Test', titul='Test')
        self.equip1 = EstadistiquesEquip.objects.create(
            temporada=self.temporada, nom='Team 1', abreviacio='T1', estadi='Stadium 1')
        self.equip2 = EstadistiquesEquip.objects.create(
            temporada=self.temporada, nom='Team 2', abreviacio='T2', estadi='Stadium 2')

    def test_model_creation(self):
        self.assertEqual(Temporada.objects.count(), 1)
        self.assertEqual(EstadistiquesEquip.objects.count(), 2)

    def test_model_methods(self):
        self.assertEqual(self.equip1.gols_favor_totals, 0)
        # Add more assertions for other methods

    def test_comparacio_edit(self):
        comparacio = Comparacio.objects.create(
            user=self.user, temporada=self.temporada, estadistiquesEquip1=self.equip1, estadistiquesEquip2=self.equip2)
        new_temp = Temporada.objects.create(any='New Test', titul='New Test')
        new_equip1 = EstadistiquesEquip.objects.create(
            temporada=new_temp, nom='New Team 1', abreviacio='NT1', estadi='New Stadium 1')
        new_equip2 = EstadistiquesEquip.objects.create(
            temporada=new_temp, nom='New Team 2', abreviacio='NT2', estadi='New Stadium 2')

        comparacio.edit(new_temp, new_equip1, new_equip2)
        comparacio.refresh_from_db()

        self.assertEqual(comparacio.temporada, new_temp)
        self.assertEqual(comparacio.estadistiquesEquip1, new_equip1)
        self.assertEqual(comparacio.estadistiquesEquip2, new_equip2)


def test_model_deletion(self):
    temporada = Temporada.objects.create(any='Test', titul='Test')
    self.assertEqual(Temporada.objects.count(), 1)
    temporada.delete()

    self.assertEqual(Temporada.objects.count(), 0)
