#!/usr/bin/env python3
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import reqparse, Resource, Api
import pymysql.cursors
import settings
import json

class Users(Resource):
	# Get all the users:
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://info3103.cs.unb.ca:50533/users
	def get(self):
		if 'username' in session:
			print(session)
			username = session['username']
			print("USERNAME")
			print(username)
			try:
				dbConnection = pymysql.connect(settings.MYSQL_HOST,
					settings.MYSQL_USER,
					settings.MYSQL_PASSWD,
					settings.MYSQL_DB,
					charset='utf8mb4',
					cursorclass= pymysql.cursors.DictCursor)
				sqlProcName = 'getAllUsers'
				cursor = dbConnection.cursor()
				cursor.callproc(sqlProcName)
				users = cursor.fetchall()
			except pymysql.MySQLError as e:
				print(e)
			finally:
				cursor.close()
				dbConnection.close()
			return make_response(jsonify({'Users': users}), 200)
		else:
			print(session)
			return make_response(jsonify({'message': "Must be logged in to view all users"}), 400)

	# Add a user
	# curl -i -H "Content-Type: application/json" -X POST -d '{"username": "'$username'", "handle": "'$handle'"}' -b cookie-jar -k https://info3103.cs.unb.ca:50533/users
	def post(self):
		if not request.json:
			abort(400) # bad request
		parser = reqparse.RequestParser()
		try:
			parser.add_argument('username', type=str, required=True, help="userName cannot be blank")
			parser.add_argument('handle', type=str, required=True, help="Handle cannot be blank")
			request_params = parser.parse_args()
			userName = request_params['username']
			handle = request_params['handle']
			dbConnection = pymysql.connect(settings.MYSQL_HOST,
				settings.MYSQL_USER,
				settings.MYSQL_PASSWD,
				settings.MYSQL_DB,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sqlProcName = 'createNewUser'
			sqlArgs = (userName, handle,)
			cursor = dbConnection.cursor()
			cursor.callproc(sqlProcName, sqlArgs)
			dbConnection.commit()
		except pymysql.MySQLError as e:
			print(e)
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify({'Message': "added user"}), 200)

	# def delete(self):
