# Generated by Django 5.0 on 2024-01-14 19:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auxiliar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=40, unique=True)),
                ('primeiro_nome', models.CharField(default='', max_length=40)),
                ('apelido', models.CharField(default='', max_length=200)),
                ('data_nascimento', models.DateTimeField(default=None)),
                ('genero', models.CharField(default='', max_length=20)),
                ('telemovel', models.IntegerField(default='')),
                ('email', models.CharField(default='', max_length=60)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Enfermeiro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=40, unique=True)),
                ('primeiro_nome', models.CharField(default='', max_length=40)),
                ('apelido', models.CharField(default='', max_length=200)),
                ('data_nascimento', models.DateTimeField(default=None)),
                ('genero', models.CharField(default='', max_length=20)),
                ('telemovel', models.IntegerField(default='')),
                ('email', models.CharField(default='', max_length=60)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Medicamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, unique=True)),
                ('dosagem', models.CharField(default='', max_length=40)),
                ('fabricante', models.CharField(default='', max_length=100)),
                ('precisa_prescricao', models.BooleanField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=40, unique=True)),
                ('primeiro_nome', models.CharField(default='', max_length=40)),
                ('apelido', models.CharField(default='', max_length=200)),
                ('data_nascimento', models.DateTimeField(default=None)),
                ('genero', models.CharField(default='', max_length=20)),
                ('telemovel', models.IntegerField(default='')),
                ('email', models.CharField(default='', max_length=60)),
                ('especialidade', models.CharField(default='', max_length=40)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Utente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=40, unique=True)),
                ('primeiro_nome', models.CharField(default='', max_length=40)),
                ('apelido', models.CharField(default='', max_length=200)),
                ('data_nascimento', models.DateTimeField(default=None)),
                ('genero', models.CharField(default='', max_length=20)),
                ('telemovel', models.IntegerField(default='')),
                ('email', models.CharField(default='', max_length=60)),
                ('contacto_emergencia', models.IntegerField(default=0)),
                ('tem_seguro', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Exame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_realizacao', models.DateTimeField(null=True)),
                ('nome_exame', models.CharField(default='', max_length=40)),
                ('resultado', models.CharField(default='', max_length=200)),
                ('enfermeiro', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hospital.enfermeiro')),
                ('medico', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hospital.medico')),
                ('utente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.utente')),
            ],
        ),
        migrations.CreateModel(
            name='Medicoes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(default='', max_length=40)),
                ('valor', models.FloatField(default='', max_length=20)),
                ('unidades', models.CharField(default='', max_length=10)),
                ('enfermeiro', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hospital.enfermeiro')),
                ('medico', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hospital.medico')),
                ('utente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.utente')),
            ],
        ),
        migrations.CreateModel(
            name='Prescricoes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio_toma', models.DateTimeField(null=True)),
                ('validade_prescricao', models.IntegerField(default=0)),
                ('dose_diaria', models.IntegerField(default=0)),
                ('medicamento', models.ManyToManyField(to='hospital.medicamento')),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.medico')),
                ('utente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.utente')),
            ],
        ),
        migrations.CreateModel(
            name='Familiar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=40, unique=True)),
                ('primeiro_nome', models.CharField(default='', max_length=40)),
                ('apelido', models.CharField(default='', max_length=200)),
                ('data_nascimento', models.DateTimeField(default=None)),
                ('genero', models.CharField(default='', max_length=20)),
                ('telemovel', models.IntegerField(default='')),
                ('email', models.CharField(default='', max_length=60)),
                ('utente', models.ManyToManyField(to='hospital.utente')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unidade_saude', models.CharField(default='', max_length=200)),
                ('data', models.DateTimeField(null=True)),
                ('exames', models.ManyToManyField(to='hospital.exame')),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.medico')),
                ('medicoes', models.ManyToManyField(to='hospital.medicoes')),
                ('prescricoes', models.ManyToManyField(to='hospital.prescricoes')),
                ('utente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.utente')),
            ],
        ),
    ]