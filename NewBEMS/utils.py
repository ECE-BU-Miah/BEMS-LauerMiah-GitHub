#!/usr/bin/python3

import subprocess
import argparse
import sqlite3
import global_settings
import datetime

# Python3 version
def getPyVersion():
	try:
		version = subprocess.check_output(['python3','-V'])
	except subprocess.CalledProcessError as cpe:
		print(cpe)
		return None

	if version:
		strVersion = version.decode('utf-8').strip()
		strVersion = strVersion.replace(" ","")
		strVersion = strVersion.lower()[:-2]
	return strVersion

# Random stuff, don't tell Dr. Miah :)
def getPyLines():
	lineCount = 0
	return lineCount

# Database access
def insertIntoTSTable(deviceId, data):
	conn = sqlite3.connect(global_settings.WEBSERVER_DIR + 'meta.db')
	curs = conn.cursor()
	tstamp = datetime.datetime.now()
	strTStamp = f"{tstamp.month}/{tstamp.day}/{tstamp.year} {tstamp.hour}:{tstamp.minute}:{tstamp.second}"
	dataValCount = 0

	# Check whether a TS table for the device exists

	# Check whether the last time stamp in the 
	curs.execute(f"SELECT * FROM Device{deviceId}TSData;")
	curs.fetchall()

	queryString = f"INSERT INTO Device{deviceId}TSData "

	curs.close()
	conn.close()

def createDeviceTSTable(deviceId):
	conn = sqlite3.connect(global_settings.WEBSERVER_DIR + 'meta.db')
	curs = conn.cursor()
	curs.execute("SELECT queryable FROM ActiveDevices WHERE id=?;",(deviceId,))
	queryableVals = curs.fetchall()

	print(queryableVals)

	if queryableVals == []:
		print("empty")

	# queryableData is a list containing queryable values delimited by a |
	queryableList = queryableData.split('|')
	queryString = f"CREATE TABLE IF NOT EXISTS Device{deviceId}TSData (timestamp text,"

	# Append queryableVals to the end of the query string followed by text to
	# denote each column as a text field.
	for i, queryableVal in enumerate(queryableList):
		if i == (len(queryableList) - 1):
			queryString += ' ' + queryableVal + ' text);'
		else:
			queryString += ' ' + queryableVal + ' text, '

	curs.execute(queryString)
	curs.commit()

	curs.close()
	conn.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("utility", help="select a utility function")
	args = parser.parse_args()
	if args.utility == "version":
		print(getPyVersion())
