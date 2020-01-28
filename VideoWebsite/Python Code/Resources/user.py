#!/usr/bin/env python3
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import reqparse, Resource, Api
import pymysql.cursors
import settings
import json

class User(Resource):
    # Get one user:
    # curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://info3103.cs.unb.ca:50533/users/<username>
    def get(self, handle):
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
            except pymysql.MySQLError as e:
                print(e)
            finally:
                cursor.close()
                dbConnection.close()
            return make_response(jsonify({'User': user}), 200)
        else:
            return make_response(jsonify({'Message': "You are not logged in"}), 400)

    # Update a users handle
    # curl -X PUT -H "Content-Type: application/json" -d '{"newHandle": "'$newHandle'"}' -b cookie-jar -k https://info3103.cs.unb.ca:48534/users/<username>
    def put(self,handle):
        if 'username' in session:
            sessionUsername = session['username']
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
                userName = user.get("userName")
            except pymysql.MySQLError as e:
                print(e)
                cursor.close()
                dbConnection.close()
            if sessionUsername == userName:
                if not request.json:
                    abort(400) # bad request
                parser = reqparse.RequestParser()
                try:
                    id = user.get("userId")
                    parser.add_argument('newHandle', type=str, required=True)
                    request_params = parser.parse_args()
                    newHandle = request_params['newHandle']
                    sqlProcName = 'updateUser'
                    sqlArgs = (id, newHandle,)
                    cursor.callproc(sqlProcName, sqlArgs)
                    dbConnection.commit()
                except pymysql.MySQLError as e:
                    print(e)
                finally:
                    cursor.close()
                    dbConnection.close()
                return make_response(jsonify({'message': 'updated user'}), 200)
            else:
                return make_response(jsonify({'message': 'you\'re the incorrect user'}), 400)
        else:
            return make_response(jsonify({'message': 'you\'re not logged in'}), 400)

    # Delete a user
    # curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://info3103.cs.unb.ca:50533/users/<username>
    def delete(self, handle):
        if 'username' in session:
            sessionUsername = session['username']
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
                userName = user.get("userName")
            except pymysql.MySQLError as e:
                print(e)
                cursor.close()
                dbConnection.close()
            if sessionUsername == userName:
                try:
                    id = user.get("userId")
                    sqlProcName = 'deleteUser'
                    sqlArgs = (id,)
                    cursor.callproc(sqlProcName, sqlArgs)
                    dbConnection.commit()
                except pymysql.MySQLError as e:
                    print(e)
                finally:
                    cursor.close()
                    dbConnection.close()
                return make_response(jsonify({'Deleted User': user}), 200)
            else:
                return make_response(jsonify({'message': 'you\'re the incorrect user'}), 400)
        else:
            return make_response(jsonify({'message': 'you\'re not logged in'}), 400)
