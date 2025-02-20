#!/usr/bin/env python3
import sys
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import reqparse, Resource, Api
from flask_session import Session
import json
from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import *
import ssl #include ssl libraries

import settings # Our server and db settings, stored in settings.py

# app = Flask(__name__)
# # Set Server-side session config: Save sessions in the local app directory.
# app.secret_key = settings.SECRET_KEY
# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_COOKIE_NAME'] = 'peanutButter'
# app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST
# Session(app



####################################################################################
#
# Error handlers
#
# @app.errorhandler(400) # decorators to add to 400 response
# def not_found(error):
# 	return make_response(jsonify( { 'status': 'Bad request' } ), 400)
#
# @app.errorhandler(404) # decorators to add to 404 response
# def not_found(error):
# 	return make_response(jsonify( { 'status': 'Resource not found' } ), 404)

####################################################################################
#
# Routing: GET and POST using Flask-Session
#
class SignIn(Resource):
	#
	# Set Session and return Cookie
	#
	# Sign in
	# curl -i -H "Content-Type: application/json" -X POST -d '{"username": "Casper", "password": "crap"}' -b cookie-jar -k https://info3103.cs.unb.ca:48534/signin
	def post(self):
		if not request.json:
			abort(400) # bad request

		# Parse the json
		parser = reqparse.RequestParser()
		try:
 			# Check for required attributes in json document, create a dictionary
			parser.add_argument('username', type=str, required=True)
			parser.add_argument('password', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request

		if request_params['username'] in session:
			settings.LOGGEDIN = True
			response = {'status': 'success'}
			responseCode = 200
		else:
			try:
				ldapServer = Server(host=settings.LDAP_HOST)
				ldapConnection = Connection(ldapServer,
					raise_exceptions=True,
					user='uid='+request_params['username']+', ou=People,ou=fcs,o=unb',
					password = request_params['password'])
				ldapConnection.open()
				ldapConnection.start_tls()
				ldapConnection.bind()
				# At this point we have sucessfully authenticated.
				session['username'] = request_params['username']
				settings.LOGGEDIN = True
				response = {'status': 'success' }
				responseCode = 201
			except LDAPException:
				settings.LOGGEDIN = False
				response = {'status': 'Access denied'}
				responseCode = 403
			finally:
				ldapConnection.unbind()
		return make_response(jsonify(response), responseCode)

	# GET: Check Cookie data with Session data
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://info3103.cs.unb.ca:48534/signin
	def get(self):
		if 'username' in session:
			username = session['username']
			response = {'status': 'success'}
			responseCode = 200
		else:
			response = {'status': 'fail'}
			responseCode = 403

		return make_response(jsonify(response), responseCode)

	# DELETE: Check Cookie data with Session data
	#
	# Sign out
	# curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://info3103.cs.unb.ca:48534/signin
	def delete(self):
		if 'username' in session:
			settings.LOGGEDIN = False
			response = {'status': 'success'}
			responseCode = 200
			session.clear()
			session.pop('username', None)
		else:
			response = {'status': 'fail'}
			responseCode = 403
	#
	#	Here's your chance to shine!
	#


####################################################################################
#
# Identify/create endpoints and endpoint objects
#
# api = Api(app)
# api.add_resource(SignIn, '/signin')


#############################################################################
# xxxxx= last 5 digits of your studentid. If xxxxx > 65535, subtract 30000
# if __name__ == "__main__":
# 	#
# 	# You need to generate your own certificates. To do this:
# 	#	1. cd to the directory of this app
# 	#	2. run the makeCert.sh script and answer the questions.
# 	#	   It will by default generate the files with the same names specified below.
# 	#
# 	context = ('cert.pem', 'key.pem') # Identify the certificates you've generated.
# 	app.run(
# 		host=settings.APP_HOST,
# 		port=settings.APP_PORT,
# 		ssl_context=context,
# 		debug=settings.APP_DEBUG)
