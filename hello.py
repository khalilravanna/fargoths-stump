import os
from flask import Flask, render_template
import urllib2
from BeautifulSoup import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def hello():
	import urllib2
	from BeautifulSoup import BeautifulSoup

	soup = BeautifulSoup(urllib2.urlopen('http://uesp.net/wiki/Special:Random'))
	try: 
		image = soup.find(attrs={"class": "image"}).img['src']
	except:
		image = 'img/fourohfargoth.png'


	return render_template('scroll.html', image=image)