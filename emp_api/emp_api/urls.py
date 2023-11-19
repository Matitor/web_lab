from django.contrib import admin
from emp_api import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    #vacanies
    path(r'vacancies/', views.VacanciesAPI.as_view(), name='vacancy-list'),
    path(r'vacancies/<int:pk>/', views.AnswerAPI.as_view(), name='answer-detail'),
    path(r'vacancies/<int:pk>/post/', views.put_detail, name='vacancy-put'),
    path(r'vacancies/post/', views.VacanciesAPI.as_view(), name='vacancy-post'),
    path(r'vacanciess/', views.get_details, name='stocks-get'),
    #answer
    #va
    #
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]