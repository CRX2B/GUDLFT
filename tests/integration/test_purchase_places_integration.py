import pytest
from server import app, clubs, competitions

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

# Test d'intégration pour vérifier le flux complet d'achat de places

def test_purchase_places_integration(client):
    club = clubs[0]
    competition = competitions[0]
    initial_points = club['points']
    initial_places = competition['numberOfPlaces']

    # Simuler la connexion
    response = client.post('/showSummary', data={'email': club['email']})
    assert response.status_code == 200

    # Essayer d'acheter plus de places que de points disponibles
    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': initial_points + 1
    })
    assert response.status_code == 200
    assert "You cannot use more points than you have" in response.get_data(as_text=True)

    # Vérifier que l'état n'a pas changé
    assert club['points'] == initial_points
    assert competition['numberOfPlaces'] == initial_places 