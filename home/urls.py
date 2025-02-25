from django.urls import path
from .views import github_webhook
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("webhook/", github_webhook, name="github_webhook"),
]
