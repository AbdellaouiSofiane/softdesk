from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework_extensions.utils import compose_parent_pk_kwarg_name

from user.serializers import SignUpSerializer
from .models import Issue, Project
from .permissions import IsAuthorOrReadOnly
from .serializers import ProjectSerializer, IssueSerializer


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


class IssueViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return self.filter_queryset_by_parents_lookups(
            Issue.objects.filter(
                Q(project__author=self.request.user) |
                Q(project__contributors__in=[self.request.user])
            ).distinct()
        ).select_related('project', 'author', 'assignee')

    def perform_create(self, serializer):
        project_id = self.kwargs.get(
            compose_parent_pk_kwarg_name('project')
        )
        user = self.request.user
        serializer.save(project_id=project_id, author=user, assignee=user)