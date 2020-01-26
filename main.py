
#import openExcelpy


class Main():

    def __init__(self,CodeFile,saveLocation,Excel): # need to implement Excel = None
        if saveLocation is None:
            saveLocation = 'C:/Users/dvlas/Desktop'
        #self.TakeInScript("testScript.py")
        self.TakeInScript(CodeFile)
        Static = StaticAnalyses(self.script,saveLocation)
        funcs = Static.getArrFuncs()

        Dynamic = DynamicAnalyses(self.script,Excel,funcs,saveLocation)


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
    def __init__(self,script,saveLocation):
        self.saveLocation = saveLocation
        self.script = script
        self.scriptNoComments = removeComments(self.script)
        self.CreateFuncs()
        self.CreateNetGraph()
        self.NumLines()
        self.NumComments()

    def getArrFuncs(self):
        return self.Funcs



    def CreateNetGraph(self):
        DG = nx.DiGraph()
        for Func in self.Funcs:
            DG.add_node(Func.getName())
        for Func in self.Funcs:
            for child in Func.getArrFuncsCalled():
                DG.add_edges_from([(Func.getName(),child.getName())])
        nx.write_graphml(DG, self.saveLocation + "/StaticFuncInteracting.graphml")




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

    def getLineNums(self):
        return (self.line,self.line + len(self.FuncText.splitlines())-1)


    def getNumParameter(self):
        return self.FuncInfoDict["NumArguments"]



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

class DynamicAnalyses:

    def __init__(self,script,Excel,funcs,saveLocation):

        self.saveLocation = saveLocation
        self.InputsRun = InputRunning(script,Excel,funcs)

        self.path = self.InputsRun.getTimingInfo()
        self.PathsUsed = self.InputsRun.getdDictTimes()
        self.FuncCallSheet = self.InputsRun.FuncCallSheet
        self.dictNumRanTimes = self.InputsRun.numTimesCalledDictarr[0]
        self.TimesTaken = self.InputsRun.timesTaken
        self.Funcs = funcs
        self.numFuncsCalled = self.InputsRun.numFuncsCalled
        self.times = self.calcTimeSpentInFuncs(self.FuncCallSheet,funcs)
        self.DyanmicGraph()

    def calcTimeSpentInFuncs(self,FuncCallSheet,funcs):
        times = {i.getName() : 0 for i in funcs}
        times["module"] = 0
        start = time.time()
        for index,q in enumerate(FuncCallSheet):
            numFuncsHere = self.numFuncsCalled[index]
            numFuncsConcated = 0
            l = np.array(q)
            counter = 1
            indexStarted = 0
            timeToSub = 0
            FuncLookingAt = l[0][0]
            timeStarted = float(l[0][1])
            while True:
                if l[counter][0] != "NOTFUNC" and l[counter][0] == FuncLookingAt:
                    numFuncsConcated += 1
                    timeFinished = float(l[counter][1])
                    times[l[counter][0].split()[0]] += ((timeFinished - timeStarted) -  timeToSub)
                    timeToSub = 0
                    l = np.concatenate((l[0:indexStarted], [["NOTFUNC",timeFinished - timeStarted]], l[counter+1:]))
                    counter = 0

                    while counter < len(l) and l[counter][0] == "NOTFUNC":
                        counter += 1
                    if counter >= len(l):

                        break
                    indexStarted = counter
                    timeToSub = 0
                    FuncLookingAt = l[counter][0]
                    timeStarted = float(l[counter][1])
                elif l[counter][0] != "NOTFUNC":
                    FuncLookingAt = l[counter][0]
                    indexStarted = counter
                    timeStarted = float(l[counter][1])
                    timeToSub = 0
                else:
                    timeToSub += float(l[counter][1])
                counter += 1
                if counter >= len(l):
                    break
            print(l)
            print("analysed one sheet")
        print(time.time()-start)
        print(times)
        return times




    def DyanmicGraph(self):
        print("got to graph creation")
        DG = nx.DiGraph()

        '''for i in self.times:
            DG.add_node(i + "\n" + str(round(self.times[i])))'''

        for i in self.PathsUsed:
            DG.add_edges_from([(i[0] + '\n' + str(round(self.times[i[0]],1)),i[1] + '\n' + str(round(self.times[i[1]],1)))])
        for i in self.dictNumRanTimes:
            DG.add_weighted_edges_from([(i[0] + '\n' + str(round(self.times[i[0]],1)),i[1] + '\n' + str(round(self.times[i[1]],1)),round(self.dictNumRanTimes[i],1))])

        print("i got to saving dyamicfunc")
        nx.write_graphml(DG, self.saveLocation + "/DynamicFuncInteracting.graphml")
        self.DynamicFuncInteracting = DG


        DG = nx.DiGraph()
        for i in self.PathsUsed:
            DG.add_node(i[0], weight =  self.times[i[0]])
            DG.add_node(i[1], weight =  self.times[i[1]])
        for i in self.dictNumRanTimes:
            DG.add_weighted_edges_from([(i[0],i[1],round(self.dictNumRanTimes[i],1))])
        self.DynamicFuncInteracting = DG









