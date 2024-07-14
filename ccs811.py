import numpy as np
import matplotlib.dates as md
import datetime as dt
import csv
import matplotlib.pyplot as plt
import tikzplotlib


class CCS811:
    
    def __init__(self,file,start="none",end="none",title="no title"):
        
        #init
        self.title = title
        
        #read data from csv to list
        data = csv.reader(open(file),delimiter=",")
        data = list(data)
        
        #extract x and y values from list
        self.t = [dt.datetime.strptime(data[i][1],"%H:%M:%S") for i in range(1,len(data))]
        
        self.finder = {"tvoc" : 0,
                       "co2": 1}
        
        self.y = [[[float(data[i][2]) for i in range(1,len(data))],"TVOC","ppb"],
                  [[float(data[i][3]) for i in range(1,len(data))],r"$CO_2$","ppm"]]
        
        #crop
        if start != "none":
            indices = []
            for i in range(len(self.t)):
                if dt.datetime.strptime(start,"%H:%M:%S") <= self.t[i]:
                    indices.append(i)
            start_i = indices[0]
        else: start_i = 0
        
        if end != "none":
            indices = []
            for i in range(len(self.t)):
                if dt.datetime.strptime(end,"%H:%M:%S") >= self.t[i]:
                    indices.append(i)
            end_i = len(indices)
        else: end_i = len(self.t)
        
        self.t = [self.t[i] for i in range(start_i,end_i)]
        for i in range(len(self.y)):
            self.y[i] = [self.y[i][j] for j in range(start_i,end_i)]
            
            
    def findplot(self,y):
        
        try:
            loc = self.finder[y]
            yy = self.y[loc]
        except:
            raise ValueError("Invalid plottype: plot has to be one of the following strings: pm1,pm25,pm4,pm10,temp,hum")
            
        return yy
    
    
    def quickplot(self):
        
        fig,ax = plt.subplots()
        plt.title(self.title)

        ax.plot(self.t,self.y[0][0])
        ax.set_ylabel = self.y[0][1] + " in " + self.y[0][2]
        
        plt.show()
        
        
    def plot(self,ax,y,color="tab:brown",secondary=False):
        
        #get plotdata
        yy = self.findplot(y)
        
        #draw plot
        ax.plot(self.t,yy[0],color=color)
        ax.set_ylabel = yy[1] + " in " + yy[2]
        ax.axes.yaxis.label.set_color(color)
        ax.tick_params(axis='y', colors=color)
        if not secondary:
            ax.spines["left"].set_color(color)
        else:
            ax.spines["right"].set_color(color)
            ax.spines["left"].set_alpha(0)


def quickplot(file): #legacy function; use CCS811-Object instead
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
    
    
def plot(file,ax,plot=1,startcrop=0,endcrop=0,color="tab:red",plotlabel="none"): #legacy function; use CCS811-Object instead
    
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