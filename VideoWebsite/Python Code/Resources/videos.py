#!/usr/bin/env python3
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import Resource, Api
import pymysql.cursors
import settings
import json
import glob
import os

class Videos(Resource):
	# Get all the Videos:
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://info3103.cs.unb.ca:50533/videos
	def get(self):
		# if 'username' in session:
			try:
				# print(glob.glob("/"))
				dbConnection = pymysql.connect(settings.MYSQL_HOST,
					settings.MYSQL_USER,
					settings.MYSQL_PASSWD,
					settings.MYSQL_DB,
					charset='utf8mb4',
					cursorclass= pymysql.cursors.DictCursor)
				sqlProcName = 'getAllVideos'
				cursor = dbConnection.cursor()
				cursor.callproc(sqlProcName)
				videos = cursor.fetchall()
				files = os.listdir("static/Uploads")
				newFiles = []
				for file in files:
					file = "static/Uploads/"+file
					newFiles.append(file)
					print(file)
			except pymysql.MySQLError as e:
				print(e)
			finally:
				cursor.close()
				dbConnection.close()
			return make_response(jsonify({'Videos': videos, 'Files': newFiles}), 200)
		# else:
		# 	return make_response(jsonify({'message': "You must be logged in"}), 400)

	# def delete(self):
