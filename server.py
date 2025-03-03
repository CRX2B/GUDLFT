import json
from flask import Flask,render_template,request,redirect,flash,url_for
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
    email = request.form['email']
    club_list = [club for club in clubs if club['email'] == email]
    
    if not club_list:
        flash('Sorry, that email was not found.')
        return redirect(url_for('index'))
    
    club = club_list[0]
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        # Vérifier si la compétition est passée
        competition_date = datetime.strptime(foundCompetition['date'], '%Y-%m-%d %H:%M:%S')
        if competition_date < datetime.now():
            flash("This competition is over - you cannot book places for a past competition")
            return render_template('welcome.html', club=foundClub, competitions=competitions)
        
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    
    # Vérifier si la compétition est passée
    competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
    if competition_date < datetime.now():
        flash("This competition is over - you cannot book places for a past competition")
        return render_template('welcome.html', club=club, competitions=competitions)
    
    # Vérification que le club a suffisamment de points
    club_points = int(club['points'])
    if placesRequired > club_points:
        flash("You don't have enough points to purchase these places")
        return render_template('welcome.html', club=club, competitions=competitions)

    # Vérification que le nombre de places demandées ne dépasse pas 12
    if placesRequired > 12:
        flash("You cannot book more than 12 places per competition")
        return render_template('welcome.html', club=club, competitions=competitions)
    
    # Si assez de points, procéder à l'achat
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    # Déduire les points utilisés
    club['points'] = str(club_points - placesRequired)
    
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)