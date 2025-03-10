import pytest
from server import clubs, competitions
import copy

@pytest.fixture
def client():
    """Fournit un client de test Flask pour les tests."""
    from server import app
    app.testing = True
    return app.test_client()

@pytest.fixture
def setup_test_data(request=None):
    """
    Crée des données de test pour les clubs et compétitions.
    
    Pour utiliser avec un nombre de points spécifique:
    @pytest.mark.parametrize('setup_test_data', [25], indirect=True)
    
    Args:
        request: Objet de requête Pytest pour paramétrer la fixture.
    
    Returns:
        Un tuple (club, competition) contenant les données de test.
    """
    # Déterminer le nombre de points (par défaut: 20)
    points = getattr(request, 'param', 20) if request else 20
    
    # Créer des copies des données de test
    test_club = {
        'name': 'Test Club',
        'email': 'test@club.com',
        'points': points
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
def past_competition():
    """
    Crée une compétition passée pour les tests.
    
    Returns:
        Les données de la compétition passée.
    """
    competition = {
        'name': 'Past Competition',
        'date': '2020-01-01 10:00:00',
        'numberOfPlaces': 10
    }
    competitions.append(competition)
    yield competition
    
    # Nettoyer après le test
    if competition in competitions:
        competitions.remove(competition)
    else:
        competitions.pop()  # Fallback si la référence n'est pas trouvée