# import libraries
import tkinter as tk #used for widgets
import pandas as pd #used for data manipulation
import numpy as np #used for data manipulation
import matplotlib #used for figures
matplotlib.use("TkAgg") #used to place figures on tkinter windows
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk #backend of matplotlib
from matplotlib.figure import Figure
import matplotlib.animation as animation #used for live graph
from matplotlib import style #used to change the style of matplotlib
import matplotlib.dates as mdates #for the time axis of graphs
from datetime import date #to convert seconds to dat format
from datetime import timedelta #to take away from datetime to display time on graph titles
from pathlib import Path
style.use("seaborn-whitegrid") #style of matplotlib charts

#global fonts for widgets to use
LARGE_FONT = ("Verdana", 14)
NORM_FONT = ("Verdana", 12, "bold")
SMALL_FONT = ("Verdana", 8)

#changes the hr/min/sec format to seconds
def date_to_seconds(hr, min, sec): 
    total = (hr*3600) + (min*60) + sec
    return total


## Pop-up message code
def popupmsg(msg): #function to create a popup
    popup = tk.Tk()

    def break_popup():
        popup.destroy()

    popup.wm_title("Notification")
    label = tk.ttk.Label(popup, text = msg, font=NORM_FONT)
    label.pack(side="top", fill = "x", pady=10)
    B1 = tk.ttk.Button(popup, text = "Okay", command = break_popup)
    B1.pack()
    popup.mainloop


#The function below was used to try graph with, but lead to errors as discussed in Evaluations - encountered issues section
#    
# def convert(seconds): 
#     min, sec = divmod(seconds, 60) 
#     hour, min = divmod(min, 60) 
#     return "%d:%02d:%02d" % (hour, min, sec) 
      

## Plots the stationary graph
def station_with_sensor(frame, sensor, start, end, graph_type):

    top = tk.Toplevel(frame) # application window of the graph
    top.title("Sensor " + str(sensor) + " - " + graph_type) # title of graph window
    sensor_folder = Path('generated_data/')
    s = "sensor_id_" + str(sensor) + ".csv" # reads sensor file
    df = pd.read_csv(sensor_folder / s)  # dataframe
    df = df[df['time_of_transmission'] > start] # filters lower time
    df = df[df['time_of_transmission'] < end] # filters higher time
    df['time_of_transmission'] = df['time_of_transmission'].astype('float64') 
    df['time_as_date'] = np.array(df["time_of_transmission"]).astype("datetime64[s]")
    df['time_as_date']  = df['time_as_date'] + timedelta(days=12472)
    time_dates = (df['time_as_date']).tolist()



    start_time = str(timedelta(seconds=start))
    end_time = str(timedelta(seconds=end))
    

    ## For graph type 'All' , since the x-axis is short is length, it will only display in hour format because it can't fit the day/date on the axis

    if(graph_type == "All"):
        #Plotting Humidity
        label = tk.Label(top, text= "Graphs of Sensor " + str(sensor) + " between " + start_time + " - " + end_time, font=NORM_FONT) # title of graph
        label.pack(pady=10, padx = 10)
        f = Figure(figsize=(1,0.5), dpi=100) #figure for humidity
        a = f.add_subplot(111)
        a.set_ylabel('Humidity')
        a.set_ylabel('%', rotation = 0,  fontsize = 10, labelpad = 10)
        a.set_xlabel('Time', fontsize = 10, labelpad = 10)
        a.plot_date(time_dates, df["hum_value"], 'b.-', label = 'Humidity') #plot humidity
        a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0) #adds legend
  
        a.xaxis_date() 
        a.xaxis.set_major_formatter(mdates.DateFormatter("%H")) #Hour format since the x-axis length is too short for date format even for long durations

        #Embedding Humidity
        f_frame = tk.Canvas(top, bg = 'white', height = 400, width = 400)
        f_frame.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)  
        f_frame.pack_propagate(0)   #prevents window from changing shape
        canvas = FigureCanvasTkAgg(f,f_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True) 
        toolbar = NavigationToolbar2Tk(canvas, f_frame)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True) 

        #Plotting Temperature
        f2 = Figure(figsize=(1, 0.5), dpi=100) #figure for temperature
        a2 = f2.add_subplot(111)
        a2.set_ylabel('°C', rotation = 0,  fontsize = 10, labelpad = 10)
        a2.set_xlabel('Time', fontsize = 10, labelpad = 10)
        a2.plot_date(time_dates, df["tem_value"], 'r.-', label = 'Temperature') #plot temperature
        a2.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
     
        a2.xaxis_date()
        a2.xaxis.set_major_formatter(mdates.DateFormatter("%H")) #Hour format since the x-axis length is too short for date format even for long durations
      
        #Embedding Temperature
        f_frame_2 = tk.Canvas(top, bg = 'white', height = 400, width = 400)
        f_frame_2.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        f_frame_2.pack_propagate(0) #prevents window from changing shape
        canvas2 = FigureCanvasTkAgg(f2,f_frame_2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        toolbar2 = NavigationToolbar2Tk(canvas2, f_frame_2)
        toolbar2.update()
        canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)

        #Plotting Energy-level
        f3 = Figure(figsize=(1,0.5), dpi=100) #figure for energy level
        a3 = f3.add_subplot(111)
        a3.set_ylabel('V', rotation = 0,  fontsize = 10, labelpad = 10)
        a3.set_xlabel('Time',fontsize = 10, labelpad = 10)
        a3.plot_date(time_dates, df["energy_level"], 'g.-', label = 'Energy-level') #plot energy level
        a3.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
 
        a3.xaxis_date()
        a3.xaxis.set_major_formatter(mdates.DateFormatter("%H")) #Hour format since the x-axis length is too short for date format even for long durations

        #Embedding energy level 
        f_frame_3 = tk.Canvas(top, bg = 'white', width = 400, height = 400)
        f_frame_3.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        f_frame_3.pack_propagate(0) #prevents window from changing shape
        canvas3 = FigureCanvasTkAgg(f3,f_frame_3)
        canvas3.draw()
        canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        toolbar3 = NavigationToolbar2Tk(canvas3, f_frame_3)
        toolbar3.update()
        canvas3._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)

    else:

        if(graph_type == "Humidity"):
            label = tk.Label(top, text= graph_type + " graph of Sensor " + str(sensor) + " for " + start_time + " - " + end_time, font=NORM_FONT) # title of graph
            label.pack(pady=10, padx = 10)
            f = Figure(figsize=(4,2), dpi=100) #4x2 inches , dpi is resolution of image
            a = f.add_subplot(111) # adds an axes to figure
            a.set_title(graph_type + " graph of Sensors " + str(sensor) + "\nfor " + start_time + " - " + end_time)
            a.set_ylabel('%', rotation = 0,  fontsize = 20, labelpad = 20)
            a.set_xlabel('Time', fontsize = 11, labelpad = 11)
            a.plot_date(time_dates , df["hum_value"], 'b.-', label = graph_type)
            a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0) # legend placement
            if((end - start) < 216000): #if below 2.5 days, have in hour format
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%H"))
            if(216000<= (end - start)): #if above 2.5 days, have in day format
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%D"))
            

        elif(graph_type == "Temperature"):
            label = tk.Label(top, text= graph_type + " graph of Sensor " + str(sensor) + " for " + start_time + " - " + end_time, font=NORM_FONT)
            label.pack(pady=10, padx = 10)
            f = Figure(figsize=(4,2), dpi=100)
            a = f.add_subplot(111)
            a.set_title(graph_type + " graph of Sensors " + str(sensor) + "\nfor " + start_time + " - " + end_time)
            a.set_ylabel('°C', rotation = 0,  fontsize = 20, labelpad = 20)
            a.set_xlabel('Time', fontsize = 11, labelpad = 11)
            a.plot_date(time_dates , df["tem_value"], 'r.-', label = graph_type)
            a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
            if((end - start) < 216000): #if below 2.5 days, have in hour format
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%H"))
            if(216000<= (end - start)): #if above 2.5 days, have in day format
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%D"))
           
            
        elif(graph_type == "Energy-Level"):
            label = tk.Label(top, text= graph_type + " graph of Sensor " + str(sensor) + " for " + start_time + " - " + end_time, font=NORM_FONT)
            label.pack(pady=10, padx = 10)
            f = Figure(figsize=(4,2), dpi=100)
            a = f.add_subplot(111)
            a.set_title(graph_type + " graph of Sensors " + str(sensor) + "\nfor " + start_time + " - " + end_time)
            a.set_ylabel('V', rotation = 0,  fontsize = 20, labelpad = 20)
            a.set_xlabel('Time', fontsize = 11, labelpad = 11)
            a.plot_date(time_dates , df["energy_level"], 'g.-', label = graph_type)
            a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
            if((end - start) < 216000): #if below 2.5 days, have in day format
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%H"))
            if(216000<= (end - start)): #if above 2.5 days, have in day format
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%D"))

        # embeds figure to window ’top ’ for display
        canvas = FigureCanvasTkAgg(f,top) # backend of matplotlib
        canvas.draw() # display canvas on window
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True) # place in window
        # navigation bar
        toolbar = NavigationToolbar2Tk(canvas, top) # backend of matplotlib
        toolbar.update() # updates navigation bar following interaction
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True) # place in window



