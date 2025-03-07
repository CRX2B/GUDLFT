import pytest
from server import app, clubs, competitions

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

def test_full_booking_flow(client, setup_test_data):
    club, competition = setup_test_data
    initial_points = club['points']
    initial_places = competition['numberOfPlaces']

    # Simuler la connexion
    response = client.post('/showSummary', data={'email': club['email']})
    assert response.status_code == 200

    # Réserver des places
    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': 2
    })
    assert response.status_code == 200
    assert 'Purchase successful' in response.get_data(as_text=True)

    # Vérifier que l'état a changé
    assert club['points'] == initial_points - 2
    assert competition['numberOfPlaces'] == initial_places - 2

    # Simuler la déconnexion
    response = client.get('/logout')
    assert response.status_code == 302  # Redirection
    assert response.headers['Location'] == 'http://localhost/'

# Test de gestion des erreurs

def test_limit_places(client, setup_test_data):
    club, competition = setup_test_data
    club['points'] = 15  # Donner suffisamment de points pour tester la limite de places

    # Essayer d'acheter plus de 12 places
    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': 13
    })
    assert response.status_code == 200
    assert 'You cannot book more than 12 places per competition' in response.get_data(as_text=True)


def test_past_competition(client, setup_test_data):
    club, competition = setup_test_data
    competition['date'] = '2000-01-01 10:00:00'  # Date passée

    # Essayer d'acheter des places pour une compétition passée
    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': 1
    })
    assert response.status_code == 200
    assert 'You cannot book places for past competitions' in response.get_data(as_text=True)


def test_logout(client):
    # Simuler une déconnexion
    response = client.get('/logout')
    assert response.status_code == 302  # Redirection
    assert response.headers['Location'] == 'http://localhost/' 