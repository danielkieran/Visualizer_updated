# import libraries

# import tkinter as tk
# import numpy as np
# import pandas as pd
# import matplotlib
# matplotlib.use("TkAgg") 
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk #backend of matplotlib
# from matplotlib.figure import Figure
# import matplotlib.animation as animation
from __future__ import print_function
from Visualizer_functions import *
from tkinter import ttk
import os
from csv import writer
from PIL import ImageTk, Image
from pathlib import Path
##Global variables
live_type = "Humidity"
live_sensor = 1
f = Figure(figsize = (5,3), dpi = 100)
a = f.add_subplot(111)
# lna, = a.plot([], [], color='red', lw = 5)


#Additional code for the graph in home page
home_type = 'Mean'
home_type2 = 'Humidity'
f2 = Figure(figsize = (11,6), dpi = 100)
b = f2.add_subplot(111)
# lnb, = b.plot([], [],color ='green', lw = 5)



## Function that updates the graph every second
def animate(i):

    a.clear()
    # b.clear()# clears the subplots of the previous update
    sensor = live_sensor # copies the global variable
    sensor_folder = Path('generated_data/')
    s = "sensor_id_" + str(sensor) + ".csv"
    df = pd.read_csv(sensor_folder / s) # create dataframe
    df['time_of_transmission'] = df['time_of_transmission'].astype('float64') 
    df['time_as_date'] = np.array(df["time_of_transmission"]).astype("datetime64[s]") 
    df['time_as_date']  = df['time_as_date'] + timedelta(days=12476)
    time_dates = (df['time_as_date']).tolist() # creates list of times in dateformat

    if (live_type == 'Humidity'): # live_type is global variable
        a.plot_date(time_dates, df["hum_value"], 'b.-', label ="Humididty")
        title = 'Live humidity of sensor ' + str(sensor) + '\nstd  = ' + str(round(df["hum_value"].std(),2))+ ', mean = ' + str(round(df["hum_value"].mean(),1)) + '%'
        a.set_title(title)
        a.set_ylabel('%', rotation = 0,  fontsize = 15, labelpad = 15) #latest measurement
        a.set_xlabel('Date', fontsize = 10, labelpad = 10)
        a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0) #legend placement
       
    elif(live_type == 'Temperature'):  #live_type is global variable
        a.plot_date(time_dates, df["tem_value"], 'r.-', label ="Temperature")
        title = 'Live temperature of sensor ' + str(sensor) + '\nstd  = ' + str(round(df["tem_value"].std(),2)) + ', mean = ' + str(round(df["tem_value"].mean(),1)) + '°C' # latest measurement
        a.set_title(title)
        a.set_ylabel('°C', rotation = 0, fontsize = 15, labelpad = 15)
        a.set_xlabel('Date', fontsize = 10, labelpad = 10)
        a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0) #legend placement

    elif(live_type == 'Energy-Level'): #live_type is global variable
        a.plot_date(time_dates, df["energy_level"], 'g.-', label ="Energy-level")
        title = 'Live energy-level of sensor ' + str(sensor) + '\nstd  = ' + str(round(df["energy_level"].std(),2)) + ', mean = ' + str(round(df["energy_level"].mean(),2)) + 'V' #latest measurement

        a.set_title(title)
        a.set_ylabel('V', fontsize = 15, labelpad = 15)
        a.set_xlabel('Date', fontsize = 10, labelpad = 10)
        a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0) #legend placement
    

   
def animate2(i):
    b.clear()
    all_sensor_data = pd.DataFrame()
    sensor_folder = Path('generated_data/')
    files = [file for file in os.listdir(sensor_folder) if not file.startswith('.')] # Ignore hidden files
    for file in files:
        dframe = pd.read_csv(sensor_folder / file)
        all_sensor_data = pd.concat([all_sensor_data, dframe]) 
    all_sensor_data['time_of_transmission'] = all_sensor_data['time_of_transmission'].astype('float64') 
    all_sensor_data['time_as_date'] = np.array(all_sensor_data["time_of_transmission"]).astype("datetime64[s]") 
    all_sensor_data['time_as_date']  = all_sensor_data['time_as_date'] + timedelta(days=12476)   
    all_sensor_data = all_sensor_data.sort_values(by = 'time_as_date', ascending = True)

    #collect global variables
    global home_type
    global home_type2 

    # df2bis.set_index('dateObs', inplace=True)
    # df2bis.index = pd.to_datetime(df2bis.index)
    # df2bis.plot()

    if (home_type == 'Mean'):
        mean_data = all_sensor_data.resample('6H', on = 'time_as_date').mean()
        mean_data = mean_data.reset_index()
        grouped_time_dates = (mean_data['time_as_date']).tolist()
        if(home_type2 == 'Humidity'):
            b.plot_date(grouped_time_dates, mean_data['hum_value'], 'b.-', label ="Humidity")
            titl = 'Mean humidity of network over time' 
            b.set_title(titl)
            b.set_ylabel('%', rotation = 0, fontsize = 15, labelpad = 15)
            b.set_xlabel('Date', fontsize = 10, labelpad = 10)
            b.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0) #legend placement

        elif(home_type2 == 'Temperature'):
            b.plot_date(grouped_time_dates, mean_data['tem_value'], 'r.-', label ="Temperature")
            titl = 'Mean temperature of network over time' 
            b.set_title(titl)
            b.set_ylabel('°C', rotation = 0, fontsize = 15, labelpad = 15)
            b.set_xlabel('Date', rotation = 0, fontsize = 10, labelpad = 10)
            b.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0) #legend placement

        elif(home_type2 == 'Energy-Level'):
            b.plot_date(grouped_time_dates, mean_data['energy_level'], 'g.-', label ="Energy-Level")
            titl = 'Mean energy-level of network over time' 
            b.set_title(titl)
            b.set_ylabel('V', rotation = 0, fontsize = 15, labelpad = 15)
            b.set_xlabel('Date', rotation = 0, fontsize = 10, labelpad = 10)
            b.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0) #legend placement
    
    elif (home_type == 'Median'):
        median_data = all_sensor_data.resample('6H', on = 'time_as_date').median()
        median_data = median_data.reset_index()
        grouped_time_dates = (median_data['time_as_date']).tolist() 
        if(home_type2 == 'Humidity'):
            b.plot_date(grouped_time_dates, median_data['hum_value'], 'b.-', label ="Humidity")
            titl = 'Median humidity of network over time' 
            b.set_title(titl)
            b.set_ylabel('%', rotation = 0, fontsize = 15, labelpad = 15)
            b.set_xlabel('Date', rotation = 0, fontsize = 10, labelpad = 10)
            b.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0) #legend placement

        elif(home_type2 == 'Temperature'):
            b.plot_date(grouped_time_dates, median_data['tem_value'], 'r.-', label ="Temperature")
            titl = 'Median temperature of network over time' 
            b.set_title(titl)
            b.set_ylabel('°C', rotation = 0, fontsize = 15, labelpad = 15)
            b.set_xlabel('Date', rotation = 0, fontsize = 10, labelpad = 10)
            b.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0) #legend placement

        elif(home_type2 == 'Energy-Level'):
            b.plot_date(grouped_time_dates, median_data['energy_level'], 'g.-', label ="Energy-level")
            titl = 'Median energy-level of network over time' 
            b.set_title(titl)
            b.set_ylabel('V', rotation = 0, fontsize = 15, labelpad = 15)
            b.set_xlabel('Date', rotation = 0, fontsize = 10, labelpad = 10)
            b.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0) #legend placemement

    elif (home_type == 'Std'):
        std_data = all_sensor_data.resample('6H', on = 'time_as_date').std()
        std_data = std_data.reset_index()
        grouped_time_dates = (std_data['time_as_date']).tolist() 

        if(home_type2 == 'Humidity'):
            b.plot_date(grouped_time_dates, std_data['hum_value'], 'b.-', label ="Humidity")
            titl = 'Standard deviation of humidity in network' 
            b.set_title(titl)
            b.set_ylabel(' ', rotation = 0, fontsize = 15, labelpad = 15)
            b.set_xlabel('Date', rotation = 0, fontsize = 10, labelpad = 10)
            b.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0) #legend placement

        elif(home_type2 == 'Temperature'):
            b.plot_date(grouped_time_dates, std_data['tem_value'], 'r.-', label ="Temperature")
            titl = 'Standard deviation of temperature in network' 
            b.set_title(titl)
            b.set_ylabel(' ', rotation = 0, fontsize = 15, labelpad = 15)
            b.set_xlabel('Date',  fontsize = 10, labelpad = 10)
            b.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0) #legend placement

        elif(home_type2 == 'Energy-Level'):
            b.plot_date(grouped_time_dates, std_data['energy_level'], 'g.-', label ="Energy-level")
            titl = 'Standard deviation of energy-level in network' 
            b.set_title(titl)
            b.set_ylabel(' ', rotation = 0, fontsize = 15, labelpad = 15)
            b.set_xlabel('Date',  fontsize = 10, labelpad = 10)
            b.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0) #legend placemement
        
   