## Multiplot 2 ##
def multi_plot2(frame, sensor, sensor2, start, end, graph_type):

    top = tk.Toplevel(frame)
    top.title('Sensor ' + str(sensor) + ', ' + str(sensor2) + ' - ' + graph_type)
    sensor_folder = Path('generated_data/')
    s = "sensor_id_" + str(sensor) + ".csv" # reads sensor file
    df = pd.read_csv(sensor_folder / s) #read first sensor csv
    df = df[df['time_of_transmission'] > start]
    df = df[df['time_of_transmission'] < end] # be careful with the dataframe index
    df['time_of_transmission'] = df['time_of_transmission'].astype('float64') 
    df['time_as_date'] = np.array(df["time_of_transmission"]).astype("datetime64[s]")
    df['time_as_date']  = df['time_as_date'] + timedelta(days=12472)
    time_dates = (df['time_as_date']).tolist() #Gather the first time dates
    
    s2 = 'sensor_id_' + str(sensor2) + '.csv'
    df2 = pd.read_csv(sensor_folder / s2) #read the second sensor csv
    df2 = df2[df2['time_of_transmission'] > start]
    df2 = df2[df2['time_of_transmission'] < end] # be careful with the dataframe index
    df2['time_of_transmission'] = df2['time_of_transmission'].astype('float64') 
    df2['time_as_date'] = np.array(df2["time_of_transmission"]).astype("datetime64[s]")
    df2['time_as_date']  = df2['time_as_date'] + timedelta(days=12472)
    time_dates2 = (df2['time_as_date']).tolist() #Gather the second time dates

    start_time = str(timedelta(seconds=start)) #string of times to use for title
    end_time = str(timedelta(seconds=end))
    

    if(graph_type == "All"):
        label = tk.Label(top, text= "Graphs of Sensor " + str(sensor) + ', ' + str(sensor2) + ' between ' + start_time + ' - ' + end_time, font=NORM_FONT)
        label.pack(pady=10, padx = 10)
        f = Figure(figsize=(1,0.5), dpi=100)
        a = f.add_subplot(111)
        a.set_ylabel('Humidity')
        a.set_ylabel('%', rotation = 0,  fontsize = 10, labelpad = 10)
        a.set_xlabel('Time', fontsize = 10, labelpad = 10)
        a.plot_date(time_dates, df['hum_value'], 'b.-', label = 'Sensor ' + str(sensor)) #plot of first sensor humidity
        a.plot_date(time_dates2, df2['hum_value'], 'c.-', label = 'Sensor ' + str(sensor2)) #plot of second sensor humidity
        a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
        a.xaxis_date()
        a.xaxis.set_major_formatter(mdates.DateFormatter("%H"))
   
        f_frame = tk.Canvas(top, bg = 'white', height = 400, width = 400)
        f_frame.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)  
        f_frame.pack_propagate(0)   
        canvas = FigureCanvasTkAgg(f,f_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True) 
        toolbar = NavigationToolbar2Tk(canvas, f_frame)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True) 
    
        f2 = Figure(figsize=(1, 0.5), dpi=100)
        a2 = f2.add_subplot(111)
        a2.set_ylabel('°C', rotation = 0,  fontsize = 10, labelpad = 10)
        a2.set_xlabel('Time', fontsize = 10, labelpad = 10)
        a2.plot_date(time_dates, df['tem_value'], 'r.-', label = 'Sensor ' + str(sensor)) #plot of first sensor temperature
        a2.plot_date(time_dates2, df2['tem_value'], 'm.-', label = 'Sensor ' + str(sensor2)) #plot of second sensor temperature
        a2.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
        a2.xaxis_date()
        a2.xaxis.set_major_formatter(mdates.DateFormatter("%H"))
 
        f_frame_2 = tk.Canvas(top, bg = 'white', height = 400, width = 400)
        f_frame_2.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        f_frame_2.pack_propagate(0)
        canvas2 = FigureCanvasTkAgg(f2,f_frame_2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        toolbar2 = NavigationToolbar2Tk(canvas2, f_frame_2)
        toolbar2.update()
        canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)

        f3 = Figure(figsize=(1,0.5), dpi=100)
        a3 = f3.add_subplot(111)
        a3.set_ylabel('V', rotation = 0,  fontsize = 10, labelpad = 10)
        a3.set_xlabel('Time',fontsize = 10, labelpad = 10)
        a3.plot_date(time_dates, df['energy_level'], 'g.-', label = 'Sensor ' + str(sensor)) #plot of first sencor energy level
        a3.plot_date(time_dates2, df2['energy_level'], 'c.-', label = 'Sensor ' + str(sensor2)) #plot of second sensor temperature
        a3.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
        a3.xaxis_date()
        a3.xaxis.set_major_formatter(mdates.DateFormatter("%H"))
        
        f_frame_3 = tk.Canvas(top, bg = 'white', width = 400, height = 400)
        f_frame_3.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        f_frame_3.pack_propagate(0)
        canvas3 = FigureCanvasTkAgg(f3,f_frame_3)
        canvas3.draw()
        canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        toolbar3 = NavigationToolbar2Tk(canvas3, f_frame_3)
        toolbar3.update()
        canvas3._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)




    else:

        if(graph_type == "Humidity"):
            label = tk.Label(top, text= "Graphs of Sensor " + str(sensor) + ', ' + str(sensor2) + ' between ' + start_time + ' - ' + end_time, font=NORM_FONT)
            label.pack(pady=10, padx = 10)
            f = Figure(figsize=(4,2), dpi=100)
            a = f.add_subplot(111)
            a.set_title(graph_type + " graph of Sensors " + str(sensor) + ', ' + str(sensor2) + "\nfor " + start_time + " - " + end_time)
            a.set_ylabel('%', rotation = 0,  fontsize = 20, labelpad = 20)
            a.set_xlabel('Time', fontsize = 11, labelpad = 11)
            a.plot_date(time_dates, df['hum_value'], 'b.-', label = 'Sensor ' + str(sensor))
            a.plot_date(time_dates2, df2['hum_value'], 'c.-', label = 'Sensor ' + str(sensor2))
            a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
            if((end - start) < 216000): #if below 2.5 days, have in day format
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%H"))
            if(216000<= (end - start)): #if above 2.5 days, have in day format
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%D"))
          
            

        elif(graph_type == "Temperature"):
            label = tk.Label(top, text= "Graphs of Sensor " + str(sensor) + ', ' + str(sensor2) + ' between ' + start_time + ' - ' + end_time, font=NORM_FONT)
            label.pack(pady=10, padx = 10)
            f = Figure(figsize=(4,2), dpi=100)
            a = f.add_subplot(111)
            a.set_title(graph_type + " graph of Sensors " + str(sensor) + ', ' + str(sensor2) + "\nfor " + start_time + " - " + end_time)
            a.set_ylabel('°C', rotation = 0,  fontsize = 20, labelpad = 20)
            a.set_xlabel('Time', fontsize = 11, labelpad = 11)
            a.plot_date(time_dates, df['tem_value'], 'r.-', label = 'Sensor ' + str(sensor))
            a.plot_date(time_dates2, df2['tem_value'], 'm.-', label = 'Sensor ' + str(sensor2))
            a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
            if((end - start) < 216000): #if below 2.5 days, have in day format
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%H"))
            if(216000<= (end - start)): #if above 2.5 days, have in day format
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%D"))

            

        elif(graph_type == "Energy-Level"):
            label = tk.Label(top, text= "Graphs of Sensor " + str(sensor) + ', ' + str(sensor2) + ' between ' + start_time + ' - ' + end_time, font=NORM_FONT)
            label.pack(pady=10, padx = 10)
            f = Figure(figsize=(4,2), dpi=100)
            a = f.add_subplot(111)
            a.set_title(graph_type + " graph of Sensors " + str(sensor) + ', ' + str(sensor2) + "\nfor " + start_time + " - " + end_time)
            a.set_ylabel('V', rotation = 0,  fontsize = 20, labelpad = 20)
            a.set_xlabel('Time', fontsize = 11, labelpad = 11)
            a.plot_date(time_dates, df['energy_level'], 'g.-', label = 'Sensor ' + str(sensor))
            a.plot_date(time_dates2, df2['energy_level'], 'c.-', label = 'Sensor ' + str(sensor2))
            a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
            if((end - start) < 216000): #if below 2.5 days, have in day format
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%H"))
            if(216000<= (end - start)): #if above 2.5 days, have in day format
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%D"))
     

        canvas = FigureCanvasTkAgg(f,top)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, top)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



