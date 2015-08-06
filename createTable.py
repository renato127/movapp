import math
import csv
import sys
import random
import urllib
import json
import httplib
import time

def readJson(json):
	with open(json, 'rt') as json_data:
		data = json.load(json_data)
		return data

def parser_csv(fileName):
	f = open(fileName, 'rt')
	parseActorsDict = {}
	try:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			parseActorsDict[row[1]] = row[2]
	finally:
		f.close()
	return parseActorsDict

def parser_actors_csv():
    f = open('actors.csv', 'rt')
    actorsNameList = []

    try:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            actorsNameList.append(row[1])
    finally:
        f.close()

    return actorsNameList

def nameNotInParse(namesCSV, namesParse):
    newNames = []

    for name in namesCSV:
        if name not in namesParse:
            newNames.append(name)

    return newNames

def main():
	#data = readJson()
	#inserirDiretores(data)
	atualizarActorsInMovie()


def inserirAtores(data):
	dictActors = getActorsDictionary(data)
	listActorsCSV = getActorsList(dictActors)
	listActorsParse = parser_actors_csv()
	listActors = nameNotInParse(listActorsCSV, listActorsParse)
	montarArrayDicionario(listActors)

def inserirDiretores(data):
	dictDirectors = getActorsDictionary(data)
	listDirectorsCSV = getActorsList(dictDirectors)
	montarArrayDicionario(listDirectorsCSV)

def atualizarActorsInMovie():
	actorsData = parser_csv('actor.csv')
	#moviesData = readJson('Movies.json')


def montarArrayDicionario(listActors):
	myArray = []
	newDict = {}
	batchLimit = 20
	i = 1
	for actor in listActors:
		newDict = {
			"method": "POST",
        	"path": "/1/classes/Director",
        	"body": {
        		"name": actor
        	}
		}
		myArray.append(newDict)
		i = i + 1
		if (i == batchLimit):
			insertListToParse(myArray)
			i = 1
			myArray = []

def insertListToParse(listActors):
	connection = httplib.HTTPSConnection('api.parse.com', 443)
	connection.connect()
	connection.request('POST', '/1/batch', json.dumps({"requests": listActors}), {
		"X-Parse-Application-Id": "wJm8XMGGzNX4EPhneuLUa6sC9gujI5Jiwnfnxl8k",
		"X-Parse-REST-API-Key": "2nc2p0ePr7RxrIVFOon8ofFZqUFfdSjegXG8qNTB",
		"Content-Type": "application/json"
	})
	result = json.loads(connection.getresponse().read())
	print result

def insertActorToParse(listActors):
	j = 0
	for i in listActors:
		movieActor = listActors[j]
		result = createObject('Actor', movieActor)
		print result
		j = j + 1

def getActorsList(data):
	myList = []
	for actor in data:
		myList.append(actor)
	return myList

def getActorsDictionary(data): 
	myDict = {}
	for movie in data['results']:
		movieActors = movie['Director']
		aMovieActors = movieActors.split(',')
		for movieActor in aMovieActors:
			movieActor = movieActor.strip()
			myDict[movieActor] = movieActor
	return myDict

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
	params = urllib.urlencode({"where":json.dumps({
	       "name": actorName
	     })})
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
