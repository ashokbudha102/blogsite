"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from post.views import index, blog,post,search,post_update,post_delete,post_create,cat_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('blog/', blog,name='post-list'),
    path('post/<id>/', post,name='post-detail'),
    path('post/<id>/update/', post_update,name='post-update'),
    path('post/<id>/delete/', post_delete,name='post-delete'),
    path('create/', post_create,name='post-create'),
    path('search/',search,name='search'),
    path('<id>/',cat_view,name='catview'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG==True:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
