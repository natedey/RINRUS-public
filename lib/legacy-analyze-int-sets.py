#!/usr/bin/env python

#This code is written by mpalma. It is a script designed to analyze the specific files "edges_by_unique_sets.txt" output by Trang's scripts and "fileskey.txt" generated by
#Thomas' scripts used to generate the combinatoric-interaction-based models.
#Warning: This code is not written with the intention of applicaiton towards other situations. The code is not guaranteed to work or work correctly if used on a different enzyme/system.
#This code is being added for documentative purposes and does not have an immediate application in RINRUS software

#Usage: ./scriptname.py arg1[,arg2,arg3,...]
#                       where arg1/2/3 represent the names of the models to be analyzed in the format 12-aa,12-ab,12-ac,...

import os, sys, re
import argparse

#special printing without [] for easier organization in excel
def specialprint(aList):
	for i in aList:
		for e in i:
			print e,
			print ",",

def superSet(aList):
	mainSet=set()
	for sublist in aList:
       		set1=set(sublist)
		mainSet.add(frozenset(set1))
	bList = []
	for elem in mainSet:
		for item in mainSet:
			if elem.issuperset(item)==True and elem !=item:
				bList.append(elem)
				break
	
	for subset in bList:
		mainSet.remove(subset)
	return list(mainSet)
	
def interactioncounter(aList):
	bList = []
	for x in aList:
		for inter in x:
			if (any(inter in y for y in bList))==True:
				for i in bList:
					if i[0]==inter:
						i[1]+=1
			elif (any(inter in y for y in bList))==False:
				bList.append([inter,1])
	return bList

#This script combines the results of the model names, model residue composition, and model interaction lists for analysis

#Extract fileskey information (model names and model residue composition)
keyfile = open("fileskey.txt", "r")
keydata = []

for line in keyfile:
    modelname = line.split(".pdb")[0].split("res_")[1]
    reslist = [int(x) for x in line.split("[")[1].split("]")[0].split(",")]
    reslist.sort()
    keydata.append([modelname,reslist])

keyfile.close()

#Extract edges_by_unique_sets.txt information (model residue composition and corresponding edges)
edgefile = open("edges_by_unique_sets.txt", "r")
edgedata = []

for line in edgefile:
    reslist = [int(x) for x in line.split("|")[0].split("(")[1].split(")")[0].split(",")]
    reslist.sort()
    edgestring = line.split("[")[1].split("]")[0]
    edgestring = re.split('\(|\)', edgestring)
    edgestring = [x.replace('\'','').split(", ") for x in edgestring if ":" in x]
    edgedata.append([reslist, edgestring])

edgefile.close()

#Merge data from keydata and edgedata based on identical reslist information
#Data Format:
#  [0]"Natural",    [1]ModelName,   [2]ResidueList,       [3]Interactions
#  [0]"Absent" ,    [1]ResidueList, [2]Interactions
#  [0]"Artificial", [1]ModelName,   [2]NaturalResidueList [3]ArtificialResidueList [4]Interactions
mergedata = []
for line in edgedata:
    isnatural = False
    for item in keydata:
        if line[0]==item[1]:
            mergedata.append(["natural",item[0],item[1],line[1]])
            isnatural = True
            continue
    if isnatural == False:
        newline = list(set(line[0])|set([300,301,302,141,169,170,411]))
        newline.sort()
        if newline == line[0]:
            mergedata.append(["absent",line[0],line[1]])
            continue
        isartificialpresent = False
        for item in keydata:
            if newline==item[1]:
                mergedata.append(["artificial",item[0],line[0],newline,line[1]])
                isartificialpresent = True
                continue
        if isartificialpresent == False:
            mergedata.append(["absent",line[0],line[1]])

#Set up a system that is able to count interaction-type frequency among one or more files

filenames = sys.argv[1]
filenames = filenames.split(",")
mylist = []
totallistscounter = 0
mainList=[]
for name in filenames:
	for item in mergedata:
		if item[1]==name:
			if item[0]=="artificial":
				for x in item[4]:
					totallistscounter+=1
					list1 = []
					for conv in x:
						if "," in conv:
							str1 = conv.replace(",","")
							list1.append(str1)
							print type(str1)
						else:	
							list1.append(conv)
					mainList.append(list1)
							
			if item[0]=="natural":
				for x in item[3]:
					totallistscounter+=1
					list1 = []
					for conv in x:
						list1.append(conv)		
					mainList.append(list1)	

								
#mylist=interactioncounter(superSet(mainList))
totList = superSet(mainList)
for i in totList:
	for x in i:
		print x
			
			
mylist.sort(key=lambda x: x[1], reverse=True)
#specialprint(mylist)
#print mylist
print " "+str(totallistscounter)

#why are the rest of conv not appending to list1




#29-ak,27-bc,30-aa,25-bk,26-bb,29-ac,29-al,29-ar,31-aa,28-ar,28-ap,26-bg,30-ah,27-ai,29-ap,29-ah,28-ac,28-au,26-ba,30-ae,27-ba,28-ax,27-aj,27-az,27-ah,30-ai,29-aq,28-ao,28-an,28-aq,26-bc
#21-bl,23-ca,21-bj,24-at,23-bg,22-as,23-bz,22-bv,21-az,20-az,25-az,22-bk,22-bs,24-bj,23-bc,24-bz