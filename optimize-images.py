#!/usr/bin/env python3
"""
Script d'optimisation des images pour A Laiz Prod
Usage: python optimize-images.py
"""

import os
from PIL import Image
import glob

def optimize_images():
    # Dossier des images sources
    image_dir = "static/images/"
    
    # Créer le dossier optimized s'il n'existe pas
    optimized_dir = os.path.join(image_dir, "optimized")
    if not os.path.exists(optimized_dir):
        os.makedirs(optimized_dir)
    
    # Formats d'image à optimiser
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.webp']
    
    for extension in image_extensions:
        for image_path in glob.glob(os.path.join(image_dir, extension)):
            # Ignorer les images déjà optimisées
            if "optimized" in image_path:
                continue
                
            try:
                # Ouvrir l'image
                with Image.open(image_path) as img:
                    # Déterminer le nom de sortie
                    filename = os.path.basename(image_path)
                    name, ext = os.path.splitext(filename)
                    output_path = os.path.join(optimized_dir, f"{name}.webp")
                    
                    # Convertir en WEBP avec une qualité optimisée
                    if img.mode in ('RGBA', 'LA'):
                        # Conserver la transparence
                        img.convert('RGBA').save(output_path, 'WEBP', quality=80, optimize=True)
                    else:
                        # Conversion standard
                        img.convert('RGB').save(output_path, 'WEBP', quality=80, optimize=True)
                    
                    print(f"Optimisée: {filename} -> {name}.webp")
                    
            except Exception as e:
                print(f"Erreur avec {image_path}: {str(e)}")

if __name__ == "__main__":
    optimize_images()
