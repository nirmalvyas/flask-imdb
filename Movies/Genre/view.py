from flask import Blueprint,g,request
import requests
from migrate import Genre,MovieGenre,Movie
from appholder import *
import json
import hashlib
import datetime
from URL_CONSTANTS import API_ROOT
from sqlalchemy import func


genre_blueprint= Blueprint('genre', __name__)



@genre_blueprint.route('/genre',methods=['GET', 'POST','PUT','DELETE'])
def genre():
    # call the service for the authenitcation
    session_id = request.values.get('session_id')
    if not session_id:
        return  json.dumps({'error':'PLS_PROVIDE_SESSION_FOR_AUTHICATION',
                    'status':0})

    resp = requests.get(API_ROOT + '/user/authenticate?session_id='+session_id)
    if resp.status_code == 200:
        resp = resp.json()
        if not resp or not isinstance(resp,dict) or ('error' in resp or resp.get('status')==0):
            return  json.dumps({'error':'AUTHENTICATION_FAILED',
                    'status':0})
        if 'data' in resp and resp.get('status')==1 and isinstance(resp['data'],list) and len(resp['data']):
            check_role = resp.get('data')[0]
            if isinstance(check_role,dict):
                if not check_role.get('role_name').lower() == 'admin':
                    return  json.dumps({'error':'NOT_AUTHORISED_CONTACT_ADMIN',
                    'status':0})
            else:
                return  json.dumps({'error':'AUTHENTICATION_FAILED',
                    'status':0})
        else:
                return  json.dumps({'error':'AUTHENTICATION_FAILED',
                    'status':0})
    else:
        return  json.dumps({'error':'AUTHENTICATION_FAILED_INTERNAL_ERROR_OCUURED',
            'status':0})


    if request.method == 'POST': 
        try:

            genre_name = request.values.get('genre_name')
            if not genre_name:
                return json.dumps({'error':'PLS_PROVIDE_GENRE_NAME',
                    'status':0})

            
            q = Genre(genre_name=genre_name,status='A'
            			)
            db.session.add(q)
            db.session.commit()
            return json.dumps({'status':1,'message':'Genre Inserted Successfully!'})
        except Exception as e:
            print "==Something went wrong==",str(e)
            return json.dumps({'error':'CANNOT_CREATE_GENRE_CHECK_LOG','status':0})

    elif request.method == 'GET':
    	try:
    		q = db.session.query(Genre.genre_name,Genre.status)
    		q = q.filter(Genre.status == 'A')
    		result_set = [u._asdict() for u in q.all()]
    		return json.dumps({'status':1,'data':result_set})
    	except Exception as e:
    		print"==Something went wrong in getting all detials for Genre==",str(e)
    		return json.dumps({'status':0,'error':'CANNOT_FETCH_DATA_FOR_GENRE'})

    elif request.method == 'PUT':
    	try:
    		# to update we need genre id
    		genre_name = request.values.get('genre_name')
    		genre_id = request.values.get('genre_id')
    		if (not genre_id or genre_id == 'NA' or genre_id is None) or (not genre_id or genre_name == 'NA' or genre_name is None):
    			return json.dumps({'error':'PLS_PROVIDE_GENRE_ID_AND_GENRE_NAME_THAT_NEED_TO_BE_EDITED',
    				'status':0})
    		try:
    			#ensure that genre is integer
    			if not isinstance(eval(genre_id),int):
    				return json.dumps({'error':'PLS_PROVIDE_GENRE_ID_IN_PROPER_FORMAT','status':0})	
    		except Exception as e:
    			print"genre_id not in proper format==",str(e)
    			return json.dumps({'error':'PLS_PROVIDE_GENRE_ID_IN_PROPER_FORMAT','status':0})
    		genre_id = int(genre_id)
    		q = db.session.query(Genre)
    		q.filter(Genre.id == genre_id).update({
    				'genre_name':genre_name,
    				'update_dttm': datetime.datetime.now()

  	  			})
    		db.session.commit()	

    		return json.dumps({'status':1,'message':'Genre Updated Successfully!'})
    	except Exception as e:
    		print"==Something went wrong in getting all detials for genre==",str(e)
    		return json.dumps({'status':0,'error':'CANNOT_UPDATING_DATA_FOR_GENRE'})


    elif request.method == 'DELETE':
    	try:
    		# to DELETE we need genre_id
    		# we will do soft delete
    		genre_id = request.values.get('genre_id')
    		if (not genre_id or genre_id == 'NA' or genre_id is None) :
    			return json.dumps({'error':'PLS_PROVIDE_GENRE_ID_THAT_NEED_TO_BE_DELETED',
    				'status':0})
    		try:
    			#ensure that genre_id is integer
    			if not isinstance(eval(genre_id),int):
    				return json.dumps({'error':'PLS_PROVIDE_GENRE_ID_IN_PROPER_FORMAT','status':0})	
    		except Exception as e:
    			print"genre_id not in proper format==",str(e)
    			return json.dumps({'error':'PLS_PROVIDE_GENRE_ID_IN_PROPER_FORMAT','status':0})
    		genre_id = int(genre_id)
    		q = db.session.query(Genre)
    		q.filter(Genre.id == genre_id).update({
    				'status':'D',
    				'update_dttm': datetime.datetime.now()

  	  			})
    		db.session.commit()	

    		return json.dumps({'status':1,'message':'Genre Deleted Successfully!'})
    	except Exception as e:
    		print"==Something went wrong in getting all detials for genre==",str(e)
    		return json.dumps({'status':0,'error':'CANNOT_DELETING_DATA_FOR_GENRE'})
    else:
        return json.dumps({'error':'UNAUTHORISED_METHOD_FOR_ACCESS','status':0})



