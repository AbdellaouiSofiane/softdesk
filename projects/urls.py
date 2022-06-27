from rest_framework_extensions.routers import ExtendedSimpleRouter

from .views import ProjectViewSet, IssueViewSet

router = ExtendedSimpleRouter()
project_router = router.register('', ProjectViewSet, basename='projects')
issues_router = project_router.register(
    r'issues',
    IssueViewSet,
    basename='project_issues',
    parents_query_lookups=['project']
)
urlpatterns = router.urls
