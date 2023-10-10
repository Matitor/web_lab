from emp_api.models import *
from rest_framework import serializers


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Vacancy
        # Поля, которые мы сериализуем
        fields = "__all__"

class AnsSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = AnswVac
        # Поля, которые мы сериализуем
        fields = "__all__"

