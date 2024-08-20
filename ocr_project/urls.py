from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ocr_app.urls')),  # Inclure les routes de l'application
]
