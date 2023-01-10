from django.urls import path, include
from rest_framework import routers
from .views import ModelViewSet

router = routers.DefaultRouter()
router.register(r'model', ModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
