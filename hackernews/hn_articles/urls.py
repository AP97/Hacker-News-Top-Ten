from django.urls import path, re_path
from hn_articles import views

urlpatterns = [
    path('', views.hn_articles, name='hn_articles'),
]