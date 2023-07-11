from mailingapp.apps import MailingappConfig
from django.urls import path

from mailingapp.views import MainListView, ClientListView, ClientCreateView, ClientDeleteView, \
    MessageListView, MessageCreateView, MessageDeleteView, \
    MailingSettingsListView, MailingSettingsCreateView, MailingSettingsDeleteView

app_name = MailingappConfig.name

urlpatterns = [
    path('', MainListView.as_view(), name='main'),

    path('clients/', ClientListView.as_view(), name='clients'),
    path('clients/create', ClientCreateView.as_view(), name='client_create'),
    path('clients/delete', ClientDeleteView.as_view(), name='client_delete'),

    path('messages/', MessageListView.as_view(), name='messages'),
    path('messages/create', MessageCreateView.as_view(), name='message_create'),
    path('messages/delete', MessageDeleteView.as_view(), name='message_delete'),

    path('mailings/', MailingSettingsListView.as_view(), name='mailings'),
    path('mailings/create', MailingSettingsCreateView.as_view(), name='mailingsettings_create'),
    path('mailings/delete', MailingSettingsDeleteView.as_view(), name='mailingssettings_delete'),
]
