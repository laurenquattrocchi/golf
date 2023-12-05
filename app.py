from flask import Flask, request, render_template #, url_for
import logging
import psycopg2
from db import DB
from getpass import getpass

# Configure application
app = Flask(__name__)

# update to pull from app
outing = 1

#DB connection
db_conn = psycopg2.connect(
    dbname="postgres",
    user="postgres")#, 
    #password="jzYezhkUW3UUXn")

# default path
@app.route('/')
def home():
    # return render_template("add_score.html")
    return render_template("homepage.html")

@app.route('/test')
def test():
    # return render_template("add_score.html")
    return render_template("test_child.html")

# updated 12/5
@app.route('/players', methods=["GET", "POST"])
def players():
    '''
    Returns all players in the database
    Inserts a player in the database and its dependencies 
    (ex: player/outing table)
    '''
    db = DB(db_conn)
    if request.method == "GET":
        try:
            success, players = db.get_players()
            if success:
                return render_template("display.html", header="Players", 
                        content=players),200
            else:
                return render_template("error.html", error=players), 500
        except TypeError as e:
            return render_template("error.html", error = e), 500

    # outing_id will have to be passed in form data somehow - hidden field?
    elif request.method == "POST":
        try:
            new = db.new_player(request.form)
            if new: # new player created
                return render_template("base.html", player=request.form['fname']), 201
            else: # db side error:
                return render_template("error.html", error=e), 500 
        except Exception as e:
            print("error when called db new player", e)
            return render_template("error.html", error=e), 500 

# updated 12/5 - needs delete still
@app.route('/players/<player_id>', methods=["GET", "PATCH", "DELETE"])
def player(player_id):
    '''player information: name, handicapp'''
    db = DB(db_conn)
    if request.method == "GET":
        try:
            success, players = db.get_players(player_id)
            if success:
                return render_template("display.html", header="Player", 
                        content=players),200
            else:
                return render_template("error.html", error=players), 500
        except TypeError as e:
            return render_template("error.html", error = e), 500
    elif request.method == "PATCH":
        print(request.form)
        db.update_player(request.form,player_id)
        return render_template("display.html", header="Updated Player"),200
    elif request.method == "DELETE":
        # need to update delete queries
        pass

# updated 12/5 -> needs error handeling, make another endpoint to get all 
# round scores for player_id?
# need to fix db.new_scores()
# @app.route('/players/<player_id>/rounds', methods=["GET", "POST", "PATCH", "DELETE"])
# get player_id from form
@app.route('/players/rounds', methods=["GET", "POST", "PATCH", "DELETE"])
def round():
    '''
    round details (score per hole) for player
        add scores for a new round

    '''
    db = DB(db_conn)
    if request.method == "GET":
        success, players = db.get_players()
        for x in players:
            print(x[0], x[1])
        print(players)
        success,courses = db.get_courses()
        print(courses)
        return render_template("add_score.html", courses=courses, players=players)
    # form include course - from drop down, send id
    elif request.method == "POST":
        print(request.form)
        db.new_scores(request.form)
        return render_template("display.html", header="ADDED SCORE")

@app.route('/players/<player_id>/scores', methods=["GET"])
def player_scores(player_id):
    '''
    returns player name, total ryder cups points and $ per outing
    '''
    # extract id from url - update this, does id need to come after scores?

@app.route('/outings', methods=["GET", "POST"])
def outings():
    '''
    Inserts a outing in the database and its dependencies 
    (ex: player/outing table)
    '''
    print(request.form)
    db = DB(db_conn)
    try:
        success = db.new_outing(request.form)
    except Exception as e:
        print(e)
    print(request.form)
    if success:
        pass
        # render name of outing created succesfully 

    '''
    Returns all outings in the database
    '''
    print(request)
    db = DB(db_conn)
    outings = db.get_outings()
    return render_template("outings.html", outings=outings)

@app.route('/outings/new', methods=["GET", "POST"])
def new_outing():
    '''
    should this be in same endpoint as outings somehow?
    builds form for new outing to be created and then sent
    to /outings
    '''
    print(request)
    db = DB(db_conn)
    outings = db.get_outings()
    # fname = players[0][1]
    if request.method == 'POST':
        # create new outing
        db.new_outing(request.form)
        outings=["we", "did", "it"]
        #if successful return success message
        return render_template("layout.html", outings=outings) 
    else:
        # get players, courses, and games for form
        players = db.get_players()
        courses = db.get_courses()
        print(courses)
        games = db.get_games()
        print(games)

        return render_template("outings.html", players=players, courses = courses,games=games)

@app.route('/outings/id', methods=["GET", "PATCH", "DELETE"])
def outing():
    '''updates/deletes/returns outing info:players, courses'''
    # extract id from url
    pass


@app.route('/outings/outing_id/scores', methods=["GET", "PATCH", "DELETE"])
def outing_scores():
    '''returns all players names, total ryder cups points and $ for outing'''
    pass
    # does id have to come last because that is info using?


@app.route('/courses', methods=["GET", "POST"])
def courses():
    '''
    Returns all courses in the database
    Inserts a course in the database and its dependencies 
    '''
    pass

@app.route('/courses/id', methods=["GET", "PATCH", "DELETE"])
def course():
    ''''''
    pass
    # extract id from url - update this

@app.route('/games', methods=["GET", "POST"])
def games():
    '''
    Returns all games in the database
    Inserts a game in the database and its dependencies 
    '''
    pass

@app.route('/games/id', methods=["GET", "PATCH", "DELETE"])
def game():
    '''
    retrieves/updates/deletes game
    '''
    pass
    # extract id from url - update this

    

if __name__ == '__main__':
    app.run(debug=True, threaded=False)