## Starting page of the program
class BeginPage(tk.Frame):

    def __init__(self, parent, controller):
        #parent here would be 'Application class'
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Welcome to the Visualizer program", font = 'Arial 20 bold')
        label.pack(side = tk.TOP, padx = 10, pady = 10)
        label2 = tk.Label(self, text = "This project was undertaken for the 4E2 Electronic Engineering Project. \nSome sections of the program are incomplete and is still being updated.\n This program is an updated version that can be used with MacOS, Linux and Windows \nwith additional graphical features", font = 'Calibri 9')
        label2.pack(padx = 10, pady = 20)
        button = tk.ttk.Button(self, text = "Agree", command=lambda: controller.show_frame(MainPage))
        button.pack(padx = 10, pady = 5)
        button_disagree = tk.ttk.Button(self, text = "Disagree", command = quit)
        button_disagree.pack(padx = 10, pady = 5)

        #canvas attribute required for each class
        self.canvas = FigureCanvasTkAgg(f2, self)
        

## Menu for the user to pick how many sensors to plot for multipage
class MultiPage(tk.Frame):

    def __init__(self, parent, controller):
        #parent here would be 'Application class'
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Enter the number of plots to make on the graph", font = 'times 20 bold')
        label.pack(side = tk.TOP, padx = 10, pady = 10)
        label2 = tk.ttk.Button(self, text = "2", command=lambda: controller.show_frame(Multi_Graph_2))
        label2.pack(padx = 10, pady = 10)
        button = tk.ttk.Button(self, text = "3", command=lambda: controller.show_frame(Multi_Graph_3))
        button.pack(padx = 10, pady = 10)
        button_disagree = tk.ttk.Button(self, text = "4", command=lambda: controller.show_frame(Multi_Graph_4))
        button_disagree.pack(padx = 10, pady = 10)

        #canvas attribute required for each class
        self.canvas = FigureCanvasTkAgg(f, self)
   
## Plots 2 sensors on 1 graph
class Multi_Graph_2(tk.Frame):

    def __init__(self, parent, controller):

        def search_command():
            sensor = e_n.get()
            sensor2 = e_n_2.get()
            s_hr = e_start_hr.get()
            s_min = e_start_min.get()
            s_sec = e_start_sec.get()
            e_hr = e_end_hr.get()
            e_min = e_end_min.get()
            e_sec = e_end_sec.get()
            VALID = 1
            
            try:
                sensor = int(sensor)
                sensor2 = int(sensor2)
            except ValueError:
                print("Sensor is not an int!")
                VALID = 0

            try:
                s_hr = int(s_hr)
                s_min = int(s_min)
                s_sec = int(s_sec)

            except ValueError:
                print("The starting time-interval is is not an int!")
                VALID = 0

            try:
                e_hr= int(e_hr)
                e_min = int(e_min)
                e_sec = int(e_sec)
            except ValueError:
                print("The ending time-interval is not an int!")
                VALID = 0
            
            
            
            if VALID == 1 and 0 < sensor < 55 and 0 < sensor2 < 55:
                start = date_to_seconds(s_hr, s_min, s_sec)
                end = date_to_seconds(e_hr, e_min, e_sec)
                
                if start > end:
                    multi_plot2(self, sensor, sensor2, end, start, g.get())
                    print('Upper and Lower time frame will be switched')
                else:
                    multi_plot2(self, sensor, sensor2, start, end, g.get())
            else:
                print("Unable to produce graph")

        tk.Frame.__init__(self, parent)
        button = tk.ttk.Button(self, text="Back to Home", command = lambda: controller.show_frame(MainPage))
        button.grid(row = 0, column = 0, padx = 20, pady = 20)
      
        label=tk.Label(self,text="Multiplot 2",fg="black",padx=5,pady=5)
        label.config(font=("Arial",18))
        label.grid(row = 0, column = 1, padx = 20, pady = 20, columnspan = 2)
        tk.Label(self, text = "Sensor Numbers").grid(row = 1, column = 0)
        tk.Label(self, text = " ", font= 'Helvetica 10 bold').grid(row = 3, column = 0, padx = 5, pady = 5)
        tk.Label(self, text = "Lower Timeframe", font= 'Arial 9 bold'). grid(row = 4, column = 0, padx = 7)
        tk.Label(self, text = "Higher Timeframe", font= 'Arial 9 bold').grid(row = 8, column = 0, padx = 7)

        e_n = tk.Entry(self, width = 4)
        e_n.grid(row = 1, column = 1, padx = 6, sticky = tk.W)
        e_n_2 = tk.Entry(self, width = 4)
        e_n_2.grid(row = 2, column = 1, padx = 6, sticky = tk.W)

        e_start_hr = tk.Entry(self)
        e_start_min = tk.Entry(self)
        e_start_sec = tk.Entry(self)
        e_end_hr = tk.Entry(self)
        e_end_min = tk.Entry(self)
        e_end_sec = tk.Entry(self)

        
        tk.Label(self, text = "Hour: ").grid(row = 5, column = 0)
        e_start_hr.grid(row=5, column=1, pady = 5)
        tk.Label(self, text = "Minutes: ").grid(row = 6, column = 0)
        e_start_min.grid(row=6, column=1, pady = 5)
        tk.Label(self, text = "Seconds: ").grid(row = 7, column = 0)
        e_start_sec.grid(row=7, column=1, pady = 5)
        
        tk.Label(self, text = "Hour: ").grid(row = 9, column = 0)
        e_end_hr.grid(row=9, column=1, pady = 5)
        tk.Label(self, text = "Minutes: ").grid(row = 10, column = 0)
        e_end_min.grid(row=10, column=1, pady = 5)
        tk.Label(self, text = "Seconds: ").grid(row = 11, column = 0)
        e_end_sec.grid(row=11, column=1, pady = 5)
        
        MODES = [("Humidity", "Humidity"), ("Temperature", "Temperature"), ("Energy-Level", "Energy-Level"), ("All", "All")]

        tk.Label(self, text="Enter Type to display:",font = 'Arial 9 bold').grid(row = 12, column = 0, pady = 7)
        g = tk.StringVar()
        x = 12
        for text, mode in MODES:
            tk.Radiobutton(self, text = text, variable = g, value = mode).grid(row = x, column = 1, padx = 5, pady = 5, sticky = tk.W)
            x += 1
        g.set("All") #automatically sets all



        quit_button = tk.Button(self, text = 'Quit')
        enter_button = tk.Button(self, text = "Enter", command = search_command)
        quit_button.grid(row = 16, column = 0, padx = 10, pady = 10)
        enter_button.grid(row = 16, column = 1,  padx = 10, pady = 10)

        #canvas attribute required for each class
        self.canvas = FigureCanvasTkAgg(f, self)

     


