from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import google
import re
    
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
    if(re.match('^Who|When', request.form['search'])):
        ggen = google.search(request.form['search'], stop=1)
        results = [google.get_page(link) for link in ggen]
        results = [soupify(x) for x in results]
        ###INPUT FILTER HERE
        return render_template("index.html", results = results)
    return render_template("index.html", results = "Please enter 'Who' or 'When'")


if __name__ == "__main__":
    app.run(debug=True)
