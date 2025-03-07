import pytest
from server import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

# Test unitaire pour vérifier que la fonction showSummary gère correctement les emails inconnus

def test_show_summary_unknown_email(client):
    with client:
        response = client.post('/showSummary', data={'email': 'unknown@example.com'})
        assert response.status_code == 200
        assert "Sorry, this email was not found" in response.get_data(as_text=True) 