from django.contrib import admin

from .models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "student_id", "status", "created_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("title", "student_id")


