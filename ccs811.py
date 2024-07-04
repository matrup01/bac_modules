import numpy as np
import matplotlib.dates as md
import datetime as dt
import csv
import matplotlib.pyplot as plt
import tikzplotlib



def quickplot(file):
    data = csv.reader(open(file),delimiter=",")
    data = list(data)
    
    
    t = [dt.datetime.strptime(data[i][1],"%H:%M:%S") for i in range(1,len(data))]
    
    tvoc = [[float(data[i][2]) for i in range(1,len(data))],"TVOC","ppb"]
    co2 = [[float(data[i][3]) for i in range(1,len(data))],r"$CO_2$","ppm"]
    
    fig,ax = plt.subplots()
    
    plt.title("CCS811")

    for element in [tvoc,co2]:
        ax.plot(t,element[0],label=element[1])
    ax.set_ylabel("einheiten falsch")
    ax.set_aspect("auto")
    ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    ax.legend()
    plt.show()
    
    
def plot(file,ax,plot=1,startcrop=0,endcrop=0,color="tab:red",plotlabel="none"):
    
    #read data from csv to list
    data = csv.reader(open(file),delimiter=",")
    data = list(data)
    
    #fix label
    if plotlabel == "none":
        label = ["TVOC",r"$CO_2$"]
    else: label = [plotlabel,plotlabel]
    
    
    #extract x and y values from list
    t = [dt.datetime.strptime(data[i][1],"%H:%M:%S") for i in range(1+startcrop,len(data)-endcrop)]
    
    tvoc = [[float(data[i][2]) for i in range(1+startcrop,len(data)-endcrop)],label[0],"ppb"]
    co2 = [[float(data[i][3]) for i in range(1+startcrop,len(data)-endcrop)],label[1],"ppm"]
    
    if plot == 1:
        ax.plot(t,tvoc[0],label=tvoc[1],color=color)
        ax.set_ylabel("TVOC in " + tvoc[2])
    else:
        ax.plot(t,co2[0],label=co2[1],color=color)
        ax.set_ylabel(r"$CO_2$" + " in " + co2[2])