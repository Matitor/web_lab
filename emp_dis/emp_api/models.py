from django.db import models
from django.utils import timezone
from datetime import datetime

class AnswToVac(models.Model):
    vac = models.ForeignKey('Vacancy', models.DO_NOTHING, blank=True, null=True)
    stat = models.ForeignKey('AnswVac', models.DO_NOTHING, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'answ_to_vac'


class AnswVac(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершен'),
        (4, 'Отклонен'),
        (5, 'Удален'),
    )
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    moderator = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, related_name='answvac_user_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'answ_vac'


class Users(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    login = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class Vacancy(models.Model):
    STATUS_CHOICES = [
        ('enabled', 'активна'),
        ('deleted', 'удалена'),
    ]
    name = models.CharField(max_length=30,verbose_name="Название вакансии")
    desc = models.CharField(max_length=255,verbose_name="Описание вакансии")
    price = models.CharField(max_length=30,verbose_name="Зарплата")
    company = models.CharField(max_length=30,verbose_name="Название компании")
    pic = models.CharField(max_length=30,verbose_name="Изображение")
    adress = models.CharField(max_length=30,verbose_name="Адрес компании")
    total_desc = models.CharField(max_length=255,verbose_name="Подробное описание вакансии")
    status = models.CharField(max_length=50, blank=True,choices=STATUS_CHOICES,null=True,verbose_name="Статус вакансии",default="enable")

    class Meta:
        managed = False
        db_table = 'vacancy'
        verbose_name="Вакансия"
        verbose_name_plural="Вакансии"
        ordering=('id', )