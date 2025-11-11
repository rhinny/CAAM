from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [#path('registro/estudiante', views.registro_estudiante, name='registro_estudiante'),
               #path('registro/adultoM', views.registro_adultoM, name='registro_adultoM'),
               path('', views.home, name='home'),
               path('usuarios/registro/', views.registro, name="registro"),
               path('usuarios/login/', views.login_view, name="login"),
               path('usuarios/comuna/', views.comuna, name = 'comuna'),
               path('usuarios/registro/seleccion/', views.seleccion, name = 'seleccion'),
               path('usuarios/logout', views.logout_view, name='logout'),
               ]
