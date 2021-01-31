from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.route, name="title"),
    path("search/", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random/", views.random_page, name="random"),
]
