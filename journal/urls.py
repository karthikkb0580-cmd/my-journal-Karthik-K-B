from django.urls import path
from . import views

app_name = "journal"

urlpatterns = [
    path("", views.home, name="home"),
    path("articles/", views.article_list, name="article_list"),
    path("articles/mine/", views.my_articles, name="my_articles"),
    path("articles/new/", views.article_create, name="article_create"),
    path("articles/<int:pk>/", views.article_detail, name="article_detail"),
    path("articles/<int:pk>/edit/", views.article_update, name="article_update"),
    path("articles/<int:pk>/delete/", views.article_delete, name="article_delete"),
]


