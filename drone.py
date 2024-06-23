import csv
import datetime as dt

class Dronedata:
    
    
    def __init__(self,file):
        
        data = csv.reader(open(file),delimiter=",")
        data = list(data)
        
        self.t = [dt.datetime.strptime(data[i][1].replace(",","."),"%I:%M:%S.%f %p") for i in range(1,len(data))]
        self.height = [float(data[i][6].replace(",",".")) for i in range(1,len(data))]
        
        
    def plot(self,ax,color="tab:purple",secondary=False):
        
        ax.plot(self.t,self.height,label="Drone height",color=color)
        ax.set_ylabel("height in m")
        ax.axes.yaxis.label.set_color(color)
        ax.tick_params(axis='y', colors=color)
        if not secondary:
            ax.spines["left"].set_color(color)
        else:
            ax.spines["right"].set_color(color)
            ax.spines["left"].set_alpha(0)
        
        
test = Dronedata("Day2-Flight1_DJIFlightRecord_2024-06-12_11-06-18-aircraft.csv")