from django import forms
from django.contrib import auth 
from django.contrib.auth.models import User

from .models import Profile


# Форма авторизации
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control","placeholder":"Логин"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control","placeholder":"Пароль"}))

    def clean(self):
        if 'password' not in self.cleaned_data and 'username' not in self.cleaned_data:
            raise forms.ValidationError('Заполните поля')

        if 'password' in self.cleaned_data and 'username' not in self.cleaned_data:
            raise forms.ValidationError('Имя пользователя обязательное поле')

        if 'username' in self.cleaned_data and 'password' not in self.cleaned_data:
            raise forms.ValidationError('Пароль обязательное поле')

        if 'username' in self.cleaned_data and 'password' in self.cleaned_data:
            self.user = auth.authenticate(username = self.cleaned_data['username'],
                                     password = self.cleaned_data['password'])
            if self.user is None:
                raise forms.ValidationError('Пользователь с таким логином и паролем не найден.')
       
        return self.cleaned_data



# Форма регистрации
class RegistrationForm(forms.ModelForm):
    username = forms.RegexField(regex=r'^[a-zA-Z0-9 \w._]+$',max_length=30,min_length = 6,
        help_text = ("Имя пользоваетля может содержать только буквы и должно быть не менее 6 символов и не более 30"),
        error_messages={'invalid': ("Имя пользователя может содержать только буквы")},
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder":"Имя пользователя"}))
    password = forms.CharField(label='Пароль', min_length = 8,
        widget=forms.PasswordInput(attrs={"class": "form-control","placeholder":"Пароль"}), 
                                error_messages={'required': 'Укажите пароль'})
    password2 = forms.CharField(label='Повторите пароль', min_length = 8,
        widget=forms.PasswordInput(attrs={"class": "form-control","placeholder":"Еще раз пароль"}),
                                error_messages={'required': 'Укажите пароль еще раз'})
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        else:
            raise forms.ValidationError('Пользователь с таким именем уже существует')

    def clean(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError({'password': 'Пароли не совпадают.'})
        return cd

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# Форма для обновления данных пользователя
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

        widgets= {'first_name':forms.TextInput(attrs={"class": "form-control", "placeholder":"Ваше имя"}),
                'last_name':forms.TextInput(attrs={"class": "form-control", "placeholder":"Ваша фамилия"}),
                'email': forms.TextInput(attrs={"class":"xlarge","placeholder":"example@mail.com"}),
        }

# Форма для обновления профиля пользователя
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('about_me', 'birthday', 'phone')
        widgets= {'birthday':forms.DateInput(attrs={"class": "form-control", "placeholder":"23.11.1990"}),
                'about_me':forms.Textarea(attrs={"class": "form-control", "rows": "5",
                                                "placeholder":"Расскажите о себе"}),
                'phone': forms.TextInput(attrs={"class":"xlarge","placeholder":"+79817654321"}),
        }