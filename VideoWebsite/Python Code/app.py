#!/usr/bin/env python3
import sys
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import reqparse, Resource, Api
from flask_session import Session
import json
from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import *
from flask_cors import CORS
import ssl #include ssl libraries

import settings
import cgitb
import cgi
cgitb.enable()

app = Flask(__name__, static_folder="static", static_url_path="/static")
# Set Server-side session config: Save sessions in the local app directory.
app.secret_key = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'peanutButter'
app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST
CORS(app)

from Resources.users import Users
from Resources.user import User
from Resources.videos import Videos
from Resources.usersVideos import UsersVideos
from Resources.uploadVideo import UploadVideo
from Resources.editVideo import EditVideo
from Resources.video import Video
from signinApp import SignIn

#
# Error handlers
#
@app.errorhandler(400) # decorators to add to 400 response
def not_found(error):
	return make_response(jsonify( { "status": "Bad request" } ), 400)

@app.errorhandler(404) # decorators to add to 404 response
def not_found(error):
	return make_response(jsonify( { "status": "Resource not found" } ), 404)

# @app.route("/")
# def root():
#       return app.send_static_file('index.html')
class Root(Resource):
    def get(self):
      return app.send_static_file('index.html')

api = Api(app)
api.add_resource(Root, '/')
api.add_resource(SignIn, '/signin')
api.add_resource(Users, '/users') # get post maybe delete?
api.add_resource(User, '/users/<string:handle>') # get update delete

api.add_resource(UsersVideos, '/users/<string:handle>/videos') # get

api.add_resource(UploadVideo, '/users/<string:handle>/videos/upload') # post
api.add_resource(EditVideo, '/users/<string:handle>/videos/<string:title>/edit') # update delete

api.add_resource(Video, '/users/<string:handle>/videos/<string:title>') # get

api.add_resource(Videos, '/videos') # get

if __name__ == "__main__":

   	context = ('cert.pem', 'key.pem') # Identify the certificates you've generated.
   	app.run(
   		host=settings.APP_HOST,
   		port=settings.APP_PORT,
   		ssl_context=context,
   		debug=settings.APP_DEBUG)
