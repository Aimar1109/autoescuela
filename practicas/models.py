from django.db import models
from django.contrib.auth.models import User


class Disponibilidad(models.Model):

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="disponibilidad", default=None)
    disp = models.JSONField(default=list)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="instructor", default=None, blank=True, null=True)

    def __str__(self):
        return f'{self.student}'


class FechaAprobado(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fecha_aprob", default=None)
    date = models.DateField()

    def __str__(self):
        return f'{self.student} - {self.date}'
    

class AlumnosInstructor(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="alumnos_instructor", default=None)
    alumnos = models.JSONField(default=list)

    def __str__(self):
        return f'{self.instructor}'