from __future__ import division

import picamera
import numpy as np
import time
from datetime import datetime
import sqlite3
import lightsensor_db

motion_dtype = np.dtype([
	('x', 'i1'),
	('y', 'i1'),
	('sad', 'u2'),
	])

database = "/home/pi/smartmeter/smart_api/lightsensor.db"
	
class MyMotionDetector(object):
	def __init__(self, camera):
		width, height = camera.resolution
		self.cols = (width + 15) // 16
		self.cols += 1 # there's always an extra column
		self.rows = (height + 15) // 16
		self.oldtime = time.time()
		self.newtime = time.time()
		self.timedelta = self.newtime - self.oldtime
			
		
	def write(self, s):
	# Load the motion data from the string to a numpy array
		data = np.fromstring(s, dtype=motion_dtype)
		# Re-shape it and calculate the magnitude of each vector
		data = data.reshape((self.rows, self.cols))
		data = np.sqrt(
			np.square(data['x'].astype(np.float)) +
			np.square(data['y'].astype(np.float))
			).clip(0, 255).astype(np.uint8)
		# If there're more than 10 vectors with a magnitude greater
		# than 60, then say we've detected motion
		if (data > 60).sum() > 10:
			print('Motion detected!')
			self.oldtime = self.newtime
			self.newtime = time.time()
			self.timedelta = self.newtime - self.oldtime
			print(self.newtime)
			# create a database connection
			conn = lightsensor_db.create_connection(database)
			with conn:	
				lightsensor_db.add_pulse(conn, datetime.now())
			time.sleep(0.3)
		# Pretend we wrote all the bytes of s
		return len(s)

	

conn = lightsensor_db.create_connection(database)
if conn is not None:
	# create projects table
	lightsensor_db.create_table(conn, lightsensor_db.sql_create_projects_table)

with picamera.PiCamera() as camera:
	camera.resolution = (160, 120)
	camera.framerate = 80
	camera.start_recording(
		# Throw away the video data, but make sure we're using H.264
		'/dev/null', format='h264',
		# Record motion data to our custom output object
		motion_output=MyMotionDetector(camera)
	)
	while True:
		camera.wait_recording(6)
	camera.stop_recording()
