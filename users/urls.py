from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import MyLoginView

app_name = 'users'

urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
]
