#!/usr/bin/python3

import subprocess
import argparse

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

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("utility", help="select a utility function")
	args = parser.parse_args()
	if args.utility == "version":
		print(getPyVersion())
