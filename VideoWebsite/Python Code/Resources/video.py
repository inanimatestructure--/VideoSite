#!/usr/bin/env python3
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import reqparse, Resource, Api
import pymysql.cursors
import settings
import json

class Video(Resource):
    # Get one video from a user:
    # curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://info3103.cs.unb.ca:50533/users/<username>/videos/<title>
    def get(self, handle, title):
        if 'username' in session:
            try:
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
                uid = user.get("userId")
                sqlProcName = 'getOneVideo'
                sqlArgs = (title, uid,)
                cursor.callproc(sqlProcName, sqlArgs)
                video = cursor.fetchone()
                if video is None:
    			             abort(404)
            except pymysql.MySQLError as e:
                print(e)
            finally:
                cursor.close()
                dbConnection.close()
            return make_response(jsonify({'Video': video}), 200)
        else:
            return make_response(jsonify({'message': 'You must be signed in'}), 400)
