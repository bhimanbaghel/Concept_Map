import sys
import io

reload(sys)
sys.setdefaultencoding("utf-8")

data_file = sys.argv[1]
fd = open("../data/"+data_file+".txt", "r")
data_lines = fd.readlines()
fd.close()
new_data = []
for index in range(len(data_lines)):
	if data_lines[index] == '\n':
		continue
	else:
		line_len = len(data_lines[index])
		if(data_lines[index][line_len-2:] == "?\n"):
			continue
		else:
			new_data.append(data_lines[index])

for index in range(len(new_data)):
	new_data[index] = new_data[index].replace(". ", ".\n")
	new_data[index] = new_data[index].replace("("," ")
	new_data[index] = new_data[index].replace(")"," ")
	new_data[index] = new_data[index].replace("--"," ")
	new_data[index] = new_data[index].replace("-"," ")

fd = io.open("../data/"+data_file+"ext_data.txt", "w", encoding='utf-8')
for line in new_data:
	fd.write(unicode(line))
fd.close()