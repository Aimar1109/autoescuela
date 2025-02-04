from django import forms

class FechaDeAprobado(forms.Form):
    fecha = forms.DateField(
        label="Ingrese la fecha de aprobado",
        widget=forms.DateInput(
            attrs={
                'type': 'date',  # Esto genera un selector de fecha en navegadores modernos
                'class': 'form-control',  # Bootstrap o cualquier clase CSS personalizada
            }
        )
    )
