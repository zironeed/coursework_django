from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView as BaseLoginView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
import config.settings
from users.forms import UserRegisterForm, UserProfileForm
from users.models import Users
from mailingapp.utils import sendmail_registration
from django.shortcuts import redirect
from django.contrib.auth import login


class TitleMixin(object):
    """Mixin for show title on pages"""
    title = None

    def get_title(self):
        return self.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Title'] = self.get_title()
        return context


class LoginView(TitleMixin, BaseLoginView):
    template_name = "users/login.html"
    title = "Login"


class LogoutView(BaseLogoutView):
    template_name = "users/login.html"


class RegisterView(TitleMixin, CreateView):
    form_class = UserRegisterForm
    template_name = "users/registration/registration_form.html"
    success_url = reverse_lazy('users:registration_reset')
    title = "Register New User"

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('users:confirm_email', kwargs={'uidb64': uid, 'token': token})
        current_site = config.settings.SITE_NAME
        sendmail_registration(
            user.email,
            "Registration on Site!",
            f"Accept your email address. Go on: http://{current_site}{activation_url}"
        )
        return redirect('users:email_confirmation_sent')


class UserConfirmationSentView(PasswordResetDoneView):
    template_name = "users/registration/registration_sent_done.html"


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = Users.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_confirmation_failed')


class UserConfirmedView(TitleMixin, TemplateView):
    template_name = 'users/registration/registration_confirmed.html'
    title = "Your email is activated."


class UserUpdateView(UpdateView):
    model = Users
    success_url = reverse_lazy("users:profile")
    form_class = UserProfileForm
    template_name = "users/profile.html"

    def get_object(self, queryset=None):
        return self.request.user


class UserResetView(PasswordResetView):
    template_name = "users/registration/password_reset_form.html"
    email_template_name = "users/registration/password_reset_email.html"
    success_url = reverse_lazy('users:password_reset_done')


class UserResetDoneView(PasswordResetDoneView):
    template_name = "users/registration/password_reset_done.html"


class UserResetConfirmView(PasswordResetConfirmView):
    template_name = "users/registration/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")


class UserResetCompleteView(PasswordResetCompleteView):
    template_name = "users/registration/password_reset_complete.html"
