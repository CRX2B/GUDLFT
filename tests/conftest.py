import pytest
import shutil
import os

@pytest.fixture(scope='function', autouse=True)
def restore_json_files():
    # Créer des copies de sauvegarde
    shutil.copy('clubs.json', 'clubs_backup.json')
    shutil.copy('competitions.json', 'competitions_backup.json')
    
    yield  # Exécute les tests
    
    # Restaurer les fichiers JSON
    shutil.copy('clubs_backup.json', 'clubs.json')
    shutil.copy('competitions_backup.json', 'competitions.json')
    
    # Supprimer les fichiers de sauvegarde
    os.remove('clubs_backup.json')
    os.remove('competitions_backup.json') 