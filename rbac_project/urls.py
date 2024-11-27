from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny


schema_view = get_schema_view(
    openapi.Info(
        title="RBAC API Documentation",
        default_version="v1",
        description="API documentation for Role-Based Access Control",
        terms_of_service="",
        contact=openapi.Contact(email="rahee9156@gmail.com"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rbac_app.urls')),
]

urlpatterns += [
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]