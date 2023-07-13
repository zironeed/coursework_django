from mailingapp.apps import MailingappConfig
from django.urls import path

from mailingapp.views import MainListView, ClientListView, ClientCreateView, ClientDeleteView, \
    MessageListView, MessageCreateView, MessageDeleteView, \
    MailingSettingsListView, MailingSettingsCreateView, MailingSettingsDeleteView, \
    ClientDetailView, ClientUpdateView, MessageDetailView, MessageUpdateView, MailingSettingsUpdateView, \
    MailingSettingsDetailView

app_name = MailingappConfig.name

urlpatterns = [
    path('', MainListView.as_view(), name='main'),

    path('clients/', ClientListView.as_view(), name='clients'),
    path('clients/create', ClientCreateView.as_view(), name='client_create'),
    path('clients/delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
    path('clients/update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
    path('clients/card/<int:pk>', ClientDetailView.as_view(), name='clients_card'),

    path('messages/', MessageListView.as_view(), name='messages'),
    path('messages/create', MessageCreateView.as_view(), name='message_create'),
    path('messages/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
    path('messages/update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('messages/card/<int:pk>', MessageDetailView.as_view(), name='message_card'),

    path('mailings/', MailingSettingsListView.as_view(), name='mailings'),
    path('mailings/create', MailingSettingsCreateView.as_view(), name='mailingsettings_create'),
    path('mailings/delete/<int:pk>', MailingSettingsDeleteView.as_view(), name='mailingssettings_delete'),
    path('mailings/update/<int:pk>', MailingSettingsUpdateView.as_view(), name='mailingssettings_update'),
    path('mailings/card/<int:pk>', MailingSettingsDetailView.as_view(), name='mailingssettings_card'),
]
