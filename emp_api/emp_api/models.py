from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import PermissionsMixin , UserManager, AbstractBaseUser

class AnswVac(models.Model):
    vac = models.ForeignKey('Vacancy', models.DO_NOTHING,related_name='vac', blank=True, null=True)
    answ = models.ForeignKey('Answer', models.DO_NOTHING, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'answ_vac'


class Answer(models.Model):
    STATUS_CHOICES = (
        ('registered','зарегистрирован'),
        ('canceled','отменен'),
        ('confirmed','сформирован'),
        ('denied','отказ'),
        ('approved','готов')
    )
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    moderator = models.ForeignKey('CustomUser', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('CustomUser', models.DO_NOTHING, related_name='answer_user_set', blank=True, null=True)
    suite = models.CharField()

    class Meta:
        managed = False
        db_table = 'answer'


class NewUserManager(UserManager):
    def create_user(self,email,password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        
        email = self.normalize_email(email) 
        user = self.model(email=email, **extra_fields) 
        user.set_password(password)
        user.save(using=self.db)
        return user

class CustomUser(AbstractBaseUser):                       # user
    password = models.CharField(max_length=256, null=False)
    is_superuser = models.BooleanField(default=False, verbose_name="Является ли пользователь админом?")
    email = models.EmailField(("email адрес"), max_length=128, unique=True, null=False)
    last_login = models.CharField(("email адрес"), max_length=128, unique=True, null=False)
    is_staff = models.BooleanField(default=False, verbose_name="Является ли пользователь модератором?")

    def __str__(self):
        return f'{self.email}'

    class Meta:
        managed = False
        db_table = 'customuser'
    
    USERNAME_FIELD = 'email'

    objects =  NewUserManager()


class Vacancy(models.Model):
    STATUS_CHOICES = [
        ('enabled', 'активна'),
        ('deleted', 'удалена'),
    ]
    name = models.CharField(max_length=30,verbose_name="Название вакансии")
    desc = models.CharField(max_length=255,verbose_name="Описание вакансии")
    price_min = models.IntegerField(blank=True, null=True,verbose_name="Нижняя грань ЗП")
    price_max = models.IntegerField(blank=True, null=True,verbose_name="Верхняя грань ЗП")
    company = models.CharField(max_length=30,verbose_name="Название компании")
    pic = models.CharField(blank=True, null=True,max_length=100,verbose_name="Изображение")
    adress = models.CharField(max_length=30,verbose_name="Адрес компании")
    total_desc = models.CharField(max_length=255,verbose_name="Подробное описание вакансии")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES,verbose_name="Статус вакансии",default="enable")

    class Meta:
        managed = False
        db_table = 'vacancy'
        verbose_name="Вакансия"
        verbose_name_plural="Вакансии"