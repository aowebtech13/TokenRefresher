from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='token_dashboard'),
    path('api/new-tokens/', views.get_new_tokens, name='get_new_tokens'),
]
