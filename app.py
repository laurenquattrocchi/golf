from flask import Flask, request, render_template, url_for
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
    return render_template("add_score.html")

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
    db.new_player_player(request.form)

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