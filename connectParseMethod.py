import math
import csv
import sys
import random
import urllib
import json
import httplib
import time

def parser_csv():
	
	f = open(sys.argv[1], 'rt')
	imdbId = []
	try:
		reader = csv.reader(f, delimiter=':')
		for row in reader:
			imdbId.append(row[0])
	finally:
		f.close()
	return imdbId

def main():
	data = getTableData('Movies')

	i = 0
	for movie in data['results']:
	  	movieActors = movie['Actors']
	  	aMovieActors = movieActors.split(',')
	  	for movieActor in aMovieActors:
	  		movieActor = movieActor.strip()
	  		parseActor = retrieveObjects('Movies', movieActor)
	  		if (parseActor['results'] == []):
	  			result = createObject('Actor', movieActor)
	  			print result

def readOmdbApi(entrada):
	dataList = []
	for i in range(len(entrada)):
		url = "http://www.omdbapi.com/?i=tt" + entrada[i]
		response = urllib.urlopen(url);
		data = json.loads(response.read())
		importDataToParse(data)
		print i
	return dataList

def getTableData(table):
	connection = httplib.HTTPSConnection('api.parse.com', 443)
	params = urllib.urlencode({"where":json.dumps({}),"count":1,"limit":0})
	connection.connect()
	connection.request('GET', '/1/classes/' + table,'', {
	       "X-Parse-Application-Id": "wJm8XMGGzNX4EPhneuLUa6sC9gujI5Jiwnfnxl8k",
	       "X-Parse-REST-API-Key": "2nc2p0ePr7RxrIVFOon8ofFZqUFfdSjegXG8qNTB"
	     })
	result = json.loads(connection.getresponse().read())
	return result

def retrieveObjects(table, actorName):
	connection = httplib.HTTPSConnection('api.parse.com', 443)
	
	connection.connect()
	connection.request('GET', '/1/classes/' + table + '?%s' % params, '', {
	       "X-Parse-Application-Id": "wJm8XMGGzNX4EPhneuLUa6sC9gujI5Jiwnfnxl8k",
	       "X-Parse-REST-API-Key": "2nc2p0ePr7RxrIVFOon8ofFZqUFfdSjegXG8qNTB"
	     })
	result = json.loads(connection.getresponse().read())
	return result

def createObject(table, actorName):
	connection = httplib.HTTPSConnection('api.parse.com', 443)
	connection.connect()
	connection.request('POST', '/1/classes/' + table, json.dumps({
       "name": actorName,
     }), {
	       "X-Parse-Application-Id": "wJm8XMGGzNX4EPhneuLUa6sC9gujI5Jiwnfnxl8k",
	       "X-Parse-REST-API-Key": "2nc2p0ePr7RxrIVFOon8ofFZqUFfdSjegXG8qNTB"
	     })
	result = json.loads(connection.getresponse().read())
	return result

# parameters:
## requesType: 'GET' OR 'POST'
## getParams: Ex: "count":1,"limit":0
## postParams: "key": value
# check Parse API for more examples: https://www.parse.com/docs/rest/guide#queries

def connectParse(parameters):
	requestType = parameters['requestType']
	getParams = parameters['getParams']
	postParams = parameters['postParams']
	table = parameters['table']

	connection = httplib.HTTPSConnection('api.parse.com', 443)
	params = urllib.urlencode({getParams})
	connection.connect()
	connection.request(requestType, '/1/classes/' + table + getParams, json.dumps({postParams}), {
		"X-Parse-Application-Id": "wJm8XMGGzNX4EPhneuLUa6sC9gujI5Jiwnfnxl8k",
		"X-Parse-REST-API-Key": "2nc2p0ePr7RxrIVFOon8ofFZqUFfdSjegXG8qNTB"
	})

if __name__ == '__main__':
	main()