## Plots 3 sensors on 1 graph
class Multi_Graph_3(tk.Frame):

    def __init__(self, parent, controller):
        
        def search_command():
            sensor = e_n.get()
            sensor2 = e_n_2.get()
            sensor3 = e_n_3.get()
            s_hr = e_start_hr.get()
            s_min = e_start_min.get()
            s_sec = e_start_sec.get()
            e_hr = e_end_hr.get()
            e_min = e_end_min.get()
            e_sec = e_end_sec.get()
            VALID = 1
            
            try:
                sensor = int(sensor)
                sensor2 = int(sensor2)
                sensor3 = int(sensor3)
            except ValueError:
                print("Sensor is not an int!")
                VALID = 0

            try:
                s_hr = int(s_hr)
                s_min = int(s_min)
                s_sec = int(s_sec)

            except ValueError:
                print("The starting time-interval is is not an int!")
                VALID = 0

            try:
                e_hr= int(e_hr)
                e_min = int(e_min)
                e_sec = int(e_sec)
            except ValueError:
                print("The ending time-interval is not an int!")
                VALID = 0
            
            
            
            if VALID == 1 and 0 < sensor < 55 and 0 < sensor2 < 55 and 0 < sensor3 < 55:
                start = date_to_seconds(s_hr, s_min, s_sec)
                end = date_to_seconds(e_hr, e_min, e_sec)
                
                if start > end:
                    multi_plot3(self, sensor, sensor2, sensor3, end, start, g.get())
                    print('Upper and Lower time frame will be switched')
                else:
                    multi_plot3(self, sensor, sensor2, sensor3, start, end, g.get())
            else:
                print("Unable to produce graph")

        tk.Frame.__init__(self, parent)
        button = tk.ttk.Button(self, text="Back to Home", command = lambda: controller.show_frame(MainPage))
        button.grid(row = 0, column = 0, padx = 20, pady = 20)
     
        label=tk.Label(self,text="Multiplot 3",fg="black",padx=5,pady=5)
        label.config(font=("Arial",18))
        label.grid(row = 0, column = 1, padx = 20, pady = 20, columnspan = 2)
        tk.Label(self, text = "Sensor Number").grid(row = 1, column = 0)
        tk.Label(self, text = " ", font= 'Helvetica 10 bold').grid(row = 4, column = 0, padx = 5, pady = 5)
        tk.Label(self, text = "Lower Timeframe", font= 'Arial 9 bold'). grid(row = 5, column = 0, padx = 7)
        tk.Label(self, text = "Higher Timeframe", font= 'Arial 9 bold').grid(row = 9, column = 0, padx = 7)

        e_n = tk.Entry(self, width = 4)
        e_n.grid(row = 1, column = 1, padx = 6, sticky = tk.W)
        e_n_2 = tk.Entry(self, width = 4)
        e_n_2.grid(row = 2, column = 1, padx = 6, sticky = tk.W)
        e_n_3 = tk.Entry(self, width = 4)
        e_n_3.grid(row = 3, column = 1, padx = 6, sticky = tk.W)

        e_start_hr = tk.Entry(self)
        e_start_min = tk.Entry(self)
        e_start_sec = tk.Entry(self)
        e_end_hr = tk.Entry(self)
        e_end_min = tk.Entry(self)
        e_end_sec = tk.Entry(self)

        
        tk.Label(self, text = "Hour: ").grid(row = 6, column = 0)
        e_start_hr.grid(row=6, column=1, pady = 5)
        tk.Label(self, text = "Minutes: ").grid(row = 7, column = 0)
        e_start_min.grid(row=7, column=1, pady = 5)
        tk.Label(self, text = "Seconds: ").grid(row = 8, column = 0)
        e_start_sec.grid(row=8, column=1, pady = 5)
        
        tk.Label(self, text = "Hour: ").grid(row = 10, column = 0)
        e_end_hr.grid(row=10, column=1, pady = 5)
        tk.Label(self, text = "Minutes: ").grid(row =11, column = 0)
        e_end_min.grid(row=11, column=1, pady = 5)
        tk.Label(self, text = "Seconds: ").grid(row = 12, column = 0)
        e_end_sec.grid(row=12, column=1, pady = 5)
        
        MODES = [("Humidity", "Humidity"), ("Temperature", "Temperature"), ("Energy-Level", "Energy-Level"), ("All", "All")]

        tk.Label(self, text="Enter Type to display:",font = 'Arial 9 bold').grid(row = 13, column = 0, pady = 7)
        g = tk.StringVar()
        x = 13
        for text, mode in MODES:
            tk.Radiobutton(self, text = text, variable = g, value = mode).grid(row = x, column = 1, padx = 5, pady = 5, sticky = tk.W)
            x += 1
        g.set("All") #automatically sets all



        quit_button = tk.Button(self, text = 'Quit')
        enter_button = tk.Button(self, text = "Enter", command = search_command)
        quit_button.grid(row = 17, column = 0, padx = 10, pady = 10)
        enter_button.grid(row = 17, column = 1,  padx = 10, pady = 10)

        #canvas attribute required for each class
        self.canvas = FigureCanvasTkAgg(f, self)

      


## Plots 4 sensors on 1 graph
class Multi_Graph_4(tk.Frame):
    def __init__(self, parent, controller):
        def search_command():
            sensor = e_n.get()
            sensor2 = e_n_2.get()
            sensor3 = e_n_3.get()
            sensor4 = e_n_4.get()
            s_hr = e_start_hr.get()
            s_min = e_start_min.get()
            s_sec = e_start_sec.get()
            e_hr = e_end_hr.get()
            e_min = e_end_min.get()
            e_sec = e_end_sec.get()
            VALID = 1

            try:
                sensor = int(sensor)
                sensor2 = int(sensor2)
                sensor3 = int(sensor3)
                sensor4 = int(sensor4)
            except ValueError:
                print("Sensor is not an int!")
                VALID = 0

            try:
                s_hr = int(s_hr)
                s_min = int(s_min)
                s_sec = int(s_sec)

            except ValueError:
                print("The starting time-interval is is not an int!")
                VALID = 0

            try:
                e_hr= int(e_hr)
                e_min = int(e_min)
                e_sec = int(e_sec)
            except ValueError:
                print("The ending time-interval is not an int!")
                VALID = 0
            
            
            
            if VALID == 1 and 0 < sensor < 55 and 0 < sensor2 < 55 and 0 < sensor3 < 55 and 0 < sensor4 < 55:
                start = date_to_seconds(s_hr, s_min, s_sec)
                end = date_to_seconds(e_hr, e_min, e_sec)
                
                if start > end:
                    multi_plot4(self, sensor, sensor2, sensor3, sensor4, end, start, g.get())
                    print('Upper and Lower time frame will be switched')
                else:
                    multi_plot4(self, sensor, sensor2, sensor3, sensor4, start, end, g.get())
            else:
                print("Unable to produce graph")

        tk.Frame.__init__(self, parent)
        button = tk.ttk.Button(self, text="Back to Home", command = lambda: controller.show_frame(MainPage))
        button.grid(row = 0, column = 0, padx = 20, pady = 20)
      
        label=tk.Label(self,text="Multiplot 4",fg="black",padx=5,pady=5)
        label.config(font=("Arial",18))
        label.grid(row = 0, column = 1, padx = 20, pady = 20, columnspan = 2)
        tk.Label(self, text = "Sensor Number").grid(row = 1, column = 0)
        tk.Label(self, text = " ", font= 'Helvetica 10 bold').grid(row = 5, column = 0, padx = 5, pady = 5)
        tk.Label(self, text = "Lower Timeframe", font= 'Arial 9 bold'). grid(row = 6, column = 0, padx = 7)
        tk.Label(self, text = "Higher Timeframe", font= 'Arial 9 bold').grid(row = 10, column = 0, padx = 7)

        e_n = tk.Entry(self, width = 4)
        e_n.grid(row = 1, column = 1, padx = 6, sticky = tk.W)
        e_n_2 = tk.Entry(self, width = 4)
        e_n_2.grid(row = 2, column = 1, padx = 6, sticky = tk.W)
        e_n_3 = tk.Entry(self, width = 4)
        e_n_3.grid(row = 3, column = 1, padx = 6, sticky = tk.W)
        e_n_4 = tk.Entry(self, width = 4)
        e_n_4.grid(row = 4, column = 1, padx = 6, sticky = tk.W)

        e_start_hr = tk.Entry(self)
        e_start_min = tk.Entry(self)
        e_start_sec = tk.Entry(self)
        e_end_hr = tk.Entry(self)
        e_end_min = tk.Entry(self)
        e_end_sec = tk.Entry(self)

        
        tk.Label(self, text = "Hour: ").grid(row = 7, column = 0)
        e_start_hr.grid(row=7, column=1, pady = 5)
        tk.Label(self, text = "Minutes: ").grid(row = 8, column = 0)
        e_start_min.grid(row=8, column=1, pady = 5)
        tk.Label(self, text = "Seconds: ").grid(row = 9, column = 0)
        e_start_sec.grid(row=9, column=1, pady = 5)
        
        tk.Label(self, text = "Hour: ").grid(row = 11, column = 0)
        e_end_hr.grid(row=11, column=1, pady = 5)
        tk.Label(self, text = "Minutes: ").grid(row = 12, column = 0)
        e_end_min.grid(row=12, column=1, pady = 5)
        tk.Label(self, text = "Seconds: ").grid(row = 13, column = 0)
        e_end_sec.grid(row=13, column=1, pady = 5)
        
        MODES = [("Humidity", "Humidity"), ("Temperature", "Temperature"), ("Energy-Level", "Energy-Level"), ("All", "All")]

        tk.Label(self, text="Enter Type to display:",font = 'Arial 9 bold').grid(row = 14, column = 0, pady = 7)
        g = tk.StringVar()
        x = 14
        for text, mode in MODES:
            tk.Radiobutton(self, text = text, variable = g, value = mode).grid(row = x, column = 1, padx = 5, pady = 5, sticky = tk.W)
            x += 1
        g.set("All") #automatically sets all

        quit_button = tk.Button(self, text = 'Quit')
        enter_button = tk.Button(self, text = "Enter", command = search_command)
        quit_button.grid(row = 18, column = 0, padx = 10, pady = 10)
        enter_button.grid(row = 18, column = 1,  padx = 10, pady = 10)

        #canvas attribute required for each class
        self.canvas = FigureCanvasTkAgg(f, self)


