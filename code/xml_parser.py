from bs4 import BeautifulSoup as BS
import io
import sys
import os

reload(sys)
sys.setdefaultencoding("utf-8")

def change_code(sentence):
	s_list = sentence.split(" ")
	s_list = [unicode(x) for x in s_list]
	return " ".join(s_list)

data_file = sys.argv[1]

os.system('java -cp "../stanford-corenlp-full-2018-02-27/*" -Xmx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse,dcoref -file ../data/'+data_file+'ext_data.txt')

xml_path = "./"+data_file+"ext_data.txt.xml"
xml_fd = open(xml_path, "r")
xml_file = xml_fd.read()
xml_soup = BS(xml_file, 'lxml')
data_fd = io.open("../data/"+data_file+"ext_data.txt", encoding='utf-8')

data_lines = data_fd.readlines()

data_fd.close()
for x in xml_soup.find_all('coreference'):
	structure_list = list(x.children)
	for s_items in structure_list:
		if s_items == "\n":
			continue
		else:
			mention_list = []
			s_items_list = list(s_items.children)
			
			for s in s_items_list:
				if s == "\n":
					continue
				mention_list.append((int(s.find('sentence').get_text()),s.find('text').get_text()))
			head_word = unicode(mention_list[0][1])
			for index in range(1,len(mention_list)):
				target_sentence = mention_list[index][0]-1
				target_word = mention_list[index][1]
				try:
					if target_word in data_lines[target_sentence]:
						# print "found"
						data_lines[target_sentence] = data_lines[target_sentence].replace(target_word, head_word)
						# print data_lines[target_sentence]
				except:
					continue
	break

out_fd = open("../data/"+data_file+"_coref.txt", "w")
for lines in data_lines:
	out_fd.write(lines)
out_fd.close()