from django.urls import path
from .views import homepage, predictFormPage, predict

urlpatterns = [
    path('', homepage, name='home'),
    path('predictForm/', predictFormPage, name='predict_form'),
    path('predict/', predict),
]