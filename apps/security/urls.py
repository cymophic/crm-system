from django.urls import path

from . import views

app_name = "security"
urlpatterns = [
    # Complete User Profile
    path(
        "complete-profile/",
        views.CompleteProfileView.as_view(),
        name="complete_profile",
    ),
    # Edit User Profile
    path("profile/edit/", views.EditProfileView.as_view(), name="edit_profile"),
]
