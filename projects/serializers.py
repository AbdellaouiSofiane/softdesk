from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):

    author = serializers.CharField(source='author.email', read_only=True)

    class Meta:
        model = Project
        fields = ('pk', 'title', 'description', 'type', 'author')
