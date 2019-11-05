from django.urls import path, re_path
from hn_search import views

urlpatterns = [
    path('', views.hn_search, name='hn_search'),
]