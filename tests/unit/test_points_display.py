import pytest
from flask import url_for
from server import app, clubs


def test_points_display_empty_data(client, setup_test_data):
    # Configurer SERVER_NAME pour le test
    app.config['SERVER_NAME'] = 'localhost:5000'
    
    # Vider directement la liste des clubs
    clubs.clear()

    # Utiliser le contexte de l'application pour générer l'URL
    with client.application.app_context():
        points_display_url = url_for('points_display')
        index_url = url_for('index', _external=True)

    # Effectuer une requête GET sur la route /points
    response = client.get(points_display_url)

    # Vérifier la redirection vers la page d'accueil
    assert response.status_code == 302
    assert response.location == index_url

    # Suivre la redirection
    response = client.get(response.location)

    # Vérifier que le message d'erreur est affiché
    assert "No data available for clubs." in response.get_data(as_text=True) 