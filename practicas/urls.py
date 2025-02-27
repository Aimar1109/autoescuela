from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('fecha_aprob/', views.alumno_aprobado, name='fecha_aprob'),
    path('disponibilidad/', views.disponibilidad, name='disponibilidad'),
    path('horario_instructor/', views.horario_instructor, name='horario_instructor')
]
