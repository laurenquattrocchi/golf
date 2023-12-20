# from sys import exception
# from tkinter import EXCEPTION
import psycopg2
import util
import psycopg2.extras
import psycopg2.errors

class DB:
    # copied from DB project --> set up
    def __init__(self, connection):
        self.conn = connection

    def delete(self, entity, id):
        '''
        delete player, course, outing and assocaited dependecies
        '''
        if entity == 'player':
            #delete from player table, player_outing, score,
            pass
        elif entity == 'course':
            # delete from course, course_outing, hole, outing_details??, 
            pass
        elif entity == 'outing':
            pass
        elif entity == 'score':
            pass
        elif entity == 'game':
            pass
    
    def valid_login(self,form):
        '''
        check if form.email.data and 
        form.password.data == valid email and password for user
        input: wtform from inputform()
        output (boolean): True if email and pswd valid, False otherwiser

        '''
        c = self.conn.cursor()
        query = '''select password from user_ where email=(%s)'''
        c.execute(query, (form.email.data,))
        #pswd = c.fetchall()
        pswd = c.fetchone()
        print(pswd)
        ### NEED TO HANDLE HASHING PASSWORD 
        if pswd[0] == form.password.data:
            return True, 4
        else:
            return False, 7

    def new_user(self,form):
        '''
        inserts new user into user_ table and player in player_ table
        input: form data
        returns (tuple): (True,) if succsfull, (False,error msg if failed)
        '''

        #confirm user by email doesn't already exist
        c = self.conn.cursor()

        # parameterize sql statement to prevent injection 
        insert_user = '''INSERT INTO user_ (player_id, email, salt, password) VALUES (%s,%s,%s,%s)  RETURNING user_id;'''
        # update to just call new player once determine which form want to move forward with wtform/html form
        insert_player = '''INSERT INTO player_ (fname, lname, handicap) VALUES (%s,%s,%s) RETURNING player_id;'''
        try:
            c.execute(insert_player, (form.first_name.data, form.last_name.data, form.handicap.data))
            player_id = c.fetchone()[0]
        except psycopg2.errors.SyntaxError as e:
            print('error inserting player', e)
            self.conn.rollback()
            return (False, e)
        
        # HASH PASSWORD BEFORE STORING
        try:
            c.execute(insert_user, (player_id, form.email.data, "placeholder", form.password.data))
            user_id = c.fetchone()[0]
        except psycopg2.errors.UniqueViolation as e:
            self.conn.rollback()
            return(False, "duplicate")
        except psycopg2.errors.SyntaxError as e:
            print('error inserting user', e)
            self.conn.rollback()
            return (False, e)
        
        try:
            self.conn.commit()
        except psycopg2.errors.SyntaxError as e:
            self.conn.rollback()
            print('error committing', e)
            return (False, e) 
   
        return (True,"")      


    def new_player(self,form):
        '''
        inserts new player into database
        input: form data
        returns (tuple): (True,) if succsfull, (False,error msg if failed)
        '''

        # parameterize sql statement to prevent injection 
        insert_player = '''INSERT INTO player_ (fname, lname, handicap) VALUES (%s,%s,%s)  RETURNING player_id;'''
        insert_dependency = '''INSERT INTO player_outing_ (player_id, outing_id) VALUES (%s,%s)'''

        #create a cursor object from connection module
        c = self.conn.cursor()

        try:
            c.execute(insert_player, (form['fname'], form['lname'], form['handicap']))
            id = c.fetchone()[0]
        except psycopg2.errors.SyntaxError as e:
            print('error inserting player', e)
            return (False, e)

        try:
            c.execute(insert_dependency, (id,  form['outingId']))
        except psycopg2.errors.SyntaxError as e:
            print('error inserting player', e)
            return (False, e)

        try:
            self.conn.commit()
        except psycopg2.errors.SyntaxError as e:
            print('error committing', e)
            return (False, e)
        
        return (True,)
    
    def new_scores(self,form, outing_id=1):
        '''
        determines handicap scores and 
        inserts new scores for a round into score table
        input: form data # outing id will be included in form data at somepoint??
        returns (tuple): (True,) if succsfull, (False,error msg if failed)
        '''
        c = self.conn.cursor()
        round_id = self.insert_round(form['course'], outing_id)
        holes = self.course_handicap(form['course'])
        handicap = self.player_handicap(form['player'])
        scores = list(form.values())[2:]  # [2:] -> player and course id first 2 values in list      
        h_score=util.h_adjusted_score(holes,scores,handicap,9)
        values=[]
        base ='''INSERT INTO score_ (PLAYER_ID, ROUND_ID, HOLE, SCORE, handicap_SCORE) VALUES %s'''
        for i,score in enumerate(h_score):
            values.append((form['player'], round_id, i+1, scores[i], score))
        try:
            psycopg2.extras.execute_values (
                c, base, values
            )
        except psycopg2.errors.SyntaxError as e:
            print('error inserting player', e)
            return (False, e)
        except Exception as e:
            print('eror', e)
            return (False, e)

        try:
            self.conn.commit()
        except psycopg2.errors.SyntaxError as e:
            print('error committing', e)
            return (False, e)
        
        return (True,"success")

        
    def new_outing(self, form):
        '''
        inserts new outing into database
        input: form data
        returns (tuple): (True,) if succsfull, (False,error msg if failed)
        '''

        # parameterize sql statement to prevent injection 
        insert_outing = '''INSERT INTO outing_ (name) VALUES (%s,)  RETURNING outing_id;'''
        insert_dependency = '''INSERT INTO course_outing_ (outing_id, course_id,) VALUES (%s,%s)'''

        #create a cursor object from connection module
        c = self.conn.cursor()

        try:
            c.execute(insert_outing, (form['name'],))
            id = c.fetchone()[0]
        except psycopg2.errors.SyntaxError as e:
            print('error inserting outing', e)
            return (False, e)

        try:
            c.execute(insert_dependency, (id,  form['course_id']))
        except psycopg2.errors.SyntaxError as e:
            print('error inserting player', e)
            return (False, e)

        try:
            self.conn.commit()
        except psycopg2.errors.SyntaxError as e:
            print('error committing', e)
            return (False, e)
        
        return (True,)

    def get_outings(self, id = None):
        # return all players regardless of outing
        c = self.conn.cursor()
        if id == None:
            c.execute('select * from outing_;')
        else:
            # paramaterize
            query = 'select * from outing_ where id = (%s)'
            c.execute(query, (id,))
        return c.fetchall()
    
    def update_outing(self, form={'name':'test', 'id':1}):
        '''
        updates outing information
        input: postgres connection object, form data (dict)
        returns (tuple): (True,) if succsfull, (False,error msg if failed) 
        '''
        c = self.conn.cursor()
        params =  []
        query = 'UPDATE outing SET '

        if 'name' in form:
            query += 'name = (%s) '
            params.append(form['name'])
           
        query += ' WHERE outing_id=(%s);'
        params.append(form['id']) 
        print(query, params)
        try:
            c.execute(query, tuple(params))
            self.conn.commit()
        #catch more specific errors
        except Exception as e:
            return (False, e)
        return (True, 'updated')  
    
    def get_courses(self, id = None):
        # return all  courses regardless of outing
        # input postgres connection object 
        c = self.conn.cursor()
        query = 'select * from course_'
        if id:
            query += 'where course_id=(%s)'
        try:
            c.execute(query, (id,))
        except psycopg2.errors.SyntaxError as e:
            return (False, e)
        except psycopg2.errors.UndefinedTable as e:
            return (False, e)
        return (True,c.fetchall())

    def get_games(self):
        # return all games
        # input: postgres connection object 
        c = self.conn.cursor()
        c.execute('select * from game_type_;')
        return c.fetchall()    
    
    def get_players(self, id=None):
        '''
        retrieves all players regardless of outing
        input: postgres connection object 
        returns: (boolean, string) tuple: True and query result if succesful, 
            False and error if fails
        '''
        c = self.conn.cursor()

        query = 'select * from player_'
        if id:
            query += 'where player_id=(%s)'
        try:
            c.execute(query, (id,))
        except psycopg2.errors.SyntaxError as e:
            return (False, e)
        except psycopg2.errors.UndefinedTable as e:
            return (False, e)
        return (True,c.fetchall())
    
    def update_player(self, form, id):
        '''
        updates player info
        input: db connection and form (dict)
        returns (tuple): 
            True and player name if success, 
            False and error if fails
        if id doesn't exist updates 0, doesn't error
        '''
        c = self.conn.cursor()
        params =  []
        query = 'UPDATE player SET '

        if 'fname' in form:
            query += 'fname = (%s) '
            params.append(form['fname'])
        if 'lname' in form:
            if 'fname' in form:
                query += ', '
            query += ' lname = (%s) '
            params.append(form['lname'])
        if 'handicap' in form:
            # only add comma if another param
            if 'fname' in form or 'lname' in form:
                query += ', '
            query += ' handicap = (%s) '
            params.append(form['handicap'])
            
        query += ' WHERE player_id=(%s);'
        params.append(id) 
        print(query, params)
        c.execute(query, tuple(params))
        self.conn.commit()
        return True  

    
    def player_details(self,id):
        # returns player and scores, grouped by outing
        c = self.conn.cursor()
        query='''SELECT outing_id, p.*, sum(score) as score, sum(handicap_score) as h_score 
                from player_ p 
                JOIN score_ s on p.player_id = s.player_id 
                where player_id=(%s) group by outing_id, p.player_id;'''
        c.execute(query, (id,))
        return c.fetchall()      

    def outing_details(self, outing_id=1):
        # returns all players in outings and their total scores
        c = self.conn.cursor()
        query='''SELECT o.name, p.*, sum(score) as score, sum(handicap_score) as h_score  
            from player_ p 
            JOIN score_ s on p.player_id = s.player_id 
            JOIN player_outing_ po on p.player_id = po.player_id 
            JOIN outing_ o on po.outing_id = o.outing_id
            where o.outing_id = (%s) group by o.outing_id, p.player_id;'''
        
        c.execute(query, (id,))
        return c.fetchall()
    
    def round_details(self, outing_id, player_id):
        # returns total player score for player by round
        c = self.conn.cursor()
        query = """SELECT round_id, sum(score) as score, sum(handicap_score) as h_score 
                   FROM score_
                   WHERE player_id = (%s) AND 
                   round_id IN (select round_id from round_ where outing_id = (%s))
                   GROUP BY round_id; """
        
        try:
            c.execute(query, (player_id,outing_id))
            totals = c.fetchall()
            print(totals)
        except Exception as e:
            self.conn.rollback()
            print('failed to execute, rolling back', e)

    def course_handicap(self, course_id):
        #get handicap for each hole
        c = self.conn.cursor() 
        query ='''select hole,handicap from hole_ where course_id=(%s)''' 
        c.execute(query,(course_id,))
        holes = c.fetchall()
        #just in case doesn't pull from database in hole order?
        holes = sorted(holes)
        return holes

    def insert_round(self,course_id, outing_id):
        # UPDATE TO only insert if doesn't already exists
        c = self.conn.cursor() 
        c.execute("SELECT round_id from round_ where course_id=(%s) and outing_id=(%s);", (course_id, outing_id))
        round_id = c.fetchall()
        if round_id==[]:
            insert_round = '''INSERT INTO round_ (course_id, outing_id) VALUES (%s,%s) RETURNING round_id'''
            c.execute(insert_round, (course_id, outing_id))
            return c.fetchone()[0]
        else:
            return round_id[0][0]

    def player_handicap(self,player_id):
        # get individual players handicap
        c = self.conn.cursor()
        h_query = '''select handicap from player_ where player_id=(%s)''' 
        c.execute(h_query,(player_id,))
        # error handle, if this errors, playerid doesn't exist
        return c.fetchall()[0][0]