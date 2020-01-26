import re
import regex
import pandas as pd
import numpy as np
import networkx as nx
import inspect



class Main():

    def __init__(self):
        #self.TakeInScript("testScript.py")
        self.TakeInScript("testScript.py")
        Static = StaticAnalyses(self.script)
        InputsRun = InputRunning(self.script,'testExcel.xlsx')


    def TakeInScript(self,location):
        self.script = open(location,"r").read()


    def SaveToExcel(self):
        pass

def removeComments(scriptorig):
    script = ""
    for line in scriptorig.splitlines():
        commentstarts = len(line)-1
        if commentstarts == -1:
            continue
        for index,let in enumerate(list(line)):
            if let == "#":
                commentstarts = index-1
                break
        script = script + line[:commentstarts+1] + "\n"
    return script

class StaticAnalyses():
    #Orchestrates all the static analyses
    # data collected = self.NumComments , self.NumLines,
    def __init__(self,script):
        self.script = script
        self.scriptNoComments = removeComments(self.script)
        self.CreateFuncs()
        self.CreateNetGraph()


        self.NumLines()
        self.NumComments()



    def CreateNetGraph(self):
        DG = nx.DiGraph()
        for Func in self.Funcs:
            DG.add_node(Func.getName())
        for Func in self.Funcs:
            for child in Func.getArrFuncsCalled():
                DG.add_weighted_edges_from([(Func.getName(),child.getName(),5)])
        nx.write_graphml(DG, "StaticFuncInteracting.graphml")




    def NumLines(self):
        self.NumLines = len((self.script.splitlines()))


    def NumComments(self):
        self.NumComments = 0
        for line in self.script.splitlines():
            if "#" in line:
                self.NumComments += 1



    def CreateFuncs(self):
        #Creates a Function Object for every function in the script
        self.Funcs = []
        for index,line in enumerate(self.script.splitlines()):
            line2 = line.strip()
            if line2[0:3] == "def":
                self.Funcs.append(Function(self.script,index,self.scriptNoComments))
        #Calls each function object to find out data about themselves
        for Func in self.Funcs:
            Func.FindName()
        for Func in self.Funcs:
            Func.collectData(self.Funcs)




class Function():
    # data collected : self.FuncName, self.FuncText, self.numParameters,
    def __init__(self,script,line,scriptNoComments):
        self.scriptNoComments = scriptNoComments
        self.script = script
        self.line = line
        self.scriptLines = self.script.splitlines()

    def collectData(self,otherFuncs):
        self.Defenition = self.scriptLines[self.line]
        self.otherFuncs = otherFuncs
        self.FuncText = self.getFuncText()
        self.GetFuncsCalled()
        self.FuncInfoDict = self.executeFunctionAndGatherInfo(self.FuncText)
        self.FuncInfoDict["Name"] = self.getName()

    def getArrFuncsCalled(self):
        return self.FuncsCalled

    def executeFunctionAndGatherInfo(self,FuncText):
        #### Need to look at what to do if self
        exec(FuncText,globals())
        codeInfos = {"NumArguments":"argcount","NumLocalVars":"nlocals","StackSize":"stacksize","varNames":"varnames"}
        FuncInfoDict = {}
        for info in codeInfos:
            strEx =  info + " = "+self.getName()+".__code__.co_" + codeInfos[info]
            exec(strEx,globals(),FuncInfoDict)

        return FuncInfoDict





    def GetFuncsCalled(self):
        self.FuncsCalled = set()

        self.FuncTextNoCommas = removeComments(self.FuncText)
        self.FuncLines = self.FuncText.splitlines()
        FuncLines = self.FuncLines[1::]
        names = [Func.getName() for Func in self.otherFuncs]
        #ADD regex looking for names of other functions
        orString = "("
        for item in names:
            orString = orString + item + "|"
        orString = orString[:-1]
        orString = orString + ")"
        OtherFuncCalls = []
        for line in FuncLines:
            matches = re.finditer(orString+r'\(.*\)',line)
            for i in matches:
                OtherFuncCalls.append(i.group(0))
                name = i.group(0).split("(")[0]
                self.FuncsCalled.add(self.getFuncFromName(name,self.otherFuncs))


    def getFuncFromName(self,Name,Funcs):
        for Func in Funcs:
            if Func.getName() == Name:
                return Func
        raise AssertionError("Func name can't be found")





    def getFuncText(self):
        firstLine = list(self.scriptLines[self.line+1])
        for index,let in enumerate(firstLine):
            min = index
            if let != " ":
                break
        finalLine = -1
        for index,line in enumerate(self.scriptLines[self.line+1::]):
            for index2,let in enumerate(list(line)):
                numspaces = index2
                if let != " ":
                    break
            if numspaces < min:
                finalLine = index + 1
                break
        if finalLine == -1:
            self.FuncText = "\n".join(self.scriptLines[self.line::])
        else:
            self.FuncText = "\n".join(self.scriptLines[self.line:finalLine+self.line])
        firstLine = list(self.scriptLines[self.line])
        for index,let in enumerate(firstLine):
            min = index
            if let != " ":
                break
        Function = ""
        for line in self.FuncText.splitlines():
            Function = Function + line[min::] + "\n"
        return Function ###Check This


    def FindName(self):
        self.Defenition = self.scriptLines[self.line]
        self.name =  self.Defenition.split()[1].split("(")[0]

    def getName(self):
        return self.name


