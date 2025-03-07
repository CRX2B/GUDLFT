import pytest
from server import app, clubs, competitions
# from server import app, clubs, competitions  # Supprimé car géré par conftest.py

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

@pytest.fixture
def setup_test_data():
    # Créer des données de test spécifiques
    test_club = {
        'name': 'Test Club',
        'email': 'test@club.com',
        'points': 5
    }
    test_competition = {
        'name': 'Test Competition',
        'date': '2030-01-01 10:00:00',
        'numberOfPlaces': 10
    }
    clubs.append(test_club)
    competitions.append(test_competition)
    yield test_club, test_competition
    # Nettoyer les données de test
    clubs.remove(test_club)
    competitions.remove(test_competition)

# Test d'intégration pour vérifier le flux complet d'achat de places

def test_purchase_places_integration(client, setup_test_data):
    club, competition = setup_test_data
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
    # Réinitialiser l'état
    club['points'] = initial_points
    competition['numberOfPlaces'] = initial_places 