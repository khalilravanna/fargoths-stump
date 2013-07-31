import os
from flask import Flask, render_template, url_for, request
import urllib2, json
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
	import datetime, time

	if request.method == 'GET':

		now = datetime.datetime.now()
		now_readable = "%d/%d/%d %d:%d" % (now.month, now.day, now.year, now.hour, now.minute)

		soup = BeautifulSoup(urllib2.urlopen('http://uesp.net/wiki/Special:Random'))
		try: 
			image = soup.find(attrs={"class": "image"}).img['src']
			success = True
		except:
			image = "static/images/fourohfargoth.png"
			success = False

		content = soup.find('p')

		if request.args.get('json'):
			if not success:
				image = "http://fargoths-stump.herokuapp.com/" + image
			return (json.dumps({'image': image, 'request_time': now_readable}), 200, {'Access-Control-Allow-Origin': '*'})
		else:
			return (render_template('scroll.html', image=image), 200, {'Access-Control-Allow-Origin': '*'})

@app.route('/foundation', methods=['GET'])
def foundation():
	if request.method == 'GET':
		soup = BeautifulSoup(urllib2.urlopen('http://uesp.net/wiki/Special:Random'))
		try: 
			image = soup.find(attrs={"class": "image"}).img['src']
			success = True
		except:
			image = "static/images/fourohfargoth.png"
			success = False

		content = soup.find('p')

		print content

		return render_template('scroll-foundation.html', image=image, content=content)

#app.run()