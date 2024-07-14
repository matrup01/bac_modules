import csv
import datetime as dt
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.dates as md
from matplotlib.colors import LogNorm
from copy import copy

class Pops:
    
    """full documentation see https://github.com/matrup01/bac_modules \n 
    file (str) ... Takes a POPS-produced csv-file (zB '112233.csv') \n
    title (str,optional) ... Takes a str and uses it as a title for quickplots \n
    start (str,optional) ... Takes a str in 'hh:mm:ss'-format and only imports data acquired after that timestamp \n
    end (str,optional) ... Takes a str in 'hh:mm:ss'-format and only imports data acquired before that timestamp \n
    bgobj (Pops,optional) ... Takes another Pops-Object and corrects the data using the given Pops-Objects as Background \n
    box (bool,optional) ... Takes a Boolean to determine which file is given (True ... produced by the box;False ... produced by the POPS hooked to a laptop) default-True"""
    
    def __init__(self,file,title="Kein Titel",start="none",end="none",bgobj="none",box=True):

        #save data
        self.filename = file
        self.title = title
        self.d_categories = [element * 1000 for element in [0.115,0.125,0.135,0.15,0.165,0.185,0.21,0.25,0.35,0.475,0.575,0.855,1.220,1.53,1.99,2.585,3.37]]
        
        #reads data from csv to list
        data = csv.reader(open(file),delimiter=",")
        data = list(data)
        
        #deletes last row if it hasnt been written completely
        if len(data[0]) > len(data[-1]):
            data = [data[i] for i in range(len(data)-1)]
        
        #extract x and y values from list
        if box:
            self.popstime = [dt.datetime.strptime("00:00:00","%H:%M:%S")-dt.timedelta(0,23)+dt.timedelta(0,7200)+dt.timedelta(0,float(data[i][23])) for i in range(1,len(data))]
            self.t = [dt.datetime.strptime(data[i][1],"%H:%M:%S") for i in range(1,len(data))]
        else:
            self.popstime = [dt.datetime.strptime("00:00:00","%H:%M:%S")-dt.timedelta(0,23)+dt.timedelta(0,7200)+dt.timedelta(0,float(data[i][0])) for i in range(1,len(data))]
            self.t = self.popstime
        
        self.ydata = [[float(data[i][j]) for i in range(1,len(data))]for j in [2,3,11,10,4,5,6,7,8,9,12,13,14,15]]
            #ydata-Syntax: [temp_bm680,rf_bm680,temp_sen55,rf_sen55,druck,gas,pm1,pm25,pm4,pm10,voc,nox,co2,tvoc]
            #ydata2-Syntax: [total,popstemp,boardtemp]
        if box:
            self.pops_bins_raw = [[float(data[i][j]) for i in range(1,len(data))]for j in [56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71]]
            self.pops_bins = [[self.pops_bins_raw[j][i] / float(data[i+1][38]) for i in range(len(data)-1)] for j in range(len(self.pops_bins_raw))]
            self.ydata2 = [[float(data[i][j]) for i in range(1,len(data))] for j in [28,43,34]]
        else:
            self.pops_bins_raw = [[float(data[i][j]) for i in range(1,len(data))]for j in [33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48]]
            self.pops_bins = [[self.pops_bins_raw[j][i] / float(data[i+1][15]) for i in range(len(data)-1)] for j in range(len(self.pops_bins_raw))]
            self.ydata2 = [[float(data[i][j]) for i in range(1,len(data))] for j in [5,20,11]]
        
        #crop
        if start != "none":
            tcounter = -1
            for element in [data[i][1] for i in range(1,len(data))]:
                tcounter += 1
                if start == element:
                  t_start = tcounter
            popscounter = -1
            unixstart = str(int(start[0:2])*3600+int(start[3:5])*60+int(start[6:8])-7177)
            for element in [data[i][23][0:5] for i in range(1,len(data))]:
                popscounter += 1
                if unixstart == element:
                    pops_start = popscounter
        else:
            t_start = 0
            pops_start = 0
            
        if end != "none":
            tcounter = -1
            for element in [data[i][1] for i in range(1,len(data))]:
                tcounter += 1
                if end == element:
                  t_end = tcounter
            popscounter = -1
            unixend = str(int(end[0:2])*3600+int(end[3:5])*60+int(end[6:8])-7177)
            for element in [data[i][23][0:5] for i in range(1,len(data))]:
                popscounter += 1
                if unixend == element:
                    pops_end = popscounter
        else:
            t_end = len(data)-1
            pops_end = len(data)-1
            
        self.t = [self.t[i] for i in range(t_start,t_end)]
        self.popstime = [self.popstime[i] for i in range(pops_start,pops_end)]
        for i in range(len(self.ydata2)):
            self.ydata2[i] = [self.ydata2[i][j] for j in range(pops_start,pops_end)]
        for i in range(len(self.ydata)):
            self.ydata[i] = [self.ydata[i][j] for j in range(t_start,t_end)]
        for i in range(len(self.pops_bins)):
            self.pops_bins[i] = [self.pops_bins[i][j] for j in range(pops_start,pops_end)]
            
        #correctbg
        if type(bgobj) == Pops:
            self.importbg(bgobj.exportbg())
        
    def internalbg(self,startmeasurementtime,bgcrop=0):
        
        #find point in list where measurement starts
        for i in range(len(self.t)):
            if str(self.t[i])[11:19].rsplit(".")[0] == startmeasurementtime:
                startmeasurement = i
        
        #correct bg
        for i in range(len(self.pops_bins)):
            correctorarray = np.array([self.pops_bins[i][j] for j in range(bgcrop,startmeasurement)])
            corrector = np.mean(correctorarray)
            self.pops_bins[i] = np.array([self.pops_bins[i][j]-corrector for j in range(startmeasurement,len(self.t))])
        self.t = [self.t[i] for i in range(startmeasurement,len(self.ydata[0]))]
        
        
    def externalbg(self,bgfile,startcrop=0,endcrop=0):
        
        #reads data from csv to list
        data = csv.reader(open(bgfile),delimiter=";")
        data = list(data)
        
        #extract data from list
        bgdata_raw = [[int(data[i][j])-1000 for i in range(1+startcrop,len(data)-endcrop)] for j in range(56,72)]
        bgdata = np.array([[bgdata_raw[j][i] / float(data[i+1+startcrop][len(data)-endcrop]) for i in range(len(data)-1)] for j in range(len(bgdata_raw))])
        bg = np.array([np.mean(element) for element in bgdata])
        
        #correct bg
        for i in range(len(self.pops_bins)):
            self.pops_bins[i] = [self.pops_bins[i][j]-bg for j in range(len(self.pops_bins[i]))]
            
            
    def exportbg(self):
        
        bins = np.array(self.pops_bins)
        bg = np.array([np.mean(element) for element in bins])
        totalbg = np.mean(np.array(self.ydata2[0]))
        return [bg,totalbg]
    
    
    def importbg(self,bg):
        
        for i in range(len(self.pops_bins)):
            self.pops_bins[i] = [self.pops_bins[i][j]-bg[0][i] for j in range(len(self.pops_bins[i]))]
        self.ydata2[0] = [self.ydata2[0][i] - bg[1] for i in range(len(self.ydata2[0]))]
        
        
    def quickplot(self,y,startcrop=0,endcrop=0):
        
        #find plotdata
        plotx,ploty,label,ylabel = self.findplottype(y)
        plotx = [plotx[i] for i in range(startcrop,len(plotx)-endcrop)]
        ploty = [ploty[i] for i in range(startcrop,len(ploty)-endcrop)]
            
        #draw plot
        fig,ax = plt.subplots()
        ax.plot(plotx,ploty,label=label)
        ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
        ax.set_ylabel(ylabel)
        plt.title(self.title)
        plt.legend()
        plt.show()
        
        
    def plot(self,ax,y,startcrop=0,endcrop=0,quakes=[],quakeslabel="kein Label",quakecolor="tab:pink",color="tab:blue",togglexticks=True,printstats=False,secondary=False,plotlabel="none"):
        
        #find plotdata
        plotx,ploty,label,ylabel = self.findplottype(y)
        plotx = [plotx[i] for i in range(startcrop,len(plotx)-endcrop)]
        ploty = [ploty[i] for i in range(startcrop,len(ploty)-endcrop)]
        
        #change label
        if plotlabel != "none":
            legendlabel = plotlabel
        else: legendlabel = label
        
        #draw plot
        ax.plot(plotx,ploty,label=legendlabel,color=color)
        ax.set_ylabel(label + " in " + ylabel)
        ax.axes.xaxis.set_visible(togglexticks)
        ax.axes.yaxis.label.set_color(color)
        ax.tick_params(axis='y', colors=color)
        if not secondary:
            ax.spines["left"].set_color(color)
        else:
            ax.spines["right"].set_color(color)
            ax.spines["left"].set_alpha(0)
        if len(quakes) != 0:
            ax.vlines(x=[dt.datetime.strptime(element, "%H:%M:%S")for element in quakes],ymin=min(ploty),ymax=max(ploty),color=quakecolor,ls="dashed",label=quakeslabel)
        
        #print stats
        if printstats:
            mean = np.mean(ploty)
            std = np.std(ploty,ddof=1)
            var = np.var(ploty,ddof=1)
            print(label + " (mean,std,var): " + str(mean) + ", " + str(std) + ", " + str(var))
        
    
    def quickheatmap(self,startcrop=0,endcrop=0):
        
        #convert to heatmapdata
        heatmapdata = [[self.pops_bins[j][i] / (math.log10(self.d_categories[j+1])-math.log10(self.d_categories[j])) for i in range(len(self.pops_bins[0])-1)] for j in range(len(self.pops_bins))]
        heatmapdata = self.replacezeros(heatmapdata)
        xx,yy = np.meshgrid(self.popstime,self.d_categories)
        
        #draw plot
        fig,ax = plt.subplots()
        im = ax.pcolormesh(xx,yy,heatmapdata,cmap="rainbow",norm=LogNorm())
        ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
        ax.set_yscale("log")
        ax.set_ylabel("Durchmesser in nm")
        plt.colorbar(im,ax=ax,label="dN/dlogdp")
        plt.show()
        
        
    def heatmap(self,ax,startcrop=0,endcrop=0,togglexticks=True,orientation="horizontal",location="top",togglecbar=True):
        
        #convert to heatmapdata
        heatmapdata = [[self.pops_bins[j][i] / (math.log10(self.d_categories[j+1])-math.log10(self.d_categories[j])) for i in range(len(self.pops_bins[0])-1)] for j in range(len(self.pops_bins))]
        heatmapdata = self.replacezeros(heatmapdata)
        xx,yy = np.meshgrid(self.popstime,self.d_categories)
        
        mask = np.array([[xx[i][j] for j in range(len(xx[i])-1)] for i in range(len(xx)-1)])
        
        heatmapdata = np.ma.masked_array(heatmapdata,mask<min(self.popstime))
        heatmapdata = np.ma.masked_array(heatmapdata,mask>max(self.popstime))
        
        #draw plot
        im = ax.pcolormesh(xx,yy,heatmapdata,cmap="RdYlBu_r",norm=LogNorm(vmin=1,vmax=10000))
        ax.set_yscale("log")
        ax.set_ylabel("Durchmesser in nm")
        ax.axes.xaxis.set_visible(togglexticks)
        if togglecbar:
            plt.colorbar(im,ax=ax,label="dN/dlogdp",orientation=orientation,location=location)
        
        #return xx,yy,heatmapdata
        
    def dndlogdp(self,ax):
        
        #calculate needed values
        means = np.array([np.mean(self.pops_bins[i]) for i in range(len(self.pops_bins))])
        dndlogdp = [means[i]/(math.log10(self.d_categories[i+1]-math.log10(self.d_categories[i]))) for i in range(len(means))]
        xvals = [self.d_categories[i] for i in range(len(means))]
        widths = [self.d_categories[i+1]-self.d_categories[i] for i in range(len(xvals))]
        
        #draw plot
        ax.bar(x=xvals,width=widths,align="edge",height=dndlogdp)
        ax.set_yscale("log")
        ax.set_ylabel("dN/dlog$D_p$")
        ax.set_xscale("log")
        ax.set_xlabel("$D_p$ in nm")
        
        
    def quickdndlogdp(self):
        
        #calculate needed values
        means = np.array([np.mean(self.pops_bins[i]) for i in range(len(self.pops_bins))])
        dndlogdp = [means[i]/(math.log10(self.d_categories[i+1]-math.log10(self.d_categories[i]))) for i in range(len(means))]
        xvals = [self.d_categories[i] for i in range(len(means))]
        widths = [self.d_categories[i+1]-self.d_categories[i] for i in range(len(xvals))]
        
        print(self.title)
        print(*dndlogdp)
        
        #draw
        fig,ax = plt.subplots()
        ax.bar(x=xvals,width=widths,align="edge",height=dndlogdp)
        ax.set_yscale("log")
        ax.set_ylabel("dN/dlog$D_p$")
        ax.set_xscale("log")
        ax.set_xlabel("$D_p$ in nm")
        plt.title(self.title)
        plt.show()
        
        
    def cumulativeparticles(self):
        
        #calculate needed values
        means = np.array([np.mean(self.pops_bins[i]) for i in range(len(self.pops_bins))])
        cparticles = np.sum(means)
        print(self.title + ": " + str(cparticles) + " counts/cm3 (cumulative)")
        
        return cparticles
        
    
    def crop(self,startcrop,endcrop):
        length = len(self.t)
        self.t = [self.t[i] for i in range(startcrop,length-endcrop)]
        self.popstime = [self.popstime[i] for i in range(startcrop,length-endcrop)]
        for i in range(len(self.ydata)):
            self.ydata[i] = [self.ydata[i][j] for j in range(startcrop,length-endcrop)]
        for i in range(len(self.pops_bins)):
            self.pops_bins[i] = [self.pops_bins[i][j] for j in range(startcrop,length-endcrop)]
        for i in range(len(self.ydata2)):
            self.ydata2[i] = [self.ydata2[i][j] for j in range(startcrop,length-endcrop)]
        
        
        
    def stats(self,y):
        
        placeholder1,data,label,unit = self.findplottype(y)
        mean = np.mean(data)
        std = np.std(data,ddof=1)
        var = np.var(data,ddof=1)
        print(label + " in " + unit + " (mean,std,var): " + str(mean) + ", " + str(std) + ", " + str(var))
    
        
    def returnstats(self,y):
        
        placeholder1,data,label,unit = self.findplottype(y)
        mean = np.mean(data)
        std = np.std(data,ddof=1)
        var = np.var(data,ddof=1)
        
        return mean,std,var
    
    
    def append(self,obj):
        
        for i in obj.popstime:
            self.popstime.append(i)
            
        for i in obj.t:
            self.t.append(i)
            
        for i in range(len(self.ydata)):
            for j in obj.ydata[i]:
                self.ydata[i].append(j)
                
        for i in range(len(self.ydata2)):
            for j in obj.ydata2[i]:
                self.ydata2[i].append(j)
                
        for i in range(len(self.pops_bins)):
            for j in obj.pops_bins[i]:
                self.pops_bins[i].append(j)
                
                
    def add(self,obj):
                    
        newpops = Pops(file=self.filename)
        newpops.t = copy(self.t)
        newpops.popstime = copy(self.popstime)
        newpops.ydata = copy(self.ydata)
        newpops.ydata2 = copy(self.ydata2)
        
        for i in obj.popstime:
            newpops.popstime.append(i)
            
        for i in obj.t:
            newpops.t.append(i)
            
        for i in range(len(newpops.ydata)):
            for j in obj.ydata[i]:
                newpops.ydata[i].append(j)
                
        for i in range(len(newpops.ydata2)):
            for j in obj.ydata2[i]:
                newpops.ydata2[i].append(j)
                
        for i in range(len(newpops.pops_bins)):
            for j in obj.pops_bins[i]:
                newpops.pops_bins[i].append(j)
                
        return newpops
                
        
        
    def findplottype(self,y):
        
        plottypes = [["temp_bm680","temperature (bm680)","°C"],["hum_bm680","rel. humidity (bm680)","%"],["temp_sen55","temperature (sen55)","°C"],["hum_sen55","rel. humidity (sen55)","%"],["druck","Luftdruck","hPa"],["gas","Gaswiderstand",r"$\Ohm$"],["pm1","PM1.0",r"$\mu$g/$m^3$"],["pm25","PM2.5",r"$\mu$g/$m^3$"],["pm4","PM4.0",r"$\mu$g/$m^3$"],["pm10","PM10.0",r"$\mu$g/$m^3$"],["voc","VOC-Index",""],["nox",r"$NO_X$-Index",""],["co2",r"$CO_2$","ppm"],["tvoc","TVOC","ppb"]]
        
        #find correct plottype
        for i in range(len(plottypes)):
            if plottypes[i][0] == y:
                plotx = self.t
                ploty = self.ydata[i]
                label = plottypes[i][1]
                ylabel = plottypes[i][2]
                
                return plotx,ploty,label,ylabel
            
        plottypes2 = [["total","sum of all bins",r"Counts/$cm^3$"],["popstemp","temperature inside POPS-box","°C"],["boardtemp","boardtemp","°C"]]
        
        for i in range(len(plottypes2)):
            if y == plottypes2[i][0]:
                plotx = self.popstime
                ploty = self.ydata2[i]
                label = plottypes2[i][1]
                ylabel = plottypes2[i][2]
            
                return plotx,ploty,label,ylabel
            
        for i in range(16):
            if "".join([char for char in y if char.isdigit()]) == str(i):
                plotx = self.popstime
                ploty = self.pops_bins[i]
                label = "b" + str(i)
                ylabel = r"Counts/$cm^3$"
                
                return plotx,ploty,label,ylabel
            
        output = "Unknown y: y must be one of the following strings: " + "".join([plottypes[i][0]+", " for i in range(len(plottypes))])
        output += "".join(["b"+str(i)+", " for i in range(15)])
        output += "b15"
        
        raise ValueError(output)
        
        
    def replacezeros(self,data):
        smallest = 10000
        for element in data:
            for i in range(len(element)):
                if element[i] < smallest and element[i] > 0:
                    smallest = element[i]
        for element in data:
            for i in range(len(element)):
                if element[i] <= 0:
                    element[i] = smallest
        return data