import random
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect

from django.urls import reverse_lazy
from django.views import generic

from client.models import MailingClient
from config import settings
from mailing import models, forms
from mailing.models import Blog
from mailing.services import get_cached_for_blog_list


# Create your views here.
class HomePage(generic.TemplateView):
    '''Контроллер домашней страницей с получением контакстных данных для передачи в html файл'''
    template_name = "home_page.html"

    def get_context_data(self, **kwargs):
        context = {}
        mails = models.Mail.objects.all().count()
        active = models.MailingSettings.objects.filter(mailing_status='AC').values_list().count(),
        clients = models.MailingClient.objects.all().count()
        random_article = models.Blog.objects.order_by('?')[:3]
        context['mails'] = mails
        context['active'] = active[0]
        context['clients'] = clients
        context['random_article'] = random_article
        return context


class MailingCreateView(LoginRequiredMixin, generic.CreateView):
    '''Контроллер создания рассылки'''
    template_name = "mailing/mail_form.html"
    model = models.MailingSettings
    form_class = forms.SettingsForm
    success_url = reverse_lazy('mailing:homepage')
    mail_data = ''
    mail_status = 'OK'

    def get_context_data(self, **kwargs):
        '''Функция получения контекстных данных и создания подформы с сообщением'''
        context_data = super().get_context_data(**kwargs)
        MailFormset = inlineformset_factory(models.MailingSettings, models.Mail, form=forms.MailForm, can_delete=False,
                                            extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = MailFormset(self.request.POST or None, instance=self.object)
        else:
            context_data['formset'] = MailFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        '''Функция для валидации формы, получения данных и их обработки'''
        data = self.get_context_data()
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()
        formset = data['formset']
        client_email = []
        mailing_subject = ''
        mailing_body = ''
        for fo in formset:
            if fo.is_valid():
                clients = fo.cleaned_data.get('client_to_message').values_list()
                for i in clients:
                    client_email.append(i[2])
                mailing_subject = fo.cleaned_data.get('mailing_subject')
                mailing_body = fo.cleaned_data.get('mailing_body')
                all_clients = fo.cleaned_data.get('all_clients')
                if all_clients:
                    client_email = list(MailingClient.objects.all().values_list('contact_email', flat=True))
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.mailing_status = "AC"
            mailing.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.author = self.request.user
            formset.save()
        self.object.save()
        ct = datetime.now()
        '''Тут сверяется время рассылки и если она истекла, то она отключается'''
        try:
            if self.object.mailing_time_start.timestamp() <= ct.timestamp() <= self.object.mailing_time_end.timestamp():
                sending = send_mail(mailing_subject, mailing_body, settings.DEFAULT_FROM_EMAIL,
                                    recipient_list=client_email,
                                    fail_silently=False)
                if sending == 1:
                    self.mail_status = 'OK'
                else:
                    self.mail_status = 'Не отправлено'

            if (self.object.mailing_periods == "DL") and ((
                                                                  self.object.mailing_time_end - self.object.mailing_time_start) <= timedelta(
                days=1)):
                self.object.mailing_status = 'FI'
                self.object.save()
            elif (self.object.mailing_periods == "WL") and ((
                                                                    self.object.mailing_time_end - self.object.mailing_time_start) <= timedelta(
                days=6)):
                self.object.mailing_status = 'FI'
                self.object.save()
            elif (self.object.mailing_periods == "ML") and ((
                                                                    self.object.mailing_time_end - self.object.mailing_time_start) <= timedelta(
                days=30)):
                self.object.mailing_status = 'FI'
                self.object.save()

            models.MailingTry.objects.create(mailing=self.object, mailing_try=datetime.now(),
                                             mailing_try_status=self.object.mailing_status,
                                             mailing_response=self.mail_status)
            return super().form_valid(form)
        except AttributeError:
            form.add_error(None, 'Установите дату рассылки.')
            return super(MailingCreateView, self).form_invalid(form)


class MailingListView(LoginRequiredMixin, generic.ListView):
    '''Контроллер списка рассылок'''
    template_name = "mailing/mail_list.html"
    model = models.Mail
    paginate_by = 10
    extra_context = {
        'title': 'Мои рассылки'
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.author != self.request.user and not self.request.user.status_type == 'MANAGER':
            raise PermissionDenied
        return self.object

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class MailingDeleteView(LoginRequiredMixin, generic.DeleteView):
    '''Контроллер для удаления рассылки'''
    model = models.Mail
    success_url = reverse_lazy('mailing:mailing')

    def delete(self, request, *args, **kwargs):
        # Получаем объект рассылки
        self.object = self.get_object()

        # Удаляем рассылку
        self.object.delete()

        messages.success(request, 'Рассылка успешно удалена.')

        return redirect(self.success_url)


class MailingUsersCreateView(LoginRequiredMixin, generic.CreateView):
    '''Контроллер для создания получателей рассылки'''
    template_name = "mailing/create_clients.html"
    model = models.MailingClient
    form_class = forms.MailingClientForm
    success_url = reverse_lazy('mailing:homepage')

    def form_valid(self, form):
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()

        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, generic.UpdateView):
    '''Контроллер для изменения рассылки. Все тоже самое, как и в создании, только с проверкой, что пользователь является автором'''
    template_name = "mailing/mail_form.html"
    model = models.MailingSettings
    form_class = forms.SettingsForm
    success_url = reverse_lazy('mailing:mailing')
    mail_data = ''
    mail_status = 'OK'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.author != self.request.user:
            raise PermissionDenied
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MailFormset = inlineformset_factory(models.MailingSettings, models.Mail, form=forms.MailForm, can_delete=False,
                                            extra=0, edit_only=True)
        if self.request.method == 'POST':
            context_data['formset'] = MailFormset(self.request.POST or None, instance=self.object)
        else:
            context_data['formset'] = MailFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        data = self.get_context_data()
        self.object = form.save()
        formset = data['formset']
        client_email = []
        mailing_subject = ''
        mailing_body = ''
        for fo in formset:
            if fo.is_valid():
                clients = fo.cleaned_data.get('client_to_message').values_list()
                for i in clients:
                    client_email.append(i[2])
                mailing_subject = fo.cleaned_data.get('mailing_subject')
                mailing_body = fo.cleaned_data.get('mailing_body')
                all_clients = fo.cleaned_data.get('all_clients')
                if all_clients:
                    client_email = list(MailingClient.objects.all().values_list('contact_email', flat=True))
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.mailing_status = "AC"
            mailing.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        self.object.save()
        ct = datetime.now()

        try:
            if self.object.mailing_time_start.timestamp() <= ct.timestamp() <= self.object.mailing_time_end.timestamp():
                sending = send_mail(mailing_subject, mailing_body, settings.DEFAULT_FROM_EMAIL,
                                    recipient_list=[client_email],
                                    fail_silently=False)
                if sending == 1:
                    self.mail_status = 'OK'
                else:
                    self.mail_status = 'Не отправлено'

            if (self.object.mailing_periods == "DL") and ((
                                                                  self.object.mailing_time_end - self.object.mailing_time_start) <= timedelta(
                days=1)):
                self.object.mailing_status = 'FI'
                self.object.save()
            elif (self.object.mailing_periods == "WL") and ((
                                                                    self.object.mailing_time_end - self.object.mailing_time_start) <= timedelta(
                days=6)):
                self.object.mailing_status = 'FI'
                self.object.save()
            elif (self.object.mailing_periods == "ML") and ((
                                                                    self.object.mailing_time_end - self.object.mailing_time_start) <= timedelta(
                days=30)):
                self.object.mailing_status = 'FI'
                self.object.save()

            models.MailingTry.objects.create(mailing=self.object, mailing_try=datetime.now(),
                                             mailing_try_status=self.object.mailing_status,
                                             mailing_response=self.mail_status)
            return super().form_valid(form)
        except AttributeError:
            form.add_error(None, 'Установите дату рассылки.')
            return super(MailingUpdateView, self).form_invalid(form)


class BlogListView(generic.ListView):
    '''Контроллер для просмотра списка блога'''
    model = Blog
    paginate_by = 3
    extra_context = {
        'title': 'Блог'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['object'] = get_cached_for_blog_list
        return context_data


class BlogDetailView(generic.DetailView):
    '''Контроллер для просмотра статьи блога'''
    model = Blog

    def get_object(self):
        obj = super().get_object()
        obj.total_views += 1
        obj.save()

        return obj


class BlogCreateView(LoginRequiredMixin, generic.CreateView, UserPassesTestMixin):
    '''Контроллер для создания статьи блога'''
    model = Blog
    fields = ("name", "post", "image")

    def test_func(self):
        return self.request.user.status_type == 'CONTENT_MANAGER'


class BlogUpdateView(LoginRequiredMixin, generic.UpdateView, UserPassesTestMixin):
    '''Контроллер для редактирования статьи блога'''
    model = Blog
    fields = ("name", "post", "image")
    success_url = reverse_lazy('mailing:blog')

    def test_func(self):
        return self.request.user.status_type == 'CONTENT_MANAGER'


class BlogDeleteView(LoginRequiredMixin, generic.DeleteView):
    '''Контроллер для удаления статьи блога'''
    model = Blog
    fields = ("name", "post", "image", "slug")
    success_url = reverse_lazy('mailing:blog')


class MailingTryListView(LoginRequiredMixin, generic.ListView):
    '''Контроллер для просмотра отчета по отправкам'''
    template_name = "mailing/mailing_report.html"
    model = models.MailingTry
    paginate_by = 10
    extra_context = {
        'title': 'Отчет по рассылкам'
    }
