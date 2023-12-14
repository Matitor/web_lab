from emp_api.models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(default=False, required=False)
    is_superuser = serializers.BooleanField(default=False, required=False)
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'is_superuser','is_staff'] 
    

class VacancySer(serializers.ModelSerializer):
  class Meta:
    model = Vacancy
    fields = "__all__"

class AnswerSer(serializers.ModelSerializer):
  class Meta:
    model = Answer
    fields = "__all__"

class AnsVacSer(serializers.ModelSerializer):
  answer=serializers.StringRelatedField(read_only=True)
  vacancy=serializers.StringRelatedField(read_only=True)
  class Meta:
    model=AnswVac
    fields="__all__"
    
class AnsVacUserSer(serializers.ModelSerializer):
  answer=serializers.StringRelatedField(read_only=True)
  vacancy=serializers.StringRelatedField(read_only=True)
  user=serializers.StringRelatedField(read_only=True)
  class Meta:
    model=Answer
    fields=['id', 'status', 'created_at', 'processed_at', 'completed_at', 'user', 'moderator', 'answer','vacancy']