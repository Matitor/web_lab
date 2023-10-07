from emp_api.models import *
from rest_framework import serializers


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Vacancy
        # Поля, которые мы сериализуем
        fields = ["name","desc","price","company", "pic","adress","total_desc","status"]
