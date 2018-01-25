'''
    File name: knn.py
    Author: Philipp Thiele
    Date created: 10/24/2017
    Date last modified: 10/25/2017
    Python Version: 2.7
'''
import math
import operator

def loadDataset(filename,set=[]):
	with open(filename) as f:
		#zeilenweises Einlesen
		dataset = f.readlines()
	#Entfernen von whitespaces
	dataset = [x.strip() for x in dataset]
	#Zerlegen der einzelnen Zeilen
	dataset = [x.split() for x in dataset]
	for x in range(len(dataset)-1):
		for y in range(0,257): #because of ID + 256 grayscale values
			dataset[x][y]=float(dataset[x][y])
		set.append(dataset[x])

def euclidDist(vec1,vec2,leng):
	dist=0
	for x in range(1,leng):#First digit is used for the ID.
		dist+=pow((vec1[x]-vec2[x]),2)
	return math.sqrt(dist)

def nearestNeighbors(trainingSet,testData,k):
	dists=[]
	length=len(testData)

	for x in range(len(trainingSet)):
		#die Distanz des Testobjekts zum Trainingsobjekt wird berechnet		
		dis=euclidDist(testData,trainingSet[x],length)

		#es wird das Trainingsobjekt mit seiner Distanz zum Testobjekt gespeichert
		dists.append((trainingSet[x],dis))
	
	#die Liste wird nach dem Wert der Distanz sortiert
	dists.sort(key=operator.itemgetter(1))

	#in einer separaten Liste werden k viele Objekte mit kleinster Distanz gespeichert
	neighbors=[]
	for x in range(k):
		neighbors.append(dists[x][0])
	return neighbors

#k is the number of NN
def main(k):
	konfusionsMatrix=[[0 for x in range(10)] for y in range(10)] 
	trainingSet=[]
	testSet=[]
	loadDataset('zip.train',trainingSet)
	loadDataset('zip.test',testSet)
	print 'trainingSet: '+repr(len(trainingSet))
	print 'testSet: '+repr(len(testSet))
	for x in range(len(testSet)/50):
	#for x in range(len(testSet)/400):
	#alternativ kann man mit einer kleineren Menge an Testobjekten testen
	#da 7290*2006 Distanzberechnungen sehr viel Zeit benoetigen
		kneighbors=nearestNeighbors(trainingSet,testSet[x],k)

		#die IDs der k-NN und die des Testobjekts werden fuer die Konfusionsmatrix genutzt
		for y in range(0,len(kneighbors)):
			konfusionsMatrix[int(round(testSet[x][0]))][int(round(kneighbors[y][0]))]+=1

	#die Konfusionsmatrix(flat, nicht prozentual) wird mit Beschriftung von Zeilen und Spalten ausgegeben
	print('   0  1  2  3  4  5  6  7  8  9')
	for x in range(0,len(konfusionsMatrix)):
		print (str(x)+' '+str(konfusionsMatrix[x]))

	#es wird eine Konfusionsmatrix mit prozentualer Verteilung erstellt
	sumID=0
	percentKonfusionMatrix=[[0 for x in range(10)] for y in range(10)]
	#zuerst wird die Anzahl der Klassifikationen gezaehlt
	for x in range(0,len(konfusionsMatrix)):
		for y in range(0,len(konfusionsMatrix[x])):
			sumID+=konfusionsMatrix[x][y]

	#es wird der prozentuale Wert fuer jede Kombination von tatsaechlicher
	#und klassifizierter ID berechnet und eingetragen
	if sumID!=0:
		for a in range(0,len(percentKonfusionMatrix)):
			for b in range(0,len(percentKonfusionMatrix[a])):
				percentKonfusionMatrix[a][b]=konfusionsMatrix[a][b]*100/sumID
	print('   0  1  2  3  4  5  6  7  8  9')
	for x in range(0,len(percentKonfusionMatrix)):
		print (str(x)+' '+str(percentKonfusionMatrix[x]))


main(1)#1-NN
main(2)#2-NN
main(3)#3-NN