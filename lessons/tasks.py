import logging

from celery import shared_task  # type: ignore[import-untyped]

logger = logging.getLogger(__name__)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def send_lesson_notification(self, lesson_id: int, student_id: int, lesson_title: str, event: str):
    logger.info(
        "Уведомление отправлено студенту %s по уроку '%s' (событие: %s).",
        student_id,
        lesson_title,
        event,
    )
    return {
        "lesson_id": lesson_id,
        "student_id": student_id,
        "lesson_title": lesson_title,
        "event": event,
    }
