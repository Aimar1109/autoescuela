from django.shortcuts import render, redirect, get_object_or_404
from .models import Disponibilidad, FechaAprobado
from .forms import FechaDeAprobado, CrearDisponibilidad
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, permission_required
import json

HORARIO_HORAS = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "16:00", "17:00", "18:00", "19:00", "20:00"]
HORARIO_DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

# Create your views here.

def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                aprob = FechaAprobado.objects.filter(student=user)
                if aprob.exists():
                    request.session['aprobado'] = True
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exits'
                })
        return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Password do not match'
                })


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form':AuthenticationForm,
        })
    else:
        user = authenticate(request,username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
            'form':AuthenticationForm,
            'error': 'Username or password is incorrect'
        })
        else:
            login(request, user)
            aprob = FechaAprobado.objects.filter(student=user)
            if aprob.exists():
                request.session['aprobado'] = True
            elif user.groups.filter(name="Instructores").exists():
                request.session['instructor'] = True
            return redirect('home')


@login_required     
def signout(request):
    logout(request)
    return redirect('home')


@login_required
def alumno_aprobado(request):
    if request.method == "GET":
        return render(request, 'aprobado.html', {
            'form': FechaDeAprobado()
        })
    else:
        date = FechaAprobado.objects.filter(student=request.user)
        if date.exists():
            date.delete()
        FechaAprobado.objects.create(student=request.user, date=request.POST['date'])
        user = request.user
        my_group = Group.objects.get(name='Alumnos')
        my_group.user_set.add(user)
        request.session['aprobado'] = True
        return redirect('disponibilidad')
    

@login_required
def disponibilidad(request):
    if request.user.groups.filter(name='Alumnos').exists():
        if request.method == 'POST':
            disponibilidad = Disponibilidad.objects.filter(student=request.user)
            if disponibilidad.exists():
                disponibilidad.delete()
            disp = []
            disp_json = dict(json.loads(request.POST.get('disponibilidad')))
            for key in disp_json:
                disp.append(disp_json[key])
        
            n_disp = []
            for y in range(len(HORARIO_DIAS)):
                dia = []
                for x in range(y, len(disp), len(HORARIO_DIAS)):
                    dia.append(disp[x])
                n_disp.append(dia)

            disponibilidad = Disponibilidad(student=request.user, disp=n_disp)
            disponibilidad.save()
            return redirect('home')
        else:
            datos = {'horas': HORARIO_HORAS,
                     'dias': HORARIO_DIAS}
            return render(request, 'disponibilidad.html', {
                'form': CrearDisponibilidad(),
                'datos': datos
            })
    else:
        return redirect('fecha_aprob')

@login_required
def horario_instructor(request):
    if request.user.groups.filter(name='Instructores').exists():
        if request.method == "GET":
            alumnos_fecha = FechaAprobado.objects.values()
            alumnos_disp = Disponibilidad.objects.values()
            tabla = []
            id_tabla = {}
            counter = 0
            for alumno in alumnos_fecha:
                for alumno_disp in alumnos_disp:
                    if alumno['student_id'] == alumno_disp['student_id']:
                        tabla.append(alumno_disp['disp'])
                        id_tabla[counter] = alumno['student_id']
                        counter += 1

            alumno_list = [[None for x in range(len(HORARIO_HORAS))] for x in range(len(HORARIO_DIAS))]
            for hora in range(0, len(HORARIO_HORAS)):
                for alumno_ind in range(len(tabla)):
                    alumno_hora = [dia[hora] for dia in tabla[alumno_ind]]
                    if False in alumno_hora:
                        continue
                    for x in range(len(alumno_list)):
                        alumno_list[x][hora] = id_tabla[alumno_ind]
            
            print(alumno_list)
            return render(request, 'horario_instructor.html', {
                'alumnos': alumno_list,
                'dias': HORARIO_DIAS,
                'horas': HORARIO_HORAS,
                'horas_list': [x for x in range(len(HORARIO_HORAS))],
                'dias_list': [x for x in range(len(HORARIO_DIAS))],
            })
    else:
        return redirect('home')