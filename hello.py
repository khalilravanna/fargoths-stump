import os
from flask import Flask, render_template, url_for, request
import urllib2, json
from BeautifulSoup import BeautifulSoup

app = Flask(__name__)

with app.test_request_context():
	url_for('static', filename='fourohfargoth.png')

@app.route('/', methods=['GET'])
def hello():
	import datetime, time

	if request.method == 'GET':

		now = datetime.datetime.now()
		now_readable = "%d/%d/%d %d:%d" % (now.month, now.day, now.year, now.hour, now.minute)

		soup = BeautifulSoup(urllib2.urlopen('http://uesp.net/wiki/Special:Random'))
		try: 
			image = soup.find(attrs={"class": "image"}).img['src']
		except:
			image = 'static/fourohfargoth.png'

		if request.args.get('json'):
			return json.dumps({'image': image, 'request_time': now_readable})
		else:
			return (render_template('scroll.html', image=image), 200, {'Access-Control-Allow-Origin': '*'})

#app.run()