from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView

from mailingapp.models import Client, Message, MailingSettings


class MainListView(ListView):
    model = Message


class ClientCreateView(CreateView):
    model = Client


class ClientListView(ListView):
    model = Client


class ClientDeleteView(DeleteView):
    model = Client


class MessageCreateView(CreateView):
    model = Message


class MessageListView(ListView):
    model = Message


class MessageDeleteView(DeleteView):
    model = Message


class MailingSettingsCreateView(CreateView):
    model = MailingSettings


class MailingSettingsListView(ListView):
    model = MailingSettings


class MailingSettingsDeleteView(DeleteView):
    model = MailingSettings
