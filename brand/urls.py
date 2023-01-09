from django.urls import include, path
from rest_framework import routers
from .views import homepage, predictFormPage, predict , SuggestionViewSet

router = routers.DefaultRouter()
router.register(r'viewsuggestions', SuggestionViewSet)



urlpatterns = [
    # path('', homepage, name='home'),
    # path('predictForm/', predictFormPage, name='predict_form'),
    # path('predict/', predict),
    path('', include(router.urls)),
    
]