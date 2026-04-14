# ./planner/models.py

from django.db import models

from apps.auth.models import User
from apps.planner.utils import (
    check_places_count,
    update_project_status,
    check_delete_conditions)


###### PROJECTS ######
class Project(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name='user',
    )
    name = models.CharField(
        max_length=255,
        help_text='Project name',
        verbose_name='project name',
    )
    description = models.TextField(
        blank=True,
        help_text='Project description (optional)',
        verbose_name='project description',
    )
    start_date = models.DateField(
        null=True,
        blank=True,
        help_text='Start date of project (optional)',
        verbose_name='start date',
    )
    is_completed = models.BooleanField(
        default=False,
        help_text='Project completed status',
        verbose_name='completed status',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='created at',
        help_text='Project created time',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='updated at',
        help_text='Project updated time',
    )

    def delete(self, *args, **kwargs):
        check_delete_conditions(self)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'project'
        verbose_name_plural = 'projects'
        unique_together = (('user', 'name'),)


##### PROJECT PLACES ######
class ProjectPlace(models.Model):
    project = models.ForeignKey(
        Project,
        related_name="places",
        on_delete=models.CASCADE,
        help_text='Project place',
        verbose_name='project place',
    )
    external_id = models.IntegerField(
        help_text='Project external id',
        verbose_name='external id',
    )
    notes = models.TextField(
        blank=True,
        help_text='Project notes',
        verbose_name='project notes',
    )
    is_visited = models.BooleanField(
        default=False,
        help_text='Project visited status',
        verbose_name='visited status',
    )

    def clean(self):
        check_places_count(self)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        update_project_status(self.project)

    def delete(self, *args, **kwargs):
        project = self.project
        super().delete(*args, **kwargs)
        update_project_status(project)

    def __str__(self):
        return self.project.name

    class Meta:
        unique_together = ("project", "external_id")
        verbose_name = 'project place'
        verbose_name_plural = 'project places'
        ordering = ['project', 'external_id']
        constraints = [
            models.UniqueConstraint(
                fields=["project", "external_id"],
                name="unique_external_id_per_project",
            )
        ]
