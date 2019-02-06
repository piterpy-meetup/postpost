from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title='postpost',
      default_version='v0.1',
      description='Default description',
      license=openapi.License(name='MIT License'),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
