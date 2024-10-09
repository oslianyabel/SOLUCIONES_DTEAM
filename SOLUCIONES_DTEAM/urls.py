from django.contrib import admin
from django.urls import path, re_path
from app import views
from django.conf import settings
from django.views.static import serve
from django.conf.urls import handler404
from django.shortcuts import render

def custom_page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_page_not_found_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('services/<int:cat>', views.servicios, name='servicios'),
    path('service/<int:service_id>', views.servicio_detail, name='servicio-detail'),
    path('login/<int:service_id>', views.login_view, name='login_view'),
    path('register/<int:service_id>', views.register_view, name='register_view'),
    path('opinion/<int:service_id>', views.opinion, name='opinion'),
    path('', views.index, name='index'),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    })
]