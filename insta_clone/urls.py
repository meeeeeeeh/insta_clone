from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentification.urls')),
    path('', include('post.urls')),
    path('', include('follow.urls')),
    path('', include('notifications.urls')),
    path('stories/', include('stories.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
