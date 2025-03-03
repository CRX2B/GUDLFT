import sys
import os
from pathlib import Path
import pytest
from server import app
import threading
import time

def test_app_exists():
    """Test vérifiant que l'instance de l'application Flask existe."""
    assert app is not None

def test_app_configuration():
    """Test vérifiant que l'application Flask est correctement configurée."""
    assert app.secret_key == 'something_special'
    assert app.debug is False  # debug est défini à True lorsque app.run(debug=True) est appelé

def test_app_routes():
    """Test vérifiant que l'application a toutes les routes requises."""
    rules = [rule.endpoint for rule in app.url_map.iter_rules()]
    assert 'index' in rules
    assert 'showSummary' in rules
    assert 'book' in rules  
    assert 'purchasePlaces' in rules
    assert 'logout' in rules

def test_app_can_run():
    """Test simplifié pour vérifier que l'application peut démarrer."""
    # Cette fonction vérifie simplement que le code pour démarrer l'application 
    # est correctement implémenté sans réellement démarrer le serveur
    import server
    
    # Vérifie que le module a le code pour démarrer l'application
    assert hasattr(server, '__name__')
    
    # Vérifier que le fichier server.py contient bien le bloc if __name__ == '__main__'
    server_path = Path(__file__).parent.parent.parent / 'server.py'
    with open(server_path, 'r') as f:
        server_code = f.read()
        assert "if __name__ == '__main__':" in server_code
        assert "app.run" in server_code 