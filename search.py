from bs4 import BeautifulSoup 
import re
import csv
import google
#Will need to pip install google and BeautifulSoup to run

#This is the google material to be used with BeautifulSoup
#It does take a while to run, if you need to do extensive testing
#I would recommend commenting it out.

print "Loading Google Data..."
gDataGen=google.search("Andrew Garfield",stop=25) #This is a generator for the first 25 links of the google search "Andrew Garfield"
gData=[] #List of all the links
for link in gDataGen: #This step takes a while (Mr.Z said this is normal)
    gData.append(google.get_page(link))
#This creates a list of all the data from each of the first 25 links. If you want more results, change 'stop=25' to a higher number
#however this will make it load much slower due to the wait time for the url pages. To see what a result looks like, you can use the line below.

#print gData[0]

#End of google material

data = open("aroundworldin80days.txt", 'r')
text = data.read()
data.close()

dict_f = open("dictionary.txt",'r')
dictionary =  dict_f.read()
dict_f.close()

match_twoNames = re.findall(r'([A-Z][a-z]+ [A-Z][a-z]+)', text)
match_titles = re.findall(r'([A-Z][a-z]+\. [A-Z][a-z]*)', text)

places = ['College', 'University', 'Institution', 'City', 'Library','Park','Street','Island','Creek','Railroad','Islands','Territory','Valley','House','River','Mountain','Mountains','Railway','Yard','Fort','Peak','Hotel','Lake', 'Camp', 'Row', 'New', 'Gate']

starting_words = ['But', 'On', 'From', 'Then', 'Down', 'To', 'A', 'An', 'The', 'In', 'Left', 'East', 'West', 'South', 'North', 'Last']
##print match_twoNames
##print match_titles

names = []
names_final= []

csv_first = csv.reader(open("firstnames.csv","rU"),dialect=csv.excel_tab)
#first_names_file = open("firstnames.csv")
#csv_first = csv.reader(first_names_file) 

csv_last = csv.reader(open("lastnames.csv","rU"),dialect=csv.excel_tab)
#last_names_file = open("lastnames.csv")
#csv_last = csv.reader(last_names_file)

first_names_list = []
last_names_list = []
all_names_list = []

for row in csv_first: 
    first_names_list.append(row[0])
for row in csv_last: 
    last_names_list.append(row[0])

all_names_list = first_names_list + last_names_list


for name in match_twoNames:
    names.append(name)
for name in match_titles:
    names.append(name)
for name in names:
    to_add = True
    first_name = name[:(name.find(' '))]
    last_name = name[(name.find(' ')) + 1:]
    first_name_l = first_name.lower()
    last_name_l = last_name.lower()        
    if (name in places) or (first_name in places) or (last_name in places):
        #names.remove(name)
        to_add = False
    if (first_name in starting_words):
        to_add = False
    elif first_name not in first_names_list and first_name not in last_names_list and name not in match_titles:
        if first_name_l in dictionary: # first name isnt common and IS in dictionary
            #names.remove(name)
            to_add=False
    elif first_name_l in dictionary and last_name_l in dictionary and (first_name not in first_names_list or last_name not in last_names_list): 
        #names.remove(name)
        to_add = False
    else: 
        if to_add == True and names_final.count(name)<1: 
            names_final.append(name)

#for name in names: 
 #   if names_final.count(name)<1: 
  #      names_final.append(name)
print names_final
