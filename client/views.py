from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from config import settings
from client.forms import UserRegisterForm, UserProfileForm
from client.models import User

from django.contrib.auth import login
from django.utils.http import urlsafe_base64_decode

from client.tokens import email_verification_token


# Create your views here.
class RegisterView(CreateView):
    '''Регистрация пользователя с получением заполненной формы и передачей этой формы в создание письма подтверждения емейла'''
    model = User
    form_class = UserRegisterForm
    template_name = 'client/register.html'
    success_url = reverse_lazy('client:login')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        subject = 'Завершение регистрации'
        message = render_to_string('client/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': email_verification_token.make_token(user),
        })
        if user.email_user(subject, message):
            print('Отправлено')

        messages.success(self.request, ('Пожалуйста подтвердите ваш email для завершения регистрации.'))
        return redirect(self.success_url)


class ProfileView(UpdateView):
    '''Класс для просмотра и редактирования профиля пользователя'''
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('client:profile')

    def get_object(self, queryset=None):
        return self.request.user


class ActivateAccount(View):
    '''Класс для активации аккаунта после подтверждения почты'''
    success_url = reverse_lazy('client:login')

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and email_verification_token.check_token(user, token):
            user.is_active = True
            user.email_verify = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('client:profile')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('client:profile')


def generate_new_password(request):
    '''Функция для создания нового пароля и отправки его на почту'''
    password = User.objects.make_random_password()
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль: {password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(password)
    request.user.save()
    return redirect(reverse('client:login'))


class ProfileDeleteView(DeleteView):
    '''Класс для удаления профиля пользователя'''
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('client:login')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Удаление профиля пользователя
        self.object.delete()

        messages.success(request, 'Профиль успешно удален.')
        return redirect(self.success_url)
