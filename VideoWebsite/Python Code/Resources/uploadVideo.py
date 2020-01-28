#!/usr/bin/env python3
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import reqparse, Resource, Api
import werkzeug
import pymysql.cursors
import settings
import json

UPLOAD_PATH = settings.FILESTORAGE_PATH

class UploadVideo(Resource):
    # Add a video
    # curl -i -H "Content-Type: application/json" -X POST -d '{"title": "'$title'", "filename": "'$filename'"}' -b cookie-jar -k https://info3103.cs.unb.ca:50533/users/<username>/videos
    def post(self, handle):
        if 'username' in session:
            sessionUsername = session['username']
            dbConnection = pymysql.connect(settings.MYSQL_HOST,
                settings.MYSQL_USER,
                settings.MYSQL_PASSWD,
                settings.MYSQL_DB,
                charset='utf8mb4',
                cursorclass= pymysql.cursors.DictCursor)
            sqlProcName = 'getOneUser'
            sqlArgs = (handle,)
            cursor = dbConnection.cursor()
            cursor.callproc(sqlProcName, sqlArgs)
            user = cursor.fetchone()
            if user is None:
                abort(404)
            userName = user.get("userName")
            if sessionUsername == userName:
                parser = reqparse.RequestParser()
                try:
                    id = user.get("userId")
                    # Pass in the file
                    parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
                    request_params = parser.parse_args()
                    filename = userName + '_' + request_params['file'].filename
                    request_params['file'].save(UPLOAD_PATH + filename)
                    sqlProcName = 'uploadAVideo'
                    sqlArgs = (filename, id,)
                    cursor.callproc(sqlProcName, sqlArgs)
                    dbConnection.commit()
                except pymysql.MySQLError as e:
                    print(e)
                finally:
                    cursor.close()
                    dbConnection.close()
                return make_response(jsonify({'Message': "added video"}), 200)
            else:
                return make_response(jsonify({'message': "Incorrect user"}), 400)
        else:
            return make_response(jsonify({'message': "You must be logged in"}), 400)
