from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from emp_api import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(r'vacancyapi/', views.get_list, name='vacancy-list'),
    path(r'vacancyapi/post/', views.post_list, name='vacancy-post'),
    path(r'vacancyapi/<int:pk>/', views.get_detail, name='vacancy-detail'),
    path(r'vacancyapi/<int:pk>/put/', views.put_detail, name='vacancy-put'),
    path(r'vacancyapi/<int:pk>/delete/', views.delete_detail, name='vacancy-delete'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]