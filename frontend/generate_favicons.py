#!/usr/bin/env python3
"""
Script pour générer les favicons PNG depuis le SVG
Utilise PIL/Pillow et cairosvg
"""

import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("❌ Pillow n'est pas installé. Installation...")
    os.system(f"{sys.executable} -m pip install -q Pillow")
    from PIL import Image, ImageDraw, ImageFont

def create_favicon_png(size, filename):
    """Crée un favicon PNG avec le logo Z en gradient"""
    # Créer une image avec fond transparent
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Couleur de fond (gradient bleu à teal)
    # Simplifié: utiliser bleu foncé
    bg_color = (37, 99, 235, 255)  # #2563eb

    # Dessiner le fond arrondi
    radius = size // 4
    draw.rounded_rectangle([(0, 0), (size, size)], radius=radius, fill=bg_color)

    # Dessiner le Z
    margin = size // 6
    stroke_width = max(2, size // 32)

    # Coordonnées du Z
    x1, y1 = margin, margin
    x2 = size - margin
    y2 = size - margin
    mid_y = size // 2

    # Ligne horizontale haute
    draw.line([(x1, y1), (x2, y1)], fill='white', width=stroke_width)
    draw.line([(x1, y1 + stroke_width), (x2, y1 + stroke_width)], fill='white', width=stroke_width)

    # Diagonale
    draw.line([(x2, y1), (x1, y2)], fill='white', width=stroke_width)

    # Ligne horizontale basse
    draw.line([(x1, y2), (x2, y2)], fill='white', width=stroke_width)
    draw.line([(x1, y2 - stroke_width), (x2, y2 - stroke_width)], fill='white', width=stroke_width)

    # Sauvegarder
    output_path = f'public/{filename}'
    img.save(output_path, 'PNG')
    print(f'✅ {filename} créé ({size}x{size})')

    return output_path

def main():
    """Génère tous les favicons nécessaires"""
    print('🎨 Génération des favicons...\n')

    # Vérifier que le dossier public existe
    if not os.path.exists('public'):
        print('❌ Dossier public/ non trouvé')
        return

    # Générer les différentes tailles
    sizes = {
        16: 'favicon-16x16.png',
        32: 'favicon-32x32.png',
        180: 'apple-touch-icon.png',
        192: 'android-chrome-192x192.png',
        512: 'android-chrome-512x512.png'
    }

    for size, filename in sizes.items():
        create_favicon_png(size, filename)

    # Créer aussi favicon.ico (32x32)
    try:
        img_32 = Image.open('public/favicon-32x32.png')
        img_32.save('public/favicon.ico', format='ICO', sizes=[(32, 32)])
        print('✅ favicon.ico créé')
    except Exception as e:
        print(f'⚠️  favicon.ico non créé: {e}')

    print('\n✨ Tous les favicons ont été générés!')
    print('📁 Fichiers créés dans /frontend/public/')

if __name__ == '__main__':
    main()
