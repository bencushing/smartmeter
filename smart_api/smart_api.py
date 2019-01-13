#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps
import lightsensor_db
from datetime import datetime
import json

app = Flask(__name__)
api = Api(app)

database = "lightsensor.db"
oldtime = datetime.min		
newtime = datetime.min


def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()

class PulseRate(Resource):		
	def get(self):
		conn = lightsensor_db.create_connection(database)
		pulses = lightsensor_db.get_last_pulses(conn, 2)
		delta = pulses[0][0] - pulses[1][0] 
		json_delta = json.dumps({"s": delta.seconds, "ms": delta.microseconds})
		print(delta)
		print(json_delta)
		return json_delta

api.add_resource(PulseRate, '/pulserate')



if __name__ == '__main__':
	app.run()
