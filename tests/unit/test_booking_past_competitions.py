import pytest
from server import app, clubs, competitions
from datetime import datetime

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

# Test unitaire pour vérifier que les réservations pour des compétitions passées sont empêchées

def test_booking_past_competition(client, past_competition):
    club = clubs[0]
    response = client.post('/purchasePlaces', data={
        'competition': past_competition['name'],
        'club': club['name'],
        'places': 1
    })
    assert response.status_code == 200
    assert "You cannot book places for past competitions" in response.get_data(as_text=True)