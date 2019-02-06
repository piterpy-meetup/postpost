from django.urls import path
from rest_framework_nested import routers

from api import views

router = routers.SimpleRouter()
router.register('users', views.UserRegistration)
router.register('workspaces', views.Workspace)
workspaces_router = routers.NestedSimpleRouter(router, r'workspaces', lookup='workspace')
workspaces_router.register('publications', views.WorkspacePublication, base_name='workspaces-publication')

urlpatterns = router.urls + workspaces_router.urls
