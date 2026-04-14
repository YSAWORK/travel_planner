# ./apps/planner/views.py


from drf_spectacular.utils import OpenApiResponse, extend_schema, OpenApiExample, extend_schema_view
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
@extend_schema_view(
    get=extend_schema(
        tags=["Projects"],
        summary="Отримати список проєктів",
        description="Отримати список усіх проєктів поточного користувача.",
        responses={
            200: OpenApiResponse(
                description="Список проєктів успішно отримано.",
                response=ProjectReadSerializer(many=True),
            ),
        },
    ),
    post=extend_schema(
        tags=["Projects"],
        summary="Створити проєкт",
        description="Створити новий проєкт для поточного користувача.",
        request=ProjectCreateSerializer,
        responses={
            201: OpenApiResponse(
                description="Проєкт успішно створено.",
                response=ProjectReadSerializer,
            ),
            400: OpenApiResponse(description="Помилка валідації."),
        },
        examples=[
            OpenApiExample(
                "Create Project Example",
                value={
                    "name": "Trip to Chicago",
                    "description": "Museums and city walk",
                    "start_date": "2026-04-20",
                },
                request_only=True,
            ),
        ],
    ),
)
class ProjectListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user).prefetch_related("places")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProjectCreateSerializer
        return ProjectReadSerializer


@extend_schema_view(
    get=extend_schema(
        tags=["Projects"],
        summary="Отримати проєкт",
        description="Отримати детальну інформацію про один проєкт поточного користувача.",
        responses={
            200: OpenApiResponse(
                description="Проєкт успішно отримано.",
                response=ProjectReadSerializer,
            ),
            404: OpenApiResponse(description="Проєкт не знайдено."),
        },
    ),
    put=extend_schema(
        tags=["Projects"],
        summary="Оновити проєкт повністю",
        description="Повністю оновити проєкт поточного користувача.",
        request=ProjectUpdateSerializer,
        responses={
            200: OpenApiResponse(
                description="Проєкт успішно оновлено.",
                response=ProjectReadSerializer,
            ),
            400: OpenApiResponse(description="Помилка валідації."),
            404: OpenApiResponse(description="Проєкт не знайдено."),
        },
    ),
    patch=extend_schema(
        tags=["Projects"],
        summary="Оновити проєкт частково",
        description="Частково оновити проєкт поточного користувача.",
        request=ProjectUpdateSerializer,
        responses={
            200: OpenApiResponse(
                description="Проєкт успішно оновлено.",
                response=ProjectReadSerializer,
            ),
            400: OpenApiResponse(description="Помилка валідації."),
            404: OpenApiResponse(description="Проєкт не знайдено."),
        },
    ),
    delete=extend_schema(
        tags=["Projects"],
        summary="Видалити проєкт",
        description="Видалити проєкт, якщо він не містить відвіданих місць.",
        responses={
            204: OpenApiResponse(description="Проєкт успішно видалено."),
            400: OpenApiResponse(description="Проєкт не можна видалити."),
            404: OpenApiResponse(description="Проєкт не знайдено."),
        },
    ),
)
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
@extend_schema_view(
    get=extend_schema(
        tags=["Project Places"],
        summary="Отримати список місць проєкту",
        description="Отримати список усіх місць, повʼязаних із конкретним проєктом.",
        responses={
            200: OpenApiResponse(
                description="Список місць проєкту успішно отримано.",
                response=ProjectPlaceReadSerializer(many=True),
            ),
            404: OpenApiResponse(description="Проєкт не знайдено."),
        },
    ),
    post=extend_schema(
        tags=["Project Places"],
        summary="Додати місце до проєкту",
        description="Додати нове місце до конкретного проєкту.",
        request=ProjectPlaceAddSerializer,
        responses={
            201: OpenApiResponse(
                description="Місце успішно додано до проєкту.",
                response=ProjectPlaceReadSerializer,
            ),
            400: OpenApiResponse(description="Помилка валідації."),
            404: OpenApiResponse(description="Проєкт не знайдено."),
        },
        examples=[
            OpenApiExample(
                "Add Project Place Example",
                value={
                    "external_id": 129884,
                    "notes": "Must visit this place first",
                },
                request_only=True,
            ),
        ],
    ),
)
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

@extend_schema_view(
    get=extend_schema(
        tags=["Project Places"],
        summary="Отримати місце проєкту",
        description="Отримати детальну інформацію про конкретне місце в межах проєкту.",
        responses={
            200: OpenApiResponse(
                description="Місце проєкту успішно отримано.",
                response=ProjectPlaceReadSerializer,
            ),
            404: OpenApiResponse(description="Місце або проєкт не знайдено."),
        },
    ),
    put=extend_schema(
        tags=["Project Places"],
        summary="Оновити місце проєкту повністю",
        description="Повністю оновити дані конкретного місця в проєкті.",
        request=ProjectPlaceUpdateSerializer,
        responses={
            200: OpenApiResponse(
                description="Місце проєкту успішно оновлено.",
                response=ProjectPlaceReadSerializer,
            ),
            400: OpenApiResponse(description="Помилка валідації."),
            404: OpenApiResponse(description="Місце або проєкт не знайдено."),
        },
    ),
    patch=extend_schema(
        tags=["Project Places"],
        summary="Оновити місце проєкту частково",
        description="Частково оновити дані конкретного місця в проєкті.",
        request=ProjectPlaceUpdateSerializer,
        responses={
            200: OpenApiResponse(
                description="Місце проєкту успішно оновлено.",
                response=ProjectPlaceReadSerializer,
            ),
            400: OpenApiResponse(description="Помилка валідації."),
            404: OpenApiResponse(description="Місце або проєкт не знайдено."),
        },
    ),
)
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
