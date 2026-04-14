# ./apps/planner/views.py

from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from apps.planner.models import Project, ProjectPlace
from apps.planner.serializers import (
    ProjectCreateSerializer,
    ProjectPlaceAddSerializer,
    ProjectPlaceReadSerializer,
    ProjectPlaceUpdateSerializer,
    ProjectReadSerializer,
    ProjectUpdateSerializer,
)
from apps.planner.utils import check_delete_conditions


###### PROJECT VIEWS ######
class ProjectListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user).prefetch_related("places")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProjectCreateSerializer
        return ProjectReadSerializer


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "project_id"

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user).prefetch_related("places")

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return ProjectUpdateSerializer
        return ProjectReadSerializer

    def perform_destroy(self, instance):
        check_delete_conditions(instance)
        instance.delete()


###### PROJECT PLACE VIEWS ######
class ProjectPlaceListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_project(self):
        try:
            return Project.objects.get(
                id=self.kwargs["project_id"],
                user=self.request.user,
            )
        except Project.DoesNotExist:
            raise ValidationError("Project not found.")

    def get_queryset(self):
        project = self.get_project()
        return project.places.all().order_by("-created_at")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProjectPlaceAddSerializer
        return ProjectPlaceReadSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project"] = self.get_project()
        return context


class ProjectPlaceDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "place_id"

    def get_project(self):
        try:
            return Project.objects.get(
                id=self.kwargs["project_id"],
                user=self.request.user,
            )
        except Project.DoesNotExist:
            raise ValidationError("Project not found.")

    def get_queryset(self):
        project = self.get_project()
        return ProjectPlace.objects.filter(project=project)

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return ProjectPlaceUpdateSerializer
        return ProjectPlaceReadSerializer
    