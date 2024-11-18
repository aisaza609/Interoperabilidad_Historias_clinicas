from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
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