## Main Menu of the Program
class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        #parent here would be 'Application class'
        tk.Frame.__init__(self, parent)
        # # LAYOUT # #
        data_folder = Path('Images/')
        # tk.Tk.iconbitmap(self, default= data_folder / 'icon.ico')
        photo = tk.PhotoImage(file = data_folder / 'Trinity_Logo.png') # image file
        photo = photo.subsample(4,4) # resize image , 1/4 size of originals

        canvas = tk.Label(self, image = photo, bg = "black")
        canvas.image = photo #image reference 
        canvas.grid(row=0, column = 0, rowspan = 2, columnspan = 2, padx = 10, pady = 10, sticky = tk.NW)

        title_label = tk.Label(self, text = "Visualizer of energy-aware schedueler", font = 'Times 35 ')
        title_label.grid(row = 0, column = 3, rowspan = 2, columnspan = 6, padx = 5, pady = 5, sticky = tk.NW)

        info_box = tk.Text(self, width = 60, height = 17, background = 'white')
        info_box.grid(row = 2, column = 0, rowspan = 2, columnspan = 3, padx = 5, pady = 5, sticky = tk.W)
        info_box.insert(tk.END, "Welcome to the Sensor Visualizer Program. This program was  part of the 4E2 Project undertaken by Daniel Kieran. The\nSensor map is taken from the Intel Data set where data of 54\nsensors were taken. Undertaken from 1/1/2020 to 9/4/2020.\n\nThis is an updated version that can be used for Linux, \nMacOS and Windows whereas the previous code only ran on\nWindows.\n\nTwo live-animated graphs instead of 1.\n\nThe HomePage live graph collects data and combines all 54\ncsv files and graphs features.\n\nSearch Sensor still under works.")

     
        map_photo = tk.PhotoImage(file = data_folder / 'diagram.png')
        map_photo = map_photo.zoom(2, 2)
        map_photo = map_photo.subsample(3, 3)
        map_label = tk.Label(self, image = map_photo, bg = 'black')
        map_label.image = map_photo
        map_label.grid(row = 5, column = 0, rowspan = 7, columnspan = 3, padx = 5, pady = 5, sticky = tk.N)

        tk.Label(self, text = 'Image of Sensor Map', font = 'Helvetica 12 bold italic').grid(row = 10, column = 0, columnspan = 3, sticky = tk.W)

        # ## Main Graph options canvas for displaying graph
        # graph_wall = tk.Frame(self, bg = "#1C78C0") #"#1C78C0" is a hash colour on tkinter
        # graph_wall.pack_propagate(0)
        # graph_wall.grid(row = 1, column = 3, columnspan = 6, padx = 5, pady = 5, rowspan = 5, sticky = tk.W)

        # ## Other options canvas to show buttons
        # other_wall = tk.Frame(self, bg = "firebrick", width = 130, height = 368)
        # other_wall.pack_propagate(0)
        # other_wall.grid(row = 1, column = 10, columnspan = 2, rowspan = 5, padx = 5, pady = 5, sticky = tk.N)

        # # LAYOUT OVER # #

        # # Widgets # #
        #widgets for graph box
        # tk.Label(graph_wall, text = "Visualisation Options", bg = "CadetBlue1", font = 'fixedsys 20').grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "we")
        # live_box = tk.Text(graph_wall, width = 60, height = 5, background = "white")
        # live_box.grid(row = 1, column = 0, columnspan = 2, padx = 10, pady = 10)
        # live_box.insert(tk.END, "This live graph updates every second to the User setting. \nClick the 'Live Graph' button to view this graph setting.")
        # tk.ttk.Button(graph_wall, text = "Live Graph", command = lambda : controller.show_frame(GraphPage)).grid(row = 1, column = 3, padx = 10, pady = 10)
        # live_box_stat = tk.Text(graph_wall, width = 60, height = 5, background = "white")
        # live_box_stat.grid(row = 2, column = 0, columnspan = 2, padx = 10, pady = 10)
        # live_box_stat.insert(tk.END, "Stationary graph for the measurements of data. Click the\n'Station' button to view this graph setting.")
        # tk.ttk.Button(graph_wall, text = "Station", command = lambda : controller.show_frame(Station_Graph)).grid(row = 2, column = 3, padx = 10, pady = 10)
        # live_box_other = tk.Text(graph_wall, width = 60, height = 5, background = "white")
        # live_box_other.grid(row = 3, column = 0, columnspan = 2, padx = 10, pady = 10)
        # live_box_other.insert(tk.END, "Other Graph options. Click 'Other' to view this graph\nsetting.")
        # tk.ttk.Button(graph_wall, text = "Other", command = lambda : controller.show_frame(Other_Options)).grid(row = 3, column = 3, padx = 10, pady = 10)

        # #widgets for other box
        # option_title = tk.Label(other_wall, text = "Other Options", bg = "lightcoral", font = 'Times 12 bold')
        # option_title.pack(side = tk.TOP, pady = 10)
        # datafile_button = tk.ttk.Button(other_wall, text = "View Datafiles", command=lambda: controller.show_frame(Data_Text))
        # datafile_button.pack(pady = 5)time_as
        # insert_data_button = tk.ttk.Button(other_wall, text = "Insert New Data", command=lambda: controller.show_frame(Insert_Data))
        # insert_data_button.pack(pady = 5)
        # sim_button = tk.ttk.Button(other_wall, text = "Example Simulation", command = lambda: controller.show_frame(Simulator)) 
        # sim_button.pack(pady = 5)

        
        def update_home_type2():
            global home_type2 
            home_type2 = str(g.get())

        graph_wall = tk.Frame(self, bg = "#1C78C0") 
        graph_wall.pack_propagate(0)
        graph_wall.grid(row = 2, column = 3, rowspan = 10, columnspan = 10, padx = 5, pady = 5, sticky = tk.W)
        # Inside the blue frame
        me_button = tk.ttk.Button(graph_wall, text = 'Mean', command = lambda:update_home_type('Mean'))
        me_button.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.W)
        mode_button = tk.ttk.Button(graph_wall, text = 'Standard deviation', command = lambda:update_home_type('Std'))
        mode_button.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = tk.W)
        med_button = tk.ttk.Button(graph_wall, text = 'Median', command = lambda:update_home_type('Median'))
        med_button.grid(row = 0, column = 2, padx = 5, pady = 5, sticky = tk.W)
        MODES = [("Humidity", "Humidity"), ("Temperature", "Temperature"), ("Energy-Level", "Energy-Level")]
        g = tk.StringVar()
        x = 0
        for text, mode in MODES:
            tk.Radiobutton(graph_wall, text = text, variable = g, value = mode, command = update_home_type2).grid(row = 1, column = x, padx = 5, pady = 5, sticky = tk.W)
            x += 1
        g.set("Humidity")

        #canvas attribute
        home_canvas = FigureCanvasTkAgg(f2, master = graph_wall)
        home_canvas.draw()
        home_canvas.get_tk_widget().grid(row = 2, column = 0, rowspan = 5, columnspan = 3, sticky = 'nsew')
        self.canvas = home_canvas


        other_wall = tk.Frame(self, bg = "#1C78C0", width = 160, height = 700) 
        other_wall.pack_propagate(0)
        other_wall.grid(row = 2, column = 15, rowspan = 11, columnspan = 2, padx = 15, pady = 5)
        option_title = tk.Label(other_wall, text = "Other Options", bg = "lightcoral", font = 'Times 12 bold')
        option_title.pack(side = tk.TOP, pady = 10)
        datafile_button = tk.ttk.Button(other_wall, text = "View Datafiles", command=lambda: controller.show_frame(Data_Text))
        datafile_button.pack(pady = 5)
        insert_data_button = tk.ttk.Button(other_wall, text = "Insert New Data", command=lambda: controller.show_frame(Insert_Data))
        insert_data_button.pack(pady = 5)
        sim_button = tk.ttk.Button(other_wall, text = "Example Simulation", command = lambda: controller.show_frame(Simulator)) 
        sim_button.pack(pady = 5)
        in_button = tk.ttk.Button(other_wall, text = "Check induvisual\nsensors", command = lambda: controller.show_frame(GraphPage)) 
        in_button.pack(pady = 5)

