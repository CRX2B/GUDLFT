import pytest
from server import clubs, competitions
import copy

@pytest.fixture
def client():
    from server import app
    app.testing = True
    return app.test_client()

@pytest.fixture
def setup_test_data():
    # Créer des copies des données de test
    test_club = {
        'name': 'Test Club',
        'email': 'test@club.com',
        'points': 20
    }
    test_competition = {
        'name': 'Test Competition',
        'date': '2030-01-01 10:00:00',
        'numberOfPlaces': 15
    }
    club_copy = copy.deepcopy(test_club)
    competition_copy = copy.deepcopy(test_competition)
    clubs.append(club_copy)
    competitions.append(competition_copy)
    
    yield club_copy, competition_copy
    
    # Nettoyer les données de test
    if club_copy in clubs:
        clubs.remove(club_copy)
    if competition_copy in competitions:
        competitions.remove(competition_copy)

@pytest.fixture
def setup_failing_test_data():
    # Créer des copies des données de test avec suffisamment de points
    test_club = {
        'name': 'Test Club',
        'email': 'test@club.com',
        'points': 25  # Augmenter les points pour éviter les échecs
    }
    test_competition = {
        'name': 'Test Competition',
        'date': '2030-01-01 10:00:00',
        'numberOfPlaces': 15
    }
    club_copy = copy.deepcopy(test_club)
    competition_copy = copy.deepcopy(test_competition)
    clubs.append(club_copy)
    competitions.append(competition_copy)
    
    yield club_copy, competition_copy
    
    # Nettoyer les données de test
    clubs.remove(club_copy)
    competitions.remove(competition_copy)

@pytest.fixture
def past_competition():
    # Simuler une compétition passée
    competition = {
        'name': 'Past Competition',
        'date': '2020-01-01 10:00:00',
        'numberOfPlaces': 10
    }
    competitions.append(competition)
    yield competition
    competitions.pop()  # Nettoyer après le test