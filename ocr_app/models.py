from django.db import models

class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    date_naissance = models.CharField(max_length=255)
    carte_nationale_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.nom} {self.prenom}'
