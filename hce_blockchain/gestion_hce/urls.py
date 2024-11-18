from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('registrar_paciente/', views.registrar_paciente, name='registrar_paciente'),
    path('actualizar_paciente/<int:paciente_id>/', views.actualizar_paciente, name='actualizar_paciente'),
    path('ver_historico_paciente/<int:paciente_id>/', views.ver_historico_paciente, name='ver_historico_paciente'),
    path('consultar_paciente/', views.consultar_paciente, name='consultar_paciente'),
]
