from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import Users
from django import forms


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class UserRegisterForm(StyleFormMixin, UserCreationForm):

    class Meta:
        model = Users
        fields = ["email", "phone", "country", "avatar", "password1", "password2"]


class UserProfileForm(StyleFormMixin, UserChangeForm):

    class Meta:
        model = Users
        fields = ["email", "password", "first_name", "last_name", "phone", "country", "avatar"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()