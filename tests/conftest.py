import pytest
import shutil
import os

# Sauvegarde des fichiers JSON avant tous les tests et restauration après
@pytest.fixture(scope="session", autouse=True)
def manage_json_files():
    """Sauvegarde et restaure les fichiers JSON pour l'ensemble de la session de test."""
    # Fichiers à sauvegarder et restaurer
    json_files = ['clubs.json', 'competitions.json']
    
    # Créer des copies de sauvegarde avant tous les tests
    for file in json_files:
        if os.path.exists(file):
            backup_file = f"{file}.test_backup"
            shutil.copy2(file, backup_file)
            print(f"Backup created for {file}")
    
    # Exécuter tous les tests
    yield
    
    # Restaurer les fichiers JSON après tous les tests
    for file in json_files:
        backup_file = f"{file}.test_backup"
        if os.path.exists(backup_file):
            shutil.copy2(backup_file, file)
            os.remove(backup_file)
            print(f"Restored {file} from backup") 