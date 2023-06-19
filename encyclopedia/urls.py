from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/<str:q>", views.search, name="search"),
    path("wiki/<str:title>", views.title, name="title"),
    path("notfound", views.not_found, name="not_found"),
]
