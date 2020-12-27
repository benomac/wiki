from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.rtrv_entry, name="rtrv_entry"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("edit/<str:to_edit>", views.edit, name="edit"),
    path("random_page", views.random_page, name="random_page")
]