## Insert_Data only works when Python IDE is run as administrator ##
## Allowing changes to files ##
## Be careful as once inserting data you cannot take it back within the program ##
class Insert_Data(tk.Frame):
    def __init__(self, parent, controller):
        
        def checker():
            
            def add_to_csv(): #this function adds the row of data to the end of specified csv file
                row_contents = [df['transmission_number'].iloc[-1] + 1, df['time_of_transmission'].iloc[-1] + time_value, temp, humid, energy, update_r, accur]
                with open(s, 'a+', newline='') as write_obj:
                    csv_writer = writer(write_obj)
                    csv_writer.writerow(row_contents)
                popupmsg('New row added to ' + s)
                print('Data inserted')
             
            ## gathers values from entryboxes
            sensor = entrybox.get()
            time_value = entrybox7.get()
            humid = entrybox2.get()
            temp = entrybox3.get()
            energy = entrybox4.get()
            update_r = entrybox5.get()
            accur = entrybox6.get()

            VALID = 1
            
            #try except methods to check if values are valid
            try:
                sensor = int(sensor)
                if(0 < sensor < 55 ):
                    print('Sensor exists')
                else:
                    print('Sensor doesn not exist')
                    VALID = 0
            except:
                print('Sensor is not an int')
                VALID = 0
            
            try:
                time_value = int(time_value)
            except:
                print('Time is not an int')
                VALID = 0
            
            try:
                humid = float(humid)
                temp = float(temp)
                energy = float(energy)
                update_r = float(update_r)
                accur = float(accur)
            except:
                print('Make sure the inputs are numbers and not letters')
                VALID = 0

            if(VALID == 1):


                #popup frame asking the user if they are sure of the change
                top = tk.Toplevel(self)
                label = tk.ttk.Label(top, text = 'Are you sure you want to add these changes?', font = 'Arial 12 bold')
                label.pack(padx = 10, pady = 10)
                frame = tk.Frame(top)
                frame.pack()
                sensor_folder = Path('generated_data/')
                s = "sensor_id_" + str(sensor) + ".csv"
                df = pd.read_csv(sensor_folder / s) 
                lbl = 'For sensor ' + str(sensor) + '\nTime of transmission: ' + str(df['time_of_transmission'].iloc[-1]) + ' --> ' + str(df['time_of_transmission'].iloc[-1] + time_value) + '\nHumidity: ' + str(df['hum_value'].iloc[-1]) + ' --> ' + str(humid) + '\nTemperature: ' + str(df['tem_value'].iloc[-1]) + ' --> ' + str(temp) + '\nEnergy-level: ' + str(df['energy_level'].iloc[-1]) + str(energy) + '\nUpdate rate: ' + str(df['update_rate'].iloc[-1]) + ' --> ' +  str(update_r) + '\nAccuracy: ' + str(df['accuracy'].iloc[-1]) + ' --> ' + str(accur)
                t_box = tk.Text(frame, width = 50, height = 10, background = "white")
                t_box.pack()
                t_box.insert(tk.END, lbl)
                tk.ttk.Button(frame, text =  'Yes', command = lambda:(add_to_csv(), top.destroy())).pack()
                tk.ttk.Button(frame, text = 'No', command = top.destroy).pack()


        tk.Frame.__init__(self, parent)
        label=tk.Label(self,text="Insert New Data",fg="black",padx=5,pady=5)
        label.config(font=("Arial",18))
        label.grid(row = 0, column = 0, padx = 20, pady = 20, columnspan = 2)
        button = tk.ttk.Button(self, text="Back to Home", command = lambda: controller.show_frame(MainPage))
        button.grid(row = 0, column = 2, padx = 20, pady = 20)
        
        label1 = tk.ttk.Label(self, text = 'Sensor', font = 'arial 9 bold')
        label1.grid(row = 1, column = 0, padx = 5, pady = 5)
        label2 = tk.ttk.Label(self, text = 'Humidity', font = 'arial 9 bold')
        label2.grid(row = 2, column = 0, padx = 5, pady = 5)
        label3 = tk.ttk.Label(self, text = 'Temperature', font = 'arial 9 bold')
        label3.grid(row = 3, column = 0, padx = 5, pady = 5)
        label4 = tk.ttk.Label(self, text = 'Energy-level', font = 'arial 9 bold')
        label4.grid(row = 4, column = 0, padx = 5, pady = 5)
        label5 = tk.ttk.Label(self, text = 'Update-Rate', font = 'arial 9 bold')
        label5.grid(row = 5, column = 0, padx = 5, pady = 5)
        label6 = tk.ttk.Label(self, text = 'Accuracy', font = 'arial 9 bold')
        label6.grid(row = 6, column = 0, padx = 5, pady = 5)
        label7 = tk.ttk.Label(self, text = 'Time in Seconds after latest reading', font = 'arial 9 bold')
        label7.grid(row = 7, column = 0, padx = 5, pady = 5)

        entrybox = tk.Entry(self, width = 4)
        entrybox.grid(padx = 5, pady = 20, row = 1, column = 1, sticky = tk.W)
        entrybox2 = tk.Entry(self, width = 4)
        entrybox2.grid(padx = 5, pady = 20, row = 2, column = 1, sticky = tk.W)
        entrybox3 = tk.Entry(self, width = 4)
        entrybox3.grid(padx = 5, pady = 20, row = 3, column = 1, sticky = tk.W)
        entrybox4 = tk.Entry(self, width = 4)
        entrybox4.grid(padx = 5, pady = 20, row = 4, column = 1, sticky = tk.W)
        entrybox5 = tk.Entry(self, width = 4)
        entrybox5.grid(padx = 5, pady = 20, row = 5, column = 1, sticky = tk.W)
        entrybox6 = tk.Entry(self, width = 4)
        entrybox6.grid(padx = 5, pady = 20, row = 6, column = 1, sticky = tk.W)
        entrybox7 = tk.Entry(self, width = 4)
        entrybox7.grid(padx = 5, pady = 20, row = 7, column = 1, sticky = tk.W)

        tk.ttk.Button(self, text = 'Enter', command = checker).grid(padx = 10, pady = 10, row = 8, column = 0)
        tk.ttk.Button(self, text = 'Exit', command = lambda: controller.show_frame(MainPage)).grid(padx = 10, pady = 10, row = 8, column = 1)

        #canvas attribute required for each class
        self.canvas = FigureCanvasTkAgg(f, self)

    


## Bar Chart page
class BarCharts(tk.Frame):
    
    def __init__(self, parent, controller):
        #parent here would be 'Application class'

        def bar_check(): #checks whether a bar chart can be built
            sensor = entrybox.get()
            bar_type = g.get()
            VALID = 1

            try:
                sensor = int(sensor)
            
            except:
                print('Sensor is not an int!')
                VALID = 0
            
            if VALID > 0 and 0 < sensor < 55:
                bar_plot(self, sensor, bar_type)
            else:
                print('Try inputs again')

        # Title and back to home page
        tk.Frame.__init__(self, parent)
        button = tk.ttk.Button(self, text="Back to Home", command = lambda: controller.show_frame(MainPage))
        button.grid(row = 0, column = 0, padx = 20, pady = 20)
        label=tk.Label(self,text="Bar Chart Page",fg="black",padx=5,pady=5)
        label.config(font=("Arial",18))
        label.grid(row = 0, column = 1, padx = 20, pady = 20, columnspan = 2)
        
        # USer fields
        tk.Label(self, text = 'Enter sensor', font = 'times 10 bold').grid(row = 1, column = 0, padx = 5, pady = 20)
        entrybox = tk.Entry(self, width = 4)
        entrybox.grid(padx = 5, pady = 20, row = 1, column = 1, sticky = tk.W)
        tk.Label(self, text = 'Enter type', font = 'times 10 bold').grid(row = 2, column = 0, padx = 10, pady = 20)
        g = tk.StringVar()
        tk.Radiobutton(self, text = 'Quantity', variable = g, value = 'Quantity').grid(row = 2, column = 1, padx = 7, pady = 20, sticky = tk.W)
        tk.Radiobutton(self, text = 'Relative Frequency', variable = g, value = 'Relative').grid(row = 3, column = 1, padx = 7, pady = 20, sticky = tk.W)
        g.set("Relative")
        tk.ttk.Button(self, text = 'Enter', command = bar_check).grid(row = 4, column = 0,padx = 5, pady = 20)
        tk.ttk.Button(self, text='Quit', command = lambda: controller.show_frame(MainPage)).grid(row = 4, column = 1,padx = 5, pady = 20)

        #canvas attribute required for each class
        self.canvas = FigureCanvasTkAgg(f, self)



