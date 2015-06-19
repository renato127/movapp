import math
import csv
import sys
import random
import urllib
import json
import httplib

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
	entrada = parser_csv()
	#print entrada
	data = readOmdbApi(entrada)

def readOmdbApi(entrada):
	dataList = []
	for i in range(len(entrada)):
		url = "http://www.omdbapi.com/?i=tt" + entrada[i]
		response = urllib.urlopen(url);
		data = json.loads(response.read())
		importDataToParse(data)
		print i
	return dataList

def importDataToParse(data):
	connection = httplib.HTTPSConnection('api.parse.com', 443)
	connection.connect()
	connection.request('POST', '/1/classes/Movies', json.dumps(data), {
       	"X-Parse-Application-Id": "wJm8XMGGzNX4EPhneuLUa6sC9gujI5Jiwnfnxl8k",
       	"X-Parse-REST-API-Key": "2nc2p0ePr7RxrIVFOon8ofFZqUFfdSjegXG8qNTB",
       	"Content-Type": "application/json"
    })
	results = json.loads(connection.getresponse().read())
	print results

if __name__ == '__main__':
	main()