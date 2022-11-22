import json, os
from ConfigLib import ProgramConfig
class LangConfig:
    CurrentPath = "\\".join(__file__.split("\\")[:-1]) + "\\"
    ConfigName = "Lang.db"
    ConfigDir = "DB" + "\\"
    ConfigFile = CurrentPath + ConfigDir + ConfigName
    AllData = {}
    Lang = None
    DefaultConfig = {"ru": {}, "en": {}}
    def __init__(self) -> None:
        self.Lang = ProgramConfig().AllData["lang"]
        if os.path.exists(self.ConfigFile) == False:
            DBCreate = open(self.ConfigFile, "w+", encoding="utf-8")
            DBCreate.write(json.dumps(self.DefaultConfig))
            DBCreate.close()
            del DBCreate
        DBOpen = open(self.ConfigFile, "r", encoding="utf-8")
        if DBOpen.read() == "":
            DBOpen.close()
            DBStart = open(self.ConfigFile, "w+", encoding="utf-8")
            DBStart.write(json.dumps(self.DefaultConfig))
            DBStart.close()
            del DBOpen
        with open(self.ConfigFile, "r", encoding="utf-8") as DBOpen:
            self.AllData = json.loads(DBOpen.read())[self.Lang]
    def GetTextByName(self, text):
        return self.AllData[text]