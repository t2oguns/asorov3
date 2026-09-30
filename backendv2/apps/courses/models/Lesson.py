from django.db import models
from apps.courses.constants import LESSON_ID_LENGTH
from apps.courses.models.Unit import Unit
from apps.courses.utils import generate_unique_short_code
from django.db import IntegrityError, transaction


class PUBLISH_STATUS(models.TextChoices):
    DRAFT ="draft", "Draft"
    GENERATED ="generated", "Generated"
    IN_REVIEW ="in_review", "In Review"
    PUBLISHED    ="published" "Published"
    ARCHIVED ="archived", "Archived"


class LessonGroup(models.Model):
    """
    Optional grouping of lessons inside a unit.
    Example:
    - "Grammar Basics"
    - "Final Project"
    - "Part 1 + Part 2"
    """

    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="lesson_groups")
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField()

    def __str__(self):
        return str("Lesson Group - " + self.title)


class Lesson(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="lessons")

    group = models.ForeignKey(LessonGroup, null=True, blank=True, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=LESSON_ID_LENGTH, unique=True, editable=False)
    description = models.TextField(blank=True)

    difficulty = models.IntegerField(default=1)

    publication_status = models.CharField(
        max_length=50,
        choices=PUBLISH_STATUS.choices,
        default=PUBLISH_STATUS.DRAFT,
    )

    # Ordering for lessons within a group.
    order = models.PositiveIntegerField()


    def __str__(self):
        return str("Lesson - " + self.title)
    
    # Override save method to generate unique short code for the lesson
    def save(self, *args, **kwargs):
        if self.code:
            return super().save(*args, **kwargs)

        while True:
            try:
                self.code = generate_unique_short_code(Lesson, "code", length=LESSON_ID_LENGTH)

                with transaction.atomic():
                    return super().save(*args, **kwargs)

            except IntegrityError:
                # Collision occurred, retry
                self.code = None
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["unit", "group", "order"],
                name="unique_lesson_order"
            )
        ]
