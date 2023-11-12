from flask import Flask, render_template, request, url_for
from stockCore import *
from bokeh.io import show
from bokeh.plotting import figure
from bokeh.io import show, output_file
from bokeh.embed import components
from bokeh.resources import CDN
from datetime import datetime, timedelta

#global variables
global fromDate, toDate, letterSelected, letters

letters=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


app=Flask(__name__)

#home page
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', title="• Home", alphabet=letters, well="well")

#letter page
@app.route('/letter', methods=['POST'])
def letter():
    if request.method=='POST':
        letterSelected=request.form['letter']

        #company function
        namesList=company(letterSelected)
        return render_template('companies.html', title="• Company", well="well", alphabet=letterSelected, companiesList=namesList,
        fromDate=datetime.now()-timedelta(days=20), toDate=datetime.now())

#graph page
@app.route('/graph', methods=['GET','POST'])
def graph():
    if request.method=='POST':

        #data collected from the form
        letterSelected=request.form['letter']
        companyIndex=str(request.form['companiesList'])
        fromDate=request.form['from_date']
        toDate=request.form['to_date']
        chartType=request.form['types']

        #sending data to the graph function and returned
        figure=stockGraph(letterSelected, companyIndex, fromDate, toDate, chartType)
        script1=figure[0]
        div1=figure[1]
        cdn_js=figure[2]
        cdn_css=figure[3]
        company=figure[4]

        return render_template('plot.html', title="• Result", script1=script1, div1=div1, cdn_js=cdn_js,
        cdn_css=cdn_css, fromDate=fromDate, toDate=toDate, alphabet=letterSelected, companiesList=[company])

#about page
@app.route('/about')
def about():
    return render_template('about.html', title="• About", well="well")

if __name__=="__main__":
    app.debug=True
    app.run()
