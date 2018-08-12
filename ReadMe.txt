::Requirements::
1. pyspotlight (pip install pyspotlight)

2. fasttext (for installation: https://github.com/facebookresearch/fastText)

3. fasttext model - 'wiki.en.bin'
	Link: https://github.com/facebookresearch/fastText/blob/master/pretrained-vectors.md navigate to English and download bin+text
	the zip file you get should be extracted in the same 			directory as ./code/ and ./data/

4. stanford-corenlp-full-2018-02-27 for Co-reference Resolution and 		OpenIE (the zip file you get should be extracted in the same 			directory as ./code/ and ./data/)
	Link: https://stanfordnlp.github.io/CoreNLP/index.html#download


::Instructions::
1. navigate to data directory and save your data there with any name but the file format should be .txt

2. navigate to code directory and run the concept_map.py with the name of you data file as argument without .txt

Example:
	DataFile:  ./data/Mydata.txt
	CodeExecution:	cd code
					python concept_map.py Mydata

NOTE: It will take several minutes specially during fasttext phase and your machine will become slow. So be patient.

Thank You!!!