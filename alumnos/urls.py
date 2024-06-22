from django.urls import path
from .views import index, crud
from alumnos import views

urlpatterns = [
    path('', index, name='index'),
    path('crud', views.crud, name='crud'),
    path('alumnos/alumnosAdd', views.alumnosAdd, name='alumnosAdd'),
]
