from StaticAnalyses import StaticAnalyses


class AnalysesStart():
    #Take In scripts Call analyses classes
    def __init__(self,CodeFileLocation,saveLocation,ExcelLocation):
        if saveLocation is None:
            saveLocation = 'C:/Users/dvlas/Desktop'

        self.script = self.TakeInScript(CodeFileLocation)
        self.RunSaticAnalyses(self.script)

    def TakeInScript(self,CodeFileLocation):
        with open(CodeFileLocation) as CodeFile:
            return CodeFile.read()

    def RunSaticAnalyses(self,script):
        Static = StaticAnalyses(script)
