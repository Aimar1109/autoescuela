from django import forms
from .models import Disponibilidad

class FechaDeAprobado(forms.Form):
    date = forms.DateField(
        label="Ingrese la fecha de aprobado",
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
            }
        )
    )

class CrearDisponibilidad(forms.ModelForm):
    class Meta:
        model = Disponibilidad
        fields = ['disp']
