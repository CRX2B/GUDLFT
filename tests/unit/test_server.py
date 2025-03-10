import pytest
from server import app

# Test: Vérification de l'accessibilité de la page d'accueil

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

if __name__ == '__main__':
    pytest.main() 