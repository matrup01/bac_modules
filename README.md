1.    pops.py:


1.1   Pops(file)

	creates a Pops-Object
	
	file (str) ... Takes a POPS-produced csv-file (eg '112233.csv')

	title (str,optional) ... Takes a str and uses it as a title for quickplots
	start (str,optional) ... Takes a str in 'hh:mm:ss'-format and only imports data acquired after that timestamp
	end (str,optional) ... Takes a str in 'hh:mm:ss'-format and only imports data acquired before that timestamp
	bgobj (Pops,optional) ... Takes another Pops-Object and corrects the data using the given Pops-Objects as Background
	box (bool,optional) ... Takes a Boolean to determine which file is given (True ... produced by the box;False ... produced by the POPS hooked to a laptop) default-True

1.2   Pops.internalbg(startmeasurementtime)

	shouldn't be used since there is the more flexible method to import a bgobj (see 1.1)
	takes data before startmeasurementtime-timestamp and treats it as bg to correct the data after it (crops bg in the process)

	startmeasurementtime (str) ... Takes a str in 'hh:mm:ss'-format and uses it to split the data from the bg

	bgcrop (int,optional) ... Takes an int and crops the start of the background by its amount seconds

1.3   Pops.externalbg(bgfile)

	shouldn't be used since there is the more flexible method to import a bgobj (see 1.1) and this function isn't compatible with data sampled using the POPS and a laptop
	takes data from another file and treats it as bg to correct the data from the Pops-object

	bgfile (str) ... Takes a POPS-produced csv-file (zB '112233.csv')

	startcrop (int,optional) ... Takes an int and crops the start of the background by its amount seconds
	endcrop (int,optional) ... Takes an int and crops the end of the background by its amount seconds 

1.4   Pops.exportbg()

	treats the data from the Pops-file as bg and returns the bg in the format [[ch0-ch15],total]
	can be used, however the method to import a bgobj (see 1.1) is better

1.5   Pops.importbg(bg)

	uses data in the format [[ch0-ch15],total] and corrects the Pops-objects data by it
	just use the method to import a bgobj, trust me it's better (see 1.1)

	bg (nested list of floats) ... Takes a list containing the data for bg-correction 

1.6   Pops.quickplot(y)

	draws a plot y vs time

	y (str) ... takes a string to determine which y should be plotted (for accepted strings see 1.16)

	startcrop (int, optional) ... Takes an int and crops the beginning of the plot by its amount seconds
	endcrop (int, optional) ... Takes an int and crops the end of the plot by its amount seconds

1.7   Pops.plot(ax,y)

	draws a plot y vs time on an existing matplotlib-axis

	ax (axis) ... takes a matplotlib-axis, on which the graph will be drawn
	y (str) ... takes a string to determine which y should be plotted (for accepted strings see 1.16)

	startcrop (int, optional) ... Takes an int and crops the beginning of the plot by its amount seconds
	endcrop (int, optional) ... Takes an int and crops the end of the plot by its amount seconds
	quakes (list of str, optional) ... takes a list of string in the format 'hh:mm:ss' and draws vertical, dashed lines at those timestamps
	quakeslabel (str, optional) ... takes a str and uses it as a label for the quakes if a legend is used
	quakecolor (str, optional) ... changes the color of the quakes, default-"tab:pink"
	color (str, optional) ... changes the color of the plot, default-"tab:blue"
	togglexticks (bool, optional) ... takes a boolean to decide if the x-ticks of ax should be visible, default-True
	printstats (bool, optional) ... takes a boolean to decide if mean, std and var of the plot should be printed to the console, default-False
	secondary (bool, optional) ... determines which y-axis should be colored (False-left axis/True-right axis), default-False

1.8   Pops.quickheatmap()

	draws a dndlogdp-heatmap over time 

	startcrop (int, optional) ... Takes an int and crops the beginning of the plot by its amount seconds
	endcrop (int, optional) ... Takes an int and crops the end of the plot by its amount seconds

1.9   Pops.heatmap(ax)

	draws a dndlogdp-heatmap over time on an existing matplotlib-axis

	startcrop (int, optional) ... Takes an int and crops the beginning of the plot by its amount seconds
	endcrop (int, optional) ... Takes an int and crops the end of the plot by its amount seconds
	togglexticks (bool, optional) ... takes a boolean to decide if the x-ticks of ax should be visible, default-True
	orientation (str, optional) ... takes a str to change the orientation of the colorbar, default-"horizontal"
	location (str, optional) ... takes a str to change the location of the colorbar relative to the plot, default-"top"
	
1.10  Pops.dndlogdp(ax)

	draws a barplot of dndlogdp-distribution on an existing matplotlib-axis

	ax (axis) ... takes a matplotlib-axis, on which the graph will be drawn

1.11  Pops.quickdndlogdp()

	draws a barplot of dndlogdp-distribution

1.12  Pops.cumulativeparticles()

	prints and returns the sum of the means of all bins
	no real usecase, was used before "total"-channel was implemented

1.13  Pops.crop(startcrop,endcrop)

	Shouldn't be used any more, use start and end in init (see 1.1)
	crops the data by startcrop seconds at the start and endrop seconds at the end

	startcrop (int) ... Takes an int and crops the beginning of the plot by its amount seconds
	endcrop (int) ... Takes an int and crops the end of the plot by its amount seconds

1.14  Pops.stats(y)

	prints mean, std and var of the given data to the console

	y (str) ... takes a string to determine which y should be plotted (for accepted strings see 1.16)

1.15  Pops.returnstats(y)

	return mean, std and var of the given data in the format [mean,std,var]

	y (str) ... takes a string to determine which y should be plotted (for accepted strings see 1.16)

