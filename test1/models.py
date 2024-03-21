from django.db import models

# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    age = models.IntegerField()
    # subjects = models.ManyToManyField('Subject')

    def __str__(self):
        raise self.first_name + ' ' + self.last_name

