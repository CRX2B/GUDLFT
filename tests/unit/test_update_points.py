import pytest
from server import app, clubs, competitions

# Test: Vérification de la mise à jour des points après achat

@pytest.mark.parametrize('setup_test_data', [25], indirect=True)
def test_points_update_after_purchase(client, setup_test_data):
    club, future_competition = setup_test_data
    initial_points = club['points']
    places_to_book = 5

    # Réservation de places
    response = client.post('/purchasePlaces', data={
        'competition': future_competition['name'],
        'club': club['name'],
        'places': places_to_book
    })

    # Vérification de la réponse
    assert response.status_code == 200
    assert "Purchase successful" in response.get_data(as_text=True)

    # Vérification de la déduction des points
    expected_points = initial_points - places_to_book
    assert club['points'] == expected_points, "Club points were not updated correctly" 