from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include

from posts.views import index, blog, post, latest_post, search


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('blog/', blog, name = 'post-list'),
    #path('blog/category-<str:category>/', blog_category, name = 'category-wise-post'),
    #path('blog/year-<int:year>/', blog_year, name = 'year-wise-post'),
    #path('blog/<int:year>/<int:id>-<slug:slug>/', post, name = 'post-detail'),
    path('post/', latest_post),
    path('post/<int:id>-<slug:slug>/', post, name = 'post-detail'),
    #path('post/<id>/', post, name = 'post-detail'), #TRY post/year/month/slug LATER
    path('search/', search, name='search'),
    url('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)