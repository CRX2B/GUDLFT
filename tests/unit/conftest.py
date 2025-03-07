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
    # Créer des données de test spécifiques
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
    print("Avant l'ajout :", competitions)
    clubs.append(test_club)
    competitions.append(copy.deepcopy(test_competition))
    print("Après l'ajout :", competitions)
    
    yield test_club, test_competition
    
    # Fonction de nettoyage
    def cleanup():
        competitions[:] = [comp for comp in competitions if not is_competition_equal(comp, test_competition)]
        clubs.remove(test_club)
    
    print("Avant la suppression :", competitions)
    cleanup()
    print("Après la suppression :", competitions)

def is_competition_equal(comp1, comp2):
    return comp1['name'] == comp2['name'] and comp1['date'] == comp2['date'] and comp1['numberOfPlaces'] == comp2['numberOfPlaces']

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