from globals import *
from bs4 import BeautifulSoup
import os

from helpers import *

directory = "CaseAnalysis"
os.chdir(DATADIR + '/' + directory)

folders = [name for name in os.listdir() if not name.startswith(".")]
unique_keywords = dict()
for folder in folders:
    year = folder
    os.chdir(folder)
    files = list(os.listdir())
    for file in files:
        with open(file) as html_file:
            soup = BeautifulSoup(html_file, 'lxml')
        
        for elem in soup(text = "Keywords:"):
            par = elem.parent.parent
            # print(par.get_text())
            keywords_list = par.get_text().replace("Keywords:", '').split(',')
            # for keyword in keywords_list:
            i = 0
            while i < len(keywords_list):
                if i == len(keywords_list)-1:
                    current_keyword = keywords_list[i].strip()
                    if current_keyword in unique_keywords:
                        unique_keywords[current_keyword][year] += 1
                    else:
                        unique_keywords[current_keyword] = dict()
                        for y in range(1953, 2019):
                            y = str(y)
                            unique_keywords[current_keyword][y] = 0
                        unique_keywords[current_keyword][year] = 1
                    i += 1
                else:
                    current_keyword = keywords_list[i].strip()
                    next_keyword = keywords_list[i+1].strip()
                    if next_keyword[0:4].isdigit() or (current_keyword.count('(') != current_keyword.count(')')):
                        i += 2
                        current_keyword = current_keyword + ", " + next_keyword
                    else:
                        i += 1

                    if current_keyword in unique_keywords:
                        unique_keywords[current_keyword][year] += 1
                    else:
                        unique_keywords[current_keyword] = dict()
                        for y in range(1953, 2019):
                            y = str(y)
                            unique_keywords[current_keyword][y] = 0
                        unique_keywords[current_keyword][year] = 1


    os.chdir('..')

KEYWORDS = [keyword for keyword in unique_keywords]

# print(KEYWORDS)
keywords_frequency = dict()
for keyword in KEYWORDS:
    year_dist = unique_keywords[keyword]
    keywords_frequency[keyword] = 0
    for year in year_dist:
        val = year_dist[year]
        keywords_frequency[keyword] += val

def dict_sort(centrality_results, n=5):
    centrality_results = sorted(list(centrality_results.items()), key= lambda k: k[1], reverse=True)[:n]
    centrality_results = dict(centrality_results)
    return(centrality_results)

keywords_frequency = dict_sort(keywords_frequency, len(KEYWORDS))
print(keywords_frequency)
print(len(KEYWORDS))

# top_subjects_frequency = dict_sort(subjects_frequency)
# for top_subject in top_subjects_frequency:
#     subj_dist = unique_subjects[top_subject]
#     subj_dist_tuple = [(year, subj_dist[year]) for year in subj_dist]
#     plot_distribution(subj_dist_tuple, "Citations of {} cases over 1953-2018".format(top_subject))
