import pytest
from server import app, clubs, competitions

# Test: Vérification du fonctionnement normal de la route book

def test_book_valid_data(client, setup_test_data):
    club, competition = setup_test_data
    
    # Accès à la page de réservation avec des données valides
    response = client.get(f'/book/{competition["name"]}/{club["name"]}')
    
    # Vérification de la réponse
    assert response.status_code == 200
    assert "Places available" in response.get_data(as_text=True)
    assert club["name"] in response.get_data(as_text=True)
    assert competition["name"] in response.get_data(as_text=True)

# Test: Vérification de la gestion d'un club inexistant

def test_book_invalid_club(client, setup_test_data):
    _, competition = setup_test_data
    
    # Accès avec un nom de club invalide
    response = client.get(f'/book/{competition["name"]}/NonExistentClub')
    
    # Vérification de la réponse et de la redirection
    assert response.status_code == 200
    assert "Something went wrong" in response.get_data(as_text=True)

# Test: Vérification de la gestion d'une compétition inexistante

def test_book_invalid_competition(client, setup_test_data):
    club, _ = setup_test_data
    
    # Accès avec un nom de compétition invalide
    response = client.get(f'/book/NonExistentCompetition/{club["name"]}')
    
    # Vérification de la réponse et de la redirection
    assert response.status_code == 200
    assert "Something went wrong" in response.get_data(as_text=True) 