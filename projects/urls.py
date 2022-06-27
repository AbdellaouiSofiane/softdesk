from rest_framework_extensions.routers import ExtendedSimpleRouter

from .views import ProjectViewSet, IssueViewSet, CommentViewSet


router = ExtendedSimpleRouter()
project_router = router.register('', ProjectViewSet, basename='projects')
issues_router = project_router.register(
    r'issues',
    IssueViewSet,
    basename='project_issues',
    parents_query_lookups=['project']
)
issues_router.register(
    r'comments',
    CommentViewSet,
    basename='issue_commnet',
    parents_query_lookups=['issue__project', 'issue']
)
urlpatterns = router.urls