class InputRunning():

    def __init__(self,script,excelFile,Funcs):
        self.excelFile = excelFile
        self.Funcs = Funcs
        self.script = script
        self.inputData = [[None for j in range(10)] for i in range(10)]
        if excelFile is not None:
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
        self.RunInputs(self.script,self.inputData)

    def getTimingInfo(self):
        return self.paths

    def getdDictTimes(self):
        return self.dictTimesArr[0]

    def funcSorting(self,script,funcs):
        script2 = ""
        for lineNum,line in enumerate(script.splitlines()):
            for i in funcs:
                if i.getName() in line:
                    numAdded = 0
                    for index,m in enumerate(regex.finditer(i.getName() + r'(\(((((?1)|[^\(\)])|(\".*\"))|(\'.*\'))*\))', line)):
                        end = m.span()[0] + len(i.getName()) + 2
                        if "def" in line:
                            if i.getNumParameter() > 0:
                                line = line[0:end-1] + "FuncName,ThisFunc," + line[end-1::]
                            else:
                                line = line[0:end-1] + "FuncName,ThisFunc" + line[end-1::]
                        else:
                            minlines = 100000
                            winningFunc = 0
                            for z in funcs:
                                if lineNum > z.getLineNums()[0] and lineNum <= z.getLineNums()[1]:
                                    numLines = z.getLineNums()[1] - z.getLineNums()[0]
                                    if numLines < minlines:
                                        minlines = numLines
                                        winningFunc = z
                            if winningFunc == 0:
                                winningFunc = f"'module','{i.getName()}'"
                            else:
                                winningFunc = "'" + winningFunc.getName() + "'" +"," + "'" + i.getName() + "'"
                            if i.getNumParameter() > 0:
                                line = line[0:end-1 + numAdded]  + winningFunc + ',' + line[numAdded + end-1::]
                                numAdded += 1 + len(winningFunc)
                            else:
                                line = line[0:end-1 + numAdded] + winningFunc + line[numAdded + end-1::]
                                numAdded += len(winningFunc)


            script2 = script2 + line + "\n"
        return script2



    def RunInputs(self,script,inputs):
        self.prints = print
        script = self.funcSorting(script,self.Funcs)
        #replacingInputs = regex.compile(r'input(\(((((?1)|[^\(\)])|(\".*\"))|(\'.*\'))*\))')
        #scriptWithInputs = replacingInputs.sub('inputsxyzxyz.__next__()', script)
        #replacingPrints = re.compile(r"print")
        #scriptWithInputs = replacingPrints.sub('saveToVariable', scriptWithInputs)
        AddingDecor = regex.compile(r"(( )*def)")
        scriptWithInputs = AddingDecor.sub("\\2\\2\\2\\2@funcDecorator\n\\1",script)
        dictOfName = {i.getName():0 for i in self.Funcs}
        dictOfName["module"] = 0
        decorString = """import inspect
import time
times = []
numFuncs = 0
def funcDecorator(a_func):
    def wrapTheFunction(*args, **kwargs):
        global numFuncs
        numFuncs += 1
        FuncName = args[1] + " " + str(DictNames[args[1]])
        DictNames[args[1]] += 1
        called.append((FuncName,time.time()))
        placeholder = a_func(*args, **kwargs)
        called.append((FuncName,time.time()))
        dicts.add((args[0],args[1]))
        if (args[0],args[1]) in numTimesCalledDict:
            numTimesCalledDict[(args[0],args[1])] += 1
        else:
            numTimesCalledDict[(args[0],args[1])] = 1


        return placeholder
    return wrapTheFunction"""

        decorString = "DictNames = " + str(dictOfName) + "\n" + decorString

        scriptWithInputs = decorString + "\n" + scriptWithInputs
        strtest = """SavedOutputs = []
dicts = set()
numTimesCalledDict = {}
def saveToVariable(toSave):
    SavedOutputs.append(toSave)
print = saveToVariable
def getNextInputXYZ(a = None,b = None,c = None,d = None,q=None):
    return inputsxyzxyz.__next__()
input = getNextInputXYZ"""
        exec(strtest,globals())
        global numTimesCalledDict
        global dicts
        self.paths = []
        self.FuncCallSheet = []
        self.timesTaken = []
        self.numFuncsCalled = []
        self.numTimesCalledDictarr = []
        self.dictTimesArr = []
        self.prints("here are the inputs")
        self.prints(inputs)

        for input in inputs:
            self.prints("done one")
            strToExec = "inputsxyzxyz = " + str(input)
            strToExec2 = "inputsxyzxyz = (item for item in inputsxyzxyz)"
            totString = strToExec + "\n" + strToExec2 + "\n" + scriptWithInputs
            starttime = time.time()
            totString = "import time" + "\n" + "called = []" + "\n" + "called.append(('module 1',time.time()))" + "\n" + totString + "\n" + "called.append(('module 1',time.time()))"
            exec(totString,globals())
            self.timesTaken.append(time.time()-starttime)
            global times
            print(self.prints(self.paths))
            self.paths.append(times)
            self.prints(self.paths)
            self.FuncCallSheet.append(called)
            self.numFuncsCalled.append(numFuncs)
            self.numTimesCalledDictarr.append(dict(numTimesCalledDict))
            self.dictTimesArr.append(set(dicts))
            self.prints(self.dictTimesArr)
            numTimesCalledDict = {}
            dicts = set()
            self.prints("doneOne")
        self.prints(inputs)
        self.prints(SavedOutputs)
        self.SavedOutputs = SavedOutputs
        self.prints(self.dictTimesArr)
        self.prints(self.numTimesCalledDictarr)
        self.prints("finished running onto analyses")





'''if __name__ == "__main__":
    mains = Main()'''
