from django.db import models
from django.contrib.auth.models import User

class Paciente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    historia_clinica = models.TextField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
