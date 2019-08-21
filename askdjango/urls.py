from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('plusfriend/', include('plusfriend.urls')),
    path('', lambda request: render(request, 'root.html'), name='root'),
]

# 장고는 개발서버에서 media 파일 지원하지 않아서 이렇게 해줌
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)