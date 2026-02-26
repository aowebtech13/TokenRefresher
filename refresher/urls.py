from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('refresh/', views.trigger_refresh, name='trigger_refresh'),
]
