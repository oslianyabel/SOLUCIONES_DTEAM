from django.contrib import admin
from django.urls import path, re_path
from app import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('services/<int:cat>', views.servicios, name='servicios'),
    path('', views.index, name='index'),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    })
]