# ./planner/models.py

from django.db import models

from apps.auth.models import User


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
        auto_now_add=True
    )

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

    def __str__(self):
        return self.project.name

    class Meta:
        unique_together = ("project", "external_id")
        verbose_name = 'project place'
        verbose_name_plural = 'project places'
        ordering = ['project', 'external_id']
