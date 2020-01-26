    def FillOutput(self,outputs,Excel):
        Gprint("Got to here ok")
        book = ex.load_workbook(Excel)
        sheet2 = book['Sheet2']

        for index,outputlist in enumerate(outputs):
            for index2,output in enumerate(outputlist):
                cell = sheet2.cell(row = index2+1,column = index+1)
                cell.value = output
        #book.save(Excel)


from removeCommets import remove_comments_and_docstrings
from Functions import Function

class StaticAnalyses:

    def __init__(self,script):
        self.script = script
        self.scriptNoComments = self.removeComments(self.script)
        #Create Function Objects
        scriptWithoutClasses = self.createFunctions(self.scriptNoComments)

    def removeComments(self,origFile):
        """removes all comments from a file"""
        return remove_comments_and_docstrings(origFile)

    def createFunctions(self,script):
        """find all Functions and create class classes on those bits of text"""
        functions = []
        scriptArray = script.splitlines()
        #Go through each line looking for class text
        for index,line in enumerate(scriptArray):
            if len(line) > 4:
                if line[0:3] == "def":
                    #looks for ending of the class
                    finishLine = None
                    for index2,line2 in enumerate(scriptArray[index+1::]):
                        if finishLine is None and len(line2) > 0 and line2[0] != " ":
                            finishLine = index2
                    # Creats a class with the relevant code appending it to the classes array
                    if finishLine is not None:
                        functions.append(Function("\n".join(scriptArray[index:finishLine])))
                    else:
                        functions.append(Function("\n".join(scriptArray[index::])))
