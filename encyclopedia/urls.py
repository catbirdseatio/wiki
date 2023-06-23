from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("random", views.random_entry, name="random"),
    path("search/<str:q>", views.search, name="search"),
    path("wiki/<str:title>", views.title, name="title"),
    path("wiki/<str:title>/update", views.update, name="update"),
    path("notfound", views.not_found, name="not_found"),
]
