from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all", views.all_pages, name="all"),
    path("wiki/<str:route>", views.return_by_title, name="page"),
    path("newpage", views.create_page, name="newpage"),
    path("newpage/<str:save_page_ifExists>", views.create_page, name="newpage"),
    path("search", views.search, name="search"),
    path("random", views.random_page, name="random"),
    path("wiki/<str:route>/edit", views.edit_page, name="edit"),
    path("warning", views.warning, name="warning" )
]
