import pytest
from server import app

def test_max_places_per_competition():
    """Test vérifiant qu'un club ne peut pas réserver plus de 12 places pour une compétition."""
    # Configuration du client de test
    client = app.test_client()
    
    # Obtenir les données du club 'Simply Lift' qui a suffisamment de points (13)
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    
    # Tenter de réserver 13 places (plus que la limite de 12)
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': '13'  # Plus que la limite de 12 places
    }, follow_redirects=True)
    
    # Vérifier que la demande est refusée avec un message approprié
    assert "You cannot book more than 12 places per competition" in response.data.decode()
    
    # Vérifier que le nombre de places disponibles dans la compétition n'a pas changé
    assert b"Number of Places: 25" in response.data
    
    # Vérifier que les points du club n'ont pas été déduits
    assert b"Points available: 13" in response.data 