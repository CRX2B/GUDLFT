import json
from flask import Flask, render_template, request, redirect,flash, url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    # BUG CORRIGÉ: Utilisation de request.form.get() au lieu de request.form['email']
    # pour éviter l'erreur lorsqu'un email inexistant est saisi
    # Cette correction empêche l'application de planter et affiche un message d'erreur approprié
    email = request.form.get('email', '')
    club_list = [club for club in clubs if club['email'] == email]
    if not club_list:
        flash("Sorry, this email was not found")
        return render_template('index.html')
    club = club_list[0]
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)

def saveClubsAndCompetitions():
    with open('clubs.json', 'w') as c:
        json.dump({'clubs': clubs}, c, indent=4)
    with open('competitions.json', 'w') as comps:
        json.dump({'competitions': competitions}, comps, indent=4)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    
    # Conversion de la date de compétition pour comparaison
    competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')

    # BUG CORRIGÉ: Vérification que la compétition n'est pas déjà passée
    # Cette vérification empêche la réservation pour des compétitions qui ont déjà eu lieu
    if competition_date < datetime.now():
        flash("You cannot book places for past competitions")
        return render_template('booking.html', club=club, competition=competition)
    # VÉRIFICATION: S'assurer que le nombre de places est positif
    # Cette vérification évite les réservations avec un nombre invalide de places
    elif placesRequired < 1:
        flash("Sorry, select a number of places greater than 0")
        return render_template('booking.html', club=club, competition=competition)
    # BUG CORRIGÉ: Vérification que le club a suffisamment de points
    # Cette vérification empêche un club de dépenser plus de points qu'il n'en possède
    elif club['points'] < placesRequired:
        flash("You cannot use more points than you have")
        return render_template('booking.html', club=club, competition=competition)
    # BUG CORRIGÉ: Limitation du nombre de places à 12 par compétition
    # Cette vérification impose une limite équitable sur le nombre de places qu'un club peut réserver
    elif placesRequired > 12:
        flash("You cannot book more than 12 places per competition")
        return render_template('booking.html', club=club, competition=competition)
    else:
        # Mise à jour du nombre de places disponibles
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        
        # BUG CORRIGÉ: Déduction des points du compte du club
        # Cette correction assure que les points sont correctement déduits lors de la réservation
        club['points'] -= placesRequired
        
        flash('Purchase successful')
        # Sauvegarde des modifications dans les fichiers JSON
        saveClubsAndCompetitions()
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

# NOUVELLE FONCTIONNALITÉ: Tableau d'affichage public des points des clubs
# Cette route permet aux utilisateurs de voir les points des clubs sans se connecter
@app.route('/points')
def points_display():
    if not clubs:
        flash("No data available for clubs.")
        return redirect(url_for('index'))
    return render_template('points.html', clubs=clubs)

if __name__ == "__main__":
    app.run()