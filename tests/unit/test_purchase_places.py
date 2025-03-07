import pytest
from server import app, clubs, competitions

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

# Test unitaire pour vérifier que les clubs ne peuvent pas utiliser plus de points qu'ils n'en ont

def test_purchase_places_exceeding_points(client):
    club = clubs[0]
    competition = competitions[0]
    initial_points = club['points']
    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': initial_points + 1  # Demande plus de points que disponible
    })
    assert response.status_code == 200
    assert "You cannot use more points than you have" in response.get_data(as_text=True)
    assert club['points'] == initial_points  # Les points ne doivent pas être déduits 