## Tells the user sensor details of the network 
class Network(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
         
        def show_data():
            sensor = e1.get()
            
            try:
                sensor = int(sensor)
                sensor_folder = Path('generated_data/')
                s = "sensor_id_" + str(sensor) + ".csv"
                df = pd.read_csv(sensor_folder / s) 
                av_tem = str(round(df['tem_value'].mean(), 1)) ## calculates various values
                max_tem = str(df['tem_value'].max())
                min_tem = str(df['tem_value'].min())
                av_hum = str(round(df['hum_value'].mean(), 1))
                max_hum = str(df['hum_value'].max())
                min_hum = str(df['hum_value'].min())
                av_ene = str(round(df['energy_level'].mean(), 1))
                max_ene = str(df['energy_level'].max())
                min_ene = str(df['energy_level'].min())
                ave_upd = str(round(df['update_rate'].mean(), 1))
                max_upd = str(df['update_rate'].max())
                min_upd = str(df['update_rate'].min())
                ave_acc = str(round(df['accuracy'].mean(), 1))
                max_acc = str(df['accuracy'].max())
                min_acc = str(df['accuracy'].min())
                f_contents = 'Average temperature: ' + av_tem + '\nMax temperature: ' + max_tem + '\nMin temperature: ' + min_tem + '\nAverage humidity: ' + av_hum + '\nMax humidity: ' + max_hum + '\nMin humidity: ' + min_hum + '\nAverage energy-Level: ' + av_ene + '\nMax energy-level: ' + max_ene + '\nMin energy-level: ' + min_ene + '\nAverage update rate : ' + ave_upd + '\nMax update rate: ' + max_upd + '\nMin update rate: ' + min_upd + '\nAverage accuracy : ' + ave_acc + '\nMax accuracy: ' + max_acc + '\nMin accuracy: ' + min_acc + '\n\n'
                textbox.insert(tk.END, f_contents)
            except:
                popupmsg('Cannot open data file') #popup message when error occurs

        
        label = tk.Label(self, text="Find details of Sensors", font=LARGE_FONT)
        label.grid(row = 0, column = 0, pady=10, padx = 10, columnspan = 10)
        button = ttk.Button(self, text="Back to Home", command = lambda: controller.show_frame(MainPage))
        button.grid(row = 0, column = 11, pady = 2, padx = 7)

        tk.Label(self, text = "Sensor Details").grid(row = 1, column = 0, columnspan = 2)
        e1 = tk.Entry(self)
        e1.grid(row = 1, column = 3, padx = 10)

        button = tk.ttk.Button(self, text = "Enter", command=show_data)
        button.grid(row = 1, column = 4, columnspan = 5, pady = 5)

        textbox = tk.Text(self, width = 75, height = 70, background = "white")
        textbox.grid(row = 3, column = 0, columnspan = 12)

        #canvas attribute required for each class
        self.canvas = FigureCanvasTkAgg(f, self)



       
## Live Graph Page ##
class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        frame = tk.Frame(self, width = 800, height = 30)
        frame.pack(fill = tk.X)
        frame.pack_propagate(0)
        # homwe_canvas = FigureCanvasTkAgg(f2, self)
        # homwe_canvas.draw()
        # homwe_canvas.get_tk_widget().grid(row = 12, column = 3, sticky = 'nsew')
        #do plt.show() type function
        canvas = FigureCanvasTkAgg(f,self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas = canvas
        # #navigation bar
        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



        #menu idgets
        tk.ttk.Button(frame, text = 'Back to Home', command = lambda: controller.show_frame(MainPage)).grid(row = 0, column = 0, padx = 10, pady = 10)
        tk.Label(frame, text = "Enter Sensor Number: ", font = 'Times 10').grid(row = 1, column = 0, padx = 5, pady = 5)
        entrybox = tk.Entry(frame, width = 4)
        entrybox.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = tk.W)
        entrybox.insert(tk.END, '1')
        MODES = [("Humidity", "Humidity"), ("Temperature", "Temperature"), ("Energy-Level", "Energy-Level")]
        tk.Label(frame, text = " ").grid(row = 1, column = 2, padx = 20)
        tk.Label(frame, text="Enter Type to display:",font = 'Times 10').grid(row = 1, column = 3, pady = 5, padx = 5)
        g = tk.StringVar()
        x = 1
        for text, mode in MODES:
            tk.Radiobutton(frame, text = text, variable = g, value = mode).grid(row = x, column = 4, padx = 5, pady = 5, sticky = tk.W)
            x += 1
        
        g.set("Humidity") #automatically set to humidity


        go_button = tk.ttk.Button(frame, text = "SELECT", command = lambda : [controller.show_frame(GraphPage), changegraph(g.get(), entrybox.get())])
        go_button.grid(row = 1, column = 5, padx = 10, pady = 12)


## Displays the csv text data into a textbox for the user to check
class Data_Text(tk.Frame):
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)

        def show_data():
            sensor = e1.get()
            try:
                sensor = int(sensor)
                sensor_folder = Path('generated_data/')
                s = "sensor_id_" + str(sensor) + ".csv"
                with open(sensor_folder / s, 'r') as f:
                    f_contents = f.read()
                    print(f_contents)

                textbox.insert(tk.END, f_contents)
            except:
                popupmsg('Cannot open data file')

        label = tk.Label(self, text="Given Sensor Data read from csv file", font=LARGE_FONT)
        label.grid(row = 0, column = 0, pady=10, padx = 10, columnspan = 10)
        button = ttk.Button(self, text="Back to Home", command = lambda: controller.show_frame(MainPage))
        button.grid(row = 0, column = 11, pady = 2, padx = 7)
        tk.Label(self, text = "Sensor Number").grid(row = 1, column = 0, columnspan = 2)
        e1 = tk.Entry(self)
        e1.grid(row = 1, column = 3, padx = 10)
        button = tk.ttk.Button(self, text = "Enter", command=show_data)
        button.grid(row = 1, column = 4, columnspan = 5, pady = 5)
        textbox = tk.Text(self, width = 75, height = 70, background = "white")
        textbox.grid(row = 3, column = 0, columnspan = 12)

        #canvas attribute required for each class
        self.canvas = FigureCanvasTkAgg(f, self)

        

## Simulation Page ##
class Simulator(tk.Frame):
    
    def __init__(self, parent, controller, bg = "black"):   
        #Function this page needs
        def load_day(val):
            def load_map(val, frame):
                for wid in frame.winfo_children():
                    if val == 0:
                        wid.configure(bg = "dark green")
                    elif val == 1:
                        wid.configure(bg = "lawn green")
                    elif val == 2:
                        wid.configure(bg = "yellow4")
                    elif val == 3:
                        wid.configure(bg = "yellow2")
                    elif val == 4:
                        wid.configure(bg = "orange")
                    elif val > 4:
                        wid.configure(bg = "red") #as days pass battery life decreases, represented by colours

            v = int(val) # integer variables for day
            load_map(v, s_map) #function to change state of s_map
            
       

        #self is the container
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Simulator", font=LARGE_FONT)
        button = ttk.Button(self, text="Back to Home", command = lambda: controller.show_frame(MainPage))
        textbox = tk.Text(self, width = 75, height = 6, background = "white")
        textbox.insert(tk.END, "This Simulation gives an example of how Sensor battery decreases as time \npasses. As days pass the batteries of the sensor lose battery-life")
        sliderlabel = tk.Label(self, text="Day", font=NORM_FONT)
        

        label.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan = 5, rowspan = 3, sticky = tk.NW)
        button.grid(row = 0, column = 6, padx = 10, pady = 10) #columnspan = 5, rowspan = 3
        textbox.grid(row = 3, column = 0, padx = 10, pady = 10, columnspan = 20, sticky = tk.W)
        sliderlabel.grid(row = 0, column = 21, padx = 10, pady = 10)
        
        #Sensor Map
        sensor_map = tk.Frame(self, bg = "green", height = 500, width = 1200)
        sensor_map.grid(row = 6, column = 0, columnspan = 30, rowspan = 20, padx = 10, pady = 10)
        sensor_map.grid_rowconfigure(6, weight = 1)
        ## widgets for sensor map placed here by grid
        s_map = tk.Frame(sensor_map, bg = "white", height = 500, width = 1200)
        s_map.grid(row = 0, column = 0, rowspan = 20, columnspan = 50, padx = 5, pady = 5)

        #configures the frame to row and columns of 20x50
        for row in range(20):
            s_map.rowconfigure(row, minsize = 10)

        for column in range(50):
            s_map.columnconfigure(column, minsize = 10)

        #placement of sensors
        sensor1 = tk.Label(s_map, text = "Sensor 1").grid(row = 3, column = 5, rowspan = 1, columnspan =1)
        sensor2 = tk.Label(s_map, text = "Sensor 2").grid(row = 7, column = 2, rowspan = 1, columnspan =1)
        sensor3 = tk.Label(s_map, text = "Sensor 3").grid(row = 13, column = 3, rowspan = 1, columnspan =1)
        sensor4 = tk.Label(s_map, text = "Sensor 4").grid(row = 17, column = 23, rowspan = 1, columnspan =1)
        sensor5 = tk.Label(s_map, text = "Sensor 5").grid(row = 19, column = 39, rowspan = 1, columnspan =1)
        sensor6 = tk.Label(s_map, text = "Sensor 6").grid(row = 4, column = 43, rowspan = 1, columnspan =1)
        sensor7 = tk.Label(s_map, text = "Sensor 7").grid(row = 7, column = 40, rowspan = 1, columnspan =1)


        #Default of sensor batteries is green
        for wid in s_map.winfo_children():
            wid.configure(bg = "dark green")

        slider = tk.Scale(self, from_=0, to_= 5, orient = tk.HORIZONTAL, tickinterval = 1, length = 500, command = load_day) #slider to change day, calls load day when changed
        slider.grid(row = 3, column = 21, padx = 10, pady = 10)
        textbox2 = tk.Text(self, width = 60, height = 6, background = "white")
        textbox2.grid(row = 28, column = 0,  sticky = tk.W)
        textbox2.insert(tk.END, "Green means battery has full battery life.\nOrange means it is in the middle.\nRed means it is Low.")

        #canvas attribute required for each class
        self.canvas = FigureCanvasTkAgg(f, self)
        


