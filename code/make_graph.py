import pygraphviz as pgv
import os
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

data_file = sys.argv[1]
G = pgv.AGraph(directed=True, center="true", overlap="false", len="f", splines="false")
fp = open("./"+data_file+"gfile.txt", "r")
lines = fp.readlines()

for line in lines:
	line = line.strip("\n")
	conf_subj_relation_object = line.split("\t")

	G.add_node(conf_subj_relation_object[0])
	G.add_node(conf_subj_relation_object[2])
	G.add_edge(conf_subj_relation_object[0], conf_subj_relation_object[2])
	edge = G.get_edge(conf_subj_relation_object[0], conf_subj_relation_object[2])
	edge.attr['label'] = conf_subj_relation_object[1]
	edge.attr['weight'] = conf_subj_relation_object[3]
	#edge.attr['penwidth'] = float(conf_subj_relation_object[3])*10

	if len(conf_subj_relation_object[1].split())<4:
		edge.attr['len'] = len(conf_subj_relation_object[1].split())*2
	else:
		edge.attr['len'] = len(conf_subj_relation_object[1].split())*0.6

#print "Wrote ./"+data_file+"simple.dot"
G.write("./"+data_file+"simple.dot")  # write to simple.dot
B = pgv.AGraph("./"+data_file+"simple.dot")  # create a new graph from file
B.layout()  # layout with default (neato)
B.draw("./"+data_file+"simple.png")  # draw png
os.system('circo -Tpng '+'./'+data_file+'simple.dot -o ./' +data_file+'_out.png')
