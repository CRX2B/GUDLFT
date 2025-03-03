import pytest
from server import app
from datetime import datetime
import server

# Ce test doit utiliser la vraie datetime.now(), pas le mock
@pytest.fixture
def use_real_datetime(monkeypatch):
    """Restore la vraie fonction datetime.now() pour ce test spécifique."""
    # On restaure le vrai module datetime dans server
    original_datetime = datetime
    monkeypatch.setattr(server, 'datetime', original_datetime)
    yield
    # Pas besoin de rétablir le mock, le fixture autouse le fera automatiquement
    # lors du teardown

def test_cannot_book_past_competitions(use_real_datetime):
    """Test vérifiant qu'on ne peut pas réserver de places pour une compétition passée."""
    # Configuration du client de test
    client = app.test_client()
    
    # Obtenir les données du club 'Simply Lift'
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    
    # Trouver une compétition dont la date est passée (toutes les dates dans competitions.json sont en 2020)
    # En utilisant la page d'accueil pour obtenir l'URL de réservation
    response = client.get('/')
    
    # Essayer de visiter la page de réservation pour une compétition passée
    response = client.get('/book/Spring%20Festival/Simply%20Lift', follow_redirects=True)
    
    # Vérifier que l'accès à la page de réservation est refusé
    # et que l'utilisateur est redirigé avec un message d'erreur approprié
    assert "This competition is over" in response.data.decode() or "past competition" in response.data.decode()
    
    # Tenter aussi de réserver directement via POST (au cas où la validation se fait seulement lors de la réservation)
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': '5'
    }, follow_redirects=True)
    
    # Vérifier que la réservation est refusée
    assert "This competition is over" in response.data.decode() or "past competition" in response.data.decode() 