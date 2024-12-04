# models.py
from django.db import models

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=10)
    numero_documento = models.CharField(max_length=20, unique=True)
    edad = models.IntegerField(default=0)
    eps = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre

class RegistroMedico(models.Model):
    paciente = models.ForeignKey(Paciente, related_name='registros', on_delete=models.CASCADE)
    fecha = models.DateField()
    descripcion = models.TextField()
    
    def __str__(self):
        return f"Registro de {self.paciente.nombre} - {self.fecha}"
