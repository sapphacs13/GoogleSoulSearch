from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import google
import re
import csv

def findDate(text):

    match_dates_md = re.findall(r'([A-Z][a-z]+ [1-2][0-9])', text)
    match_dates_md.append(re.findall(r'([A-Z][a-z]+ 0[1-9])', text))
    match_dates_mdy = re.findall(r'(A-Z][a-z]+ [1-2][0-9], [0-9]*)', text)
    match_dates_mdy.append(re.findall(r'([A-Z][a-z]+ 0[1-9], [0-9]*)', text))

    #opened = open(fil, 'r')
    #text = fil.read()
    #opened.close()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    dates = []
    to_add = True
    dates_final = []
    
    for date in match_dates_md:
        dates.append(date)
    for date in match_dates_mdy:
        dates.append(date)
    for date in dates:
      #  date_month = date[:date.find(' ')]
        #print date_month
       # if date_month not in months:
       #     to_add = False
       # if to_add == True:
        dates_final.append(date)
    return dates_final

def findName(text):
    #opened = open(data, 'r')
    #text = opened.read()
    #opened.close()
    dict_f = open("dictionary.txt",'r')
    dictionary =  dict_f.read()
    dict_f.close()

    ##NOW MATCH
    
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
    counter = 0
    for name in names:
        if counter > 10:
            break
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
                counter = counter + 1
    
        #for name in names: 
        #   if names_final.count(name)<1: 
        #      names_final.append(name)
        #
    return names_final

def soupify(webtext):
    soup = BeautifulSoup(webtext)
    scraped = soup.get_text()
    return scraped.encode('utf-8')

app = Flask(__name__)

@app.route("/")
def mainpage():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def showresults():
    if(re.match('^Who', request.form['search'])):
        ggen = google.search(request.form['search'], stop=1)
        results = [google.get_page(link) for link in ggen]
        results = [soupify(x) for x in results]
        results = [findName(x) for x in results]
        return render_template("index.html", results = results)
    elif(re.match('^When', request.form['search'])):
        ggen = google.search(request.form['search'], stop=1)
        results = [google.get_page(link) for link in ggen]
        results = [soupify(x) for x in results]
        results = [findDate(x) for x in results]
        return render_template("index.html", results = results)
    return render_template("index.html", results = "Please enter 'Who' or 'When'")


if __name__ == "__main__":
    app.run(debug=True)
