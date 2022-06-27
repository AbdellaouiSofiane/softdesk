from rest_framework import serializers

from .models import Project, Issue


class ProjectSerializer(serializers.ModelSerializer):

    author = serializers.CharField(source='author.email', read_only=True)

    class Meta:
        model = Project
        fields = ('pk', 'title', 'description', 'type', 'author')


class IssueSerializer(serializers.ModelSerializer):
    project = serializers.CharField(source='project.title', read_only=True)
    author = serializers.CharField(source='author.email', read_only=True)
    assignee = serializers.CharField(source='assignee.email', read_only=True)

    class Meta:
        model = Issue
        fields = (
            'pk', 'title', 'description', 'tag', 'priority',
            'status', 'project', 'author', 'assignee'
        )