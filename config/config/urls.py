import debug_toolbar

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="PyConnect API",
        default_version='v1',
        description="API for account and blog systems",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="in process"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [

                  path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                  path('admin/', admin.site.urls),
                  path('__debug__/', include(debug_toolbar.urls)),

                  # Defaults
                  path('social/', include('allauth.urls'), name='social'),

                  # Apps
                  path('account/', include('account_system.urls')),
                  path('blog/', include('blog_system.urls')),

                  # Api
                  path('api/account/', include('account_system_api.urls')),
                  path('api/blog/', include('blog_system_api.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
