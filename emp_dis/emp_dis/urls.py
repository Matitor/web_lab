from django.contrib import admin
from django.urls import path

from emp_dis import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.GetServices, name='all'),
    #path('sendText', views.sendText, name='sendText'),
    path('vacancy/<int:idd>/', views.GetService, name='vacancy_url'),
]