from rest_framework_nested import routers

from api import views

router = routers.SimpleRouter()
router.register('users', views.UserRegistration)
router.register('workspaces', views.WorkspaceListCreate)
workspaces_router = routers.NestedSimpleRouter(router, 'workspaces', lookup='workspace')

# workspaces_router.register(
#     'publications',
#     views.WorkspacePublication,
#     base_name='workspace-publication',
# )
workspaces_router.register(
    'members',
    views.WorkspaceMemberCreate,
    base_name='workspace-memberrr',
)
workspaces_router.register(
    'members',
    views.WorkspaceMemberList,
    base_name='workspace-member',
)
# workspaces_router.register(
#     'members',
#     views.WorkspaceMemberUpdateDestroy,
#     base_name='workspace-member',
# )


urlpatterns = router.urls + workspaces_router.urls
