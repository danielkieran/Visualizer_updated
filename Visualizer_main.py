#LIBRARIES
import tkinter as tk
from pathlib import Path
from Visualizer_pages import *
##### BASELINE #######
class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        self._running_anim = None
        tk.Tk.__init__(self, *args, **kwargs)
        # data_folder = Path('/Images/')
        # tk.Tk.iconbitmap(self, default= data_folder / 'icon.ico') #set icon for applicatiob
        tk.Tk.wm_title(self, "Visualizer of sensor network") # define tab title
        container = tk.Frame(self) # frame for menu
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight =1)
        container.grid_columnconfigure(0, weight =1)
        menubar = tk.Menu(container) # creates top level menu

        ## File_Menu ##
        filemenu = tk.Menu(menubar, tearoff=0) #tearoff is the cut lines
        filemenu.add_command(label="Save Settings", command = lambda: popupmsg("Not supported just yet"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit) # add pulldown commands
        menubar.add_cascade(label="File", menu = filemenu) # add pulldown to parent Menu


        ### Edit ###
        displaymenu = tk.Menu(menubar, tearoff = 1)
        displaymenu.add_command(label = "Network Details", command = lambda: self.show_frame(Network))
        displaymenu.add_command(label = "Live Graph", command = lambda: self.show_frame(GraphPage))
        displaymenu.add_command(label = "Bar Charts", command = lambda: self.show_frame(BarCharts))
        displaymenu.add_command(label="Single Plot Graph", command = lambda: self.show_frame(Station_Graph))
        displaymenu.add_command(label="Multiple Plot Graph", command = lambda: self.show_frame(MultiPage))
        displaymenu.add_command(label = "Search Day", command = lambda: self.show_frame(SearchDay))
        menubar.add_cascade(label="View", menu = displaymenu)

        ### Tutorial ###
        tutorialmenu = tk.Menu(menubar, tearoff = 1)
        tutorialmenu.add_command(label = "Play", command = lambda: tutorial_page())
        menubar.add_cascade(label="Tutorial", menu = tutorialmenu)


        ### Display ###
        tk.Tk.config(self,menu=menubar) 


        #equals empty dictionary
        self.frames = {} 
        
        for F in (BeginPage, MainPage, Station_Graph, GraphPage, BarCharts, MultiPage, Multi_Graph_2, Multi_Graph_3, Multi_Graph_4, Data_Text, Simulator, Other_Options, Insert_Data, SearchDay, Network): 
            # initialise pages and place in same position
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #show_frame shows the frame that we want to see
        self.show_frame(BeginPage) # the first page of program
        
    def show_frame(self, cont): 
        frame = self.frames[cont]
        frame.tkraise()
        frame.canvas.draw_idle()
        #tkraise raises the frame to the top
        
app = Application() #creates object of application
app.geometry("1280x720") #size of program window
ani1 = animation.FuncAnimation(f, animate, interval=500, blit = False) #animate object for GraphPage graph
ani2 = animation.FuncAnimation(f2, animate2, interval=500, blit = False) #animate object for MainPage graph
app.mainloop() #runs the program infinitely