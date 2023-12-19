from rest_framework import permissions
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.contrib import admin
from emp_api import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
routerUser = routers.DefaultRouter()
# routerDishes = routers.DefaultRouter()


urlpatterns = [
    #VAC
    path(r'vacancies/', views.VacanciesAPI.as_view(), name='vacancies'),
    path(r'vacancies/<int:pk>', views.VacancyAPI.as_view(), name='vacancy'),
    path(r'vacancies/<int:pk>/post', views.PAnswToVac, name = 'vac_put'),
    #ANSW
    path(r'answer/', views.AnswersAPI.as_view(), name='answers'),
    path(r'answer/<int:pk>', views.AnswerAPI.as_view(), name='answer'),
    path(r'answerr/<int:pk>', views.delete, name='answert'),
    path(r'answer/<int:pk>/confirm', views.ConfirmAnsw, name = 'answer_confirm'),
    path(r'answer/accept', views.ToAnsw, name = 'answer_accept'),
    path(r'answer/del', views.delete, name = 'answer_del_user'),

    #VAC-ANSW
    path(r'vac_answ/<int:pk>', views.VacAnsAPI.as_view(), name='vac_answ'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('create/',  views.create, name='create'),
    path('login/',  views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user_info', views.user_info, name='user_info')
]
'''
sudo service redis-server start
redis-cli
'''