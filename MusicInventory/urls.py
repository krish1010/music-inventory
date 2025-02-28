from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('music/', include('music_app.urls')),
    path('accounts/', include('accounts.urls')),
]
