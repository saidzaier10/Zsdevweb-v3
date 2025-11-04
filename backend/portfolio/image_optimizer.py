"""
Utilitaire pour optimiser automatiquement les images uploadées
Compresse les images PNG et JPEG pour réduire la taille sans perte visible de qualité
"""
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def optimize_image(image_file, max_width=1920, max_height=1920, quality=85):
    """
    Optimise une image en la redimensionnant si nécessaire et en la compressant

    Args:
        image_file: Le fichier image à optimiser
        max_width: Largeur maximale (default: 1920px)
        max_height: Hauteur maximale (default: 1920px)
        quality: Qualité JPEG (default: 85)

    Returns:
        InMemoryUploadedFile: Image optimisée
    """
    try:
        # Ouvrir l'image
        img = Image.open(image_file)

        # Convertir RGBA en RGB si nécessaire (pour JPEG)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background

        # Redimensionner si l'image est trop grande
        if img.width > max_width or img.height > max_height:
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

        # Sauvegarder dans un buffer
        output = BytesIO()

        # Déterminer le format
        format_name = image_file.name.split('.')[-1].upper()
        if format_name == 'JPG':
            format_name = 'JPEG'

        # Sauvegarder avec compression
        if format_name in ('JPEG', 'JPG'):
            img.save(output, format='JPEG', quality=quality, optimize=True)
            content_type = 'image/jpeg'
        elif format_name == 'PNG':
            img.save(output, format='PNG', optimize=True)
            content_type = 'image/png'
        elif format_name == 'WEBP':
            img.save(output, format='WEBP', quality=quality, method=6)
            content_type = 'image/webp'
        else:
            # Format non supporté, retourner l'original
            return image_file

        output.seek(0)

        # Créer un nouveau fichier uploadé
        optimized_file = InMemoryUploadedFile(
            output,
            'ImageField',
            image_file.name,
            content_type,
            sys.getsizeof(output),
            None
        )

        return optimized_file

    except Exception as e:
        print(f"❌ Erreur lors de l'optimisation de l'image: {e}")
        # En cas d'erreur, retourner l'original
        return image_file


def get_image_info(image_file):
    """
    Obtient des informations sur une image

    Returns:
        dict: Informations sur l'image (format, dimensions, taille)
    """
    try:
        img = Image.open(image_file)
        image_file.seek(0)  # Reset file pointer

        return {
            'format': img.format,
            'mode': img.mode,
            'width': img.width,
            'height': img.height,
            'size': image_file.size,
        }
    except Exception as e:
        print(f"❌ Erreur lors de la lecture des infos de l'image: {e}")
        return None
