from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from client.apps import ClientConfig
from client.views import RegisterView, ProfileView, ActivateAccount, generate_new_password, ProfileDeleteView

app_name = ClientConfig.name
'''Тут находятся урлы для работы с приложением клиент. Подключены логин, логаут, просмотр и изменение профиля, активация, генерация пароля и удаление профиля'''
urlpatterns = [
    path('', LoginView.as_view(template_name='client/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('profile/genpassword/', generate_new_password, name='generate_new_password'),
    path('delete/<int:pk>', ProfileDeleteView.as_view(), name='profile_delete'),
]
