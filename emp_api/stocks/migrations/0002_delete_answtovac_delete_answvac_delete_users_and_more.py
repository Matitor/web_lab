# Generated by Django 4.2.4 on 2023-11-15 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AnswToVac',
        ),
        migrations.DeleteModel(
            name='AnswVac',
        ),
        migrations.DeleteModel(
            name='Users',
        ),
        migrations.DeleteModel(
            name='Vacancy',
        ),
    ]
