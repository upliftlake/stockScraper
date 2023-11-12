import datetime, pandas
from pandas_datareader import data
from bokeh.plotting import figure
from bokeh.io import show, output_file
from bokeh.embed import components
from bokeh.resources import CDN
from os import listdir

#global variable
global link

#link for the company csv files
link="Companies"

#return the company names for that specific letter
def company(letter):
    files=listdir(link)
    for file in files:
        if file[:-4]==letter:
            fileLink=link+"//"+file
            df=pandas.read_csv(fileLink)
            names=list(df.iloc[:,4])
            return names

#returns the parameters for the graph
def stockGraph(letter, symbolIndex, fromDate, toDate, chartType):
    files=listdir(link)
    for file in files:
        if file[:-4]==letter:
            fileLink=link+"//"+file
            df=pandas.read_csv(fileLink)

            #finding the company symbol
            symbols=list(df.iloc[:,6])
            symbols=symbols[int(symbolIndex)]

            #finding the company name
            selectedCompanyName=list(df.iloc[:,4])
            selectedCompanyName=selectedCompanyName[int(symbolIndex)]

            try:
                startDay=datetime.datetime(int(fromDate[:4]),int(fromDate[6:7]),int(fromDate[-2:]))
                endDay=datetime.datetime(int(toDate[:4]),int(toDate[6:7]),int(toDate[-2:]))
                ds=data.DataReader(name=symbols, data_source='yahoo', start=startDay, end=endDay)
                x=ds.index
                y=str(ds['High'])

                #scale_width automatically changes width with respect to browser width
                f=figure(x_axis_type='datetime', plot_width=1000, plot_height=400, sizing_mode="scale_width")

                #labeling of the axes
                f.title.text=symbols+" Stock Analysis from "+str(startDay)[:-9]+" to "+str(endDay)[:-9]
                f.title.text_color="#B80000"
                f.xaxis.axis_label="Date"
                f.yaxis.axis_label="Stock Price in $"
                f.grid.grid_line_alpha=0.4

                if chartType=='1':
                    #for the candle-lit graph
                    l=[]
                    color=''
                    for i,j in zip(list(ds.iloc[:,2]),list(ds.iloc[:,3])):
                        if i>j:
                            color='#848484'
                        else:
                            color='#FA5858'
                        l.append(color)

                    f.segment(x0=ds.index, y0=list((ds.iloc[:,0])), x1=ds.index, y1=list((ds.iloc[:,1])), color="#000000", line_width=1)
                    f.quad(top=list((ds.iloc[:,2])),
                    bottom=list((ds.iloc[:,3])),
                    left=ds.index-pandas.Timedelta(hours=6),
                    right=ds.index+pandas.Timedelta(hours=6),
                    color=l, line_color="#000000")

                    #companents for embedding
                    script1, div1=components(f)

                    #variables for the graph for another page
                    cdn_js=CDN.js_files
                    cdn_css=CDN.css_files
                else:
                    #for the line graph
                    f.line(x,list((ds.iloc[:,3])),line_width=2)
                    script1, div1=components(f)

                    #variables for the graph for another page
                    cdn_js=CDN.js_files
                    cdn_css=CDN.css_files

                return (script1, div1, cdn_js[0], cdn_css[0], selectedCompanyName)
            except:
                pass
