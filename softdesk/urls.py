from django.urls import path, include


urlpatterns = [
    path('', include('user.urls')),
    path('projects/', include('projects.urls')),
]