## Multiplot 3 ##
def multi_plot3(frame, sensor, sensor2, sensor3, start, end, graph_type):

    #read from sensor 1
    top = tk.Toplevel(frame)
    top.title('Sensor ' + str(sensor) + ', ' + str(sensor2) + ', ' + str(sensor3) + ' - ' + graph_type)
    sensor_folder = Path('generated_data/')
    s = 'sensor_id_' + str(sensor) + '.csv'
    df = pd.read_csv(sensor_folder / s) 
    df = df[df['time_of_transmission'] > start]
    df = df[df['time_of_transmission'] < end] 
    df['time_of_transmission'] = df['time_of_transmission'].astype('float64') 
    df['time_as_date'] = np.array(df["time_of_transmission"]).astype("datetime64[s]")
    df['time_as_date']  = df['time_as_date'] + timedelta(days=12472)
    time_dates = (df['time_as_date']).tolist()
    
    #read from sensor 2
    s2 = 'sensor_id_' + str(sensor2) + '.csv'
    df2 = pd.read_csv(sensor_folder /s2) 
    df2 = df2[df2['time_of_transmission'] > start]
    df2 = df2[df2['time_of_transmission'] < end] 
    df2['time_of_transmission'] = df2['time_of_transmission'].astype('float64') 
    df2['time_as_date'] = np.array(df2["time_of_transmission"]).astype("datetime64[s]")
    df2['time_as_date']  = df2['time_as_date'] + timedelta(days=12472)
    time_dates2 = (df2['time_as_date']).tolist()

    #read from sensor 3
    s3 = 'sensor_id_' + str(sensor3) + '.csv'
    df3 = pd.read_csv(sensor_folder /s3) 
    df3 = df3[df3['time_of_transmission'] > start]
    df3 = df3[df3['time_of_transmission'] < end] 
    df3['time_of_transmission'] = df3['time_of_transmission'].astype('float64') 
    df3['time_as_date'] = np.array(df3["time_of_transmission"]).astype("datetime64[s]")
    df3['time_as_date']  = df3['time_as_date'] + timedelta(days=12472)
    time_dates3 = (df3['time_as_date']).tolist()

    #times for dates on title
    start_time = str(timedelta(seconds=start))
    end_time = str(timedelta(seconds=end))
    

    if(graph_type == "All"):
        label = tk.Label(top, text= "Graphs of Sensor " + str(sensor) + ', ' + str(sensor2) + ', ' + str(sensor3) + ' between ' + start_time + ' - ' + end_time, font=NORM_FONT)
        label.pack(pady=10, padx = 10)
        f = Figure(figsize=(1,0.5), dpi=100)
        a = f.add_subplot(111)
        a.set_ylabel('Humidity')
        a.set_ylabel('%', rotation = 0,  fontsize = 10, labelpad = 10)
        a.set_xlabel('Time', fontsize = 10, labelpad = 10)
        a.plot_date(time_dates, df['hum_value'], 'b.-', label = 'Sensor ' + str(sensor))
        a.plot_date(time_dates2, df2['hum_value'], 'c.-', label = 'Sensor ' + str(sensor2))
        a.plot_date(time_dates3, df3['hum_value'], '.-', label = 'Sensor ' + str(sensor3))
        a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
        a.xaxis_date()
        a.xaxis.set_major_formatter(mdates.DateFormatter("%H"))

        f_frame = tk.Canvas(top, bg = 'white', height = 400, width = 400)
        f_frame.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)  
        f_frame.pack_propagate(0)   
        canvas = FigureCanvasTkAgg(f,f_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True) 
        toolbar = NavigationToolbar2Tk(canvas, f_frame)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True) 
    
        f2 = Figure(figsize=(1, 0.5), dpi=100)
        a2 = f2.add_subplot(111)
        a2.set_ylabel('°C', rotation = 0,  fontsize = 10, labelpad = 10)
        a2.set_xlabel('Time', fontsize = 10, labelpad = 10)
        a2.plot_date(time_dates, df['tem_value'], 'r.-', label = 'Sensor ' + str(sensor))
        a2.plot_date(time_dates2, df2['tem_value'], 'm.-', label = 'Sensor ' + str(sensor2))
        a2.plot_date(time_dates3, df3['tem_value'], '.-', label = 'Sensor ' + str(sensor3))
        a2.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
        a2.xaxis_date()
        a2.xaxis.set_major_formatter(mdates.DateFormatter("%H"))

        f_frame_2 = tk.Canvas(top, bg = 'white', height = 400, width = 400)
        f_frame_2.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        f_frame_2.pack_propagate(0)
        canvas2 = FigureCanvasTkAgg(f2,f_frame_2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        toolbar2 = NavigationToolbar2Tk(canvas2, f_frame_2)
        toolbar2.update()
        canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)

        f3 = Figure(figsize=(1,0.5), dpi=100)
        a3 = f3.add_subplot(111)
        a3.set_ylabel('V', rotation = 0,  fontsize = 10, labelpad = 10)
        a3.set_xlabel('Time',fontsize = 10, labelpad = 10)
        a3.plot_date(time_dates, df['energy_level'], 'g.-', label = 'Sensor ' + str(sensor))
        a3.plot_date(time_dates2, df2['energy_level'], 'c.-', label = 'Sensor ' + str(sensor2))
        a3.plot_date(time_dates3, df3['energy_level'], '.-', label = 'Sensor ' + str(sensor3))
        a3.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
        a3.xaxis_date()
        a3.xaxis.set_major_formatter(mdates.DateFormatter("%H"))

        f_frame_3 = tk.Canvas(top, bg = 'white', width = 400, height = 400)
        f_frame_3.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        f_frame_3.pack_propagate(0)
        canvas3 = FigureCanvasTkAgg(f3,f_frame_3)
        canvas3.draw()
        canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        toolbar3 = NavigationToolbar2Tk(canvas3, f_frame_3)
        toolbar3.update()
        canvas3._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)

    else:

        if(graph_type == "Humidity"):
            label = tk.Label(top, text= "Graphs of Sensor " + str(sensor) + ', ' + str(sensor2) + ', '+str(sensor3)+' between ' + start_time + ' - ' + end_time, font=NORM_FONT)
            label.pack(pady=10, padx = 10)
            f = Figure(figsize=(4,2), dpi=100)
            a = f.add_subplot(111)
            a.set_title(graph_type + " graph of Sensors " + str(sensor) + ', ' + str(sensor2) + ', ' + str(sensor3) + "\nfor " + start_time + " - " + end_time)
            a.set_ylabel('%', rotation = 0,  fontsize = 20, labelpad = 20)
            a.set_xlabel('Time', fontsize = 11, labelpad = 11)
            a.plot_date(time_dates, df['hum_value'], 'b.-', label = 'Sensor ' + str(sensor))
            a.plot_date(time_dates2, df2['hum_value'], 'c.-', label = 'Sensor ' + str(sensor2))
            a.plot_date(time_dates3, df3['hum_value'], '.-', label = 'Sensor ' + str(sensor3))
            a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
            if((end - start) < 216000): #if below 2.5 days, have in day format
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%H"))
            if(216000<= (end - start)): #if above 2.5 days, have in day format
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%D"))
            

        elif(graph_type == "Temperature"):
            label = tk.Label(top, text= "Graphs of Sensor " + str(sensor) + ', ' + str(sensor2) + ', '+str(sensor3)+' between ' + start_time + ' - ' + end_time, font=NORM_FONT)
            label.pack(pady=10, padx = 10)
            f = Figure(figsize=(4,2), dpi=100)
            a = f.add_subplot(111)
            a.set_title(graph_type + " graph of Sensors " + str(sensor) + ', ' + str(sensor2) + ', ' + str(sensor3) + "\nfor " + start_time + " - " + end_time)
            a.set_ylabel('°C', rotation = 0,  fontsize = 20, labelpad = 20)
            a.set_xlabel('Time', fontsize = 11, labelpad = 11)
            a.plot_date(time_dates, df['tem_value'], 'r.-', label = 'Sensor ' + str(sensor))
            a.plot_date(time_dates2, df2['tem_value'], 'm.-', label = 'Sensor ' + str(sensor2))
            a.plot_date(time_dates3, df3['tem_value'], '.-', label = 'Sensor ' + str(sensor3))
            a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
            if((end - start) < 216000): #if below 2.5 days, have in day format
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%H"))
            if(216000<= (end - start)): #if above 2.5 days, have in day format
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%D"))
           
            

        elif(graph_type == "Energy-Level"):
            label = tk.Label(top, text= "Graphs of Sensor " + str(sensor) + ', ' + str(sensor2) + ', '+str(sensor3)+' between ' + start_time + ' - ' + end_time, font=NORM_FONT)
            label.pack(pady=10, padx = 10)
            f = Figure(figsize=(4,2), dpi=100)
            a = f.add_subplot(111)
            a.set_title(graph_type + " graph of Sensors " + str(sensor) + ', ' + str(sensor2) + ', ' + str(sensor3) + "\nfor " + start_time + " - " + end_time)
            a.set_ylabel('V', rotation = 0,  fontsize = 20, labelpad = 20)
            a.set_xlabel('Time', fontsize = 11, labelpad = 11)
            a.plot_date(time_dates, df['energy_level'], 'g.-', label = 'Sensor ' + str(sensor))
            a.plot_date(time_dates2, df2['energy_level'], 'b.-', label = 'Sensor ' + str(sensor2))
            a.plot_date(time_dates3, df3['energy_level'], '.-', label = 'Sensor ' + str(sensor3))
            a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
            if((end - start) < 216000): #if below 2.5 days, have in day format
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%H"))
            if(216000<= (end - start)): #if above 2.5 days, have in day format
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%D"))

        canvas = FigureCanvasTkAgg(f,top)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, top)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



