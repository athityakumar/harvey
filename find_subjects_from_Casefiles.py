from globals import *
from bs4 import BeautifulSoup
import os

from helpers import *

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
					unique_subjects[subject][year] += 1
				else:
					unique_subjects[subject] = dict()
					for y in range(1953, 2019):
						y = str(y)
						unique_subjects[subject][y] = 0
					unique_subjects[subject][year] = 1

	os.chdir('..')

SUBJECTS = [subject for subject in unique_subjects]

subjects_frequency = dict()
for cat in unique_subjects:
	year_dist = unique_subjects[cat]
	subjects_frequency[cat] = 0
	for year in year_dist:
		val = year_dist[year]
		subjects_frequency[cat] += val

def dict_sort(centrality_results, n=5):
	centrality_results = sorted(list(centrality_results.items()), key= lambda k: k[1], reverse=True)[:n]
	centrality_results = dict(centrality_results)
	return(centrality_results)

top_subjects_frequency = dict_sort(subjects_frequency)
for top_subject in top_subjects_frequency:
	subj_dist = unique_subjects[top_subject]
	subj_dist_tuple = [(year, subj_dist[year]) for year in subj_dist]
	plot_distribution(subj_dist_tuple, "Citations of {} cases over 1953-2018".format(top_subject))
