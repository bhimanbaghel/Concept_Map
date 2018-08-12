import sys
import os

data_file = sys.argv[1]

print "Data Extraction Phase: Started"
os.system('python extract_data.py '+ `data_file`)
print "Data Extraction Phase: Completed\n"

print "Coreference Resolution Phase: Started"
os.system('python xml_parser.py '+ `data_file`)
print "Coreference Resolution Phase: Completed\n"

os.system('python project.py '+ `data_file`)

print "Graph Visualization Phase: Started"
os.system('python make_graph.py '+ `data_file`)

os.system('eog ' + data_file +'simple.png')
print "Graph Visualization Phase: Completed\n"
print "THANK YOU!!!"