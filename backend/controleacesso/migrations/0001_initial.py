
# Generated by Django 3.1 on 2020-08-27 01:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=40)),
                ('codigo', models.CharField(blank=True, max_length=20, null=True)),
                ('foto', models.ImageField(upload_to='rosto')),
                ('face_encoded', models.CharField(blank=True, max_length=3500, null=True)),
                ('bloqueado', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'pessoa',
            },
        ),
        migrations.CreateModel(
            name='Acesso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField()),
                ('tipoAcesso', models.CharField(max_length=10)),
                ('fkpessoa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='controleacesso.pessoa')),
            ],
            options={
                'db_table': 'acesso',
            },
        ),
    ]
