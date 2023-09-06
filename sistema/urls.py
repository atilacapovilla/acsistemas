from django.urls import path
from .views import home, SistemaList

app_name = 'sistema'

urlpatterns = [
    path('', home, name='home'),
    path('sistema/', SistemaList.as_view(), name='sistema'),
]
