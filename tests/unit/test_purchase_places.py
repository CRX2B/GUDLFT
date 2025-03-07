import pytest
from server import app, clubs, competitions

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

# Test unitaire pour vérifier que les clubs ne peuvent pas utiliser plus de points qu'ils n'en ont

def test_purchase_places_exceeding_points(client, setup_test_data):
    club, future_competition = setup_test_data
    initial_points = club['points']
    # Demander un nombre de places qui dépasse les points disponibles, tout en restant inférieur ou égal à 12
    places_to_book = initial_points + 1
    response = client.post('/purchasePlaces', data={
        'competition': future_competition['name'],
        'club': club['name'],
        'places': places_to_book
    })
    assert response.status_code == 200
    assert "You cannot use more points than you have" in response.get_data(as_text=True)
    assert club['points'] == initial_points  # Les points ne doivent pas être déduits 

def test_reserve_zero_places(client, setup_test_data):
    club, competition = setup_test_data

    # Essayer de réserver 0 places
    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': 0
    })
    assert response.status_code == 200
    assert "Sorry, select a number of places greater than 0" in response.get_data(as_text=True) 