from globals import *
from bs4 import BeautifulSoup
import os

directory = "CaseAnalysis"
os.chdir(DATADIR + '/' + directory)

folders = [name for name in os.listdir() if not name.startswith(".")]
unique_subjects = []
all_subjects = []
count = 0
bad_files = 0
remove_this = 0
for folder in folders:
	remove_this = remove_this + 1 
	os.chdir(folder)
	count = count + len(os.listdir())
	files = list(os.listdir())
	print("\n Folder " + str(remove_this) + " of 66 folders")
	for file in files:
		with open(file) as html_file:
			soup = BeautifulSoup(html_file, 'lxml')

		# print(soup.prettify())
		num = 0
		for content in soup.find_all('div', class_ = 'locatorSection'):
			num = num + 1
			try:	
				if num == 3:
					# print("File: " + file)
					subject_header = content.p.strong
					# print(subject_header.next_sibling)
					subject_list = subject_header.next_sibling.split(";")
					# if subject_header.next_sibling not in unique_subjects:
					# 	unique_subjects.append(subject_header.next_sibling)	
					for subject in subject_list:	
						all_subjects.append(subject)
						if subject not in unique_subjects:
							unique_subjects.append(subject)
			except:	
				print("File: " + file)
				bad_files = bad_files + 1

	os.chdir('..')

print("Number of bad files: " + str(bad_files))
print("Total files scanned: " + str(count))
print("Number of unique subjects found: " + str(len(unique_subjects)))

frequency_subject = dict()
for subject in unique_subjects:
	freq = 0
	frequency_subject[subject] = all_subjects.count(subject)

print("Frequency of each subject")
print(frequency_subject)

# TODO: File handling for differently formatted html files

#############################################

# Directory by directory scanning
# os.chdir(DATADIR + "/" + directory + "/" + "1953")

# all_subjects = []
# unique_subjects = []
# files = list(os.listdir())
# for file in files:

# 	with open(file) as html_file:
# 		soup = BeautifulSoup(html_file, 'lxml')

# 		# print(soup.prettify())
# 		num = 0
# 		for content in soup.find_all('div', class_ = 'locatorSection'):
# 			num = num + 1
# 			try:
# 				if num == 3:
# 					subject_header = content.p.strong
# 					# print(subject_header.next_sibling)
# 					subject_list = subject_header.next_sibling.split(";")
# 					for subject in subject_list:	
# 						all_subjects.append(subject)
# 						if subject not in unique_subjects:
# 							unique_subjects.append(subject)
# 			except: 
# 				pass
# print(len(all_subjects))
# print(len(unique_subjects))
# print(unique_subjects)
# print(all_subjects)
# frequency_subject = dict()
# for subject in unique_subjects:
# 	freq = 0
# 	frequency_subject[subject] = all_subjects.count(subject)

# print(frequency_subject)

##############################################

# for individual bad_files
# 
# files = list(os.listdir())
# for file in files:
# 	with open(file) as html_file:
# 		soup = BeautifulSoup(html_file, 'lxml')

# 	# print(soup.prettify())
# 	num = 0
# 	for content in soup.find_all('div', class_ = 'locatorSection'):
# 		num = num + 1
# 		if num == 2:
# 			subject_header = content.p.strong
# 			print(subject_header.next_sibling)
