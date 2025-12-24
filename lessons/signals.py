from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Lesson
from .tasks import send_lesson_notification


@receiver(pre_save, sender=Lesson)
def store_previous_status(sender: Lesson, instance: Lesson, **kwargs) -> None:
    # Use setattr to avoid lint errors about a missing attribute.
    previous_status = None
    if instance.pk:
        try:
            previous_status = sender.objects.get(pk=instance.pk).status
        except sender.DoesNotExist:
            previous_status = None
    setattr(instance, "_previous_status", previous_status)


@receiver(post_save, sender=Lesson)
def lesson_lifecycle_handler(sender, instance: Lesson, created: bool, **kwargs) -> None:
    event = None

    if created:
        event = "created"
    else:
        previous_status = getattr(instance, "_previous_status", None)
        if previous_status and previous_status != instance.status and instance.status == Lesson.Status.COMPLETED:
            event = "completed"

    if event:
        send_lesson_notification.delay(
            lesson_id=instance.id,
            student_id=instance.student_id,
            lesson_title=instance.title,
            event=event,
        )
