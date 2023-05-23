import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def load_clubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def load_competitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
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
    club = [club for club in clubs if club["email"] == request.form["email"]][0]
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/show_summary_get/<email>", methods=["GET"])
def show_summary_get(email):
    """Render the welcome template after a booking edge case"""
    clubs = sorted(load_clubs(), key=lambda club: club["name"])
    competitions = load_competitions()
    try:
        club = next(club for club in clubs if club["email"] == email)
    except StopIteration:
        message = "Sorry, that email wasn't found"
        flash(message)
        return redirect(url_for("index"))
    return render_template(
        "welcome.html", club=club, clubs=clubs, competitions=competitions
    )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    found_club = [c for c in clubs if c["name"] == club][0]
    found_competition = [c for c in competitions if c["name"] == competition][0]
    if found_club and found_competition:
        date_competition = datetime.strptime(
            found_competition["date"], "%Y-%m-%d %H:%M:%S"
        )
        if date_competition < datetime.now():
            message = "You can't purchase places on a past competition."
            flash(message)
            return redirect(url_for("show_summary_get", email=found_club["email"]))
        return render_template(
            "booking.html", club=found_club, competition=found_competition
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
    placesRequired = int(request.form["places"])
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
