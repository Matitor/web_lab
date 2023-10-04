from django.contrib import admin
from django.urls import path

from emp_dbapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.GetVacancies, name='all'),
    path('vacancy/<int:idd>/', views.GetVacancy, name='vacancy_url'),
    path('delete-group/<int:id>', views.delete_vac, name="delete-vac"),
]