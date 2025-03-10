import pytest
from server import app

# Test: Vérification de la gestion des emails inconnus

def test_show_summary_unknown_email(client):
    with client:
        response = client.post('/showSummary', data={'email': 'unknown@example.com'})
        assert response.status_code == 200
        assert "Sorry, this email was not found" in response.get_data(as_text=True) 