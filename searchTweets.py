# -*- coding: utf-8 -*-
from pattern.web import Twitter, plaintext
from pattern.db  import Datasheet
from pattern.en  import sentiment, modality
from pattern     import web

import os, sys; #sys.path.append("/Users/lifang/Desktop/Twitter") # path to Pattern module.
import glob
import re
import datetime
import time
import codecs
import md5

# Load SentiWordNet.
# Function sentiment_score() is called on each tweet translated to English.


t = Twitter(license=('PPMGBpHSVPn3llFITqxNPjaPT', 'rTrN7mGujHa9yw4HLwL0bp1myGe0BTTd9b0ZDyph1zO2KEMDfd', ('300267303-RBMZZjO9BXcq7CoCvvYqaFVumg4OEHsr3OpUfNzC', 'cFIBENL7SMFvJdsGKGlkvN8ShqN0FEXyGM6aLIMjwpzwr')))


indexFile = open('index.txt', 'r')
idData = indexFile.read()
indexList = idData.splitlines()

#for i in range(len(indexList)):
#    indexList[i] = [x.strip() for x in indexList[i].split(',')]

rundate = datetime.datetime.today()
filedate = ("%s-%s-%s") % (rundate.day, rundate.month, rundate.year)
#web.cache.path = os.path.join("cache", today)

# Create a unicode CSV file to store results.
# Put the current date in the filename for reference.
# Note: you can also use the pattern.table module to create CSV-files,
# but this module didn't exist yet at the time of the experiment.
folderpath = "/Users/lifang/Desktop/Interview/Twitter/Data/"
filename = "harvest_%s.txt" % filedate
if not os.path.exists(folderpath + filename):
    f = open(filename, "w")
    #f.write(codecs.BOM_UTF8)
    f.close()

# Open today's CSV file in append-mode.
harvest = open(filename, "a")

# Build an index of tweets we already did yesterday.
# Each tweet is assigned an id based on the query, tweet message and date.
# Those with an id already in the CSV files don't need to pass through Google translate.
SEEN = {}
for f in glob.glob("harvest*.txt"):
    f = open(f)
    s = f.read(); f.close()
    #print s
    if s == "":
        continue
    s = s.strip().split("\n")
    s = [x.split("\t") for x in s]
    #print s
    for x in s:
        if len(x) != 5:
            # This row wasn't saved correctly, probably something to do with \n or \t
            print "check %s %s" % (f, s)
        else:
            SEEN[web.u(x[0])] = True

# 

lang = 'en'
#full name of Country
country = '"United States"'
distance = '2000mi' #for US
location = 'near:'+country+' within:'+distance
verified = '"filter:verified"'
#location = near:"United States" within:2000mi

while True:
	for index in indexList:
    		searchSentence = '@'+index+' lang:'+lang+' '
    		#print(searchSentence)
    		tweets = t.search(searchSentence, start = 1, count = 100)
    		#except Exception, e:
    		#	time.sleep(600)
    		#    try: tweets = t.search(searchSentence, start = 1, count = 10)
    		#	except:
    		#		print "error"
    		#		tweets = []
    		for i, tweet in enumerate(tweets):
			txt = web.plaintext(tweet.description)
        		txt = txt.replace("#", "# ").replace("  ", " ") # Clean twitter hashtags
        		txt = txt.replace("\n", " ").replace("  ", " ")
        		txt = txt.replace("\t", " ").replace("  ", " ")
			id = md5.new(web.bytestring(searchSentence+"###"+txt+"###"+tweet.date)).hexdigest()
			if id not in SEEN:
				print index + ' ' + txt
				print sentiment(txt)
				s = "\t".join((id, index, txt, str(sentiment(txt)), tweet.date))
				harvest.write(web.bytestring(s)+"\n	")
	today = datetime.datetime.today()
	if today.day != rundate.day:
		break

harvest.close()