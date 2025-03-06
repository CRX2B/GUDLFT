import pytest
from server import app

# Fixture pour créer un client de test pour l'application Flask
@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

# Test pour s'assurer que la page d'index se charge correctement
# Cela vérifie que la route '/' renvoie un code de statut 200
# indiquant que la page est accessible

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

if __name__ == '__main__':
    pytest.main() 