## MultiPlot4 ##
def multi_plot4(frame, sensor, sensor2, sensor3, sensor4, start, end, graph_type):
    #read from sensor 1
    top = tk.Toplevel(frame)
    top.title('Sensor ' + str(sensor) + ', ' + str(sensor2) + ', ' + str(sensor3) + ', ' + str(sensor4) +' - ' + graph_type)
    sensor_folder = Path('generated_data/')
    s = 'sensor_id_' + str(sensor) + '.csv'
    df = pd.read_csv(sensor_folder / s) 
    df = df[df['time_of_transmission'] > start]
    df = df[df['time_of_transmission'] < end] 
    df['time_of_transmission'] = df['time_of_transmission'].astype('float64') 
    df['time_as_date'] = np.array(df["time_of_transmission"]).astype("datetime64[s]")
    df['time_as_date']  = df['time_as_date'] + timedelta(days=12472)
    time_dates = (df['time_as_date']).tolist()
    
    #read from sensor 1
    s2 = 'sensor_id_' + str(sensor2) + '.csv'
    df2 = pd.read_csv(sensor_folder /s2) 
    df2 = df2[df2['time_of_transmission'] > start]
    df2 = df2[df2['time_of_transmission'] < end] 
    df2['time_of_transmission'] = df2['time_of_transmission'].astype('float64') 
    df2['time_as_date'] = np.array(df2["time_of_transmission"]).astype("datetime64[s]")
    df2['time_as_date']  = df2['time_as_date'] + timedelta(days=12472)
    time_dates2 = (df2['time_as_date']).tolist()

    #read from sensor 1
    s3 = 'sensor_id_' + str(sensor3) + '.csv'
    df3 = pd.read_csv(sensor_folder / s3) 
    df3 = df3[df3['time_of_transmission'] > start]
    df3 = df3[df3['time_of_transmission'] < end] 
    df3['time_of_transmission'] = df3['time_of_transmission'].astype('float64') 
    df3['time_as_date'] = np.array(df3["time_of_transmission"]).astype("datetime64[s]")
    df3['time_as_date']  = df3['time_as_date'] + timedelta(days=12472)
    time_dates3 = (df3['time_as_date']).tolist()

    #read from sensor 1
    s4 = 'sensor_id_' + str(sensor4) + '.csv'
    df4 = pd.read_csv(sensor_folder / s4) 
    df4 = df4[df4['time_of_transmission'] > start]
    df4 = df4[df4['time_of_transmission'] < end] 
    df4['time_of_transmission'] = df4['time_of_transmission'].astype('float64') 
    df4['time_as_date'] = np.array(df4["time_of_transmission"]).astype("datetime64[s]")
    df4['time_as_date']  = df4['time_as_date'] + timedelta(days=12472)
    time_dates4 = (df4['time_as_date']).tolist()

    #times for title
    start_time = str(timedelta(seconds=start))
    end_time = str(timedelta(seconds=end))
    

    if(graph_type == "All"):
        label = tk.Label(top, text= "Graphs of Sensor " + str(sensor) + ', ' + str(sensor2) + ', ' + str(sensor3) + ', ' + str(sensor4) +' between ' + start_time + ' - ' + end_time, font=NORM_FONT)
        label.pack(pady=10, padx = 10)
        f = Figure(figsize=(1,0.5), dpi=100)
        a = f.add_subplot(111)
        a.set_ylabel('Humidity')
        a.set_ylabel('%', rotation = 0,  fontsize = 10, labelpad = 10)
        a.set_xlabel('Time', fontsize = 10, labelpad = 10)
        a.plot_date(time_dates, df['hum_value'], 'b.-', label = 'Sensor ' + str(sensor))
        a.plot_date(time_dates2, df2['hum_value'], 'c.-', label = 'Sensor ' + str(sensor2))
        a.plot_date(time_dates3, df3['hum_value'], '.-', label = 'Sensor ' + str(sensor3))
        a.plot_date(time_dates4, df4['hum_value'], '.-', label = 'Sensor ' + str(sensor4))
        a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
        a.xaxis_date()
        a.xaxis.set_major_formatter(mdates.DateFormatter("%H"))

        f_frame = tk.Canvas(top, bg = 'white', height = 400, width = 400)
        f_frame.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)  
        f_frame.pack_propagate(0)   
        canvas = FigureCanvasTkAgg(f,f_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True) 
        toolbar = NavigationToolbar2Tk(canvas, f_frame)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True) 
    
        f2 = Figure(figsize=(1, 0.5), dpi=100)
        a2 = f2.add_subplot(111)
        a2.set_ylabel('°C', rotation = 0,  fontsize = 10, labelpad = 10)
        a2.set_xlabel('Time', fontsize = 10, labelpad = 10)
        a2.plot_date(time_dates, df['tem_value'], 'r.-', label = 'Sensor ' + str(sensor))
        a2.plot_date(time_dates2, df2['tem_value'], 'm.-', label = 'Sensor ' + str(sensor2))
        a2.plot_date(time_dates3, df3['tem_value'], '.-', label = 'Sensor ' + str(sensor3))
        a2.plot_date(time_dates3, df3['tem_value'], '.-', label = 'Sensor ' + str(sensor4))
        a2.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
        a2.xaxis_date()
        a2.xaxis.set_major_formatter(mdates.DateFormatter("%H"))

        f_frame_2 = tk.Canvas(top, bg = 'white', height = 400, width = 400)
        f_frame_2.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        f_frame_2.pack_propagate(0)
        canvas2 = FigureCanvasTkAgg(f2,f_frame_2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        toolbar2 = NavigationToolbar2Tk(canvas2, f_frame_2)
        toolbar2.update()
        canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)

        f3 = Figure(figsize=(1,0.5), dpi=100)
        a3 = f3.add_subplot(111)
        a3.set_ylabel('V', rotation = 0,  fontsize = 10, labelpad = 10)
        a3.set_xlabel('Time',fontsize = 10, labelpad = 10)
        a3.plot_date(time_dates, df['energy_level'], 'g.-', label = 'Sensor ' + str(sensor))
        a3.plot_date(time_dates2, df2['energy_level'], 'c.-', label = 'Sensor ' + str(sensor2))
        a3.plot_date(time_dates3, df3['energy_level'], '.-', label = 'Sensor ' + str(sensor3))
        a3.plot_date(time_dates4, df4['energy_level'], '.-', label = 'Sensor ' + str(sensor4))
        a3.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
        a3.xaxis_date()
        a3.xaxis.set_major_formatter(mdates.DateFormatter("%H"))

        f_frame_3 = tk.Canvas(top, bg = 'white', width = 400, height = 400)
        f_frame_3.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        f_frame_3.pack_propagate(0)
        canvas3 = FigureCanvasTkAgg(f3,f_frame_3)
        canvas3.draw()
        canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        toolbar3 = NavigationToolbar2Tk(canvas3, f_frame_3)
        toolbar3.update()
        canvas3._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)

    else:

        if(graph_type == "Humidity"):
            label = tk.Label(top, text= "Graphs of Sensor " + str(sensor) + ', ' + str(sensor2) + ', '+str(sensor3) + ', ' + str(sensor4) + ' between ' + start_time + ' - ' + end_time, font=NORM_FONT)
            label.pack(pady=10, padx = 10)
            f = Figure(figsize=(4,2), dpi=100)
            a = f.add_subplot(111)
            a.set_title(graph_type + " graph of Sensors " + str(sensor) + ', ' + str(sensor2) + ', ' + str(sensor3) + ', ' + str(sensor4) + "\nfor " + start_time + " - " + end_time)
            a.set_ylabel('%', rotation = 0,  fontsize = 20, labelpad = 20)
            a.set_xlabel('Time', fontsize = 11, labelpad = 11)
            a.plot_date(time_dates, df['hum_value'], 'b.-', label = 'Sensor ' + str(sensor))
            a.plot_date(time_dates2, df2['hum_value'], 'c.-', label = 'Sensor ' + str(sensor2))
            a.plot_date(time_dates3, df3['hum_value'], 'g.-', label = 'Sensor ' + str(sensor3))
            a.plot_date(time_dates4, df4['hum_value'], 'm.-', label = 'Sensor ' + str(sensor4))
            a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
            if((end - start) < 216000):
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%H"))
            if(216000<= (end - start)):
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%D"))
            

        elif(graph_type == "Temperature"):
            label = tk.Label(top, text= "Graphs of Sensor " + str(sensor) + ', ' + str(sensor2) + ', '+str(sensor3) + ', ' + str(sensor4) + ' between ' + start_time + ' - ' + end_time, font=NORM_FONT)
            label.pack(pady=10, padx = 10)
            f = Figure(figsize=(4,2), dpi=100)
            a = f.add_subplot(111)
            a.set_title(graph_type + " graph of Sensors " + str(sensor) + ', ' + str(sensor2) + ', ' + str(sensor3) + ', ' + str(sensor4) + "\nfor " + start_time + " - " + end_time)
            a.set_ylabel('°C', rotation = 0,  fontsize = 20, labelpad = 20)
            a.set_xlabel('Time', fontsize = 11, labelpad = 11)
            a.plot_date(time_dates, df['tem_value'], 'r.-', label = 'Sensor ' + str(sensor))
            a.plot_date(time_dates2, df2['tem_value'], 'm.-', label = 'Sensor ' + str(sensor2))
            a.plot_date(time_dates3, df3['tem_value'], 'g.-', label = 'Sensor ' + str(sensor3))
            a.plot_date(time_dates4, df4['tem_value'], 'b.-', label = 'Sensor ' + str(sensor4))
            a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
            if((end - start) < 216000):
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%H"))
            if(216000<= (end - start)):
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%D"))
           
            

        elif(graph_type == "Energy-Level"):
            label = tk.Label(top, text= "Graphs of Sensor " + str(sensor) + ', ' + str(sensor2) + ', '+str(sensor3) + ', ' + str(sensor4) + ' between ' + start_time + ' - ' + end_time, font=NORM_FONT)
            label.pack(pady=10, padx = 10)
            f = Figure(figsize=(4,2), dpi=100)
            a = f.add_subplot(111)
            a.set_title(graph_type + " graph of Sensors " + str(sensor) + ', ' + str(sensor2) + ', ' + str(sensor3) + ', ' + str(sensor4) + "\nfor " + start_time + " - " + end_time)
            a.set_ylabel('V', rotation = 0,  fontsize = 20, labelpad = 20)
            a.set_xlabel('Time', fontsize = 11, labelpad = 11)
            a.plot_date(time_dates, df['energy_level'], 'g.-', label = 'Sensor ' + str(sensor))
            a.plot_date(time_dates2, df2['energy_level'], 'c.-', label = 'Sensor ' + str(sensor2))
            a.plot_date(time_dates3, df3['energy_level'], '.-', label = 'Sensor ' + str(sensor3))
            a.plot_date(time_dates4, df4['energy_level'], '.-', label = 'Sensor ' + str(sensor4))
            a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
            if((end - start) < 216000):
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%H"))
            if(216000<= (end - start)):
                a.xaxis_date()
                a.xaxis.set_major_formatter(mdates.DateFormatter("%D"))

        canvas = FigureCanvasTkAgg(f,top)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, top)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


