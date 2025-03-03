"""
Configuration commune pour tous les tests.
Ce fichier est automatiquement chargé par pytest.
"""
import sys
import os
from pathlib import Path

# Ajoute le répertoire racine du projet au PYTHONPATH
# pour permettre aux tests d'importer les modules du projet
sys.path.append(str(Path(__file__).parent.parent))