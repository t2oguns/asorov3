from rest_framework import serializers
from .models import Unit, Lesson
from apps.exercises.serializers import SlideSerializer

class LessonSerializer(serializers.ModelSerializer):
    slides = SlideSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "order", "difficulty", "group", "code", "slides"]

class LessonDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "order", "difficulty", "group", "code"]

class UnitSerializer(serializers.ModelSerializer):
    lessons = LessonDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Unit
        fields = ["id", "title", "description", "order", "lessons"]