import numpy as np
import matplotlib.dates as md
import datetime as dt
import csv
import matplotlib.pyplot as plt
import tikzplotlib



def quickplot(file):
    data = csv.reader(open(file),delimiter=",")
    data = list(data)
    
    
    t = [dt.datetime.strptime(data[i][1],"%H:%M:%S") for i in range(1,len(data)-2)]
    
    pm1 = [[float(data[i][6]) for i in range(1,len(data)-2)],"PM1",r'$\mu$g/$m^3$']
    pm25 = [[float(data[i][7]) for i in range(1,len(data)-2)],"PM2,5","$\mu$g/$m^3$"]
    pm4 = [[float(data[i][8]) for i in range(1,len(data)-2)],"PM4","$\mu$g/$m^3$"]
    pm10 = [[float(data[i][9]) for i in range(1,len(data)-2)],"PM10","$\mu$g/$m^3$"]
    
    fig,ax = plt.subplots()
    
    plt.title("SEN55")

    for element in [pm1,pm25,pm4,pm10]:
        ax.plot(t,element[0],label=element[1])
    ax.set_ylabel(pm1[2])
    ax.set_aspect("auto")
    ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    ax.legend()
    plt.show()
    
    
def plot(file,ax,plot,startcrop=0,endcrop=0,color="tab:red",plotlabel="none"):
    
    #read data from csv to list
    data = csv.reader(open(file),delimiter=",")
    data = list(data)
    
    
    #extract x and y values from list
    t = [dt.datetime.strptime(data[i][1],"%H:%M:%S") for i in range(1+startcrop,len(data)-endcrop)]
    
    finder = {
        "pm1" : 0,
        "pm25" : 1,
        "pm4" : 2,
        "pm10" : 3,
        "temp" : 4,
        "hum" : 5}
    
    y = [[[float(data[i][6]) for i in range(1+startcrop,len(data)-endcrop)],"PM1",r'$\mu$g/$m^3$'],
         [[float(data[i][7]) for i in range(1+startcrop,len(data)-endcrop)],"PM2,5","$\mu$g/$m^3$"],
         [[float(data[i][8]) for i in range(1+startcrop,len(data)-endcrop)],"PM4","$\mu$g/$m^3$"],
         [[float(data[i][9]) for i in range(1+startcrop,len(data)-endcrop)],"PM10","$\mu$g/$m^3$"],
         [[float(data[i][2]) for i in range(1+startcrop,len(data)-endcrop)],"temperature","°C"],
         [[float(data[i][3]) for i in range(1+startcrop,len(data)-endcrop)],"humidity","%"]]
    
    try:
        loc = finder[plot]
        yy = y[loc]
    except:
        print("invalid plottype, plot has to be one of the following: pm1,pm25,pm4,pm10,temp,hum")
        return
    
    if plotlabel != "none":
        label = plotlabel
    else: label = yy[1]
    
    ax.plot(t,yy[0],label=label,color=color)
    ax.set_ylabel(yy[1] + " in " + yy[2])
