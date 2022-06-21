from email.mime import base
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProjectViewSet

router = DefaultRouter()
router.register('', ProjectViewSet, basename='projects')
urlpatterns = router.urls
