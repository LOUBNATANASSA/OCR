from django.urls import path
from .views import upload_image, save_info

urlpatterns = [
    path('ocr/', upload_image, name='upload_image'),  # Route pour le téléchargement de l'image
    path('save_info/', save_info, name='save_info'),  # Route pour enregistrer les informations
]
