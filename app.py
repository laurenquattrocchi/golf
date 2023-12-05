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

@app.route('/players', methods=["GET", "POST"])
def players():
    '''
    Returns all players in the database
    Inserts a player in the database and its dependencies 
    (ex: player/outing table)
    '''
    db = DB(db_conn)
    if request.method == "GET":
        print(request.form)
        players = db.get_players()
    elif request.method == "POST":
        try:
            new = db.new_player(request.form)
        except Exception as e:
            print("error when called db new player", e)
        if new: # new player created
            return render_template("base.html", players=fname), 201
        else: # db side error:
            return render_template("error.html", e), 500   
    fname = players
    return render_template("base.html", players=fname)

@app.route('/players/<player_id>', methods=["GET", "PATCH", "DELETE"])
def player(player_id):
    '''player information: name, handicapp'''
    pass
    # extract id from url - update this

@app.route('/players/<player_id>/rounds', methods=["GET", "POST", "PATCH", "DELETE"])
def round(player_id):
    '''
    round details (score per hole) for player
        add scores for a new round

    '''
    # extract id from url - update this, does id need to come after rounds?
    db = DB(db_conn)
    db.new_scores(2,1, request.form)
    fname='test'
    return render_template("base.html", players=fname)

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
        print(players)
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