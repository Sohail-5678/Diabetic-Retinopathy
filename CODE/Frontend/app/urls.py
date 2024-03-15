from . import views
from django.urls import path

urlpatterns = [
    path("home", views.index, name='index'),
    path("about", views.about, name='about'),
    path("upload", views.upload, name='upload'),
    path("result", views.upload, name='result'),
    path("", views.login, name='login'),
    path("register", views.register, name='register'),
    path("graphs", views.graphs, name="graphs")
]
