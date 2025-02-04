from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Disponibilidad(models.Model):
    alumno = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_aprob = models.DateField(default=None)

    l_nueve = models.BooleanField(default=False)
    l_diez = models.BooleanField(default=False)
    l_once = models.BooleanField(default=False)
    l_doce = models.BooleanField(default=False)
    l_una = models.BooleanField(default=False)
    l_cuatro = models.BooleanField(default=False)
    l_cinco = models.BooleanField(default=False)
    l_seis = models.BooleanField(default=False)
    l_siete = models.BooleanField(default=False)

    ma_nueve = models.BooleanField(default=False)
    ma_diez = models.BooleanField(default=False)
    ma_once = models.BooleanField(default=False)
    ma_doce = models.BooleanField(default=False)
    ma_una = models.BooleanField(default=False)
    ma_cuatro = models.BooleanField(default=False)
    ma_cinco = models.BooleanField(default=False)
    ma_seis = models.BooleanField(default=False)
    ma_siete = models.BooleanField(default=False)

    mi_nueve = models.BooleanField(default=False)
    mi_diez = models.BooleanField(default=False)
    mi_once = models.BooleanField(default=False)
    mi_doce = models.BooleanField(default=False)
    mi_una = models.BooleanField(default=False)
    mi_cuatro = models.BooleanField(default=False)
    mi_cinco = models.BooleanField(default=False)
    mi_seis = models.BooleanField(default=False)
    mi_siete = models.BooleanField(default=False)

    j_nueve = models.BooleanField(default=False)
    j_diez = models.BooleanField(default=False)
    j_once = models.BooleanField(default=False)
    j_doce = models.BooleanField(default=False)
    j_una = models.BooleanField(default=False)
    j_cuatro = models.BooleanField(default=False)
    j_cinco = models.BooleanField(default=False)
    j_seis = models.BooleanField(default=False)
    j_siete = models.BooleanField(default=False)

    v_nueve = models.BooleanField(default=False)
    v_diez = models.BooleanField(default=False)
    v_once = models.BooleanField(default=False)
    v_doce = models.BooleanField(default=False)
    v_una = models.BooleanField(default=False)
    v_cuatro = models.BooleanField(default=False)
    v_cinco = models.BooleanField(default=False)
    v_seis = models.BooleanField(default=False)
    v_siete = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.alumno} - {self.fecha_aprob}'