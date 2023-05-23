import json
from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def load_competitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = load_competitions()
clubs = load_clubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
    except IndexError:
        message = "Sorry, that email wasn't found"
        flash(message)
        return redirect(url_for('index'))
    return render_template('welcome.html',club=club,competitions=competitions)

@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    places_required = int(request.form["places"])
    clubPoints = int(club["points"])

    if places_required > 12:
        message = "You can't book more than 12 places"
        flash(message)
        return redirect(
            url_for("book", club=club["name"], competition=competition["name"])
        )
    elif clubPoints < placesRequired:
        message = "You don't have enough points."
        flash(message)
        return redirect(
            url_for("book", club=club["name"], competition=competition["name"])
        )
    else:
        competition["numberOfPlaces"] = (
            int(competition["numberOfPlaces"]) - places_required
        )
        flash("Great-booking complete!")
        return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
