import pytest
from server import app, clubs, competitions

# Test: Vérification de la limite de 12 places par compétition

@pytest.mark.parametrize('setup_test_data', [25], indirect=True)
def test_limit_places_per_competition(client, setup_test_data):
    club, competition = setup_test_data
    initial_places = competition['numberOfPlaces']

    # Tentative de réservation de 13 places
    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': 13
    })
    assert response.status_code == 200
    assert "You cannot book more than 12 places per competition" in response.get_data(as_text=True)

    # Vérification que le nombre de places reste inchangé
    assert competition['numberOfPlaces'] == initial_places
    competition['numberOfPlaces'] = initial_places 