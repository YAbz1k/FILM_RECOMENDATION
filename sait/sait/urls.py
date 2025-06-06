from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]

# В режиме DEBUG добавляем раздачу статики
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# И раздачу медиа-файлов (загруженных через ImageField)
urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)

