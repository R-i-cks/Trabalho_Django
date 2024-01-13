from django.db import models
# Create your models here.


class Pessoa(models.Model):
    nome = models.CharField(max_length=40, unique=True) # usado como username
    primeiro_nome = models.CharField(max_length=40)
    apelido = models.CharField(max_length=200)
    data_nascimento = models.DateTimeField()
    genero = models.CharField(max_length=20)
    telemovel = models.IntegerField(max_length=9)
    email = models.CharField(max_length=60)
    class Meta:
        abstract = True     # Comporta-se como um extends, contudo a tabela pessoa não é criada

class Utente(Pessoa):
    contacto_emergencia = models.IntegerField(max_length=15)
    tem_seguro = models.BooleanField()

    def __str__(self):
        return self.nome

class Medico(Pessoa):
    especialidade = models.CharField(max_length=40)
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
    dosagem = models.CharField(max_length=40)
    fabricante = models.CharField(max_length=100)
    data_validade = models.DateTimeField()
    precisa_prescricao = models.BooleanField()

    def __str__(self):
        return self.nome
class Medicoes(models.Model):
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=40)
    valor = models.FloatField(max_length=20)
    unidades = models.CharField(max_length=10)

class Prescricoes(Medicamento):
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    inicio_toma = models.DateTimeField()
    validade_prescricao = models.IntegerField(max_length=2) # deste modo representa o número de meses que será válida
    dose_diaria = models.IntegerField(max_length=2) # representa o numero de comprimidos por dia

class Exame(models.Model):
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE)
    data_realizacao = models.DateTimeField()
    nome_exame = models.CharField(max_length=40)
    resultado = models.CharField(max_length=200)

class Consulta(models.Model):
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    prescricoes = models.ManyToManyField(Prescricoes)
    unidade_saude = models.CharField(max_length=200)
    data = models.DateTimeField()
    medicoes = models.CharField(Medicoes)





