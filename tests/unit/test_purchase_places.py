import pytest
from server import app, clubs, competitions

# Test: Vérification de la limite de points pour les réservations

def test_purchase_places_exceeding_points(client, setup_test_data):
    club, future_competition = setup_test_data
    initial_points = club['points']
    # Nombre de places supérieur aux points disponibles
    places_to_book = initial_points + 1
    
    response = client.post('/purchasePlaces', data={
        'competition': future_competition['name'],
        'club': club['name'],
        'places': places_to_book
    })
    assert response.status_code == 200
    assert "You cannot use more points than you have" in response.get_data(as_text=True)
    # Vérification que les points restent inchangés
    assert club['points'] == initial_points

# Test: Vérification du refus des réservations à zéro places

def test_reserve_zero_places(client, setup_test_data):
    club, competition = setup_test_data

    # Tentative de réservation de 0 places
    response = client.post('/purchasePlaces', data={
        'competition': competition['name'],
        'club': club['name'],
        'places': 0
    })
    assert response.status_code == 200
    assert "Sorry, select a number of places greater than 0" in response.get_data(as_text=True) 