from django.urls import path
from django.views.decorators.cache import cache_page

from mailing import views
from mailing.apps import MailingConfig

app_name = MailingConfig.name

# Урлы для работы с приложением рассылки, включают в себя рассылку и блог. Также идет кэширование домашней страницы
urlpatterns = [
    path('', cache_page(60)(views.HomePage.as_view(template_name='mailing/home_page.html')), name='homepage'),
    path('create/', views.MailingCreateView.as_view(template_name='mailing/mail_form.html'), name='create'),
    path('mailing/', views.MailingListView.as_view(template_name='mailing/mail_list.html'), name='mailing'),
    path('delete/<int:pk>', views.MailingDeleteView.as_view(), name='mailing_delete'),
    path('users_to_mail/', views.MailingUsersCreateView.as_view(template_name='mailing/create_clients.html'), name='users_to_mail'),
    path('update/<int:pk>', views.MailingUpdateView.as_view(template_name='mailing/mail_form.html'), name='update'),
    path('blog/', views.BlogListView.as_view(), name='blog'),
    path('blog/create/', views.BlogCreateView.as_view(), name='blog_create'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_details'),
    path('blog/update/<slug:slug>/', views.BlogUpdateView.as_view(), name='blog_update'),
    path('blog/delete/<slug:slug>/', views.BlogDeleteView.as_view(), name='blog_delete'),
    path('mailing_report/', views.MailingTryListView.as_view(template_name='mailing/mailing_report.html'), name='mailing_report'),
]
