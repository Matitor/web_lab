# Generated by Django 4.2.4 on 2023-10-10 22:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emp_dbapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vacancy',
            options={'managed': False, 'verbose_name': 'Вакансия', 'verbose_name_plural': 'Вакансии'},
        ),
    ]
