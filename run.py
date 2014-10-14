from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import google
import re

app = Flask(__name__)

@app.route("/")
def mainpage():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def showresults():
    results = request.form['search']
    results = google.search(results, stop=10)
   # results = google.get_page(results)
        # [results.extract() for results in soup('script')]
    return render_template("index.html", results = results)
    
if __name__ == "__main__":
    app.run(debug=True)
