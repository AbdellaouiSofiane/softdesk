from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.serializers import SignUpSerializer
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

    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):
        project = self.get_object()
        users = User.objects.filter(
            Q(pk=project.author.id) |
            Q(pk__in=project.contributors.all().values('pk'))
        )
        serializer = SignUpSerializer(users, many=True)
        return Response(serializer.data)

    @users.mapping.post
    def add_user(self, request, pk=None):
        project = self.get_object()
        user = get_object_or_404(User, email=request.data.get('email', None))
        project.contributors.add(user)
        serializer = SignUpSerializer(user)
        return Response(serializer.data)

    @action(
        detail=True, methods=['delete'], url_path=r'users/(?P<id>[^/.]+)'
    )
    def remove_user(self, request, pk, id):
        project = self.get_object()
        user = get_object_or_404(User, pk=id)
        project.contributors.remove(user)
        serializer = SignUpSerializer(user)
        return Response(serializer.data)