class InputRunning():

    def __init__(self,script,excelFile):
        self.script = script
        self.testcases = pd.ExcelFile(excelFile)
        self.FirstSheet = self.testcases.sheet_names[0]
        self.SecondSheet = self.testcases.sheet_names[1]
        self.testcasesSheet = self.testcases.parse(self.FirstSheet)
        self.OutputSheet = self.testcases.parse(self.SecondSheet)
        self.inputData = []
        for j in range(1,len(self.testcasesSheet.columns)+1):
            placeholder = [str(i) if str(i) != '""' else "" for i in self.testcasesSheet[j].to_numpy()]
            self.inputData.append([i if i != '""' else "" for i in placeholder])
        self.Outputs = []
        for j in range(1,len(self.OutputSheet.columns)+1):
            placeholder = [str(i) for i in self.OutputSheet[j].to_numpy() if str(i) != "nan"]
            self.Outputs.append([i if i != '""' else "" for i in placeholder])
        print(self.inputData)
        print(self.Outputs)
        self.RunInputs(self.script,self.inputData)

    def RunInputs(self,script,inputs):
        replacingInputs = regex.compile(r'input(\(((((?1)|[^\(\)])|(\".*\"))|(\'.*\'))*\))')
        scriptWithInputs = replacingInputs.sub('inputsxyzxyz.__next__()', script)
        replacingPrints = re.compile(r"print")
        scriptWithInputs = replacingPrints.sub('saveToVariable', scriptWithInputs)
        AddingDecor = regex.compile(r"(( )*def)")
        scriptWithInputs = AddingDecor.sub("\\2\\2\\2\\2@funcDecorator\n\\1",scriptWithInputs)

        decorString = """import inspect
import time
times = []
def funcDecorator(a_func):
    def wrapTheFunction(*args, **kwargs):
        start = time.time()
        placeholder = a_func(*args, **kwargs)
        times.append(((inspect.stack()[1][3],a_func.__name__),time.time()-start))
        return placeholder
    return wrapTheFunction"""

        scriptWithInputs = decorString + "\n" + scriptWithInputs
        exec("""SavedOutputs = []
def saveToVariable(toSave):
    SavedOutputs.append(toSave)""",globals())
        self.paths = []
        for input in inputs:
            strToExec = "inputsxyzxyz = " + str(input)
            strToExec2 = "inputsxyzxyz = (item for item in inputsxyzxyz)"
            totString = strToExec + "\n" + strToExec2 + "\n" + scriptWithInputs
            exec(totString,globals())
            self.paths.append(times)

        self.SavedOutputs = SavedOutputs



mains = Main()
'''if __name__ == "__main__":
    mains = Main()'''
