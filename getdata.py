from pops import Pops
from sen55 import SEN55
from ccs811 import CCS811
import csv

def getdata(day=["*"],height=["*"],loc=["*"],pops=True,sen55=False,ccs811=False,file="flights_lookuptable.csv"):
    
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
                
    #mask out flights that dont meet criteria
    data = []
    for dat,decider in zip(raw_data,mask):
        if decider == 1:
            data.append(dat)
                
    #create Pops-Objects
    if pops:
        popsout = [Pops(file=data[i][7],start=data[i][5],end=data[i][6],timecorr=int(data[i][10]),relobj=Pops(file=data[i][7],start=data[i][3],end=data[i][4],timecorr=int(data[i][10]))) for i in range(len(data))]
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
