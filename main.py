import math
import csv
import sys
import random
import urllib
import json

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
	readOmdbApi(entrada)

def readOmdbApi(entrada):
	for i in range(len(entrada)):
		url = "http://www.omdbapi.com/?i=tt" + entrada[i]
		response = urllib.urlopen(url);
		data = json.loads(response.read())
		print data

if __name__ == '__main__':
	main()