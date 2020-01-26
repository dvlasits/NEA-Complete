from tkinter import *
from tkinter import filedialog


def run():
    print("wow this ran")

def askopenfile():
        print(filedialog.askopenfile(mode = 'r').name)

def askopenfileExcel():
        print(filedialog.askopenfile(mode = 'r').name)

def askSaveInfo():
        print(filedialog.askdirectory())

root = Tk()
frame = Frame(root)
frame.pack()
bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )
RunButton = Button(frame, text = 'Run Analyses', fg ='red',width = '25', command = run)
RunButton.pack( side = TOP)
CodeFile = Button(frame, text = 'Find Code File', fg='brown',width = '25', command = askopenfile)
CodeFile.pack( side = BOTTOM )
ExcelFile = Button(frame, text = 'Find Excel File', fg='brown',width = '25', command = askopenfileExcel)
ExcelFile.pack( side = BOTTOM )
SaveInfo = Button(frame, text = 'Where to save info', fg='brown',width = '25', command = askSaveInfo)
SaveInfo.pack( side = BOTTOM )
root.mainloop()
