#!/usr/bin/python3

import sys
import re
import json
import textwrap
import pprint
import os

path=""
if len(sys.argv) == 2:
	path = sys.argv[1]
	if path[:-1] != '/':
		path += '/'

textSelectors = set()
setOfSelectors = set()

for filename in os.listdir(path):
	if filename.endswith(".mss"):
		setUsed = False
		with open(path+filename, 'r') as file:
			filedata = file.read().replace('\n','')
		# remove comments
		print("Checking "+filename)
		filedata = re.sub('/\*.*?\*/','',filedata,re.DOTALL)
		segments = re.split('(#[a-zA-Z-:]+[[ ])|(\.[a-zA-Z-:]+[[ ])', filedata, flags=re.DOTALL)

		for element in segments:
			if element is not None and element is not '':

				if (element.startswith("#") or element.startswith('.')):
					#print(element)
					if (setUsed):
						setOfSelectors.clear()
						setUsed = False
					setOfSelectors.add(element[:-1])
				elif "text-name:" in element:
					print(" "*2 + str(setOfSelectors) + " has text in it")
					textSelectors.update(setOfSelectors)
					setUsed = True
				elif "{" in element:
					#print("{ found")
					setUsed = True

# remove css pseudo classes
newset = set()
for foundSelector in textSelectors:
	if foundSelector.find(":") > 0:
		newset.add(foundSelector[:foundSelector.find(":")])
	else:
		newset.add(foundSelector)
textSelectors = newset

# find entries for found ids and classes in the project mml file			
with open(path+'project.mml') as data_file:    
	data = json.load(data_file)

idlist = []
classlist = []

# select all ids (all without # or . at the front!)
for i in range(len(data['Layer'])):
     idlist.append(data['Layer'][i]['id'])
for i in range(len(data['Layer'])):
	classlist.append(data['Layer'][i]['class']) #most of them are empty for standard project.mml

#print
printwidth = 200

pp = pprint.PrettyPrinter(width=printwidth)
for selector in textSelectors:
	if selector.startswith('#'):
		print("\n"+selector+" has the following datasource:")		
		datasource = ""
		if idlist.count(selector[1:]) > 0:
			datasource = data['Layer'][idlist.index(selector[1:])]['Datasource']
		else:
			for entry in idlist:
				if selector[1:] in entry:
					datasource = data['Layer'][idlist.index(entry)]['Datasource']
					break
		pp.pprint(datasource)
	if selector.startswith('.'):
		print("\n"+selector+" has the following datasource:")		
		datasource = ""
		if classlist.count(selector[1:]) > 0:
			datasource = data['Layer'][classlist.index(selector[1:])]['Datasource']
		else:
			for entry in classlist:
				if selector[1:] in entry:
					datasource = data['Layer'][classlist.index(entry)]['Datasource']
					break
		pp.pprint(datasource)