## Plots the bar chart on the figure
def bar_plot(frame, sensor, bar_type):

    top = tk.Toplevel(frame) #creates window to place bar graph
    sensor_folder = Path('generated_data/')
    s = 'sensor_id_' + str(sensor) + '.csv'
    df = pd.read_csv(sensor_folder / s) #reads from selected sensor number
    f = Figure(figsize=(8,4), facecolor='white') # creates figure
    a = f.add_subplot(111) #adds an axes to figure
    a.set_title('Update chart of Sensor ' + str(sensor) + ', mean = '+ str(round(df['update_rate'].mean())), fontsize = 20) # title of graph
    top.title("Sensor " + str(sensor)+ " bar chart")
    df["update_rate_sectioned"] = pd.cut(df.update_rate, [0, 500, 1000, 1500, 2000, 2500], labels=['0-500', '500-1000','1000-1500', '1500-2000', '2000-2500']) #divides data into categories of intervals
    
    if bar_type == 'Relative': # show the relative frequency 
        update_interval = df["update_rate_sectioned"].value_counts(normalize = True, sort = False) # update_interval is a series containing counts of unique values, normalize = true makes it relative frequency
        a.set_ylabel('Relative\nFrequency', fontsize = 12, labelpad = 32, rotation = 0)
        update_interval.plot(kind = 'bar', ax = a, rot = 0, label = 'Update time frequency')
    else:  # show the frequency with quantity
        update_interval = df["update_rate_sectioned"].value_counts(sort = False) # update_interval is a series containing counts of unique values
        a.set_ylabel('Quantity', fontsize = 12, labelpad = 32, rotation = 0)
        update_interval.plot(kind = 'bar', ax = a, rot = 0, label = 'Update time quantity')
    
    a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0) # legend placement
    # Embed the figure to tkinter window ’top ’
    canvas = FigureCanvasTkAgg(f, top)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    toolbar = NavigationToolbar2Tk(canvas, top)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)




