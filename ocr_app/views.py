from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import re
from .models import UserInfo
from .serializers import UserInfoSerializer

ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg']

def extract_uppercase_and_numbers(text):
    pattern = re.compile(r'[A-Z0-9]+')
    matches = pattern.findall(text)
    return ' '.join(matches)

def extract_numbers(text):
    pattern = re.compile(r'\d+')
    matches = pattern.findall(text)
    return ''.join(matches)  # Return as a continuous string of numbers

def preprocess_image(img):
    img = img.convert('L')  # Convert to grayscale
    img = img.filter(ImageFilter.GaussianBlur(1))  # Apply Gaussian blur
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)  # Increase contrast
    img = img.filter(ImageFilter.SHARPEN)  # Sharpen the image
    img = img.point(lambda x: 0 if x < 128 else 255, '1')  # Binarize the image
    return img

def extract_info_from_image(img):
    try:
        rois = {
            'nom': (140, 40, 360, 100),
            'prenom': (140, 90, 300, 140),
            'date_naissance': (200, 90, 450, 160),
            'id': (50, 260, 220, 320)  # Coordonnées pour l'ID
        }

        extracted_info = {}

        for key, box in rois.items():
            try:
                roi_img = img.crop(box)  # Extraire la région d'intérêt (ROI)
                roi_img = preprocess_image(roi_img)  # Appliquer le prétraitement
                text = pytesseract.image_to_string(roi_img, config='--psm 6')

                extracted_info[key] = extract_uppercase_and_numbers(text)  # Appliquer le même traitement pour tous les champs
            except Exception as e:
                print(f"Erreur lors du traitement de la région {key}: {e}")
                extracted_info[key] = ''  # Laisser le champ vide si une erreur se produit

        return extracted_info
    except Exception as e:
        print(f"Erreur lors de l'extraction des informations : {e}")
        return {}



@api_view(['POST'])
def upload_image(request):
    if 'file' not in request.FILES:
        return Response({'error': 'Aucun fichier fourni.'}, status=400)
    
    file = request.FILES['file']
    if file.name.split('.')[-1].lower() not in ALLOWED_IMAGE_EXTENSIONS:
        return Response({'error': 'Format de fichier non autorisé.'}, status=400)
    
    try:
        img = Image.open(file)
        extracted_info = extract_info_from_image(img)
        
        # Ne pas enregistrer les informations, juste les retourner
        return Response({'extracted_info': extracted_info})
    except Exception as e:
        return Response({'error': str(e)}, status=500)

# Vue pour enregistrer les informations une fois que l'utilisateur clique sur "Enregistrer"
@api_view(['POST'])
def save_info(request):
    try:
        data = request.data
        
        # Enregistrer les informations uniquement ici
        user_info, created = UserInfo.objects.update_or_create(
            carte_nationale_id=data.get('id', ''),
            defaults={
                'nom': data.get('nom', ''),
                'prenom': data.get('prenom', ''),
                'date_naissance': data.get('date_naissance', ''),
            }
        )
        return JsonResponse({'message': 'Les informations ont été enregistrées avec succès.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
