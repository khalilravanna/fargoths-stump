import os
from flask import Flask, render_template
import urllib2
from BeautifulSoup import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def hello():
	soup = BeautifulSoup(urllib2.urlopen('http://uesp.net/wiki/Special:Random'))
	image = soup.img['src']
	return render_template('scroll.html', image=image)