from globals import *
from bs4 import BeautifulSoup
import os

directory = "CaseAnalysis"
os.chdir(DATADIR + '/' + directory)

folders = [name for name in os.listdir() if not name.startswith(".")]
unique_subjects = dict()
for folder in folders:
	year = folder
	os.chdir(folder)
	files = list(os.listdir())
	for file in files:
		with open(file) as html_file:
			soup = BeautifulSoup(html_file, 'lxml')
		
		for elem in soup(text = "Subject:"):
			par = elem.parent.parent
			subject_list = par.get_text().replace("Subject:", '').split(';')
			for subject in subject_list:
				subject = subject.strip()
				if subject in unique_subjects:
					if year in unique_subjects[subject]:
						unique_subjects[subject][year] += 1
					else:
						unique_subjects[subject][year] = 1
				else:
					unique_subjects[subject] = dict()
					unique_subjects[subject][year] = 1

	os.chdir('..')
