from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.views.generic import ListView, FormView

from .errors import nice_errors
from .models import Profile
from .forms import *
from post.models import Post


class UserLoginView(FormView):
    """
    Представление авторизации пользователя
    """
    form_class = LoginForm
    template_name = 'main/login.html'
    login_error = ""

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(self.request, user)
                return HttpResponseRedirect('/')
            else:
                login_error = "Ваш пользователь заблокирован"
        else:
            login_error = nice_errors(form)
        return render(request, self.template_name, {'form': form, 'login_error': login_error})



class RegistrationView(FormView):
    """
    Регистрация пользователя
    """

    template_name = 'main/registration.html'
    form_class = RegistrationForm

    def get(self, request):
        user_form = self.form_class
        return render(request, self.template_name, {'user_form': user_form})


    def post(self, request):
        reg_error = ""
        user_form = RegistrationForm(self.request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            auth.logout(request)
            auth.login(request, new_user)
            return render(request, 'main/registration_done.html', {'new_user': new_user})
        else:
            reg_error = nice_errors(user_form)
        return render(request, self.template_name, {'user_form': user_form, 'reg_error': reg_error})



class UpdateProfileView(FormView):
    """
    Представление для обновления профиля пользователя
    Здесь можно заполнить информацию для расширенной модели пользователя
    """

    template_name = 'main/edit_profile.html'
    form_class = RegistrationForm
    

    def get(self, request):
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, self.template_name, locals())

    def post(self, request):
        upd_error = ""
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'профиль успешно обновлен')
        else:
            upd_error = nice_errors(profile_form)
        return render(request, self.template_name, {
        'user_form': user_form,
        'profile_form': profile_form,
        'upd_error': upd_error,
    })


class ProfileListView(ListView):
    """
    Вьюха просмотра профиля пользователя
    """
    context_object_name = 'posts'
    template_name = 'main/view_profile.html'

    def get_queryset(self):
        self.author = get_object_or_404(Profile, user__id=self.kwargs['user_id'])
        return Post.objects.filter(author__id=self.kwargs['user_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.author
        return context
