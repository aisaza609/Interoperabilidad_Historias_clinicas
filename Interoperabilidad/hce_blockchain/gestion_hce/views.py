from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Paciente

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def registrar_paciente(request):
    return render(request, 'registrar_paciente.html')

@login_required
def actualizar_paciente(request, paciente_id):
    return render(request, 'actualizar_paciente.html')

@login_required
def ver_historico_paciente(request, paciente_id):
    return render(request, 'ver_historico_paciente.html')

@login_required
def consultar_paciente(request):
    return render(request, 'consultar_paciente.html')
# views.py
from django.shortcuts import render

def consultar_paciente(request):
    # Paciente de prueba
    pacientes = [
        {
            'id': 1,
            'nombre': "Paciente Prueba",
            'tipo_documento': "CC",
            'numero_documento': "123456789",
            'edad': 30,
            'eps': "EPS Prueba"
        }
    ]
    
    return render(request, 'consultar_paciente.html', {'pacientes': pacientes})

def actualizar_paciente(request, paciente_id):
    # Paciente de prueba (simulado)
    paciente = {
        'id': paciente_id,
        'nombre': "Paciente Prueba",
        'tipo_documento': "CC",
        'numero_documento': "123456789",
        'edad': 30,
        'eps': "EPS Prueba",
        'observaciones': "Observaciones iniciales del paciente"
    }
    
    return render(request, 'actualizar_paciente.html', {'paciente': paciente})
def guardar_actualizacion_paciente(request, paciente_id):
    # Aquí puedes manejar los datos enviados desde el formulario si fuera necesario
    if request.method == 'POST':
        print(f"Datos recibidos: {request.POST}")  # Para depuración
        # Redirige a la página de consulta o muestra un mensaje de éxito
        return HttpResponseRedirect(reverse('consultar_paciente'))
    # Si no es POST, redirige de nuevo
    return HttpResponseRedirect(reverse('consultar_paciente'))

def ver_historico_paciente(request, paciente_id):
    paciente = {
        'id': paciente_id,
        'nombre': "Paciente Prueba",
        'numero_documento': "123456789"
    }

    historico = [
        {
            'fecha': "2024-01-10",
            'diagnostico': "Infección respiratoria",
            'codigo_diagnostico': "J20",
            'servicio_asignado': "Consulta General",
            'observaciones': "Paciente presentó fiebre y tos seca."
        },
        {
            'fecha': "2024-02-15",
            'diagnostico': "Dolor lumbar",
            'codigo_diagnostico': "M54.5",
            'servicio_asignado': "Fisioterapia",
            'observaciones': "Inicio de terapia física; se recomienda seguimiento."
        }
    ]

    return render(request, 'ver_historico_paciente.html', {'paciente': paciente, 'historico': historico})

