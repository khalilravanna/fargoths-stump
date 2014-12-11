import os
from flask import Flask, render_template, url_for, request
from urlparse import urlparse
import urllib2, json
from bs4 import BeautifulSoup
from pymongo import Connection

app = Flask(__name__)

debug = True
mock_data = False

MONGO_URL = os.environ.get('MONGOHQ_URL')

if MONGO_URL:
  # Get a connection
  connection = Connection(MONGO_URL)
  # Get the database
  db = connection[urlparse(MONGO_URL).path[1:]]
else:
  # Not on an app with the MongoHQ add-on, do some localhost action
  connection = Connection('localhost', 27017)
  db = connection['MyDB']

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

def increment_page_views():
	myObj = db.analytics.find_one({'event':'page_views'})
	if not myObj:
  		myObj = {'event':'page_views', 'count':1}
	else:
		myObj['count'] += 1
	db.analytics.save(myObj)

@app.route('/', methods=['GET'])
def home():
	increment_page_views()
	return render_template('scroll-angular.html')

def get_full_image(link, lores=False):
	parts = link.split('/')
	parts.pop(3)
	parts.pop(6)

	if not lores:
		# http://images.uesp.net/4/40/MW-npc-Zennammu.jpg/
		return parts[0] + '//' + parts[2] + '/' + parts[3] + '/' + parts[4] + '/' + parts[5]
	# http://images.uesp.net/thumb/4/40/MW-npc-Zennammu.jpg/
	new_link = parts[0] + '//' + parts[2] + '/thumb/' + parts[3] + '/' + parts[4] + '/' + parts[5]
	# http://images.uesp.net/thumb/4/40/MW-npc-Zennammu.jpg/<size>-MW-npc-Zennammu.jpg/
	new_link = new_link + '/600px-' + parts[5]
	print parts
	return new_link

def check_scroll(image):
	myScroll = db.scrolls.find_one({'image':image})
	if myScroll:
		return myScroll
	return False

def save_scroll(scroll):
	myScroll = db.scrolls.find_one({'image':scroll['image']})
	if not myScroll:
  		myScroll = scroll
  		myScroll['count'] = 1
	else:
		myScroll['count'] += 1
	db.scrolls.save(myScroll)

# hardcode urls for npc pages
npc_urls = ['http://www.uesp.net/wiki/Category:Morrowind-NPC_Images',
	'http://www.uesp.net/w/index.php?title=Category:Morrowind-NPC_Images&filefrom=Chirranirr%0AMW-npc-Chirranirr.jpg#mw-category-media',
	'http://www.uesp.net/w/index.php?title=Category:Morrowind-NPC_Images&filefrom=Felayn+Andral%0AMW-npc-Felayn+Andral.jpg#mw-category-media',
	'http://www.uesp.net/w/index.php?title=Category:Morrowind-NPC_Images&filefrom=Janand+Maulinie%0AMW-npc-Janand+Maulinie.jpg#mw-category-media',
	'http://www.uesp.net/w/index.php?title=Category:Morrowind-NPC_Images&filefrom=Nelso+Salenim%0AMW-npc-Nelso+Salenim.jpg#mw-category-media',
	'http://www.uesp.net/w/index.php?title=Category:Morrowind-NPC_Images&filefrom=Skeetul%0AMW-npc-Skeetul.jpg#mw-category-media',
	'http://www.uesp.net/w/index.php?title=Category:Morrowind-NPC_Images&filefrom=Yambagorn+gor-Shulor%0AMW-npc-Yambagorn+gor-Shulor.jpg#mw-category-media']

