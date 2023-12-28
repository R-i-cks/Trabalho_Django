from django.db import models

# Create your models here.

class Utente(models.Model):
    nome = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nome

class Medico(models.Model):
    nome = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nome
class Medicamento(models.Model):
    nome = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nome

class Consulta(models.Model):
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    prescricoes = models.ManyToManyField(Medicamento)