## stationary graph ##
class Station_Graph(tk.Frame):
    def __init__(self, parent, controller):
        
        def check_input():
            # function that checks if inputs are correct
            #. get () fetches current text in entrybox
            sensor = e_n.get()
            s_hr = e_start_hr.get()
            s_min = e_start_min.get()
            s_sec = e_start_sec.get()
            e_hr = e_end_hr.get()
            e_min = e_end_min.get()
            e_sec = e_end_sec.get()
            VALID = 1

            # sequence of try / except statements to check values

            try:
                sensor = int(sensor)
            except ValueError:
                print("Sensor is not an int!")
                VALID = 0

            try:
                s_hr = int(s_hr)
                s_min = int(s_min)
                s_sec = int(s_sec)

            except ValueError:
                print("The starting time-interval is is not an int!")
                VALID = 0

            try:
                e_hr= int(e_hr)
                e_min = int(e_min)
                e_sec = int(e_sec)
            except ValueError:
                print("The ending time-interval is not an int!")
                VALID = 0
            
            
            
            if VALID == 1 and 0 < sensor < 55: # must also be in sensor no. limits
                start = date_to_seconds(s_hr, s_min, s_sec) # covert hr/min /sec
                end = date_to_seconds(e_hr, e_min, e_sec) # covert hr/ min / sec
                
                if start > end:
                    station_with_sensor(self, sensor, end, start, g.get())
                    print('Upper and Lower time frame will be switched')
                else:
                    station_with_sensor(self, sensor, start, end, g.get())
            else:
                print("Unable to produce graph")

        tk.Frame.__init__(self, parent)
        ## Title and Back Button ##
        button = tk.ttk.Button(self, text="Back to Home", command = lambda: controller.show_frame(MainPage))
        button.grid(row = 0, column = 0, padx = 20, pady = 20)
        label=tk.Label(self,text="Stationary Graph",fg="black",padx=5,pady=5)
        label.config(font=("Arial",18))
        label.grid(row = 0, column = 1, padx = 20, pady = 20, columnspan = 2)

        
        ## Input layout ##
        tk.Label(self, text = "Sensor Number").grid(row = 1, column = 0)
        tk.Label(self, text = " ", font= 'Helvetica 10 bold').grid(row = 2, column = 0, padx = 5, pady = 5)
        tk.Label(self, text = "Lower Timeframe", font= 'Arial 9 bold'). grid(row = 3, column = 0, padx = 7)
        tk.Label(self, text = "Hour: ").grid(row = 4, column = 0)
        tk.Label(self, text = "Minutes: ").grid(row = 5, column = 0)
        tk.Label(self, text = "Seconds: ").grid(row = 6, column = 0)
        tk.Label(self, text = "Higher Timeframe", font= 'Arial 9 bold').grid(row = 7, column = 0, padx = 7)
        tk.Label(self, text = "Hour: ").grid(row = 8, column = 0)
        tk.Label(self, text = "Minutes: ").grid(row = 9, column = 0)
        tk.Label(self, text = "Seconds: ").grid(row = 10, column = 0)
        tk.Label(self, text="Enter Type to display:",font = 'Arial 9 bold').grid(row = 11, column = 0, pady = 7)

        ## Sensor Input field ##
        e_n = tk.Entry(self, width = 4)
        e_n.grid(row = 1, column = 1, padx = 6, sticky = tk.W)

        ## Time input field ##
        e_start_hr = tk.Entry(self)
        e_start_hr.grid(row=4, column=1, pady = 5)
        e_start_min = tk.Entry(self)
        e_start_min.grid(row=5, column=1, pady = 5)
        e_start_sec = tk.Entry(self)
        e_start_sec.grid(row=6, column=1, pady = 5)
        e_end_hr = tk.Entry(self)
        e_end_hr.grid(row=8, column=1, pady = 5)
        e_end_min = tk.Entry(self)
        e_end_min.grid(row=9, column=1, pady = 5)
        e_end_sec = tk.Entry(self)
        e_end_sec.grid(row=10, column=1, pady = 5)

        
        
        ## Graph type input ##
        MODES = [("Humidity", "Humidity"), ("Temperature", "Temperature"), ("Energy-Level", "Energy-Level"), ("All", "All")]
        g = tk.StringVar()
        x = 11
        for text, mode in MODES:
            tk.Radiobutton(self, text = text, variable = g, value = mode).grid(row = x, column = 1, padx = 5, pady = 5, sticky = tk.W)
            x += 1
        g.set("All") #automatically sets all


        ## Enter and Quit button ##
        quit_button = tk.Button(self, text = 'Quit')
        enter_button = tk.Button(self, text = "Enter", command = check_input)
        quit_button.grid(row = 15, column = 0, padx = 10, pady = 10)
        enter_button.grid(row = 15, column = 1,  padx = 10, pady = 10)

        #canvas attribute required for each class
        self.canvas = FigureCanvasTkAgg(f, self)

      

## SearchDay is incomplete ##
## Was supposed to be for the sensor map ##        
class SearchDay(tk.Frame):
    def __init__(self, parent, controller):
        
        def search_command():
            day = e_d.get()
            month = e_m.get()
            year = e_y.get()
            search(day, month, year)

        tk.Frame.__init__(self, parent)
        button = tk.ttk.Button(self, text="Back to Home", command = lambda: controller.show_frame(MainPage))
        button.grid(row = 0, column = 0, padx = 20, pady = 20)
        
        label=tk.Label(self,text="Search Page",fg="black",padx=5,pady=5)
        label.config(font=("Arial",18))
        label.grid(row = 0, column = 1, padx = 20, pady = 20)

        tk.Label(self, text = "Day").grid(row = 1, column = 0)
        tk.Label(self, text = "Month").grid(row = 2, column = 0)
        tk.Label(self, text = "Year"). grid(row = 3, column = 0)

        e_d = tk.Entry(self)
        e_m = tk.Entry(self)
        e_y = tk.Entry(self)

        e_d.grid(row=1, column=1)
        e_m.grid(row=2, column=1)
        e_y.grid(row=3, column=1)

        quit_button = tk.ttk.Button(self, text = 'Quit', width = 100)
        enter_button = tk.ttk.Button(self, text = "Enter", command = lambda: popupmsg("Not supported just yet"), width = 100)
        quit_button.grid(row = 4, column = 0, padx = 10, pady = 10,sticky = tk.W)
        enter_button.grid(row = 4, column = 1,  padx = 10, pady = 10, sticky = tk.W)

        #canvas attribute required for each class
        self.canvas = FigureCanvasTkAgg(f, self)

       

