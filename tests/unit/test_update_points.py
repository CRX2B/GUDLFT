import pytest
from server import app, clubs, competitions

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()


def test_points_update_after_purchase(client, setup_failing_test_data):
    club, future_competition = setup_failing_test_data
    initial_points = club['points']
    places_to_book = 5  # Nombre de places à réserver

    # Effectuer l'achat de places
    response = client.post('/purchasePlaces', data={
        'competition': future_competition['name'],
        'club': club['name'],
        'places': places_to_book
    })

    # Vérifier que la réponse est correcte
    assert response.status_code == 200
    assert "Purchase successful" in response.get_data(as_text=True)

    # Vérifier que les points ont été mis à jour correctement
    expected_points = initial_points - places_to_book
    assert club['points'] == expected_points, "Club points were not updated correctly" 