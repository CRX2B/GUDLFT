"""
Configuration commune pour tous les tests.
Ce fichier est automatiquement chargé par pytest.
"""
import sys
import os
import pytest
from pathlib import Path
from datetime import datetime
import server

# Ajoute le répertoire racine du projet au PYTHONPATH
# pour permettre aux tests d'importer les modules du projet
sys.path.append(str(Path(__file__).parent.parent))

# Classe pour mocker datetime.now()
class MockDateTime(datetime):
    @classmethod
    def now(cls, *args, **kwargs):
        # Retourne une date fixe en 2020 (avant les dates des compétitions)
        return datetime(2020, 1, 1)

@pytest.fixture(autouse=True)
def mock_datetime_now(monkeypatch):
    """Remplace datetime.now() par une version mockée pour tous les tests."""
    # On patch le module importé dans server
    import server
    monkeypatch.setattr(server, 'datetime', MockDateTime)