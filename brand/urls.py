from django.urls import include, path
from rest_framework import routers
from .views import homepage, predictFormPage, predict , SuggestionViewSet , CreateSuggestionView , SuggestionView

router = routers.DefaultRouter()
router.register(r'viewsuggestions', SuggestionViewSet)



urlpatterns = [
    path('', homepage, name='home'),
    path('predictForm/', predictFormPage, name='predict_form'),
    path('predict/', predict),
    path('viewRooms',SuggestionView.as_view()),
    path('createRoom',CreateSuggestionView.as_view()),
    
]