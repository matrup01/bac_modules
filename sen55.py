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
    
    
def plot(file,ax,plot=1,startcrop=0,endcrop=0,color="tab:red"):
    
    #read data from csv to list
    data = csv.reader(open(file),delimiter=",")
    data = list(data)
    
    
    #extract x and y values from list
    t = [dt.datetime.strptime(data[i][1],"%H:%M:%S") for i in range(1+startcrop,len(data)-endcrop)]
    
    pm1 = [[float(data[i][6]) for i in range(1+startcrop,len(data)-endcrop)],"PM1",r'$\mu$g/$m^3$']
    pm25 = [[float(data[i][7]) for i in range(1+startcrop,len(data)-endcrop)],"PM2,5","$\mu$g/$m^3$"]
    pm4 = [[float(data[i][8]) for i in range(1+startcrop,len(data)-endcrop)],"PM4","$\mu$g/$m^3$"]
    pm10 = [[float(data[i][9]) for i in range(1+startcrop,len(data)-endcrop)],"PM10","$\mu$g/$m^3$"]
    
    if plot == 1:
        ax.plot(t,pm1[0],label=pm1[1],color=color)
        ax.set_ylabel(pm1[1] + " in " + pm1[2])
    elif plot == 2:
        ax.plot(t,pm25[0],label=pm25[1],color=color)
        ax.set_ylabel(pm25[1] + " in " + pm25[2])
    elif plot == 3:
        ax.plot(t,pm4[0],label=pm4[1],color=color)
        ax.set_ylabel(pm4[1] + " in " + pm4[2])
    else:
        ax.plot(t,pm10[0],label=pm10[1],color=color)
        ax.set_ylabel(pm10[1] + " in " + pm10[2])