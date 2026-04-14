# ./apps/planner/admin.py

from django.contrib import admin
from .models import Project, ProjectPlace

###### PLACE ADMIN (INLINE) ######
class ProjectPlaceInline(admin.TabularInline):
    model = ProjectPlace
    extra = 0
    fields = ("external_id", "is_visited", "notes")
    readonly_fields = ()
    ordering = ("external_id",)

###### PROJECT ADMIN ######
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "user",
        "start_date",
        "is_completed",
        "created_at",
    )
    list_filter = (
        "is_completed",
        "start_date",
        "created_at",
    )
    search_fields = (
        "name",
        "description",
        "user__email",
        "user__username",
    )
    readonly_fields = ("created_at",)
    inlines = [ProjectPlaceInline]

    fieldsets = (
        (
            "Main info",
            {
                "fields": (
                    "user",
                    "name",
                    "description",
                    "start_date",
                    "is_completed",
                )
            },
        ),
        (
            "System info",
            {
                "fields": ("created_at",),
            },
        ),
    )

###### PLACE ADMIN ######
@admin.register(ProjectPlace)
class ProjectPlaceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "project",
        "external_id",
        "is_visited",
    )
    list_filter = ("is_visited", "project")
    search_fields = (
        "project__name",
        "notes",
        "external_id",
    )
    fields = (
        "project",
        "external_id",
        "notes",
        "is_visited",
    )
