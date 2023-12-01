# from sys import exception
# from tkinter import EXCEPTION
import psycopg2
import util
import psycopg2.extras
import psycopg2.errors as errors

class DB:
    # copied from DB project --> set up
    def __init__(self, connection):
        self.conn = connection

    def new_player(self,form):
        '''
        inserts new player into database
        input: form data
        returns (tuple): (True,) if succsfull, (False,error msg if failed
        '''

        # parameterize sql statement to prevent injection 
        insert_player = '''INSERT INTO players (fname, lname, handicapp) VALUES (%s,%s,%s)  RETURNING player_id;'''
        insert_dependency = '''INSERT INTO player_outing (player_id, outing_id) VALUES (%s,%s)'''

        #create a cursor object from connection module
        c = self.conn.cursor()

        try:
            c.execute(insert_player, (form['fname'], form['lname'], form['handicapp']))
            id = c.fetchone()[0]
        except psycopg2.errors.SyntaxError as e:
            print('error inserting player', e)
            return (False, e)

        try:
            c.execute(insert_dependency, (id, 1))
        except psycopg2.errors.SyntaxError as e:
            print('error inserting player', e)
            return (False, e)

        try:
            self.conn.commit()
        except psycopg2.errors.SyntaxError as e:
            print('error committing', e)
            return (False, e)
        
        return (True,)
    
    def new_scores(self,player_id, course_id, form, outing_id=1):
        c = self.conn.cursor()
        round_id = self.insert_round(course_id, outing_id)
        holes = self.course_handicapp(course_id)
        handicapp = self.player_handicapp(player_id)
        h_score=util.h_adjusted_score(holes,list(form.values()),handicapp,9)

        print(h_score)
        value_base = '['
        values=[]
        #value_base = ''

        base ='''INSERT INTO score (PLAYER_ID, ROUND_ID, HOLE, SCORE, HANDICAPP_SCORE) VALUES %s'''
        # have to build value part of string and scores to calc h_score
        # for i, hole in enumerate(form.items()):
        #     hole,score = hole
        #     base = base + ' (%s,%s,%s,%s,%s)'
        #records_list_template = ','.join(['%s'] * len(h_score))

        #insert_query = base.format(records_list_template)
        for i,score in enumerate(h_score):
            value_base = value_base + f'({player_id}, {round_id}, {i+1}, {score}, {h_score[i]}), ' 
            values.append((player_id, round_id, i+1, score, h_score[i]))

        value_base = value_base[:-2] + ']'

        print(base)

        values2 = [
            (1, 1, 1, 0, 0),
            (1, 1, 2, 2, 2),
            (1, 1, 3, 3, 3),
            (1, 1, 4, 3, 3),
            (1, 1, 5, 3, 3),
            (1, 1, 6, 3, 3),
            (1, 1, 7, 4, 4),
            (1, 1, 8, 6, 6),
            (1, 1, 9, 6, 6)
        ]
        value_base = list(value_base)
        print(type(value_base))
        print(values)
        print(type(values))
        try:
            psycopg2.extras.execute_values (
                c, base, values
            )
        except psycopg2.errors.SyntaxError as e:
            print(str(e))
        except Exception as e:
            print(e)

        self.conn.commit()
        # c.execute(insert_query, value_base)
        
    def new_outing(self, form):
        # insert into table
        # return true if insert is success
        print(form)
        return None

    def get_outings(self, id = None):
        # return all players regardless of outing
        c = self.conn.cursor()
        if id == None:
            c.execute('select * from outing;')
        else:
            # paramaterize
            c.execute('select * from outing where id = id;')
        return c.fetchall()
    
    def update_outing(self):
        pass
    
    def get_courses(self):
        # return all players regardless of outing
        c = self.conn.cursor()
        c.execute('select * from course;')
        return c.fetchall()

    def get_games(self):
        # return all players regardless of outing
        c = self.conn.cursor()
        c.execute('select * from game_type;')
        return c.fetchall()    
    
    def get_players(self):
        # return all players regardless of outing
        c = self.conn.cursor()
        c.execute('select * from player;')
        return c.fetchall()
    
    def player_details(self,id):
        # returns player and scores, grouped by outing
        c = self.conn.cursor()
        query='''SELECT outing_id, p.*, sum(score) as score, sum(handicapp_score) as h_score 
                from players p 
                JOIN scores s on p.player_id = s.player_id 
                where player_id=(%s) group by outing_id, p.player_id;'''
        c.execute(query, (id,))
        return c.fetchall()      

    def outing_details(self, outing_id=1):
        # returns all players in outings and their total scores
        c = self.conn.cursor()
        query='''SELECT o.name, p.*, sum(score) as score, sum(handicapp_score) as h_score  
            from players p 
            JOIN scores s on p.player_id = s.player_id 
            JOIN player_outing po on p.player_id = po.player_id 
            JOIN outings o on po.outing_id = o.outing_id
            where o.outing_id = (%s) group by o.outing_id, p.player_id;'''
        
        c.execute(query, (id,))
        return c.fetchall()
    
    def round_details(self, outing_id, player_id):
        # returns total player score for player by round
        c = self.conn.cursor()
        query = """select p.*, """
    
    def course_handicapp(self, course_id):
        #get handicapp for each hole
        c = self.conn.cursor() 
        query ='''select hole,handicapp from hole where course_id=(%s)''' 
        c.execute(query,(course_id,))
        holes = c.fetchall()
        #just in case doesn't pull from database in hole order?
        holes = sorted(holes)
        return holes

    def insert_round(self,course_id, outing_id):
        # only insert if doesn't already exists
        c = self.conn.cursor() 
        c.execute("SELECT round_id from round where course_id=(%s) and outing_id=(%s);", (course_id, outing_id))
        round_id = c.fetchall()
        if round_id==[]:
            insert_round = '''INSERT INTO round (course_id, outing_id) VALUES (%s,%s) RETURNING round_id'''
            c.execute(insert_round, (course_id, outing_id))
            return c.fetchone()[0]
        else:
            return round_id[0][0]

    def player_handicapp(self,player_id):
        # get individual players handicapp
        c = self.conn.cursor()
        h_query = '''select handicapp from player where player_id=(%s)''' 
        c.execute(h_query,(player_id,))
        # error handle, if this errors, playerid doesn't exist
        return c.fetchall()[0][0]


    def test(self):
        from psycopg2 import extras
        # Create a cursor
        c = self.conn.cursor()

        # Your list of values
        values = [
            (1, 1, 1, 0, 0),
            (1, 1, 2, 2, 2),
            (1, 1, 3, 3, 3),
            (1, 1, 4, 3, 3),
            (1, 1, 5, 3, 3),
            (1, 1, 6, 3, 3),
            (1, 1, 7, 4, 4),
            (1, 1, 8, 6, 6),
            (1, 1, 9, 6, 6)
        ]

        # Your base SQL query
        base = '''INSERT INTO score (PLAYER_ID, ROUND_ID, HOLE, SCORE, HANDICAPP_SCORE) VALUES %s'''

        # Execute the query using execute_values
        print(extras.execute_values(c, base, values))