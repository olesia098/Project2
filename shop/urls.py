from rest_framework.routers import DefaultRouter
from main.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

router = DefaultRouter()
router.register('post', PostViewSet)


schema_view = get_schema_view(
    openapi.Info(
        title='Python18 My_blog project',
        description='Интернет магазин',
        default_version='v1'
    ),
    public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('aoi-auth', include('rest_framework.urls')),
    # path('v1/api/add-image/', PostImageView.as_view()),
    path('v1/api/categories/', CategoryListView.as_view()),
    path('v1/api/account/', include('account.urls')),
    path('v1/api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
