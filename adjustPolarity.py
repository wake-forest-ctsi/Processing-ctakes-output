#!/usr/bin/python
#
# This program takes a ctakes xmi file as input and outputs the disease codes 
# or the icd10 codes with the polarity information 
#
# Issues: There are duplicates in the output because of the different code schemes within ICD
#
# Input: xmi file
# Output: Terminal output 
# 

import sys
from collections import namedtuple

if len(sys.argv) != 2:
	print 'Usage: ./adjustPolarity.py <inputFile>'
	sys.exit()

inputfile = sys.argv[1] 

with open (inputfile, 'rt') as myfile:  	# Open inputfile for reading text
	contents = myfile.read()          	# Read the entire file into a string

parsed = contents.split("<") 

#for x in parsed[:]:
#	print x


#Inititalizing lists of data that need to be stored
begins     = []
ends       = []
ids        = []
polarities = [] 

conceptCount = 0

# Parsing only parts of the xmi document containing this info
for x in parsed[:]:
	if x.startswith("textsem:DiseaseDisorderMention"):
		#print x
		xsub = x.split("\"")
		begins.append(xsub[5])
		#print xsub[5]
		ends.append(xsub[7])
		#print xsub[7]
		ids.append(xsub[11])
		#print xsub[11]
		polarities.append(xsub[19])
		#print xsub[19]
		#print " "

	if x.startswith("refsem:UmlsConcept"):
		conceptCount = conceptCount + 1;
# If there are no ICD tags found then the lists will be empty
# output no tags and exit the program 

if len(begins) == 0:
	print ""
	print "There were no tags found"

	sys.exit()

#Converting to int
begins = map(int,begins)
ends   = map(int,ends)

## DEBUGGING ##

#for begin in begins[:]:
#	print begin
#print " "

#for end in ends[:]:
#	print end
#print " "

#for id in ids[:]:
#	print id
#print " "

#for polarity in polarities[:]:
#        print polarity
#print " "

#Constructing adjusted polarity array 
polarity_array = [1] * max(ends)

#print polarity_array
#print len(polarity_array)

#Assigning -1 in any place which a polarity of -1 exists. This is what we will use to find adjusted Polarity 
index = 0  
for pol in polarities[:]:
	if pol == "-1":
		#print index
		#print begins[index], ": ", ends[index]
		polarity_array[(begins[index]-1):(ends[index])] = [-1] * (ends[index]-begins[index]+1) 

	index = index + 1

## DEBUGGING ##

#print polarity_array
#print len(polarity_array)

#index = 0 
#for pol in polarity_array[:]: 
#	if pol == -1:
#		print index
#	index = index + 1


#Create datastructure for output
dictList = [] 
for k in range(conceptCount):
	dictList.append({"CUI":0, "codeScheme":0, "code":0, "originalPolarity":0, "adjustedPolarity":0, "codeText":0 }) 

#for k in range(20):
#	print dictList[k]

#Parse the dictionary codes and link it with the original and adjusted polarity 
index = 0
for x in parsed[:]:
        if x.startswith("refsem:UmlsConcept"):
                print x
                xsub = x.split("\"")
                #for i in xsub[:]:
		#	print i 
		#print " "
		
		tempID = xsub[1]
		#print "trying to find ", tempID

		dictList[index]["codeText"] = xsub[15]	
		dictList[index]["CUI"] = xsub[11]
		dictList[index]["codeScheme"] = xsub[3]
		dictList[index]["code"] = xsub[5]
		
		# relation is the value of the mapping between polarity and disease disorder		
		relation = 0 
		for str in ids[:]:
			if tempID in str:
				break
			relation = relation + 1
		
		
		#Only do this if there is a mapping in between DDM and UC
		#There does not always have to be a mapping
		if relation != len(ids):
			#print relation
			dictList[index]["originalPolarity"] = polarities[relation] 
			dictList[index]["adjustedPolarity"] = polarity_array[begins[relation]]
		
		#print  begins[relation],":",  ends[relation]-1
		#print  polarity_array[begins[relation]],":",  polarity_array[ends[relation]-1]
		
		index = index + 1

for k in range(conceptCount):
       	if dictList[k]["codeScheme"] != 0: 	#Don't print the extras 
		print dictList[k]

#print polarity_array
