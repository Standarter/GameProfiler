import os, json
class PredictCache:
    CurrentPath = "\\".join(__file__.split("\\")[:-1]) + "\\"
    ConfigName = "PredictCache.db"
    ConfigDir = "DB" + "\\"
    ConfigFile = CurrentPath + ConfigDir + ConfigName
    LoadedData = {}
    def ExistDir(self):
        if os.path.exists(self.ConfigDir):
            return True
        else:
            os.mkdir(self.ConfigDir)
    def ExistFile(self):
        if os.path.exists(self.ConfigFile):
            return True
        else:
            DB = open(self.ConfigFile, "w+", encoding="utf-8")
            DB.close()
    def EmptyFile(self):
        self.ExistDir()
        self.ExistFile()
        with open(self.ConfigFile, "r", encoding="utf-8") as DB:
            if DB.read() == "":
                with open(self.ConfigFile, "w", encoding="utf-8") as DBW:
                    DBW.write("{}")
    def AllFileTests(self):
        self.EmptyFile()
    def SetPredictScore(self, GameName, Score):
        self.LoadedData[GameName] = int(Score)
        self.Save()
    def SetPredictScoreNoSave(self, GameName, Score):
        self.LoadedData[GameName] = int(Score)
    def GetPredictScore(self, GameName):
        return int(self.LoadedData[GameName])
    def GameInLib(self, GameName):
        return GameName in self.LoadedData.keys()
    def Save(self):
        with open(self.ConfigFile, "w", encoding="utf-8") as DB:
            DB.write(json.dumps(self.LoadedData))
    def Delete(self):
        try:
            os.remove(self.ConfigFile)
        except:
            pass
    def __init__(self) -> None:
        self.AllFileTests()
        DB = open(self.ConfigFile, "r", encoding="utf-8")
        self.LoadedData = DB.read()
        DB.close()
        self.LoadedData = json.loads(self.LoadedData)