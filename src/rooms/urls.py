"""
URL configuration for helpy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path("profile/<int:pk>/", views.profile_view, name="profile"),
    path("profile/edit/", views.profile_edit_view, name="profile-edit"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("topics/", views.topics_list_view, name="topics-list"),
    path("activity/", views.activities_list_view, name="activity-list"),
    path("", views.rooms_list_view, name="rooms-list"),
    path("create", views.room_create_view, name="rooms-create"),
    path("<int:pk>/", views.room_detail_view, name="rooms-detail"),
    path("<int:pk>/update", views.room_update_view, name="rooms-update"),
    path("<int:pk>/delete", views.room_delete_view, name="rooms-delete"),
    path(
        "<int:pk>/message-delete_<int:id>/",
        views.message_delete_view,
        name="message-delete",
    ),
]
