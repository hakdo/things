from flask import Flask
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def hello():
	return "Hello there"

@app.route('/downloads')
def dloads():
	try:
		if os.name == 'posix':
			# List downloads on *nix machines
			out = subprocess.check_output('ls ~/Downloads', shell=True)
		else:
			# List downloads on Windows machines
			out = subprocess.check_output('dir %HOMEDRIVE%%HOMEPATH%\Downlaods', shell=True)
		return out
	except:
		return "Downloads folder not in standard location"
