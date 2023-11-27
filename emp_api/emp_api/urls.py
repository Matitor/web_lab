from django.contrib import admin
from emp_api import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    #VAC
    path(r'vacancies/', views.VacanciesAPI.as_view(), name='vacancies'),
    path(r'vacancies/<int:pk>', views.VacancyAPI.as_view(), name='vacancy'),
    path(r'vacancies/<int:pk>/post', views.PAnswToVac, name = 'vacancy_add'),

    #ANSW
    path(r'answer/', views.AnswersAPI.as_view(), name='answers'),
    path(r'answer/<int:pk>', views.AnswerAPI.as_view(), name='answer'),
    path(r'answer/<int:pk>/confirm', views.ConfirmAnsw, name = 'answer_confirm'),
    path(r'answer/<int:pk>/accept', views.ToAnsw, name = 'answer_accept'),

    #VAC-ANSW
    path(r'vac_answ/<int:pk>', views.VacAnsAPI.as_view(), name='vac_answ'),
    
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),

]