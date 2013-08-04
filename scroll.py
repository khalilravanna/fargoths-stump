import os
from flask import Flask, render_template, url_for, request
import urllib2, json
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

@app.route('/', methods=['GET'])
def home():
	return render_template('scroll-angular.html')

@app.route('/old', methods=['GET'])
def oldStump():
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

@app.route('/npc', methods=['GET'])
def npc():
	import json, random, time
	from bs4 import BeautifulSoup

	start = time.time();

	# hardcode urls for npc pages
	npc_urls = ['http://www.uesp.net/wiki/Category:Morrowind-NPC_Images', 
		'http://www.uesp.net/w/index.php?title=Category:Morrowind-NPC_Images&filefrom=Chirranirr%0AMW-npc-Chirranirr.jpg#mw-category-media',
		'http://www.uesp.net/w/index.php?title=Category:Morrowind-NPC_Images&filefrom=Felayn+Andral%0AMW-npc-Felayn+Andral.jpg#mw-category-media',
		'http://www.uesp.net/w/index.php?title=Category:Morrowind-NPC_Images&filefrom=Janand+Maulinie%0AMW-npc-Janand+Maulinie.jpg#mw-category-media',
		'http://www.uesp.net/w/index.php?title=Category:Morrowind-NPC_Images&filefrom=Nelso+Salenim%0AMW-npc-Nelso+Salenim.jpg#mw-category-media',
		'http://www.uesp.net/w/index.php?title=Category:Morrowind-NPC_Images&filefrom=Skeetul%0AMW-npc-Skeetul.jpg#mw-category-media',
		'http://www.uesp.net/w/index.php?title=Category:Morrowind-NPC_Images&filefrom=Yambagorn+gor-Shulor%0AMW-npc-Yambagorn+gor-Shulor.jpg#mw-category-media']

	random_page = random.randint(0, len(npc_urls)-1)
	soup = BeautifulSoup(urllib2.urlopen(npc_urls[random_page]))
	items = soup.find_all('li', 'gallerybox')

	print 'Opened index page in %s seconds' % (time.time()-start)

	num = random.randint(0, len(items)-1)

	link = items[num].find('a').get('href')
	link = 'http://www.uesp.net' + link

	soup = BeautifulSoup(urllib2.urlopen(link))
	image = soup.find('div', 'fullImageLink').find('a').get('href')

	print 'Opened image page in %s seconds' % (time.time()-start)

	page = soup.find(id='mw-imagepage-linkstoimage-ns110').find('a').get('href') # ns110 seems to be the code for the actual page
	page = 'http://www.uesp.net' + page
	
	soup = BeautifulSoup(urllib2.urlopen(page))
	paragraphs = soup.find('div', 'mw-content-ltr').find_all('p') 

	print 'Opened npc page in %s seconds' % (time.time()-start)

	try:
		title = paragraphs[6].find('b').text
	except:
		title = ''
	content = ''
	# for some reason the 7th paragrph is the start of the ones about the character
	for num in range(6, len(paragraphs)):
		content = content + str(paragraphs[num])
	#print content

	print 'Total time: %s seconds' % (time.time()-start)

	#return render_template('scroll-angular.html', image=image, content=content, title=title)
	return (json.dumps({'title': title, 'image': image, 'content': content}), 200, {'Access-Control-Allow-Origin': '*'})

#app.run(debug=True)