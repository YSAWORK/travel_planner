# ./apps/planner/serializers.py

from rest_framework import serializers
from django.db import transaction
from django.db.utils import IntegrityError

from apps.planner.models import Project, ProjectPlace
from apps.planner.utils import check_external_id_via_api, update_project_status


###### PLACE SERIALIZER ######
class ProjectPlaceReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPlace
        fields = (
            "id",
            "external_id",
            "notes",
            "is_visited",
        )
        read_only_fields = fields


class ProjectPlaceCreateSerializer(serializers.Serializer):
    external_id = serializers.IntegerField(min_value=1)
    notes = serializers.CharField(required=False, allow_blank=True, default="")

    @staticmethod
    def validate_external_id(value: int) -> int:
        """Validate that external_id exists in the Art Institute API."""
        return check_external_id_via_api(value)


class ProjectPlaceAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPlace
        fields = (
            "id",
            "external_id",
            "notes",
            "is_visited",
        )
        read_only_fields = (
            "id",
            "is_visited",
        )

    @staticmethod
    def validate_external_id(value: int) -> int:
        """Validate that external_id exists in the Art Institute API."""
        return check_external_id_via_api(value)

    def validate(self, attrs):
        project = self.context["project"]
        external_id = attrs["external_id"]
        if project.places.count() >= 10:
            raise serializers.ValidationError(
                {"places": ["Project cannot contain more than 10 places."]}
            )
        if project.places.filter(external_id=external_id).exists():
            raise serializers.ValidationError(
                {"external_id": ["This place is already added to the project."]}
            )
        return attrs

    def create(self, validated_data):
        project = self.context["project"]
        place = ProjectPlace.objects.create(project=project, **validated_data)
        update_project_status(project)
        return place


class ProjectPlaceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPlace
        fields = (
            "notes",
            "is_visited",
        )

    def update(self, instance: ProjectPlace, validated_data):
        instance.notes = validated_data.get("notes", instance.notes)
        instance.is_visited = validated_data.get("is_visited", instance.is_visited)
        instance.save(update_fields=["notes", "is_visited"])
        update_project_status(instance.project)
        return instance


###### PROJECT SERIALIZER ######
class ProjectReadSerializer(serializers.ModelSerializer):
    places = ProjectPlaceReadSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "description",
            "start_date",
            "is_completed",
            "created_at",
            "places",
        )
        read_only_fields = (
            "id",
            "is_completed",
            "created_at",
            "places",
        )

    @staticmethod
    def validate_name(value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Project name cannot be empty.")
        return value


class ProjectCreateSerializer(serializers.ModelSerializer):
    places = ProjectPlaceCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "description",
            "start_date",
            "is_completed",
            "places",
        )
        read_only_fields = (
            "id",
            "is_completed",
        )

    @staticmethod
    def validate_name(value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Project name cannot be empty.")
        return value

    @staticmethod
    def validate_places(value: list[dict]) -> list[dict]:
        if not value:
            raise serializers.ValidationError(
                "Project must contain at least one place."
            )
        if len(value) > 10:
            raise serializers.ValidationError(
                "Project cannot contain more than 10 places."
            )
        external_ids = [item["external_id"] for item in value]
        if len(external_ids) != len(set(external_ids)):
            raise serializers.ValidationError(
                "The same place cannot be added to the project more than once."
            )
        return value

    def create(self, validated_data):
        places_data = validated_data.pop("places")
        user = self.context["request"].user
        try:
            with transaction.atomic():
                project = Project.objects.create(user=user, **validated_data)

                project_places = [
                    ProjectPlace(
                        project=project,
                        external_id=place_data["external_id"],
                        notes=place_data.get("notes", ""),
                    )
                    for place_data in places_data
                ]
                ProjectPlace.objects.bulk_create(project_places)
                update_project_status(project)
                return project
        except IntegrityError:
            raise serializers.ValidationError(
                {
                    "places": [
                        "Duplicate external_id for the same project is not allowed."
                    ]
                }
            )


class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "description",
            "start_date",
            "is_completed",
            "created_at",
        )
        read_only_fields = (
            "id",
            "is_completed",
            "created_at",
        )

    @staticmethod
    def validate_name(value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Project name cannot be empty.")
        return value
