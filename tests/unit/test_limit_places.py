import pytest
from server import app, clubs, competitions

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

# Test unitaire pour vérifier que les clubs ne peuvent pas réserver plus de 12 places par compétition

def test_limit_places_per_competition(client, setup_test_data):
    club, competition = setup_test_data
    initial_places = competition['numberOfPlaces']

    # Essayer de réserver plus de 12 places
    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': 13  # Plus que le maximum autorisé de 12
    })
    assert response.status_code == 200
    assert "You cannot book more than 12 places per competition" in response.get_data(as_text=True)

    # Vérifier que le nombre de places n'a pas changé
    assert competition['numberOfPlaces'] == initial_places
    # Réinitialiser l'état
    competition['numberOfPlaces'] = initial_places 