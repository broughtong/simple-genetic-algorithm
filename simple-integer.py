#!/usr/bin/env python

import threading
import Queue
import random

generation = 0
population = 10
reproductionRate = 3
target = 83
maxVal = 100
minVal = -100
mutationFactor = 5

def problem(value):
	return abs(target - value)

class Populant(threading.Thread):
	def __init__(self, returnQueue, value):
		threading.Thread.__init__(self)
		self.returnQueue = returnQueue
		self.value = value
	def run(self):
		result = problem(self.value)
		self.returnQueue.put(str(result) + ":" + str(self.value))

prevGenResults = []
for i in xrange(0, population):
	prevGenResults.append(random.randrange(minVal, maxVal + 1))

while True:

	populationList = []
	resultQueue = Queue.Queue()

	print "New generation: " + str(generation) + " --- Target is: " + str(target)
	print "Current population: "
	print prevGenResults
	print

	for i in xrange(0, population):

		newPopulant = Populant(resultQueue, prevGenResults[i])
		newPopulant.start()
		populationList.append(newPopulant)
		
	for i in xrange(0, population):
	
		populationList[i].join()

	returnValues = []
	for i in xrange(0, population):
		val = resultQueue.get()
		val = val.split(":")
		returnValues.append([int(val[0]), int(val[1])])

	returnValues = sorted(returnValues)	
	returnValues = returnValues[:reproductionRate]

	prevGenResults = []
	for i in xrange(0, population):
		parent = int(returnValues[i%reproductionRate][1])
		mutation = random.randrange(parent - mutationFactor, parent + mutationFactor)
		prevGenResults.append(mutation)

	generation += 1

	userInput = raw_input()

	if userInput != '':
		break
