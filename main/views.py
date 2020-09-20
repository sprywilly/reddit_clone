from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .errors import nice_errors
from .models import Profile
from .forms import *


def user_login(request):
    login_error = ""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                login_error = "Ваш пользователь заблокирован"
        else:
            login_error = nice_errors(form)
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form, 'login_error': login_error})


def registration(request):
    reg_error = ""
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            auth.logout(request)
            #new_user = auth.authenticate(username=user_form.cleaned_data['username'], \
            #                           password=user_form.cleaned_data['password'])
            auth.login(request, new_user)
            return render(request, 'main/registration_done.html', {'new_user': new_user})
        else:
            reg_error = nice_errors(user_form)
    else:
        user_form = RegistrationForm()
    return render(request, 'main/registration.html', {'user_form': user_form, 'reg_error': reg_error})


def user_logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save(commit=False)
            profile_form.save(commit=False)
            messages.success(request, 'профиль успешно обновлен')
        else:
            messages.error(request, 'ошибка при обновлении профиля')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'main/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def get_profile(request, user_id):
    profile = Profile.objects.get(id=user_id)
    return render(request, 'main/view_profile.html', {'profile': profile})
