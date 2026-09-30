from rest_framework import serializers
from .models import Slide
from apps.vocabulary.serializers import LexemeSerializer, ConstructionSerializer

class SlideSerializer(serializers.ModelSerializer):
    lexeme = LexemeSerializer(read_only=True)
    exercise_sentence = serializers.SerializerMethodField()

    class Meta:
        model = Slide
        fields = ["id", "lexeme", "learning_target", "exercise_sentence", "order", "slide_type"]

    def get_exercise_sentence(self, obj):
        construction = self.context.get("exercise_sentences", {}).get(obj.lexeme_id)
        if construction is None:
            return None
        return ConstructionSerializer(construction, context=self.context).data
