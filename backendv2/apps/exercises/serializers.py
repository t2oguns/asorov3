from rest_framework import serializers
from .models import Slide
from apps.vocabulary.serializers import LexemeSerializer

class SlideSerializer(serializers.ModelSerializer):
    lexeme = LexemeSerializer(read_only=True)

    class Meta:
        model = Slide
        fields = ["id", "lexeme", "learning_target", "order", "slide_type"]
