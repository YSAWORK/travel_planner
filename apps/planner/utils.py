# ./apps/planner/utils.py
import httpx
from django.core.cache import cache
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException


def check_places_count(instance):
    """Checks places count"""
    from apps.planner.models import ProjectPlace

    if not instance.pk:
        places_count = ProjectPlace.objects.filter(project=instance.project).count()
        if places_count >= 10:
            raise ValidationError("Max 10 places allowed")


def update_project_status(project):
    """Check and update project completion status."""
    places = project.places.all()
    if places.exists() and all(place.is_visited for place in places):
        new_status = True
    else:
        new_status = False
    if project.is_completed != new_status:
        project.is_completed = new_status
        project.save(update_fields=["is_completed"])


def check_delete_conditions(project):
    """Checks delete conditions"""
    if project.places.filter(is_visited=True).exists():
        raise ValidationError(
            {"non_field_errors": ["Cannot delete project with visited places."]}
        )


def check_external_id_via_api(item_id: int) -> int:
    """Validate external id via Art Institute API"""
    cache_tll = getattr(settings, "CACHE_TTL", 3600)
    cache_key = f"external_id:{item_id}"
    cached = cache.get(cache_key)
    if cached is True:
        return item_id
    if cached is False:
        raise ValidationError("Place external id not found in Art Institute API")
    url = f"{settings.API_BASE_URL}/{item_id}"
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(url)
    except httpx.TimeoutException:
        raise APIException("External API timeout. Please try again later.")
    except httpx.RequestError:
        raise APIException("External API is unavailable. Please try again later.")
    if response.status_code == 200:
        cache.set(cache_key, True, cache_tll)
        return item_id
    if response.status_code == 404:
        cache.set(cache_key, False, cache_tll)
        raise ValidationError("Place external id not found in Art Institute API")
    raise APIException(f"Unexpected response from external API: {response.status_code}")
