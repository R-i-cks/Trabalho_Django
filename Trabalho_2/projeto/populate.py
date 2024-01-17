from django.utils import timezone
from hospital.models import *
from django.contrib.auth.models import User, Group
import random
from datetime import datetime


def data_aleatoria(ano_min=1940, ano_limite=2023):
    ano = random.randint(ano_min, ano_limite)
    mes = random.randint(1, 12)
    dia = random.randint(1, 28)  # versao simplificada
    hora = random.randint(0, 23)
    minuto = random.randint(0, 59)
    segundo = random.randint(0, 59)

    data = datetime(ano, mes, dia, hora, minuto, segundo)
    data_aware = timezone.make_aware(data, timezone.get_current_timezone())

    return data_aware


def telemovel():
    operadora = random.choice(["91", "92", "93", "96"])
    resto = "".join(str(random.randrange(0, 9)) for _ in range(7))
    return int(f"{operadora}{resto}")


def run():
    grupo_medicos, created = Group.objects.get_or_create(name="Medico")
    grupo_utentes, created = Group.objects.get_or_create(name="Utente")
    grupo_enfermeiros, created = Group.objects.get_or_create(name="Enfermeiro")
    grupo_profissionais, created = Group.objects.get_or_create(name="Profissional")
    grupo_auxiliares, created = Group.objects.get_or_create(name="Auxiliar")
    grupo_familiares, created = Group.objects.get_or_create(name="Familiar")

    nomes_masculinos = ["João", "Manuel", "Carlos", "António", "Luís"]
    nomes_femininos = ["Maria", "Ana", "Isabel", "Sofia", "Margarida"]
    apelidos = [
        "Silva",
        "Santos",
        "Oliveira",
        "Ferreira",
        "Pereira",
        "Costa",
        "Martins",
        "Rodrigues",
        "Almeida",
        "Ribeiro",
    ]
    especialidades = ["Cardiologia", "Clinica Geral", "Pediatria", "Cirurgia Geral"]

    dosagens = ["500mg", "200mg", "250mg", "20mg", "1000mg", "10mg", "325mg"]
    fabricantes = [
        "Johnson & Johnson",
        "Pfizer",
        "GlaxoSmithKline",
        "Bayer",
        "Novartis",
        "Roche",
        "Sanofi",
        "Merck",
    ]

    for i in range(1, 51):  # criar utente e respetivo utilizador
        genero = random.choice(["M", "F"])
        if genero == "M":
            primeiro = random.choice(nomes_masculinos)
        else:
            primeiro = random.choice(nomes_femininos)

        u = Utente(
            nome=f"utente_{i}",
            email=f"utente_{i}@email.com",
            genero=genero,
            primeiro_nome=primeiro,
            apelido=random.choice(apelidos),
            data_nascimento=data_aleatoria(ano_limite=2014),
            telemovel=telemovel(),
            contacto_emergencia=telemovel(),
            tem_seguro=random.choice([True, False]),
        )
        user = User.objects.create_user(
            f"utente_{i}", f"utente_{i}@email.com", "password"
        )
        user.groups.add(grupo_utentes)
        user.save()
        u.save()
    for i in range(1, 51):
        genero = random.choice(["M", "F"])
        if genero == "M":
            primeiro = random.choice(nomes_masculinos)
        else:
            primeiro = random.choice(nomes_femininos)

        m = Medico(
            nome=f"medico_{i}",
            email=f"medico_{i}@email.com",
            genero=genero,
            primeiro_nome=primeiro,
            apelido=random.choice(apelidos),
            data_nascimento=data_aleatoria(ano_limite=2014),
            telemovel=telemovel(),
            especialidade=random.choice(especialidades),
        )
        user = User.objects.create_user(
            f"medico_{i}", f"medico_{i}@email.com", "password"
        )
        user.groups.add(grupo_medicos, grupo_profissionais)
        user.save()
        m.save()

    for i in range(1, 51):
        genero = random.choice(["M", "F"])
        if genero == "M":
            primeiro = random.choice(nomes_masculinos)
        else:
            primeiro = random.choice(nomes_femininos)

        e = Enfermeiro(
            nome=f"enfermeiro_{i}",
            email=f"enfermeiro_{i}@email.com",
            genero=genero,
            primeiro_nome=primeiro,
            apelido=random.choice(apelidos),
            data_nascimento=data_aleatoria(ano_limite=2014),
            telemovel=telemovel(),
        )
        user = User.objects.create_user(
            f"enfermeiro_{i}", f"enfermeiro_{i}@email.com", "password"
        )
        user.groups.add(grupo_enfermeiros, grupo_profissionais)
        user.save()
        e.save()

    for i in range(1, 51):  # Auxiliar
        genero = random.choice(["M", "F"])
        if genero == "M":
            primeiro = random.choice(nomes_masculinos)
        else:
            primeiro = random.choice(nomes_femininos)

        a = Auxiliar(
            nome=f"auxiliar_{i}",
            email=f"auxiliar_{i}@email.com",
            genero=genero,
            primeiro_nome=primeiro,
            apelido=random.choice(apelidos),
            data_nascimento=data_aleatoria(ano_limite=2014),
            telemovel=telemovel(),
        )
        user = User.objects.create_user(
            f"auxiliar_{i}", f"auxiliar_{i}@email.com", "password"
        )
        user.groups.add(grupo_auxiliares, grupo_profissionais)
        user.save()
        a.save()

    for i in range(1, 51):  # Familiar
        genero = random.choice(["M", "F"])
        if genero == "M":
            primeiro = random.choice(nomes_masculinos)
        else:
            primeiro = random.choice(nomes_femininos)

        f = Familiar(
            nome=f"familiar_{i}",
            email=f"familiar_{i}@email.com",
            genero=genero,
            primeiro_nome=primeiro,
            apelido=random.choice(apelidos),
            data_nascimento=data_aleatoria(ano_limite=2014),
            telemovel=telemovel(),
        )
        f.save()
        utente = Utente.objects.all().filter(nome=f"utente_{i}").first()
        f.utente.add(utente)
        user = User.objects.create_user(
            f"familiar_{i}", f"familiar_{i}@email.com", "password"
        )
        user.groups.add(grupo_familiares)
        user.save()

    # Fim da criacao dos diferentes tipos de pessoas

    for i in range(1, 51):
        med = Medicamento(
            nome=f"medicamento {i}",
            dosagem=random.choice(dosagens),
            fabricante=random.choice(fabricantes),
            precisa_prescricao=random.choice([True, False]),
        )
        med.save()

    upcs = ["Hospital de Braga", "Hospital de S.João", "Hospital de Santa Maria"]
    for i in range(1, 51):
        u = Utente.objects.all().filter(nome=f"utente_{i}").first()
        m = Medico.objects.all().filter(nome=f"medico_{i}").first()
        c = Consulta(
            utente=u,
            medico=m,
            data=data_aleatoria(2024, 2026),
            unidade_saude=random.choice(upcs),
        )
        c.save()
        tipos_disponiveis = ["peso", "altura", "PA"]

        for j in range(2):
            tipo = random.choice(tipos_disponiveis)
            tipos_disponiveis.remove(tipo)

            if tipo == "peso":
                valor = random.randrange(50, 100)
                unidade = "kg"
            elif tipo == "altura":
                valor = random.uniform(1.5, 2.10)
                unidade = "m"
            else:
                valor = random.randrange(80, 160)
                unidade = "mmHg"
            medicacao = Medicoes(utente=u, tipo=tipo, valor=valor, unidades=unidade)
            medicacao.save()
            if random.randrange(0, 50) > 25:
                medicacao.medico = m
            else:
                enfermeiro = (
                    Enfermeiro.objects.all().filter(nome=f"enfermeiro_{i}").first()
                )
                medicacao.enfermeiro = enfermeiro
            c.medicoes.add(medicacao)
        # --------------------------------------------------
        # Prescrições

        for a in range(2):
            medicamento = Medicamento.objects.get(pk=random.randint(1, 51))
            prescricao = Prescricoes(
                medicamento=medicamento,
                utente=u,
                medico=m,
                inicio_toma=data_aleatoria(2023, 2024),
                validade_prescricao=random.randint(1, 24),
                dose_diaria=random.randint(1, 7),
            )
            prescricao.save()
            c.prescricoes.add(prescricao)

        # --------------------------------------------------
        # Exames

        exames = [
            "Hemograma",
            "Colesterol Total",
            "Glicemia em Jejum",
            "Creatinina",
            "Hemoglobina Glicada",
        ]

        exames_resultados = {
            "Hemograma": [
                "Normal",
                "Anemia leve",
                "Leucocitose",
                "Trombocitopenia",
                "Normal",
            ],
            "Colesterol Total": [
                "Desejável",
                "Limítrofe",
                "Alto",
                "Muito Alto",
                "Desejável",
            ],
            "Glicemia em Jejum": [
                "Normal",
                "Pré-diabetes",
                "Diabetes",
                "Normal",
                "Pré-diabetes",
            ],
            "Creatinina": [
                "Normal",
                "Levemente elevada",
                "Elevada",
                "Normal",
                "Levemente elevada",
            ],
            "Hemoglobina Glicada": [
                "Normal",
                "Pré-diabetes",
                "Diabetes",
                "Normal",
                "Pré-diabetes",
            ],
        }

        for b in range(2):
            exame = random.choice(exames)
            resultado = random.choice(exames_resultados[exame])
            e = Exame(
                utente=u,
                data_realizacao=data_aleatoria(2023, 2024),
                nome_exame=exame,
                resultado=resultado,
            )

            e.save()
            if b == 1:
                e.medico = m
            else:
                enfermeiro = (
                    Enfermeiro.objects.all().filter(nome=f"enfermeiro_{i}").first()
                )
                e.enfermeiro = enfermeiro
            c.exames.add(e)
        # --------------------------------------------------
