from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache

import config.settings

from mailingapp.utils import sendmail
from mailingapp.models import Client, Message, MailingSettings, Statistic
from mailingapp.forms import ClientCreateForm, MessageCreateForm, MailingSettingsCreateForm, StatisticForm
from blog.models import Blog


class MainListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailingapp/main.html"

    def get_queryset(self):

        if config.settings.CACHE_ENABLED:
            key = 'main_blog'
            cache_data = cache.get(key)

            if cache_data is None:
                cache_data = Blog.objects.order_by('?')[:3]
                cache.set(key, cache_data)

        else:
            cache_data = Blog.objects.order_by('?')[:3]

        return cache_data

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Main"

        context["Blog"] = self.get_queryset()

        context["all_mailingsettings"] = len(MailingSettings.objects.all())
        context["active_mailingsettings"] = len(MailingSettings.objects.filter(is_published=True))
        context["all_client"] = len(Client.objects.all())
        context["unique_client"] = len(Client.objects.all().values('email').distinct())

        return context


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientCreateForm

    def get_context_data(self, *, object_list=None, context_object_name=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Add New Client"

        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailingapp:clients')

    def form_valid(self, form):

        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    fields = ["full_name", "comment", "email"]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Update Client"

        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailingapp:clients')

    def form_valid(self, form):
        return super().form_valid(form)


class ClientListView(ListView):
    model = Client

    def get_queryset(self):
        queryset = super().get_queryset().all()

        if not self.request.user.is_staff:
            queryset = super().get_queryset().filter(owner=self.request.user)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Client"
        context["Client"] = self.get_queryset()

        return context


class ClientDetailView(DetailView):
    model = Client

    def get_object(self, queryset=None):
        one_client = super().get_object()

        return one_client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Client Full Information"
        context["Client"] = self.get_object()

        return context


class ClientDeleteView(DeleteView):
    model = Client

    def get_context_data(self, *, object_list=None, context_object_name=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Delete Client"

        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailingapp:clients')


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Create Message Template"

        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailingapp:messages')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class MessageListView(ListView):
    model = Message

    def get_queryset(self):
        queryset = super().get_queryset().all()

        if not self.request.user.is_staff:
            queryset = super().get_queryset().filter(owner=self.request.user)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Message"
        context["Message"] = self.get_queryset

        return context


class MessageDetailView(DetailView):
    model = Message

    def get_object(self, queryset=None):
        one_message = super().get_object()
        return one_message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Message Full Information"
        context["Message"] = self.get_object()

        return context


class MessageUpdateView(UpdateView):
    model = Message
    fields = ["title", "body"]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Update Message"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailingapp:messages')

    def form_valid(self, form):
        return super().form_valid(form)


class MessageDeleteView(DeleteView):
    model = Message

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Delete Message"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailingapp:messages')


class MailingSettingsCreateView(CreateView):
    model = MailingSettings
    form_class = MailingSettingsCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Create New Mailing"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailingapp:mailings')

    def form_valid(self, form):

        # Create default data statistic
        current_mailing = self.object
        self.object = form.save()

        self.object.owner = self.request.user
        self.object.save()

        Statistic.objects.create(mailing_id=self.object.pk)

        schedule_mailing_time = self.object.time
        current_time = datetime.now().time()

        if schedule_mailing_time <= current_time:

            send_message = self.object.message.get_info()
            sendmail(self.object.pk, self.object.clients.all(), send_message[0], send_message[1])
            self.object.status = "FINISHED"
            self.object.save()

        return super().form_valid(form)


class MailingSettingsListView(ListView):
    model = MailingSettings

    def get_queryset(self):
        queryset = super().get_queryset().all()

        if not self.request.user.is_staff:
            queryset = super().get_queryset().filter(owner=self.request.user)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "MailingSettings"
        context["MailingSettings"] = MailingSettings.objects.all()

        return context


class MailingSettingsDetailView(DetailView):
    model = MailingSettings

    def get_object(self, queryset=None):
        one_mailing = super().get_object()
        return one_mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Mailing Full Information"
        current_object = self.get_object()

        context["Mailing"] = current_object
        context["Statistic"] = current_object.get_statistic[0]

        return context


class MailingSettingsUpdateView(UpdateView):
    model = MailingSettings
    fields = ["title", "time", "frequency", "message", "client", "is_published"]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Update Mailing"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailingapp:mailings')

    def form_valid(self, form):
        schedule_mailing_time_update = form.cleaned_data["time"]
        current_time = datetime.now().time()

        self.object.status = "CREATED"
        self.object.save()

        if schedule_mailing_time_update <= current_time and self.object.is_published is True:
            message_data = self.object.message.get_info()
            sendmail(self.object.pk, self.object.clients.all(), message_data[0], message_data[1])

            self.object.status = "FINISHED"
            self.object.save()

        return super().form_valid(form)


class MailingSettingsDeleteView(DeleteView):
    model = MailingSettings

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Delete Mailing"

        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailingapp:mailings')
