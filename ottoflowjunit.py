import xml.etree.ElementTree as ET,sys,os
flowname = "thisflow"
viewstatesset = set()
eventsset = set()
testmethods = []

def createViewstatesConstants(newFile):
	for vs in viewstatesset:
		#print('private static final String '+ 'VIEWSTATE_'+ vs.upper() + ' = "' + vs+'";\n')
		newFile.write('private static final String '+ 'VIEWSTATE_'+ vs.upper().replace("-","_") + ' = "' + vs+'";\n')

def createEventsConstants(newFile):
	for e in eventsset:
		#print('private static final String '+ 'EVENT_' + e.upper() + ' = "' + e+'";\n')
		newFile.write('private static final String '+ 'EVENT_' + e.upper().replace("-","_") + ' = "' + e+'";\n')

def createTest(state, event, to):
	return ('@Test\npublic void test_'+state.replace("-","_")+'_'+event.replace("-","_")+'() {\n\tinitializeFor'+flowname.capitalize()+'();\n\tassertFlowExecutionActive();\n\tsetCurrentState('+'VIEWSTATE_'+ state.upper()+');\n\tonEventId(context,'+'EVENT_'+event.upper()+');\n\tassertCurrentStateEquals('+'VIEWSTATE_'+ to.upper()+');\n}\n')

def createMethods(newFile):
	for m in testmethods:
		newFile.write(m)

def getData(flowDir):
	if(flowDir.endswith('.flow.xml')):
		tree = ET.parse(flowDir)
		root = tree.getroot()
		for child in root:
			if(child.tag == '{http://www.springframework.org/schema/webflow}view-state'):
				viewstatesset.add(child.get('id'))
				for e in child:
					if(e.get('on') is not None):
						eventsset.add(e.get('on'))
					if(e.tag == '{http://www.springframework.org/schema/webflow}transition'):
						testmethods.append(createTest(child.get('id'),e.get('on'),e.get('to')))
			else:
				for e in child:
					if(e.get('on') is not None):
						eventsset.add(e.get('on'))

def createOutputFile(flowDir):
	newFile = open(flowDir+'_ottoflow.java','w')
	newFile.write("//GENERATED WITH OTTOFLOW SCRIPT\n")
	getData(flowDir)
	createViewstatesConstants(newFile)
	createEventsConstants(newFile)
	createMethods(newFile)
	newFile.close()

def main():
	if len(sys.argv) <2:
		print("add file or dir to arguments")
	else: 
		flowDir = sys.argv[1]
		if os.path.isfile(flowDir) and flowDir.endswith('.flow.xml'):
			createOutputFile(flowDir)
		else:
			for fname in os.listdir(flowDir):
				if fname.endswith('.flow.xml'):
					path = os.path.join(flowDir, fname)
					if os.path.isdir(path):
						if(sys.argv<3):
							continue
						elif('r' in sys.argv[2]):
							createOutputFile(path)
							viewstatesset = set()
							eventsset = set()
							testmethods = []
					else:
						createOutputFile(path)
						viewstatesset = set()
						eventsset = set()
						testmethods = []

if __name__ == "__main__":
	main()