import math
import csv
import sys
import random
import urllib
import json
import httplib
import simplejson

def main():
	getEztvShows()

def getEztvShows(): 
	showsId = []
	i = 1
	numShows = 18
	while i < numShows :
		url = "http://eztvapi.re/shows/" + str(i)
		response = urllib.urlopen(url);
		data = json.loads(response.read())
		for j in data:
			showsId.append(j['imdb_id'])
		i = i + 1
	readOmdbApi(showsId)

def readOmdbApi(entrada):
	print len(entrada)
	dataList = []
	for i in range(len(entrada)):
		url = "http://www.omdbapi.com/?i=" + entrada[i]
		response = urllib.urlopen(url);
		data = json.loads(response.read())
		importDataToParse(data, 'Serie')
		print i
	return dataList

def importDataToParse(data, table):
	connection = httplib.HTTPSConnection('api.parse.com', 443)
	connection.connect()
	connection.request('POST', '/1/classes/' + table, json.dumps(data), {
       	"X-Parse-Application-Id": "wJm8XMGGzNX4EPhneuLUa6sC9gujI5Jiwnfnxl8k",
       	"X-Parse-REST-API-Key": "2nc2p0ePr7RxrIVFOon8ofFZqUFfdSjegXG8qNTB",
       	"Content-Type": "application/json"
    })
	results = json.loads(connection.getresponse().read())
	print results

if __name__ == '__main__':
	main()