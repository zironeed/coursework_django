from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView

from mailingapp.utils import sendmail
from mailingapp.models import Client, Message, MailingSettings
from mailingapp.forms import ClientCreateForm


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Create New Mailing"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailingapp:mailings')

    def form_valid(self, form):
        print("---------------------------------------------------------")
        self.object = form.save()
        send_message = self.object.message.get_info()

        for client in self.object.clients.all():
            print(client.email)
            sendmail(client.email, send_message[0], send_message[1])
        return super().form_valid(form)


class MailingSettingsListView(ListView):
    model = MailingSettings

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "MailingSettings"
        context["MailingSettings"] = MailingSettings.objects.all()
        return context


class MailingSettingsDeleteView(DeleteView):
    model = MailingSettings

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Delete Transmission"
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('mailing:transmissions')
