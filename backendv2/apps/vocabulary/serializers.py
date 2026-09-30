from rest_framework import serializers
from .models import Construction, ConstructionComponent, Highlight, ConstructionLexeme
from apps.vocabulary.models import Lexeme


class LexemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lexeme
        fields = ["id", "lemma", "normalized_lemma", "tone_pattern", "translation"]


class HighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Highlight
        fields = ["id", "start_index", "end_index"]


class ConstructionComponentSerializer(serializers.ModelSerializer):
    lexeme = LexemeSerializer(read_only=True)
    child_construction = serializers.SerializerMethodField()
    highlights = HighlightSerializer(many=True, read_only=True)

    class Meta:
        model = ConstructionComponent
        fields = ["id", "position", "lexeme", "child_construction", "highlights"]

    def get_child_construction(self, obj):
        if obj.child_construction_id is None:
            return None
        # Recurses through the same serializer — bounded by however deep
        # your prefetch went; see note below.
        return ConstructionSerializer(obj.child_construction, context=self.context).data


class ConstructionSerializer(serializers.ModelSerializer):
    components = ConstructionComponentSerializer(many=True, read_only=True)

    class Meta:
        model = Construction
        fields = [
            "id", "native_text", "normalized_text", "construction_type",
            "translation", "notes", "difficulty", "components",
        ]