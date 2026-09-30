import string
import secrets
import random
from collections import defaultdict
from apps.vocabulary.models import Construction, ConstructionLexeme, ConstructionType

ALPHANUMERIC_CHARS = string.ascii_letters + string.digits

def generate_unique_short_code(ModelClass, field_name, length=6):
    """
    Generates a unique 6-character alphanumeric code for Lesson.
    Retries until a unique code is found.
    """

    while True:
        # Generate a random 6-character string
        code = ''.join(secrets.choice(ALPHANUMERIC_CHARS) for _ in range(length))
        # Check if this code already exists in the database
        exists = ModelClass.objects.filter(
            **{field_name: code}
        ).exists()

        if not exists:
            return code

class LessonCodeConverter:
    regex = r"[A-Za-z0-9]{6}"  # match LESSON_ID_LENGTH

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value

