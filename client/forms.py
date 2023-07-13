from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from client.models import User


class UserRegisterForm(UserCreationForm):
    '''Форма для регистрации пользователя'''
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserProfileForm(UserChangeForm):
    '''Форма для профиля пользователя. В ините убираем редактирование пароля'''
    class Meta:
        model = User
        fields = ('full_name', 'email', )

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
