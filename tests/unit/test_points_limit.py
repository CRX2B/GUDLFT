import pytest
from server import app

def test_club_cannot_exceed_points():
    """Test vérifiant qu'un club ne peut pas réserver plus de places que ses points ne le permettent."""
    # Configuration du client de test
    client = app.test_client()
    
    # Obtenir les données d'un club (Simply Lift a 13 points)
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    
    # Tenter de réserver plus de places que les points ne le permettent (ex: 14 places)
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': '14'  # Plus que les 13 points disponibles
    }, follow_redirects=True)
    
    # Vérifier que la demande est refusée en vérifiant que le message d'erreur est présent
    # en utilisant une version simplifiée de la chaîne de caractères
    assert "have enough points" in response.data.decode()
    
    # Vérifier que le nombre de places disponibles dans la compétition n'a pas changé
    assert b"Number of Places: 25" in response.data 