@app.route('/npc', methods=['GET'])
def npc():
	import json, random, time
	from bs4 import BeautifulSoup

	if mock_data:
		return json.dumps({"content": "<p><b>Skink-in-Tree's-Shade</b>, an <a href=\"http://www.uesp.net/wiki/Morrowind:Argonian\" title=\"Morrowind:Argonian\">Argonian</a> <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Sorcerer\" title=\"Morrowind:Sorcerer\">sorcerer</a>, resides in the <a href=\"http://www.uesp.net/wiki/Morrowind:Mage%27s_Guild_(Wolverine_Hall)\" title=\"Morrowind:Mage's Guild (Wolverine Hall)\">Mage's Guild</a> at Wolverine Hall near <a href=\"http://www.uesp.net/wiki/Morrowind:Sadrith_Mora\" title=\"Morrowind:Sadrith Mora\">Sadrith Mora</a>. He is the primary quest giver there and can allow you to join the guild.</p><p>He wears a <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Common_Shirt\" title=\"Morrowind:Common Shirt\">common shirt</a> with matching <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Common_Pants\" title=\"Morrowind:Common Pants\">pants</a>, and he wields a <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Glass_Dagger\" title=\"Morrowind:Glass Dagger\">glass dagger</a>. Like all Argonians, he is <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Resist_Poison\" title=\"Morrowind:Resist Poison\">immune to poison</a>, has a <a href=\"http://www.uesp.net/wiki/Morrowind:Resist_Common_Disease\" title=\"Morrowind:Resist Common Disease\">resistance to disease</a>, and can <a href=\"http://www.uesp.net/wiki/Morrowind:Water_Breathing\" title=\"Morrowind:Water Breathing\">breathe underwater</a>. Aside from that, he knows: <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Burden_of_Sin\" title=\"Morrowind:Spells/Burden of Sin\">Burden of Sin</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Crushing_Burden\" title=\"Morrowind:Spells/Crushing Burden\">Crushing Burden</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Crushing_Burden_of_Sin\" title=\"Morrowind:Spells/Crushing Burden of Sin\">Crushing Burden of Sin</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Cruel_Weary\" title=\"Morrowind:Spells/Cruel Weary\">Cruel Weary</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Great_Feather\" title=\"Morrowind:Spells/Great Feather\">Great Feather</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Summon_Greater_Bonewalker\" title=\"Morrowind:Spells/Summon Greater Bonewalker\">Summon Greater Bonewalker</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Summon_Scamp\" title=\"Morrowind:Spells/Summon Scamp\">Summon Scamp</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Wizard_Rend\" title=\"Morrowind:Spells/Wizard Rend\">Wizard Rend</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Commanding_Touch\" title=\"Morrowind:Spells/Commanding Touch\">Commanding Touch</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Reflect\" title=\"Morrowind:Spells/Reflect\">Reflect</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Weak_Spelldrinker\" title=\"Morrowind:Spells/Weak Spelldrinker\">Weak Spelldrinker</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Wild_Spelldrinker\" title=\"Morrowind:Spells/Wild Spelldrinker\">Wild Spelldrinker</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Slowfall\" title=\"Morrowind:Spells/Slowfall\">Slowfall</a>, and <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Summon_Skeletal_Minion\" title=\"Morrowind:Spells/Summon Skeletal Minion\">Summon Skeletal Minion</a>.</p><p>This humble Argonian holds his difficult Mages Guild branch with grace and diplomacy. Of all Guild leaders he also seems the most concerned about Vvardenfell's contemporary events. Dark afflictions such as vampirism and ash creatures appear as his chosen field of academic study. Despite being a Mages Guild member, he is somewhat respected by <a href=\"http://www.uesp.net/wiki/Morrowind:House_Telvanni\" title=\"Morrowind:House Telvanni\">House Telvanni</a>, having been noted by them as being <i>\"almost as sage and learned as Telvanni aspirants five times his age\"</i>. He is also rumored to carry his anti-<a href=\"http://www.uesp.net/wiki/Morrowind:Slavery\" title=\"Morrowind:Slavery\">slavery</a> politics a little too far, much farther than Imperial law would normally allow.</p><p>Skink-in-Tree's-Shade is the <a href=\"http://www.uesp.net/wiki/Morrowind:Master_Trainers\" title=\"Morrowind:Master Trainers\">Master Trainer</a> for <a href=\"http://www.uesp.net/wiki/Morrowind:Speechcraft\" title=\"Morrowind:Speechcraft\">Speechcraft</a> and also provides medium <a href=\"http://www.uesp.net/wiki/Morrowind:Trainers\" title=\"Morrowind:Trainers\">training</a> in <a href=\"http://www.uesp.net/wiki/Morrowind:Mysticism\" title=\"Morrowind:Mysticism\">Mysticism</a> and <a href=\"http://www.uesp.net/wiki/Morrowind:Enchant\" title=\"Morrowind:Enchant\">Enchant</a>, and is the second-highest enchant after the hostile master trainer, <a href=\"http://www.uesp.net/wiki/Morrowind:Qorwynn\" title=\"Morrowind:Qorwynn\">Qorwynn</a>. However, you must be at least a <a href=\"http://www.uesp.net/wiki/Morrowind:Mages_Guild#Mages_Guild_Ranks\" title=\"Morrowind:Mages Guild\">Magician</a> in the Mages Guild to receive Skink's services.</p>", "image": "http://images.uesp.net/thumb/1/13/MW-npc-Skink-in-Tree%27s-Shade.jpg/600px-MW-npc-Skink-in-Tree%27s-Shade.jpg", "title": "Skink-in-Tree's-Shade"})
	start = time.time();

	# Assign variables based on the query params
	lores = request.args.get('lores')
	image_only = request.args.get('image_only')
	debug = request.args.get('debug')


	# Pick a random page, and grab the images container from it
	random_page = random.randint(0, len(npc_urls)-1)
	soup = BeautifulSoup(urllib2.urlopen(npc_urls[random_page]))
	items = soup.find_all('li', 'gallerybox')

	if debug:
		print 'Opened index page in %s seconds' % (time.time()-start)

	# Pick a random image from the container
	num = random.randint(0, len(items)-1)
	# And get the link and image
	thumb_link = items[num].find('img').get('src')
	image = get_full_image(thumb_link, True if lores else False)

	# If they just want the image then return here
	if image_only:
		return (json.dumps({'image': image}), 200, {'Access-Control-Allow-Origin': '*'})

	# Get and construct the link for the full page
	link = items[num].find('a').get('href')
	link = 'http://www.uesp.net' + link

	# Open the image page link
	soup = BeautifulSoup(urllib2.urlopen(link))

	# Check if we've already got a cached copy for this npc and return it if so
	cached = check_scroll(image)
	if cached:
		cached['cached'] = True
		return (json.dumps({'title': cached['title'], 'image': cached['image'], 'content': cached['content'], 'cached': cached['cached']}), 200, {'Access-Control-Allow-Origin': '*'})

	if debug:
		print 'Opened image page in %s seconds' % (time.time()-start)

	# Parse for the link to the full wiki page on npc
	page = soup.find(id='mw-imagepage-linkstoimage-ns110').find('a').get('href') # ns110 seems to be the code for the actual page
	page = 'http://www.uesp.net' + page

	# Open the full wiki page
	soup = BeautifulSoup(urllib2.urlopen(page))

	# Get the paragraphs from the page
	paragraphs = soup.find('div', 'mw-content-ltr').find_all('p')

	if debug:
		print 'Opened npc page in %s seconds' % (time.time()-start)

	# Get the title if it exists
	try:
		title = paragraphs[6].find('b').text
	except:
		title = ''
	content = ''
	# for some reason the 7th paragrph is the start of the ones about the character
	for num in range(6, len(paragraphs)):
		content = content + str(paragraphs[num])

	if debug:
		print 'Total time: %s seconds' % (time.time()-start)

	scroll = {'title': title, 'image': image, 'content': content}
	save_scroll(scroll)
	return (json.dumps({'title': title, 'image': image, 'content': content}), 200, {'Access-Control-Allow-Origin': '*'})

if __name__ == '__main__':
  # Bind to PORT if defined, otherwise default to 5000.
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=debug)