@genre_blueprint.route('/genre_movie',methods=['GET', 'POST','PUT','DELETE'])
def genre_movie():
    session_id = request.values.get('session_id')
    if not session_id:
        return  json.dumps({'error':'PLS_PROVIDE_SESSION_FOR_AUTHICATION',
                    'status':0})
    resp = requests.get(API_ROOT + '/user/authenticate?session_id='+session_id)
    if resp.status_code == 200:
        resp = resp.json()
        if not resp or not isinstance(resp,dict) or ('error' in resp or resp.get('status')==0):
            return  json.dumps({'error':'AUTHENTICATION_FAILED',
                    'status':0})
        if 'data' in resp and resp.get('status')==1 and isinstance(resp['data'],list) and len(resp['data']):
            check_role = resp.get('data')[0]
            if isinstance(check_role,dict):
                if not check_role.get('role_name').lower() == 'admin':
                    return  json.dumps({'error':'NOT_AUTHORISED_CONTACT_ADMIN',
                    'status':0})
            else:
                return  json.dumps({'error':'AUTHENTICATION_FAILED',
                    'status':0})
        else:
                return  json.dumps({'error':'AUTHENTICATION_FAILED',
                    'status':0})
    else:
        return  json.dumps({'error':'AUTHENTICATION_FAILED_INTERNAL_ERROR_OCUURED',
            'status':0})

    if request.method == 'POST': 
        try:

            movie_id = request.values.get('movie_id')
            genre_id = request.values.get('genre_id')
            if not genre_id or not movie_id:
                return json.dumps({'error':'PLS_PROVIDE_GENRE_NAME_MOVIE_NAME',
                    'status':0})

            
            q = MovieGenre(genre_id=genre_id,movie_id=movie_id,status='A'
                        )
            db.session.add(q)
            db.session.commit()
            return json.dumps({'status':1,'message':'Genre for movie Inserted Successfully!'})
        except Exception as e:
            print "==Something went wrong==",str(e)
            return json.dumps({'error':'CANNOT_CREATE_GENRE_CHECK_LOG','status':0})

    elif request.method == 'GET':
        try:
            q = db.session.query(MovieGenre.genre_id,MovieGenre.movie_id,Movie.movie_name,
                Genre.genre_name
                )
            q = q.join(Movie,MovieGenre.movie_id == Movie.id)
            q = q.join(Genre,MovieGenre.genre_id == Genre.id)
            q = q.filter(Genre.status == 'A')
            result_set = [u._asdict() for u in q.all()]
            return json.dumps({'status':1,'data':result_set})
        except Exception as e:
            print"==Something went wrong in getting all detials for Genre Movie==",str(e)
            return json.dumps({'status':0,'error':'CANNOT_FETCH_DATA_FOR_GENRE'})

    elif request.method == 'PUT':
        try:
            # to update we need genre id
            movie_id = request.values.get('movie_id')
            genre_id = request.values.get('genre_id')
            moviegenre_id = request.values.get('moviegenre_id')
            if (not moviegenre_id or moviegenre_id == 'NA' or moviegenre_id is None) or (not genre_id or genre_id == 'NA' or genre_id is None) or (not movie_id or movie_id == 'NA' or movie_id is None):
                return json.dumps({'error':'PLS_PROVIDE_GENRE_ID_AND_GENRE_NAME_MOVIE_NAME_THAT_NEED_TO_BE_EDITED',
                    'status':0})
            try:
                #ensure that genre is integer
                if not isinstance(eval(moviegenre_id),int):
                    return json.dumps({'error':'PLS_PROVIDE_GENRE_ID_IN_PROPER_FORMAT','status':0}) 
            except Exception as e:
                print"genre_id not in proper format==",str(e)
                return json.dumps({'error':'PLS_PROVIDE_GENRE_ID_IN_PROPER_FORMAT','status':0})
            moviegenre_id = int(moviegenre_id)
            q = db.session.query(MovieGenre)
            q.filter(MovieGenre.id == moviegenre_id).update({
                    'genre_id':genre_id,
                    'movie_id':movie_id,
                    'update_dttm': datetime.datetime.now()

                })
            db.session.commit() 

            return json.dumps({'status':1,'message':'Genre and Movie Updated Successfully!'})
        except Exception as e:
            print"==Something went wrong in getting all detials for genre==",str(e)
            return json.dumps({'status':0,'error':'CANNOT_UPDATING_DATA_FOR_GENRE_MOVIE'})


    elif request.method == 'DELETE':
        try:
            # to DELETE we need moviegenre_id
            # we will do soft delete
            moviegenre_id = request.values.get('moviegenre_id')
            if (not moviegenre_id or moviegenre_id == 'NA' or moviegenre_id is None) :
                return json.dumps({'error':'PLS_PROVIDE_GENRE_ID_THAT_NEED_TO_BE_DELETED',
                    'status':0})
            try:
                #ensure that moviegenre_id is integer
                if not isinstance(eval(moviegenre_id),int):
                    return json.dumps({'error':'PLS_PROVIDE_MOVIE_GENRE_ID_IN_PROPER_FORMAT','status':0}) 
            except Exception as e:
                print"moviegenre_id not in proper format==",str(e)
                return json.dumps({'error':'PLS_PROVIDE_MOVIE_GENRE_ID_IN_PROPER_FORMAT','status':0})
            moviegenre_id = int(moviegenre_id)
            q = db.session.query(MovieGenre)
            q.filter(MovieGenre.id == moviegenre_id).update({
                    'status':'D',
                    'update_dttm': datetime.datetime.now()

                })
            db.session.commit() 

            return json.dumps({'status':1,'message':'Genre Movie Deleted Successfully!'})
        except Exception as e:
            print"==Something went wrong in getting all detials for genre==",str(e)
            return json.dumps({'status':0,'error':'CANNOT_DELETING_DATA_FOR_GENRE_MOVIE'})
    else:
        return json.dumps({'error':'UNAUTHORISED_METHOD_FOR_ACCESS','status':0})