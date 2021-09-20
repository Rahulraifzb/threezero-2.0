from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('auth/', admin.site.urls),
    path("",include("core.backend.home.urls")),
    path("",include("core.backend.quiz.urls")),
    path("",include("core.backend.authentication.urls"))
]

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