1.16  Pops.findplot(y)

	matches the given str with the correct data and returns [xdata,ydata,label,ylabel]

	y (str) ... takes a string to determine which y should be plotted 

	Accepted strings: temp_bme680, rf_bme680, temp_sen55, rf_sen55, druck, gas, pm1, pm25, pm4, pm10, voc, nox, co2, tvoc, popstemp, boardtemp, total, every other str containing one of the numbers 0-15 will be interpreted as a bin

1.17  Pops.replacezeros(data)

	inputs data and replaces every 0 with the lowest value in the data
	is used to avoid blank spots in the heatmap, apart from that no reasonable usecase

	data (nested list of floats) ... input data array


2.    fluoreszenz.py


2.1   FData(file) 

	creates an FData-object

	file (str) ... takes an FSpec-produced csv-file

	title (str, optional) ... takes a str and uses it as a title for quickplots
	encoding_artifacts (bool, optional) ... takes a boolean to determine if there are encoding artifacts that need to be removed, default-True
	start (str,optional) ... takes a str in 'hh:mm:ss'-format and only imports data acquired after that timestamp
	end (str,optional) ... takes a str in 'hh:mm:ss'-format and only imports data acquired before that timestamp
	skiprows (int, optional) ... takes an int and skips the first rows (may be used if the first rows are corrupted), default-0

2.2   FData.internalbg(startmeasurementtime)

	takes data before startmeasurementtime-timestamp and treats it as bg to correct the data after it (crops bg in the process)

	startmeasurementtime (str) ... Takes a str in 'hh:mm:ss'-format and uses it to split the data from the bg

	bgcrop (int,optional) ... Takes an int and crops the start of the background by its amount datapoints

2.3   FData.externalbg(bgfile)

	takes data from another file and treats it as bg to correct the data from the FData-object

	bgfile (str) ... Takes a FSpec-produced csv-file

	startcrop (int,optional) ... Takes an int and crops the start of the background by its amount datapoints
	endcrop (int,optional) ... Takes an int and crops the end of the background by its amount datapoints

2.4   FData.quickplot(channelno)

	draws a plot of the intensity of the given channel vs time

	channelno (int) ... decides which channel should be plotted

	startcrop (int, optional) ... Takes an int and crops the beginning of the plot by its amount datapoints
	endcrop (int, optional) ... Takes an int and crops the end of the plot by its amount datapoints

2.5   FData.plot(channelno,ax)

	draws a plot of the intensity of the given channel vs time on an existing matplotlib-axis

	channelno (int) ... decides which channel should be plotted
	ax (axis) ... takes a matplotlib-axis, on which the graph will be drawn

	quakes (list of str, optional) ... takes a list of string in the format 'hh:mm:ss' and draws vertical, dashed lines at those timestamps
	quakeslabel (str, optional) ... takes a str and uses it as a label for the quakes if a legend is used
	quakecolor (str, optional) ... changes the color of the quakes, default-"tab:purple"
	color (str, optional) ... changes the color of the plot, default-"tab:green"
	startcrop (int, optional) ... Takes an int and crops the beginning of the plot by its amount datapoints
	endcrop (int, optional) ... Takes an int and crops the end of the plot by its amount datapoints

2.6   FData.crop(startcrop,endcrop)

	Shouldn't be used any more, use start and end in init (see 2.1)
	crops the data by startcrop datapoints at the start and endrop datapoints at the end

	startcrop (int) ... Takes an int and crops the beginning of the plot by its amount datapoints
	endcrop (int) ... Takes an int and crops the end of the plot by its amount datapoints


3.    ccs811.py


3.1   quickplot(file)

	draws a plot of tvoc and co2 vs time

	file (str) ... takes a ccs811-produced csv-file

3.2   plot(file,ax)

	draws a plot of tvoc vs time or co2 vs time on an existing matplotlib-axis

	file (str) ... takes a ccs811-produced csv-file
	ax (axis) ... takes a matplotlib-axis, on which the graph will be drawn

	plot (int, optional) ... if it's 1 tvoc will be drawn, else co2 will be drawn, default-1
	startcrop (int, optional) ... Takes an int and crops the beginning of the plot by its amount datapoints
	endcrop (int, optional) ... Takes an int and crops the end of the plot by its amount datapoints
	color (str, optional) ... changes the color of the plot, default-"tab:red"


4.    drone.py


4.1   Dronedata(file)

	creates a Dronedata-object

	file (str) ... takes a drone-produced csv-file

4.2   Dronedata.plot(ax)

	draws a plot of height vs time on an existing matplotlib-axis

	ax (axis) ... takes a matplotlib-axis, on which the graph will be drawn

	color (str, optional) ... changes the color of the plot, default-"tab:purple"
	secondary (bool, optional) ... determines which y-axis should be colored (False-left axis/True-right axis), default-False


5.    sen55.py



5.1   quickplot(file)

	draws a plot of pm1, pm2.5, pm4 and pm10 vs time

	file (str) ... takes a sen55-produced csv-file

5.2   plot(file,ax)

	draws a plot of a pm-value vs time on an existing matplotlib-axis

	file (str) ... takes a sen55-produced csv-file
	ax (axis) ... takes a matplotlib-axis, on which the graph will be drawn

	plot (int, optional) ... determines which graph will be drawn (1-pm1, 2-pm25, 3-pm4, else-pm10), default-1
	startcrop (int, optional) ... Takes an int and crops the beginning of the plot by its amount datapoints
	endcrop (int, optional) ... Takes an int and crops the end of the plot by its amount datapoints
	color (str, optional) ... changes the color of the plot, default-"tab:red"