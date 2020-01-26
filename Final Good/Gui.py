#Packages required
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

#Other files
from AnalysesStart import AnalysesStart


class GUI:

    def __init__(self):
        self.ExcelFile = None
        self.saveLocation = None
        self.root = Tk()
        #Creating Gui Screen
        frame = Frame(self.root)
        frame.pack()
        bottomframe = Frame(self.root)
        CodeFile = Button(frame, text = 'Find Code File', fg='brown',width = '25', command = self.askopenfile)
        CodeFile.pack( side = TOP )
        ExcelFile = Button(frame, text = 'Find Excel File', fg='brown',width = '25', command = self.askopenfileExcel)
        ExcelFile.pack( side = TOP )
        SaveLocation = Button(frame, text = 'Which folder to save?', fg='brown',width = '25', command = self.askSaveInfo)
        SaveLocation.pack( side = TOP )
        bottomframe.pack( side = BOTTOM )
        RunButton = Button(frame, text = 'Run Analyses', fg ='red',width = '25', command = self.run)
        RunButton.pack( side = TOP)


        self.root.mainloop()


    def run(self):
        #Starts the analyses
        messagebox.showinfo("Analyses started","The analyses of your code has begun")
        mains = AnalysesStart(self.CodeFile,self.saveLocation,self.ExcelFile)
        messagebox.showinfo("Analyses complete","The analyses of your code is completed please view all files in the file you saved them")

    def askopenfile(self):
        #get CodeFile Location
        self.CodeFile = filedialog.askopenfile(mode = 'r').name

    def askopenfileExcel(self):
        #get ExcelFileLocation
        self.ExcelFile = filedialog.askopenfile(mode = 'r').name
        print(self.ExcelFile)

    def askSaveInfo(self):
        #Get Save Location
        self.saveLocation = filedialog.askdirectory()
        print(self.saveLocation)
