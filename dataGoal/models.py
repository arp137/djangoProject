from django.db import models


# Create your models here.
class Estadi(models.Model):
    nom = models.CharField(max_length=50)

    def __str__(self):
        return f"L'estadi {self.nom}."


class Equip(models.Model):
    nom = models.CharField(max_length=50)
    abreviacio = models.CharField(max_length=3)
    estadi = models.OneToOneField(Estadi, on_delete=models.CASCADE)


class Gol(models.Model):
    equip_a_favor = models.OneToOneField(Equip, on_delete=models.CASCADE, related_name='gol_a_favor')
    equip_en_contra = models.OneToOneField(Equip, on_delete=models.CASCADE, related_name='gol_en_contra')
    minute = models.IntegerField()

    def __str__(self):
        return f"L'equip {self.equip_a_favor} ha marcat gol al equip {self.equip_en_contra} al minut {self.minute}."


class Partit(models.Model):
    equip_local = models.ForeignKey(Equip, on_delete=models.CASCADE, related_name='equip_local')
    equip_visitant = models.ForeignKey(Equip, on_delete=models.CASCADE, related_name='equip_visitant')
    gols = models.ForeignKey(Gol, on_delete=models.CASCADE)
    estadi = models.OneToOneField(Estadi, on_delete=models.CASCADE)

    def __str__(self):
        return f"L'equip  {self.equip_local} juga contra l'equip {self.equip_visitant} a l'estadi {self.minute}."
