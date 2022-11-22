import json, os
class ProgramConfig:
    CurrentPath = "\\".join(__file__.split("\\")[:-1]) + "\\"
    ConfigName = "ProgramConfig.db"
    ConfigDir = "DB" + "\\"
    ConfigFile = CurrentPath + ConfigDir + ConfigName
    AllData = {}
    DefaultConfig = {"max_loss": 0.15, 
                    "max_try": 25, 
                    "lang": "en"}
    def __init__(self) -> None:
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
            self.AllData = json.loads(DBOpen.read())