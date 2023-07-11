from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, DetailView
from datetime import datetime, timezone

import pytz

from mailingapp.utils import sendmail
from mailingapp.models import Client, Message, MailingSettings, Statistic
from mailingapp.forms import ClientCreateForm, MessageCreateForm, MailingSettingsCreateForm, StatisticForm


class MainListView(ListView):
    model = Message
    template_name = "mailingapp/main.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Main"
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


class ClientListView(ListView):
    model = Client

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Clients"
        context["Clients"] = Client.objects.all()
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


class MessageListView(ListView):
    model = Message

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Messages"
        context["Messages"] = Message.objects.all()
        return context


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
        print(current_mailing)
        print()
        self.object = form.save()

        Statistic.objects.create(mailing_id=self.object.pk)
        schedule_mailing_time = self.object.time
        current_time = datetime.now().time()
        print(schedule_mailing_time, current_time)

        if schedule_mailing_time <= current_time:
            send_message = self.object.message.get_info()
            print("!SEND MESSAGE!")

            for client in self.object.clients.all():

                print(client.email)
                print(client)
                sendmail(client.email, send_message[0], send_message[1])

            current_time = datetime.now(pytz.timezone('Europe/Moscow'))
            print(current_time)

            wu = Statistic.objects.get(mailing_id=self.object.pk)
            wu.status = "FINISHED"
            wu.mail_answer = "OK"
            wu.time = datetime.now(pytz.timezone('Europe/Moscow'))
            wu.save()

        return super().form_valid(form)


class MailingSettingsListView(ListView):
    model = MailingSettings

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
        print(current_object.get_statistic[0])
        return context


class MailingSettingsDeleteView(DeleteView):
    model = MailingSettings

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Delete Transmission"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailing:transmissions')