## Horizontal bar chart plot
def bar_plot_h(frame, sensor, bar_type):

    top = tk.Toplevel(frame)
    sensor_folder = Path('generated_data/')
    s = 'sensor_id_' + str(sensor) + '.csv'
    df = pd.read_csv(sensor_folder / s)
    f = Figure(figsize=(8,4), facecolor='white')        
    a = f.add_subplot(111)
    a.set_title('Update chart of Sensor ' + str(sensor) + ', mean = '+ str(round(df['update_rate'].mean())), fontsize = 20)
    
    top.title("Sensor " + str(sensor)+ " bar chart")
    df["update_rate_sectioned"] = pd.cut(df.update_rate, [0, 500, 1000, 1500, 2000, 2500], labels=['0-500', '500-1000','1000-1500', '1500-2000', '2000-2500'])
    
    if bar_type == 'Relative':
        update_interval = df["update_rate_sectioned"].value_counts(normalize = True, sort = False)
        a.set_xlabel('Relative\nFrequency', fontsize = 12, labelpad = 32, rotation = 0)
        a.set_ylabel('Update\nrate', fontsize = 12, labelpad = 32, rotation = 0)
        update_interval.plot(kind = 'barh', ax = a, rot = 0, label = 'Update time frequency')
    else:
        update_interval = df["update_rate_sectioned"].value_counts(sort = False)
        a.set_xlabel('Quantity', fontsize = 12, labelpad = 32, rotation = 0)
        a.set_ylabel('Update\nrate', fontsize = 12, labelpad = 32, rotation = 0)
        update_interval.plot(kind = 'barh', ax = a, rot = 0, label = 'Update time quantity')
    
    a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
    canvas = FigureCanvasTkAgg(f, top)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    toolbar = NavigationToolbar2Tk(canvas, top)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)




