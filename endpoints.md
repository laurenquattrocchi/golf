| HTTP Method	|	Endpoint	        |	Description
| -------         -------                 -------
| GET	        |	/players	        |	returns all players
| POST	        |	/players	        |	adds new players
| GET	        |	/players/id	        |	returns player information: name, handicapp
| PATCH	        |	/players/id	        |	updates player information: name, handicapp
| DELETE	    |	/players/id	        |	deletes player information: name, handicapp
| GET	        |	/players/id/rounds	|	return round details (score per hole) for player
| POST	        |	/players/id/rounds	|	adds new round for player (score for 9 or 18 holes)
| GET	        |	/players/id/scores	|	returns player name, total ryder cups points and $ per outing
| POST	        |	/outings	        |	adds new outing
| GET	        |	/outings	        |	returns all outings
| DELETE	    |	/outings/id	        |	deletes outing
| PATCH	        |	/outings/id	        |	updates outing info:players, courses
| GET	        |	/outings/id	        |	returns outing info:players, courses
| GET	        |	/outings/id/scores	|	returns all players from outing and there total points and $
| POST	        |	/courses	        |	adds new course
| GET	        |	/courses	        |	returns list of courses
| PATCH	        |	/courses/id	        |	updates course info
| GET	        |	/courses/id	        |	returns course info
| DELETE	    |	/courses/id	        |	deletes course
| POST	        |	/games	            |	adds new game criteria
| GET	        |	/games	            |	returns list of games
| DELETE	    |	/games/id	        |	deletes game
| PATCH	        |	/games/id	        |	updates game
| GET	        |	/games/id	        |	returns game criteria
