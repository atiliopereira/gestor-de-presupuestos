from django.contrib.auth import login
from django.contrib.auth.models import Group, Permission
from django.db import transaction
from django.shortcuts import render, redirect

from sistema.forms import UsuarioForm, SignUpForm


@transaction.atomic
def signup(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        usuario_form = UsuarioForm(request.POST)

        if signup_form.is_valid() and usuario_form.is_valid():
            user = signup_form.save()
            user.refresh_from_db()
            user.usuario.usuario.is_staff = True
            grupo, creado = Group.objects.get_or_create(name='usuarios')
            if creado:
                permisos = Permission.objects.all()
                for permiso in permisos:
                    grupo.permissions.add(permiso)
            grupo.user_set.add(user.usuario.usuario)
            user.save()

            usuario_form = UsuarioForm(request.POST, instance=user.usuario)
            usuario_form.full_clean()
            usuario_form.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('/admin')
    else:
        signup_form = SignUpForm()
        usuario_form = UsuarioForm()
    return render(request, 'admin/sistema/usuario/signup.html', {
        'signup_form': signup_form,
        'usuario_form': usuario_form,
    })
