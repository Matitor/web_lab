# Generated by Django 4.2.4 on 2023-11-15 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnswToVac',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'answ_to_vac',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AnswVac',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('зарегистрирован', 'registered'), ('отменен', 'canceled'), ('сформирован', 'confirmed'), ('отказ', 'denied'), ('готов', 'complited')], max_length=50, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('processed_at', models.DateTimeField(blank=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'answ_vac',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('login', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('role', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'users',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Название вакансии')),
                ('desc', models.CharField(max_length=255, verbose_name='Описание вакансии')),
                ('price', models.CharField(max_length=30, verbose_name='Зарплата')),
                ('company', models.CharField(max_length=30, verbose_name='Название компании')),
                ('pic', models.CharField(max_length=30, verbose_name='Изображение')),
                ('adress', models.CharField(max_length=30, verbose_name='Адрес компании')),
                ('total_desc', models.CharField(max_length=255, verbose_name='Подробное описание вакансии')),
                ('status', models.CharField(blank=True, choices=[('enabled', 'активна'), ('deleted', 'удалена')], default='enable', max_length=50, null=True, verbose_name='Статус вакансии')),
            ],
            options={
                'verbose_name': 'Вакансия',
                'verbose_name_plural': 'Вакансии',
                'db_table': 'vacancy',
                'ordering': ('id',),
                'managed': False,
            },
        ),
    ]
