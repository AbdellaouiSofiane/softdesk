from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Project
from .permissions import IsAuthorOrReadOnly
from .serializers import ProjectSerializer


User = get_user_model()


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Project.objects.filter(
            Q(author=self.request.user) |
            Q(contributors__in=[self.request.user])
        ).distinct().select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
