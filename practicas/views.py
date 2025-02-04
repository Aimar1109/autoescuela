from django.shortcuts import render, redirect, get_object_or_404
from .models import Disponibilidad
from .forms import FechaDeAprobado
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, permission_required
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
            return redirect('home')


@login_required     
def signout(request):
    logout(request)
    return redirect('home')


@login_required
def alumno_aprobado(request):
    if request.method == "GET":
        return render(request, 'h.html', {
            'form': FechaDeAprobado()
        })
    else:
        Disponibilidad.objects.create(alumno=request.user, fecha_aprob=request.POST['fecha'])
        user = request.user
        my_group = Group.objects.get(name='Alumnos')
        my_group.user_set.add(user)
        return redirect('home')