## Other Options
class Other_Options(tk.Frame):
    ## Other options included ##
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ## Title and back to home button ##
        button = tk.ttk.Button(self, text="Back to Home", command = lambda: controller.show_frame(MainPage))
        button.grid(row = 0, column = 2, padx = 20, pady = 20)
        label=tk.Label(self,text="Other Options",fg="black",padx=5,pady=5)
        label.config(font=("Arial",25))
        label.grid(row = 0, column = 0, padx = 20, pady = 20, columnspan = 2)

        ## Checks if bar chart can be created from inputs
        def bar_check():
            ## fetches user inputs with .get() method
            sensor = entrybox.get()
            bar_type = g.get()
            VALID = 1
            #try xcept methods to check validity of inputs
            try:
                sensor = int(sensor)
            
            except:
                print('Sensor is not an int!')
                VALID = 0
            
            if VALID > 0 and 0 < sensor < 55:
                bar_plot_h(self, sensor, bar_type)
            else:
                print('Try inputs again')

        #checks whether the histogram inputs are valid
        def hist_check():
            ## fetches user inputs with .get() method
            sensor = entrybox2.get()
            bar_type = g2.get()
            sensor_property = g3.get()
            VALID = 1

            try:
                sensor = int(sensor)
            
            except:
                print('Sensor is not an int!')
                VALID = 0
            
            if VALID > 0 and 0 < sensor < 55:
                hist_plot(self, sensor, bar_type, sensor_property)
            else:
                print('Try inputs again')

        ## Horizontal Bar chart##
        title_h = tk.Label(self, text="Horizontal Bar Chart", font = 'arial 10 bold', padx=5, pady=5)
        title_h.grid(row = 1, column = 0, padx = 5, pady = 5)
        tk.Label(self, text = 'Enter sensor', font = 'times 10').grid(row = 2, column = 0, padx = 5, pady = 20)
        entrybox = tk.Entry(self, width = 4)
        entrybox.grid(padx = 5, pady = 20, row = 2, column = 1, sticky = tk.W)
        tk.Label(self, text = 'Enter type', font = 'times 10').grid(row = 3, column = 0, padx = 10, pady = 20)

        g = tk.StringVar() #variable type for radiobuttons
        tk.Radiobutton(self, text = 'Quantity', variable = g, value = 'Quantity').grid(row = 3, column = 1, padx = 7, pady = 20, sticky = tk.W)
        tk.Radiobutton(self, text = 'Relative Frequency', variable = g, value = 'Relative').grid(row = 4, column = 1, padx = 7, pady = 20, sticky = tk.W)
        g.set("Relative")#set to 'Relative' first
        
        ## Enter and Quit Button ## 
        #Enter goes to bar_check
        tk.ttk.Button(self, text = 'Enter', command = bar_check).grid(row = 5, column = 0,padx = 5, pady = 20)
        tk.ttk.Button(self, text='Quit', command = lambda: controller.show_frame(MainPage)).grid(row = 5, column = 1, padx = 5, pady = 20)


        ## Histogram ##
        ## Still a work in progress, doesn not effectively display update rate or accuracy
        title_h2 = tk.Label(self, text="Histogram of Accuracy and Update Rate", font = 'arial 10 bold', padx=5, pady=5)
        title_h2.grid(row = 1, column = 4, padx = 5, pady = 5)
        tk.Label(self, text = 'Enter sensor', font = 'times 10').grid(row = 2, column = 4, padx = 5, pady = 20)
        entrybox2 = tk.Entry(self, width = 4)
        entrybox2.grid(padx = 5, pady = 20, row = 2, column = 5, sticky = tk.W)
        tk.Label(self, text = 'Enter type', font = 'times 10').grid(row = 3, column = 4, padx = 10, pady = 20)

        g2 = tk.StringVar()#variable type for radiobuttons
        tk.Radiobutton(self, text = 'Quantity', variable = g2, value = 'Quantity').grid(row = 3, column = 5, padx = 7, pady = 20, sticky = tk.W)
        tk.Radiobutton(self, text = 'Relative Frequency', variable = g2, value = 'Relative').grid(row = 4, column = 5, padx = 7, pady = 20, sticky = tk.W)
        g2.set("Relative")

        tk.Label(self, text = 'Type', font = 'times 10').grid(row = 5, column = 4, padx = 10, pady = 10)
        g3 = tk.StringVar()#variable type for radiobuttons
        tk.Radiobutton(self, text = 'Update Rate', variable = g3, value = 'Update Rate').grid(row = 5, column = 5, padx = 7, pady = 20, sticky = tk.W)
        tk.Radiobutton(self, text = 'Accuracy', variable = g3, value = 'Accuracy').grid(row = 6, column = 5, padx = 7, pady = 20, sticky = tk.W)
        g3.set("Accuracy")

        #Enter goes to hist_check
        tk.ttk.Button(self, text = 'Enter', command = hist_check).grid(row = 7, column = 4,padx = 5, pady = 20)
        tk.ttk.Button(self, text='Quit', command = lambda: controller.show_frame(MainPage)).grid(row = 7, column = 5, padx = 5, pady = 20)

        #canvas attribute required for each class
        self.canvas = FigureCanvasTkAgg(f, self)

       

## Change Graph setting  (for Live Graph)##
def changegraph(graphtype, number):
    VALID = 1
    #check if sensor number is int
    try:
        number = int(number)
    except ValueError:
        print("Number is not an int!")
        VALID = 0
    
    global live_type #access to changing global variable values
    global live_sensor  #access to changing global variable values
    
    if VALID == 1:
        if 0 < number < 55: #change the global variables only when sensor number is valid
            live_sensor = number
            live_type = graphtype
        else:
            live_sensor = live_sensor 
     



def update_home_type(graphtype):
    global home_type
    home_type = str(graphtype)

## TUTORIAL ##
def tutorial_page():
    #Tutorial causes a new window to appear once a button on the parent window is selected
    def simulation():
        page.destroy()
        page2 = tk.Tk()
        page2.wm_title('Simulation tutorial')
        label = ttk.Label(page2, text = 'Simulation', font = 'arial 10 bold')
        label.pack()
        label2 = ttk.Label(page2, text = 'The Simulation page allows the user to change the time setting with the slider. \nThe change in battery-life of the sensors can be seen', font = 'arial 9')
        label2.pack()
        page2.mainloop()

    def bar_chart():
        page.destroy()
        page2 = tk.Tk()
        page2.wm_title('Bar Chart tutorial')
        label = ttk.Label(page2, text = 'Bar Chart', font = 'arial 10 bold')
        label.pack()
        label2 = ttk.Label(page2, text = 'The Bar chart option models the update rate of the sensors.\nEnter the sensor number and observe its behaviour.\nIt is possible to model the relative frequency or see its quantities.', font = 'arial 9')
        label2.pack()
        page2.mainloop()

    def multiplot_graph():
        
        def multiplot_graph_2():
            page2.destroy()
            page3 = tk.Tk()
            page3.wm_title('Multiple Plot graph tutorial')
            label = ttk.Label(page3, text = 'Multiple Plot Graph', font = 'arial 10 bold')
            label.pack()
            label2 = ttk.Label(page3, text = 'Once selecting the number of sensors, enter the details on the Input page. The figure is created on a seperate window.', font = 'arial 9')
            label2.pack()
            page3.mainloop()

        page.destroy()
        page2 = tk.Tk()
        page2.wm_title('Multiple Plot graph tutorial')
        label = ttk.Label(page2, text = 'Multiple Plot Graph', font = 'arial 10 bold')
        label.pack()
        label2 = ttk.Label(page2, text = 'The Multiple Plot graph enables the user to select multiple sensors to plot on the single figure.\nEnter the number of sensors to graph on the start page.', font = 'arial 9')
        label2.pack()
        
        button = tk.ttk.Button(page2, text = 'Next', command = multiplot_graph_2)
        button.pack()
        page2.mainloop()   

    def stationary_graph():
        page.destroy()
        page2 = tk.Tk()
        page2.wm_title('Stationary graph tutorial')
        label = ttk.Label(page2, text = 'Stationary Graph', font = 'arial 10 bold')
        label.pack()
        label2 = ttk.Label(page2, text = 'The Stationary graph enables the user to view the behaviour of sensors.\nEnter the sensor number, property and time interval to model.\nPress Enter to display figure.', font = 'arial 9')
        label2.pack()
        page2.mainloop()

    page = tk.Tk()
    page.wm_title('Tutorial')
    label = ttk.Label(page, text = 'What do you need help with?', font = 'arial 10 bold')
    label.pack(side = 'top', fill = 'x', pady = 10)
    B1 = ttk.Button(page, text = 'The Stationary Graph', command=stationary_graph)
    B1.pack()
    B2 = ttk.Button(page, text = 'The Multiple Graph', command = multiplot_graph)
    B2.pack()
    B3 = ttk.Button(page, text = 'The Bar Chart', command = bar_chart)
    B3.pack()
    B4 = ttk.Button(page, text = 'Simulation', command = simulation)
    B4.pack()


