import spotlight as sl
import os
import numpy as np
from scipy import spatial
import operator
import time
import sys
import io

reload(sys)
sys.setdefaultencoding("utf-8")

data_file = sys.argv[1]
FastTextDIR = "/home/bhinu/fastText/fasttext"
FastTextModel = "../wiki.en/wiki.en.bin"

url = 'http://model.dbpedia-spotlight.org/en/annotate'
confidence = 0.4
support = 20
start = time.time()

with open("../data/"+data_file+"_coref.txt", "r") as f:
	document = f.read()

print "Identifying Concept Phase: Started"
data = document
concepts_dictionary_list = sl.annotate(url,data,confidence=confidence,support=support)

concept_list = []
for concept in concepts_dictionary_list:
	if concept['surfaceForm'].lower() not in concept_list:
		concept_list.append(concept['surfaceForm'].lower())


with open("./"+data_file+"concepts.txt", "w") as f:
	for c in concept_list:
		f.write(c+"\n")

print "Identifying Concept Phase: Completed\n"

print "FastText Vector Generation Phase: Started"

os.system( FastTextDIR + ' print-word-vectors ' + FastTextModel+' < ./'+data_file+'concepts.txt > ./'+data_file+'concept_vec.txt')

word_dict = {}

with open("./"+data_file+"concept_vec.txt", "r") as f:
	lines = f.readlines()

for line in lines:
	word = unicode(line.split(" ")[0])
	vec = np.asarray((line.strip().split(" "))[1:], dtype = np.float32)
	if word not in word_dict:
		word_dict.update({word:vec})

concept_dict = {}

for concept in concept_list:
	words = concept.strip().split(" ")
	res_vec = word_dict[unicode(words[0])]
	if (len(words) > 1):
		for i in range(1,len(words)):
			res_vec += word_dict[unicode(words[i])]
	concept_dict.update({concept:res_vec})

print "FastText Vector Generation Phase: Completed\n"

print "Cosine Similarity Calculation Phase: Started"
similarity = {}

for c1 in concept_dict.keys():
	for c2 in concept_dict.keys():
		sim = 1 - spatial.distance.cosine(concept_dict[c1], concept_dict[c2])
		similarity.update({(c1,c2):sim})
		similarity.update({(c2,c1):sim})

similarit = sorted(similarity.items(), key=operator.itemgetter(1), reverse = True)

print "Cosine Similarity Calculation Phase: Completed\n"

print "Relation Extraction Phase: Started"

os.system('java -mx4g -cp "../stanford-corenlp-full-2018-02-27/*" edu.stanford.nlp.naturalli.OpenIE ../data/'+data_file+'_coref.txt > ./'+data_file+'relations.txt')

with io.open("./"+data_file+"relations.txt", "r", encoding='utf-8') as f:
	relations = f.readlines()

def add_concepts(old_list):
	new_list = []#old_list
	extra = []
	for w in old_list:
		if w not in concept_list:
			extra.append(unicode(w))
		else:
			new_list.append(w)
	for concept in concept_list:
		words = concept.split(" ")
		if len(words) > 0:
			for w in words:
				if unicode(w) in extra:
					new_list.extend(concept)
					break
	new_list = list(set(new_list).intersection(set(concept_list)))
	return new_list
def make_str(l):
	s = ""
	for w in l:
		s = s + w + " "
	return s.rstrip()

def make_one_relation(l):
	for rel in concepts_rel:
		if rel[0] == l[0] and rel[2] == l[2] and len(rel[1]) >= len(l[1]):
			return False
	return True
relations_list = []

for line in relations:
	sub = line.split("\t")[1].lower()
	rel = line.split("\t")[2].lower()
	obj = line.strip().split("\t")[3].lower()
	relations_list.append([sub,rel,obj])
	# print sub,"<--->",rel,"<--->",obj

concepts_rel = []

for rel in relations_list:
	sub = rel[0].split(" ")
	# print sub
	obj = rel[2].split(" ")
	sub_list = list(set(sub).intersection(set(word_dict.keys())))
	obj_list = list(set(obj).intersection(set(word_dict.keys())))
	sub_list = add_concepts(sub_list)
	obj_list = add_concepts(obj_list)
	if len(sub_list) > 0 and len(obj_list) > 0 :
		for c1 in sub_list:
			for c2 in obj_list:
				s = c1
				o = c2
				sim = similarity[(s,o)]
				s_i = sub.index(s)
				o_i = obj.index(o)
				r = make_str(sub[s_i+1:]) +" "+ rel[1] +" "+ make_str(obj[:o_i])
				flag = make_one_relation([s,r,o])
				if flag and sim >= 0.1:
					concepts_rel.append([s,r,o,sim])

print "Relation Extraction Phase: Completed\n"

gf = open("./"+data_file+"gfile.txt","w")
for rel in concepts_rel:
	gf.write(rel[0]+"\t"+rel[1]+"\t"+rel[2]+"\t"+str(rel[3])+"\n")
gf.close()



