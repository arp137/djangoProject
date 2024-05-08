from django.db import models
from django.utils import timezone

# Create your models here.
class Temporada (models.Model):
    any = models.CharField(max_length=50)
    titul = models.CharField(max_length=50)

class EstadistiquesEquip(models.Model):
    temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE)
    nom = models.CharField(max_length=50)
    abreviacio = models.CharField(max_length=3)
    estadi = models.CharField(max_length=50)
    escut_url = models.URLField(max_length=200, default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTCugpPDzvVCn-fLGeKlz8A772i7SvZJ8OyJA&usqp=CAU')

    gols_favor_local = models.IntegerField(default=0)
    gols_favor_visitant = models.IntegerField(default=0)

    gols_en_contra_local = models.IntegerField(default=0)
    gols_en_contra_visitant = models.IntegerField(default=0)

    victorias_local = models.IntegerField(default=0)
    victorias_visitant = models.IntegerField(default=0)

    empates_local = models.IntegerField(default=0)
    empates_visitant = models.IntegerField(default=0)

    derrotas_local = models.IntegerField(default=0)
    derrotas_visitant = models.IntegerField(default=0)

    @property
    def gols_favor_totals(self):
        return self.gols_favor_local + self.gols_favor_visitant

    @property
    def gols_en_contra_totals(self):
        return self.gols_en_contra_local + self.gols_en_contra_visitant

    @property
    def diferencia_gols_local(self):
        return self.gols_favor_local - self.gols_en_contra_local

    @property
    def diferencia_gols_visitant(self):
        return self.gols_favor_visitant - self.gols_en_contra_visitant

    @property
    def diferencia_gols_totals(self):
        return self.gols_favor_totals - self.gols_en_contra_totals

    @property
    def victorias_totals(self):
        return self.victorias_local + self.victorias_visitant

    @property
    def empates_totals(self):
        return self.empates_local + self.empates_visitant

    @property
    def derrotas_totals(self):
        return self.derrotas_local + self.derrotas_visitant

    @property
    def puntos_local(self):
        return self.victorias_local * 3 + self.empates_local

    @property
    def puntos_visitant(self):
        return self.victorias_visitant * 3 + self.empates_visitant

    @property
    def puntos_totals(self):
        return self.puntos_local + self.puntos_visitant

class Comparacio(models.Model):
    last_save_date = models.DateTimeField(default=timezone.now)
    temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE)
    estadistiquesEquip1 = models.ForeignKey(EstadistiquesEquip, on_delete=models.CASCADE, related_name='equip1')
    estadistiquesEquip2 = models.ForeignKey(EstadistiquesEquip, on_delete=models.CASCADE, related_name='equip2')

