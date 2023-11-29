from flask import Flask, request, render_template #, url_for
import logging
import psycopg2
from db import DB

# Configure application
app = Flask(__name__)

# update to pull from app
outing = 1

#DB connection REMOVE HARD CODING
db_conn = psycopg2.connect("dbname=postgres user=postgres password=jzYezhkUW3UUXn")

# default path
@app.route('/')
def home():
    # return render_template("add_score.html")
    return render_template("homepage.html")

@app.route('/test')
def test():
    # return render_template("add_score.html")
    return render_template("test_child.html")

@app.route('/add_player', methods=["POST"])
def add_player():
    '''
    Inserts a player in the database and its dependencies 
    (ex: player/outing table)
    '''
    # fname = request.form['fname']
    # lname = request.form['lname']
    # handi = request.form['handicapp']
    print(request.form)
    db = DB(db_conn)
    db.new_player(request.form)

    return render_template("base.html")

@app.route('/get_players', methods=["GET"])
def get_players():
    '''
    Returns all players in the database
    '''
    # fname = request.form['fname']
    # lname = request.form['lname']
    # handi = request.form['handicapp']
    print(request.form)
    db = DB(db_conn)
    players = db.all_player()
    # fname = players[0][1]
    fname = players

    return render_template("base.html", players=fname)

@app.route('/add_outing', methods=["POST"])
def add_outing():
    '''
    Inserts a player in the database and its dependencies 
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

    return render_template("base.html")

@app.route('/outings/new', methods=["GET", "POST"])
def new_outings():
    '''
    should this be in same endpoint as outings somehow?
    '''
    # fname = request.form['fname']
    # lname = request.form['lname']
    # handi = request.form['handicapp']
    print(request)
    db = DB(db_conn)
    outings = db.all_outings()
    # fname = players[0][1]
    if request.method == 'POST':
        # create new outing
        db.new_outing(request.form)
        outings=["we", "did", "it"]
        #if successful return success message
        return render_template("layout.html", outings=outings) 
    else:
        # get players, courses, and games for form
        players = db.all_players()
        print(players)
        courses = db.all_courses()
        print(courses)
        games = db.all_games()
        print(games)

        return render_template("outings.html", players=players, courses = courses,games=games)

@app.route('/outings', methods=["GET"])
def outings():
    '''
    Returns all outings in the database
    '''
    # fname = request.form['fname']
    # lname = request.form['lname']
    # handi = request.form['handicapp']
    print(request)
    db = DB(db_conn)
    outings = db.all_outings()
    return render_template("outings.html", outings=outings)

# @app.route('/add_outing', methods=["POST"])
# def add_outing():
#     """Inserts new outting into DB"""
@app.route('/input_scores', methods=["POST"])
def input_scores():
    '''add scores for a new round'''
    db = DB(db_conn)
    db.new_scores(2,1, request.form)
    fname='test'
    return render_template("base.html", players=fname)

    

if __name__ == '__main__':
    app.run(debug=True, threaded=False)