from __future__ import annotations

from datetime import datetime

from django.db import models


class Lesson(models.Model):
    id: models.BigAutoField["Lesson", int] = models.BigAutoField(primary_key=True)
    _previous_status: str | None = None

    class Status(models.TextChoices):
        DRAFT = "draft", "Черновик"
        SCHEDULED = "scheduled", "Запланирован"
        IN_PROGRESS = "in_progress", "В процессе"
        COMPLETED = "completed", "Завершен"

    title: models.CharField["Lesson", str] = models.CharField(max_length=255)
    description: models.TextField["Lesson", str] = models.TextField(blank=True)
    student_id: models.PositiveIntegerField["Lesson", int] = models.PositiveIntegerField()
    status: models.CharField["Lesson", str] = models.CharField(
        max_length=20, choices=Status.choices, default=Status.SCHEDULED
    )
    scheduled_at: models.DateTimeField["Lesson", datetime | None] = models.DateTimeField(null=True, blank=True)
    created_at: models.DateTimeField["Lesson", datetime] = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField["Lesson", datetime] = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    @property
    def is_completed(self) -> bool:
        return self.status == self.Status.COMPLETED
