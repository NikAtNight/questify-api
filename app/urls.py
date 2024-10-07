from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, get_resolver
from rest_framework_nested import routers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.users.views import (
    UserViewSet,
)
from app.habits.views import (
    HabitViewSet,
    UserHabitViewSet
)


@api_view(['GET'])
def list_urls(request):
    url_patterns = get_resolver().url_patterns
    urls = []
    for pattern in url_patterns:
        if hasattr(pattern, 'url_patterns'):
            for sub_pattern in pattern.url_patterns:
                urls.append(str(sub_pattern.pattern))
        else:
            urls.append(str(pattern.pattern))
    return Response(urls)


app_router = routers.SimpleRouter()
app_router.register(r'users', UserViewSet, basename='users')
app_router.register(r'habits', HabitViewSet, basename='habits')
app_router.register(r'user-habits', UserHabitViewSet, basename='user-habits')

combined_urls = app_router.urls

urlpatterns = [
    path('skynet/doc/', include('django.contrib.admindocs.urls')),
    path('skynet/', admin.site.urls),
    path('api/urls/', list_urls),
    path('api/', include((combined_urls, 'questify'), namespace='v1')),
    path("prometheus/", include("django_prometheus.urls")),
] + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
) + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

admin.site.site_header = "Questify Admin - v1"
admin.site.site_title = "Questify Admin Portal"
admin.site.index_title = "Welcome to Questify Portal"
