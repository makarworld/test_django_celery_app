import logging
from unittest.mock import patch

import pytest

from lessons.models import Lesson
from lessons.tasks import send_lesson_notification

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def _force_celery_eager(settings):
    """Включаем eager-режим для Celery, чтобы .delay исполнялся синхронно."""
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True
    yield


def test_creation_dispatches_created_event():
    with patch("lessons.signals.send_lesson_notification.delay") as mocked_delay:
        lesson = Lesson.objects.create(
            title="Test lesson",
            description="Signal flow",
            student_id=42,
            status=Lesson.Status.SCHEDULED,
        )

    mocked_delay.assert_called_once()
    kwargs = mocked_delay.call_args.kwargs
    assert kwargs["event"] == "created"
    assert kwargs["lesson_id"] == lesson.id
    assert kwargs["student_id"] == lesson.student_id


def test_completion_transition_dispatches_completed_event():
    lesson = Lesson.objects.create(
        title="Lifecycle",
        description="Status changes",
        student_id=10,
        status=Lesson.Status.SCHEDULED,
    )

    with patch("lessons.signals.send_lesson_notification.delay") as mocked_delay:
        lesson.status = Lesson.Status.COMPLETED
        lesson.save(update_fields=["status", "updated_at"])

    mocked_delay.assert_called_once()
    assert mocked_delay.call_args.kwargs["event"] == "completed"


def test_non_completed_status_change_does_not_dispatch():
    lesson = Lesson.objects.create(
        title="No complete",
        description="Intermediate",
        student_id=11,
        status=Lesson.Status.SCHEDULED,
    )

    with patch("lessons.signals.send_lesson_notification.delay") as mocked_delay:
        lesson.status = Lesson.Status.IN_PROGRESS
        lesson.save(update_fields=["status", "updated_at"])

    mocked_delay.assert_not_called()


def test_send_lesson_notification_task_result_and_logging(caplog):
    payload = {"lesson_id": 99, "student_id": 7, "lesson_title": "Celery", "event": "created"}

    with caplog.at_level(logging.INFO):
        result = send_lesson_notification.delay(**payload)
        assert result.get() == payload

    assert any("Уведомление отправлено" in record.message for record in caplog.records)


