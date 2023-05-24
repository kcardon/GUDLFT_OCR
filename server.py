import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def load_competitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__, static_folder="static")
app.secret_key = "something_special"

competitions = load_competitions()
clubs = load_clubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/show_summary", methods=["POST"])
def show_summary():
    """Render the welcome template when coming from the login page"""
    clubs = sorted(load_clubs(), key=lambda club: club["name"])
    try:
        club = next(club for club in clubs if club["email"] == request.form["email"])

    except StopIteration:
        message = "Sorry, that email wasn't found"
        flash(message)
        return redirect(url_for("index"))
    return render_template(
        "welcome.html", club=club, clubs=clubs, competitions=competitions
    )


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
    clubs = load_clubs()
    competitions = load_competitions()
    try:
        foundClub = next(c for c in clubs if c["name"] == club)
        foundCompetition = next(c for c in competitions if c["name"] == competition)
    except StopIteration:
        flash("Something went wrong-please try again")
        return render_template(
            "welcome.html", club=club, clubs=clubs, competitions=competitions
        )
    competitionDate = datetime.strptime(foundCompetition["date"], "%Y-%m-%d %H:%M:%S")
    if competitionDate < datetime.now():
        message = "You can't book places on a past competition."
        flash(message)
        return redirect(
            url_for(
                "show_summary_get",
                email=foundClub["email"],
            )
        )
    return render_template("booking.html", club=foundClub, competition=foundCompetition)


@app.route("/purchasePlaces", methods=["POST"])
def purchase_places():
    clubs = load_clubs()
    competitions = load_competitions()

    competition = next(
        c for c in competitions if c["name"] == request.form["competition"]
    )
    club = next(c for c in clubs if c["name"] == request.form["club"])

    placesRequired = int(request.form["places"])
    clubPoints = int(club["points"])
    competitionPlaces = int(competition["numberOfPlaces"])
    print(clubPoints)
    # Should not book more than 12 places
    if placesRequired > 12:
        message = "You can't book more than 12 places"
        flash(message)
        return redirect(
            url_for(
                "book", club=club["name"], clubs=clubs, competition=competition["name"]
            )
        )
    # Should not book more places than points available
    elif clubPoints < placesRequired:
        print(
            "The club has "
            + str(clubPoints)
            + " points and you need "
            + str(placesRequired)
        )
        message = "You don't have enough points."
        flash(message)
        return redirect(
            url_for(
                "book", club=club["name"], clubs=clubs, competition=competition["name"]
            )
        )
    # else, should update competition number of places and club points.
    # if not enough places, book max places as available and display the competition as full.
    else:
        bookedPlaces = min(competitionPlaces, placesRequired)
        competitionPlaces -= bookedPlaces
        competition["numberOfPlaces"] = competitionPlaces
        club["points"] = int(club["points"]) - bookedPlaces
        flash("You purchase is completed.")
        flash(
            "You have successfully booked "
            + str(bookedPlaces)
            + " places for the "
            + competition["name"]
            + " competition."
        )
        if competitionPlaces < 1:
            flash("The competition is full.")
        return render_template(
            "welcome.html", club=club, clubs=clubs, competitions=competitions
        )


@app.route("/clubs_board")
def clubs_board():
    """display a board with each club and their number of available points"""
    clubs = sorted(load_clubs(), key=lambda club: club["name"])
    return render_template("clubs_board.html", clubs=clubs)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
