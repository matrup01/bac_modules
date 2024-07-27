from pops import Pops
from sen55 import SEN55
from ccs811 import CCS811
import csv
import itertools
import matplotlib.pyplot as plt
import numpy as np
import json
import os

def getdata(day=["*"],height=["*"],loc=["*"],bgstart="",pops=True,sen55=False,ccs811=False,file="flights_lookuptable.csv"):
    
    #import flight-file
    raw_data = csv.reader(open(file),delimiter=",")
    raw_data = list(raw_data)
    raw_data = [raw_data[i] for i in range(2,len(raw_data))]
    
    #mask to mask out flights which dont meet criteria and create output-dict
    mask = [1 for i in range(len(raw_data))]
    out = {}
    
    #check if each flight meets day-criteria
    if day != ["*"]:
        for i in range(len(mask)):
            if not raw_data[i][0] in day:
                mask[i] = 0
                
    #check if each flight meets height-criteria
    if height != ["*"]:
        for i in range(len(mask)):
            if not raw_data[i][1] in height:
                mask[i] = 0
                
    #check if each flight meets loc-criteria
    if loc != ["*"]:
        for i in range(len(mask)):
            if not raw_data[i][2] in loc:
                mask[i] = 0
                
    #check if flight has certain bgstart
    if bgstart != "":
        for i in range(len(mask)):
            if bgstart != raw_data[i][3]:
                mask[i] = 0
                
    #mask out flights that dont meet criteria
    data = []
    for dat,decider in zip(raw_data,mask):
        if decider == 1:
            data.append(dat)
                
    #create Pops-Objects
    if pops:
        relobjs = [Pops(file=data[i][7],start=data[i][3],end=data[i][4],timecorr=int(data[i][10])) for i in range(len(data))]
        popsout = [Pops(file=data[i][7],start=data[i][5],end=data[i][6],timecorr=int(data[i][10]),title=(data[i][0]+data[i][5]),relobj=relobjs[i]) for i in range(len(data))]
        out["pops"] = popsout
    
    #create SEN55-Objects
    if sen55:
        senout = [SEN55(file=data[i][8],start=data[i][5],end=data[i][6]) for i in range(len(data))]
        out["sen55"] = senout
     
    #create CCS811-Objects
    if ccs811:
        ccsout = [CCS811(file=data[i][9],start=data[i][5],end=data[i][6]) for i in range(len(data)) if data[i][9] != "no data collected"]
        out["ccs811"] = ccsout
    
    return out


def flightvals(day,flight,file="flights_lookuptable.csv"):
    
    #import flight-file
    raw_data = csv.reader(open(file),delimiter=",")
    raw_data = list(raw_data)
    
    #crop data
    data = []
    for element in raw_data:
        if element[0] == day:
            data.append(element)
            
    #find flight
    flights = list(set([data[i][3] for i in range(len(data))]))
    flights.sort()
    bgstart = flights[flight-1]
    
    #find vals
    vals = []
    for element in data:
        if element[3] == bgstart:
            val = element[2] + element[1]
            vals.append(val)
    vals = list(set(vals))
    
    #outputs: [day,bgstart,loc,height]
    output = [[day,bgstart,"".join(element[i] for i in range(len(element)-2)),"".join(element[i] for i in range(len(element)-2,len(element)))] for element in vals]
    
    return output


def flightsummary(day,flight,y,file="flights_lookuptable.csv",ylims=[-100,300],averaged=False):
    
    #init variables
    correctflights = flightvals(day,flight,file=file)
    ylabel = y if y != "pops_underpm25" else "small particles"
    title = day + " " + "flight" + str(flight) + " " + ylabel
    labels = []
    totaly = []
    
    #get data
    for element in correctflights:
        
        data = getdata(day=[element[0]],height=[element[3]],loc=[element[2]],bgstart=element[1],file=file)
        
        if averaged:
            for dat in data["pops"]:
                dat.average()
        
        label = element[2] + " " + element[3] + "m"
        ydata = [dat.returndata(y) for dat in data["pops"]]
        
        if len(ydata) == 1:
            ydata = ydata[0]
        else:
            ydata = list(itertools.chain(*ydata))
        
        labels.append(label)
        totaly.append(ydata)
        
        
    #draw plot
    fig,ax = plt.subplots()

    plt.title(title)
    ax.violinplot(dataset=totaly,showmeans=False,showmedians=False,showextrema=False)
    ax.boxplot(x=totaly,labels=labels,showmeans=True,showfliers=False)
    for i in range(len(totaly)):
        mean = np.mean(totaly[i])
        std = np.std(totaly[i],ddof=1)
        stdy = [mean+std,mean-std]
        ax.scatter(x=[i+1,i+1],y=stdy,color="tab:purple",marker="x")
    ax.set_ylabel("% of background")
    ax.set_ylim(ylims)

    plt.show()

 
def means(flightlist,y,outputfilename,file="flights_lookuptable.csv"): # takes a list of linenumbers of the flights from lookuptable

    #import flight-file
    raw_data = csv.reader(open(file),delimiter=",")
    data = list(raw_data)
    
    means = []
    
    for element in flightlist:
        element -= 1
        relobj = Pops(file=data[element][7],start=data[element][3],end=data[element][4],timecorr=int(data[element][10])) 
        pops = Pops(file=data[element][7],start=data[element][5],end=data[element][6],timecorr=int(data[element][10]),title=(data[element][0]+data[element][5]),relobj=relobj)
        
        means.append([pops.returnstats(y)[0],pops.returndata(y)])
       
    path = os.path.dirname(os.path.abspath(__file__))
    
    if not ".json" in outputfilename:
        outputfilename += ".json"
        
    if not os.path.exists(path + "/json"):
        os.makedirs(path + "/json")
        
    if not os.path.exists(path + "/json/" + y):
        os.makedirs(path + "/json/" + y)
        
    fullpath = path + "/json/" + y + "/" + outputfilename
    
    f = open(fullpath,"w")
    json.dump(means,f)
    f.close()