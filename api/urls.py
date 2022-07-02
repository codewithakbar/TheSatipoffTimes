from django.urls import path
from .views import PostAPIView

urlpatterns = [
    path('api/', PostAPIView.as_view()),
]