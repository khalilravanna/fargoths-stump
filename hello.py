import os
from flask import Flask
import urllib2
from BeautifulSoup import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def hello():
	soup = BeautifulSoup(urllib2.urlopen('http://uesp.net/wiki/Special:Random'))
	return soup.img['src']