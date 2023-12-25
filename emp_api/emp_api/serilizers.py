from emp_api.models import *
from rest_framework import serializers

class VacancySer(serializers.ModelSerializer):
  class Meta:
    model = Vacancy
    fields = "__all__"
class UserOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email']
class AnswerSer(serializers.ModelSerializer):
  user_email = UserOnlySerializer(source='user')
  moderator_email = UserOnlySerializer(source='moderator')
  class Meta:
        model = Answer
        fields = ['id', 'user_email', 'moderator_email', 'created_at', 'processed_at', 'completed_at','status']


class AnsVacSer(serializers.ModelSerializer):
  answer=serializers.StringRelatedField(read_only=True)
  vacancy=serializers.StringRelatedField(read_only=True)
  
  class Meta:
    model=AnswVac
    fields="__all__"
class UserSer(serializers.ModelSerializer):
  class Meta:
    model =Users
    fields="__all__"
class AnsVacUserSer(serializers.ModelSerializer):
  answer=serializers.StringRelatedField(read_only=True)
  vacancy=serializers.StringRelatedField(read_only=True)
  user_email = UserOnlySerializer(source='user')
  moderator_email = UserOnlySerializer(source='moderator')
  class Meta:
    model=Answer
    fields=['id', 'status', 'created_at', 'processed_at', 'completed_at', 'user_email', 'moderator_email', 'answer','vacancy']