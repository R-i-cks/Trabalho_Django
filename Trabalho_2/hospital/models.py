from django.db import models
# Create your models here.


class Pessoa(models.Model):
    nome = models.CharField(max_length=40, unique=True) # usado como username
    primeiro_nome = models.CharField(max_length=40, default="")
    apelido = models.CharField(max_length=200, default="")
    data_nascimento = models.DateTimeField(default=None)
    genero = models.CharField(max_length=20,default="")
    telemovel = models.IntegerField(default="")
    email = models.CharField(max_length=60,default="")
    class Meta:
        abstract = True     # Comporta-se como um extends, contudo a tabela pessoa não é criada

class Utente(Pessoa):
    contacto_emergencia = models.IntegerField(default=0)
    tem_seguro = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class Medico(Pessoa):
    especialidade = models.CharField(max_length=40,default="")
    def __str__(self):
        return self.nome

class Enfermeiro(Pessoa):
    def __str__(self):
        return self.nome
class Auxiliar(Pessoa):
    def __str__(self):
        return self.nome

class Familiar(Pessoa):
    utente = models.ManyToManyField(Utente)   # uma pessoa pode ser familiar de várias



class Medicamento(models.Model):
    nome = models.CharField(max_length=200, unique=True)
    dosagem = models.CharField(max_length=40, default="")
    fabricante = models.CharField(max_length=100, default="")
    precisa_prescricao = models.BooleanField(default="")

    def __str__(self):
        return self.nome
class Medicoes(models.Model):
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, null=True)
    enfermeiro = models.ForeignKey(Enfermeiro, on_delete=models.CASCADE, null=True)
    tipo = models.CharField(max_length=40, default="")
    valor = models.FloatField(max_length=20, default="")
    unidades = models.CharField(max_length=10, default="")

class Prescricoes(models.Model):

    medicamento = models.ManyToManyField(Medicamento)
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    inicio_toma = models.DateTimeField(null=True)
    validade_prescricao = models.IntegerField(default=0)
    dose_diaria = models.IntegerField(default=0)

class Exame(models.Model):
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, null=True)
    enfermeiro = models.ForeignKey(Enfermeiro, on_delete=models.CASCADE, null=True)
    data_realizacao = models.DateTimeField(null=True)
    nome_exame = models.CharField(max_length=40, default="")
    resultado = models.CharField(max_length=200, default="")

class Consulta(models.Model):
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    unidade_saude = models.CharField(max_length=200, default="")
    data = models.DateTimeField(null=True)
    medicoes = models.ManyToManyField(Medicoes)
    prescricoes = models.ManyToManyField(Prescricoes)
    exames = models.ManyToManyField(Exame)