## Histogram plot ##
## does not effectively work as bins are divided in the number of unique numbers ##
## work in progress ##
def hist_plot(frame, sensor, bar_type, sensor_property):

    top = tk.Toplevel(frame)
    sensor_folder = Path('generated_data/')
    s = 'sensor_id_' + str(sensor) + '.csv'
    df = pd.read_csv(sensor_folder / s)
    f = Figure(figsize=(8,4), facecolor='white')        
    a = f.add_subplot(111)
    top.title("Sensor " + str(sensor)+ " histogram")
    
    if sensor_property == 'Accuracy':
        a.set_title('Accuracy histogram of Sensor ' + str(sensor) + ', mean = '+ str(round(df['accuracy'].mean(), 2)), fontsize = 20)
        if bar_type == 'Relative':
            accuracy_interval = df['accuracy'].value_counts(normalize = True, sort = False)
            a.set_ylabel('Accuracy', fontsize = 12, labelpad = 32, rotation = 0)
            accuracy_interval.plot(kind = 'hist', bins = 20, ax = a, aplha = 0.1, rot = 0, label = 'Accuracy frequency')
        else:
            accuracy_interval = df['accuracy'].value_counts(sort = False)
            a.set_ylabel('Accuracy', fontsize = 12, labelpad = 32, rotation = 0)
            accuracy_interval.plot(kind = 'hist', bins = 20, ax = a, alpha = 0.1, rot = 0, label = 'Accuracy')

    else:
        a.set_title('Update rate histogram of Sensor ' + str(sensor) + ', mean = '+ str(round(df['accuracy'].mean(),2)), fontsize = 20)
        if bar_type == 'Relative':
            accuracy_interval = df['update_rate'].value_counts(normalize = True, sort = False)
            a.set_ylabel('Update rate', fontsize = 12, labelpad = 32, rotation = 0)
            accuracy_interval.plot(kind = 'hist', bins = 20, alpha = 0.25, ax = a, rot = 0, label = 'Update rate frequency')
        else:
            accuracy_interval = df['update_rate'].value_counts(sort = False)
            a.set_ylabel('Update rate', fontsize = 12, labelpad = 32, rotation = 0)
            accuracy_interval.plot(kind = 'hist', bins = 20, alpha = 0.25, ax = a, rot = 0, label = 'Update rate')
    
    a.legend(bbox_to_anchor = (0, 1.02, 1, .102), loc = 3, ncol = 2, borderaxespad = 0)
    canvas = FigureCanvasTkAgg(f, top)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    toolbar = NavigationToolbar2Tk(canvas, top)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)




