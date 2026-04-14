# ./apps/planner/urls.py

from django.urls import path

from apps.planner import views

app_name = "app_planner"

###### URLs #######
urlpatterns = [
    path(
        "projects/", views.ProjectListCreateView.as_view(), name="project-list-create"
    ),
    path(
        "projects/<int:project_id>/",
        views.ProjectDetailView.as_view(),
        name="project-detail",
    ),
    path(
        "projects/<int:project_id>/places/",
        views.ProjectPlaceListCreateView.as_view(),
        name="project-place-list-create",
    ),
    path(
        "projects/<int:project_id>/places/<int:place_id>/",
        views.ProjectPlaceDetailView.as_view(),
        name="project-place-detail",
    ),
]
