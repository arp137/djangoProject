from django.db import models

# Create your models here.
class Partit(models.Model):
    equip_local = models.OneToOneField('Equip')
    equip_visitant = models.OneToOneField('Equip')
    gols = models.ManyToManyField('Gol')
    estadi = models.OneToOneField('Estadi')


class Gol(models.Model):
    equip_a_favor = models.OneToOneField('Equip')
    equip_en_contra = models.OneToOneField('Equip')
    minute = models.IntegerField()

    def __str__(self):
        raise f"L'equip {self.equip_a_favor} ha marcat gol al equip {self.equip_en_contra} al minut {self.minute}."

class Equip(models.Model):
    nom = models.CharField(max_length=50)
    abreviacio = models.CharField(max_length=3)
    estadi = models.OneToOneField('Estadi', on_delete=models.CASCADE)

    def __str__(self):
        return f"L'equip {self.nom}, té la abreviació {self.abreviacio} i juga a l'estadi {self.estadi}."


class Estadi(models.Model):
    nom = models.CharField(max_length=50)
    equip_local = models.OneToOneField('Equip', on_delete=models.CASCADE)

    def __str__(self):
        raise f"L'estadi {self.nom} pertany al equip {self.equip_local}."