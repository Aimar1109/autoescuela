from django.shortcuts import render, redirect, get_object_or_404
from .models import Disponibilidad, FechaAprobado, AlumnosInstructor
from .forms import FechaDeAprobado, CrearDisponibilidad
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, permission_required
import datetime
import json

HORARIO_HORAS = ["09:00", "10:00", "11:00", "12:00", "13:00", "16:00", "17:00", "18:00", "19:00"]
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
                if not AlumnosInstructor.objects.filter(instructor=request.user).exists():
                    AlumnosInstructor.objects.create(instructor=request.user, alumnos=[[None for x in range(len(HORARIO_HORAS))] for x in range(len(HORARIO_DIAS))])
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
        fecha_usuario = datetime.datetime.strptime(request.POST['date'], '%Y-%m-%d').date()
        if fecha_usuario > datetime.date.today():
            return render(request, 'aprobado.html', {
            'form': FechaDeAprobado(),
            'error': "Introduce la fecha de hoy o anterior."
        })
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
            skip = []
            for alumno in alumnos_fecha:
                for alumno_disp in alumnos_disp:
                    if alumno['student_id'] == alumno_disp['student_id']:
                        tabla.append(alumno_disp['disp'])
                        id_tabla[counter] = alumno['student_id']
                        counter += 1

            instructor = AlumnosInstructor.objects.get(instructor=request.user)
            alumnos_list = instructor.alumnos

            #print(alumnos_list)
            
            for hora in range(0, len(HORARIO_HORAS)):
                if alumnos_list[0][hora] != None:
                    continue
                find = False
                for alumno_ind in range(len(tabla)):
                    if alumno_ind not in skip:
                        alumno_hora = [dia[hora] for dia in tabla[alumno_ind]]
                        if False in alumno_hora:
                            continue
                        
                        disponibilidad = Disponibilidad.objects.get(student_id=id_tabla[alumno_ind])
                        disponibilidad.instructor = request.user
                        disponibilidad.save()
                        
                        skip.append(alumno_ind)
                        for x in range(len(alumnos_list)):
                            alumnos_list[x][hora] = id_tabla[alumno_ind]
                        break
            
            instructor.alumnos = alumnos_list

            instructor.save()

            HORARIO_HORAS_p = [["09:00",[]], 
                               ["10:00",[]], 
                               ["11:00",[]], 
                               ["12:00",[]], 
                               ["13:00",[]], 
                               ["16:00",[]], 
                               ["17:00",[]], 
                               ["18:00",[]], 
                               ["19:00",[]]]

            for h in range(len(HORARIO_HORAS_p)):
                if alumnos_list[0][h] == None:
                    HORARIO_HORAS_p[h][1] = ["" for x in range(5)]
                    continue
                HORARIO_HORAS_p[h][1] = [User.objects.get(id=alumnos_list[0][h]).username for x in range(5)]


            return render(request, 'horario_instructor.html', {
                'alumnos': alumnos_list,
                'dias': HORARIO_DIAS,
                'alumnos': HORARIO_HORAS_p
            })
    else:
        return redirect('home')
    


@login_required
def practico_aprobado(request):
    if request.method == 'GET':
        return render(request, 'practico_aprobado.html', {
            'form': FechaDeAprobado()
        })
    else:
        fecha_usuario = datetime.datetime.strptime(request.POST['date'], '%Y-%m-%d').date()
        teorico_fecha = FechaAprobado.objects.get(student=request.user).date

        if fecha_usuario > datetime.date.today() or fecha_usuario < teorico_fecha:
            return render(request, 'practico_aprobado.html', {
            'form': FechaDeAprobado(),
            'error': "Introduce la fecha de hoy o anterior y mayor a la fecha de aprobado del teorico."
        })

        request.session['aprobado'] = False
        my_group = Group.objects.get(name='Alumnos_practicos')
        my_group.user_set.add(request.user)

        del_group = Group.objects.get(name='Alumnos')
        del_group.user_set.remove(request.user)
        
        instructor = AlumnosInstructor.objects.get(instructor=Disponibilidad.objects.get(student=request.user).instructor)
        for dia in range(len(instructor.alumnos)):
            for hora in range(len(instructor.alumnos[dia])):
                if instructor.alumnos[dia][hora] == request.user.id:
                    instructor.alumnos[dia][hora] = None
        
        instructor.save()

        FechaAprobado.objects.filter(student=request.user).delete()
        Disponibilidad.objects.filter(student=request.user).delete()

        return redirect('home')