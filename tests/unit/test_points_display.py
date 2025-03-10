import pytest
from flask import url_for
from server import app, clubs

# Test: Vérification du comportement avec des données clubs vides

def test_points_display_empty_data(client, setup_test_data):
    # Configuration pour le test
    app.config['SERVER_NAME'] = 'localhost:5000'
    
    # Simulation de l'absence de données clubs
    clubs.clear()

    # Génération des URLs dans le contexte d'application
    with client.application.app_context():
        points_display_url = url_for('points_display')
        index_url = url_for('index', _external=True)

    # Accès à la page des points
    response = client.get(points_display_url)

    # Vérification de la redirection
    assert response.status_code == 302
    assert response.location == index_url

    # Suivi de la redirection
    response = client.get(response.location)

    # Vérification du message d'erreur
    assert "No data available for clubs." in response.get_data(as_text=True) 