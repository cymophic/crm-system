from django.urls import path

from . import views

app_name = "base"

urlpatterns = [
    # Index URL
    path("", views.IndexView.as_view(), name="index"),
]
