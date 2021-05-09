from django.contrib import admin
from django.urls import path
from .views import SearchView

urlpatterns = [
    path('', SearchView, name='search-request'),
]
