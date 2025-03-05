from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models  import ContentType
from .models import Disponibilidad

def setup_groups(sender, **kwargs):
    # Crear o recuperar el grupo "Alumnos"
    alumnos_group, _ = Group.objects.get_or_create(name='Alumnos')

    # Crear o recuperar el grupo "Instructores"
    instructores_group, _ = Group.objects.get_or_create(name='Instructores')

    alumnos_practico_group, _ = Group.objects.get_or_create(name='Alumnos_practicos')

    # Asignar permisos específicos al grupo "Instructores"
    permisos = [
        'add_schedule',  # Cambia "schedule" por el nombre de tu modelo
        'change_schedule',
        'delete_schedule',
        'view_schedule',
    ]

    content_type = ContentType.objects.get_for_model(Disponibilidad)
    for permiso_codename in permisos:
        try:
            permiso = Permission.objects.get(codename=permiso_codename, content_type=content_type)
            alumnos_group.permissions.add(permiso)
        except Permission.DoesNotExist:
            print(f"Permiso '{permiso_codename}' no encontrado.")

    # Asignar permisos de solo lectura al grupo "Alumnos"
    try:
        permiso_ver = Permission.objects.get(codename='view_schedule', content_type=content_type)
        instructores_group.permissions.add(permiso_ver)
    except Permission.DoesNotExist:
        print("Permiso 'view_schedule' no encontrado.")

    print("Grupos configurados correctamente.")