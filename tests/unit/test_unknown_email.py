import pytest
from server import app

def test_unknown_email_handling():
    """Test vérifiant que l'application gère correctement les emails inconnus."""
    # Configuration du client de test
    client = app.test_client()
    # Test avec un email qui n'existe pas dans la base de données
    response = client.post('/showSummary', data={'email': 'unknown@example.com'})
    # Vérifier que la réponse n'est pas un code d'erreur 500 (erreur serveur)
    assert response.status_code != 500
    # Vérifier qu'on est redirigé vers la page d'accueil ou qu'on reçoit un message d'erreur approprié
    assert b'Sorry, that email was not found.' in response.data or response.location == '/' 