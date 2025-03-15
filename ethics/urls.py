# ethics/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('form', views.submit_ethics_form, name='submit_ethics_form'),
]
