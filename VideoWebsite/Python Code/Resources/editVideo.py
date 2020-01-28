#!/usr/bin/env python3
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import reqparse, Resource, Api
import pymysql.cursors
import settings
import json
import os

class EditVideo(Resource):
    # Update a video
    # curl -X PUT -H "Content-Type: application/json" -d '{"newTitle": "'$newTitle'", "newFileName": "'$newFileName'"}' -b cookie-jar -k https://info3103.cs.unb.ca:50533/users/<username>/videos/<title>
    def put(self, handle, title):
        if 'username' in session:
            sessionUsername = session['username']
            dbConnection = pymysql.connect(settings.MYSQL_HOST,
                settings.MYSQL_USER,
                settings.MYSQL_PASSWD,
                settings.MYSQL_DB,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)
            sqlProcName = 'getOneUser'
            sqlArgs = (handle,)
            cursor = dbConnection.cursor()
            cursor.callproc(sqlProcName, sqlArgs)
            user = cursor.fetchone()
            if user is None:
                         abort(404)
            userName = user.get("userName")
            if sessionUsername == userName:
                if not request.json:
                    abort(400)
                parser = reqparse.RequestParser()
                try:
                    uid = user.get("userId")
                    sqlProcName = 'getOneVideo'
                    sqlArgs = (title, uid,)
                    cursor.callproc(sqlProcName, sqlArgs)
                    video = cursor.fetchone()
                    if video is None:
                        abort(404)
                    vid = video.get("videoId")
                    parser.add_argument('newTitle', type=str, required=True)
                    request_params = parser.parse_args()
                    newTitle = request_params['newTitle']
                    sqlProcName = 'updateVideo'
                    sqlArgs = (vid, newTitle)
                    cursor.callproc(sqlProcName, sqlArgs)
                    dbConnection.commit()
                except pymysql.MySQLError as e:
                    print(e)
                finally:
                    cursor.close()
                    dbConnection.close()
                return make_response(jsonify({'message': 'updated video'}), 200)
            else:
                return make_response(jsonify({'message': 'incorrect user'}), 400)
        else:
            return make_response(jsonify({'message': 'you\'re not logged in'}), 400)

    # Delete a video
    # curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://info3103.cs.unb.ca:50533/users/<username>/videos/<title>
    def delete(self, handle, title):
        if 'username' in session:
            sessionUsername = session['username']
            dbConnection = pymysql.connect(settings.MYSQL_HOST,
                settings.MYSQL_USER,
                settings.MYSQL_PASSWD,
                settings.MYSQL_DB,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)
            sqlProcName = 'getOneUser'
            sqlArgs = (handle,)
            cursor = dbConnection.cursor()
            cursor.callproc(sqlProcName, sqlArgs)
            user = cursor.fetchone()
            if user is None:
                         abort(404)
            userName = user.get("userName")
            if sessionUsername == userName:
                try:
                    id = user.get("userId")
                    sqlProcName = 'getOneVideo'
                    sqlArgs = (title, id,)
                    cursor.callproc(sqlProcName, sqlArgs)
                    video = cursor.fetchone()
                    if video is None:
                        abort(404)
                    videoId = video.get("videoId")
                    videoFileName = video.get("fileName")
                    sqlProcName = 'deleteVideo'
                    sqlArgs = (id,videoId)
                    cursor.callproc(sqlProcName, sqlArgs)
                    dbConnection.commit()
                    os.unlink('static/Uploads/'+videoFileName)
                except pymysql.MySQLError as e:
                    print(e)
                finally:
                    cursor.close()
                    dbConnection.close()
                return make_response(jsonify({'message': 'deleted video'}), 200)
            else:
                return make_response(jsonify({'message': 'incorrect user'}), 400)
        else:
            return make_response(jsonify({'message': 'you\'re not logged in'}), 400)
