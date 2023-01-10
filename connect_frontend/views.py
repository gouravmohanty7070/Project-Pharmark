from django.shortcuts import render
from rest_framework import viewsets
from .models import Model
from .serializers import ModelSerializer

class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer

# Create your views here.
