from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from .models import Unit, Lesson
from .serializers import UnitSerializer, LessonSerializer

# Create your views here.

class UnitList(generics.ListAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.AllowAny]


class LessonView(RetrieveAPIView):
    queryset = Lesson.objects.prefetch_related("slides__slide_lexemes")
    serializer_class = LessonSerializer
    lookup_field = "code"
    lookup_url_kwarg = "code"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
