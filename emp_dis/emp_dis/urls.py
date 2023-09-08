from django.contrib import admin
from django.urls import path

from emp_dis import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.GetServices),
    path('service/<int:id>/', views.GetService, name='service_url'),
    path('sendText', views.sendText, name='sendText'),
]