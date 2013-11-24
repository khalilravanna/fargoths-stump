import os
from flask import Flask, render_template, url_for, request
import urllib2, json
from bs4 import BeautifulSoup

app = Flask(__name__)

debug = False

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

def get_full_image(link):
	parts = link.split('/')
	parts.pop(3)
	parts.pop(6)
	new_link = parts[0] + '//' + parts[2] + '/' + parts[3] + '/' + parts[4] + '/' + parts[5]
	return new_link

@app.route('/npc', methods=['GET'])
def npc():
	import json, random, time
	from bs4 import BeautifulSoup

	if debug:
		return json.dumps({"content": "<p><b>Skink-in-Tree's-Shade</b>, an <a href=\"http://www.uesp.net/wiki/Morrowind:Argonian\" title=\"Morrowind:Argonian\">Argonian</a> <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Sorcerer\" title=\"Morrowind:Sorcerer\">sorcerer</a>, resides in the <a href=\"http://www.uesp.net/wiki/Morrowind:Mage%27s_Guild_(Wolverine_Hall)\" title=\"Morrowind:Mage's Guild (Wolverine Hall)\">Mage's Guild</a> at Wolverine Hall near <a href=\"http://www.uesp.net/wiki/Morrowind:Sadrith_Mora\" title=\"Morrowind:Sadrith Mora\">Sadrith Mora</a>. He is the primary quest giver there and can allow you to join the guild.</p><p>He wears a <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Common_Shirt\" title=\"Morrowind:Common Shirt\">common shirt</a> with matching <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Common_Pants\" title=\"Morrowind:Common Pants\">pants</a>, and he wields a <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Glass_Dagger\" title=\"Morrowind:Glass Dagger\">glass dagger</a>. Like all Argonians, he is <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Resist_Poison\" title=\"Morrowind:Resist Poison\">immune to poison</a>, has a <a href=\"http://www.uesp.net/wiki/Morrowind:Resist_Common_Disease\" title=\"Morrowind:Resist Common Disease\">resistance to disease</a>, and can <a href=\"http://www.uesp.net/wiki/Morrowind:Water_Breathing\" title=\"Morrowind:Water Breathing\">breathe underwater</a>. Aside from that, he knows: <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Burden_of_Sin\" title=\"Morrowind:Spells/Burden of Sin\">Burden of Sin</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Crushing_Burden\" title=\"Morrowind:Spells/Crushing Burden\">Crushing Burden</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Crushing_Burden_of_Sin\" title=\"Morrowind:Spells/Crushing Burden of Sin\">Crushing Burden of Sin</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Cruel_Weary\" title=\"Morrowind:Spells/Cruel Weary\">Cruel Weary</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Great_Feather\" title=\"Morrowind:Spells/Great Feather\">Great Feather</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Summon_Greater_Bonewalker\" title=\"Morrowind:Spells/Summon Greater Bonewalker\">Summon Greater Bonewalker</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Summon_Scamp\" title=\"Morrowind:Spells/Summon Scamp\">Summon Scamp</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Wizard_Rend\" title=\"Morrowind:Spells/Wizard Rend\">Wizard Rend</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Commanding_Touch\" title=\"Morrowind:Spells/Commanding Touch\">Commanding Touch</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Reflect\" title=\"Morrowind:Spells/Reflect\">Reflect</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Weak_Spelldrinker\" title=\"Morrowind:Spells/Weak Spelldrinker\">Weak Spelldrinker</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Wild_Spelldrinker\" title=\"Morrowind:Spells/Wild Spelldrinker\">Wild Spelldrinker</a>, <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Slowfall\" title=\"Morrowind:Spells/Slowfall\">Slowfall</a>, and <a class=\"mw-redirect\" href=\"http://www.uesp.net/wiki/Morrowind:Spells/Summon_Skeletal_Minion\" title=\"Morrowind:Spells/Summon Skeletal Minion\">Summon Skeletal Minion</a>.</p><p>This humble Argonian holds his difficult Mages Guild branch with grace and diplomacy. Of all Guild leaders he also seems the most concerned about Vvardenfell's contemporary events. Dark afflictions such as vampirism and ash creatures appear as his chosen field of academic study. Despite being a Mages Guild member, he is somewhat respected by <a href=\"http://www.uesp.net/wiki/Morrowind:House_Telvanni\" title=\"Morrowind:House Telvanni\">House Telvanni</a>, having been noted by them as being <i>\"almost as sage and learned as Telvanni aspirants five times his age\"</i>. He is also rumored to carry his anti-<a href=\"http://www.uesp.net/wiki/Morrowind:Slavery\" title=\"Morrowind:Slavery\">slavery</a> politics a little too far, much farther than Imperial law would normally allow.</p><p>Skink-in-Tree's-Shade is the <a href=\"http://www.uesp.net/wiki/Morrowind:Master_Trainers\" title=\"Morrowind:Master Trainers\">Master Trainer</a> for <a href=\"http://www.uesp.net/wiki/Morrowind:Speechcraft\" title=\"Morrowind:Speechcraft\">Speechcraft</a> and also provides medium <a href=\"http://www.uesp.net/wiki/Morrowind:Trainers\" title=\"Morrowind:Trainers\">training</a> in <a href=\"http://www.uesp.net/wiki/Morrowind:Mysticism\" title=\"Morrowind:Mysticism\">Mysticism</a> and <a href=\"http://www.uesp.net/wiki/Morrowind:Enchant\" title=\"Morrowind:Enchant\">Enchant</a>, and is the second-highest enchant after the hostile master trainer, <a href=\"http://www.uesp.net/wiki/Morrowind:Qorwynn\" title=\"Morrowind:Qorwynn\">Qorwynn</a>. However, you must be at least a <a href=\"http://www.uesp.net/wiki/Morrowind:Mages_Guild#Mages_Guild_Ranks\" title=\"Morrowind:Mages Guild\">Magician</a> in the Mages Guild to receive Skink's services.</p>", "image": "http://images.uesp.net/thumb/1/13/MW-npc-Skink-in-Tree%27s-Shade.jpg/600px-MW-npc-Skink-in-Tree%27s-Shade.jpg", "title": "Skink-in-Tree's-Shade"})
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

	thumb_link = items[num].find('img').get('src')
	image = get_full_image(thumb_link)

	if request.args.get('image_only') and not request.args.get('lores'):
		return (json.dumps({'image': image}), 200, {'Access-Control-Allow-Origin': '*'})

	link = items[num].find('a').get('href')
	link = 'http://www.uesp.net' + link

	soup = BeautifulSoup(urllib2.urlopen(link))
	if request.args.get('lores'):
		image = soup.find('div', 'fullImageLink').find('img').get('src')
		if request.args.get('image_only'):
			return (json.dumps({'image': image}), 200, {'Access-Control-Allow-Origin': '*'})


	print 'Opened image page in %s seconds' % (time.time()-start)

	page = soup.find(id='mw-imagepage-linkstoimage-ns110').find('a').get('href') # ns110 seems to be the code for the actual page
	page = 'http://www.uesp.net' + page

	soup = BeautifulSoup(urllib2.urlopen(page))

	# replace all links with their full path first
	links = soup.find_all('a')
	for link in links:
		split = str(link.get('href')).split('/')
		if len(split) > 1:
			if split[1] == 'wiki':
				old_link = str(link.get('href'))
				new_link = 'http://www.uesp.net' + old_link
				print new_link
				link['href'] = new_link

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

app.run(debug=debug)
