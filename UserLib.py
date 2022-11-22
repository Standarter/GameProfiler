import random, json, string, os
class UserConfigs:
    CurrentPath = "\\".join(__file__.split("\\")[:-1]) + "\\"
    ConfigName = "UserConfig.db"
    ConfigDir = "DB" + "\\"
    ConfigFile = CurrentPath + ConfigDir + ConfigName
    DB = None
    def __init__(self) -> None:
        self.LoadDB()
    def FileExist(self):
        return os.path.exists(self.ConfigFile)
    def FileNotExist(self):
        return os.path.exists(self.ConfigFile) == False
    def FileEmpty(self):
        return open(self.ConfigFile, "r", encoding="utf-8").read() == ""
    def LoadDB(self):
        if self.FileNotExist() or self.FileEmpty():
            self.CreateDefaultUserConfig()
        DBOpen = open(self.ConfigFile, "r", encoding="utf-8")
        self.DB = json.loads(DBOpen.read())
        DBOpen.close()
    def CreateDefaultUserConfig(self):
        UserStats = {
            "Username": "".join([random.choice(string.hexdigits) for _ in range(32)]),
            "Games": {}
        }
        UserDB = open(self.ConfigFile, "w", encoding="utf-8")
        UserDB.write(json.dumps(UserStats))
        UserDB.close()
        return True
    def GetUserName(self):
        if self.FileNotExist():
            self.CreateDefaultUserConfig()
        return self.DB["Username"]
    def GetGameScore(self, GameName: str):
        if GameName in self.DB["Games"]:
            return self.DB["Games"][GameName]
        return False
    def GetAllScoredGames(self):
        return list(self.DB["Games"].keys())
    def GetAvgGamesScore(self):
        if len(self.DB["Games"].keys()) > 0:
            return sum([self.DB["Games"][name] for name in self.DB["Games"].keys()])/len(self.DB["Games"].keys())
        else:
            return -1
    def SetGameScore(self, GameName: str, GameScore: int):
        if os.path.exists(self.ConfigFile) == False:
            DBCreate = open(self.ConfigFile, "w+", encoding="utf-8")
            DBCreate.write("{}")
            DBCreate.close()
        DBOpen = open(self.ConfigFile, "r", encoding="utf-8")
        if DBOpen.read() == "":
            DBStart = open(self.ConfigFile, "w+", encoding="utf-8")
            DBStart.write("{}")
            DBStart.close()
        DBOpen.close()
        DBOpen = open(self.ConfigFile, "r", encoding="utf-8")
        DBDict = json.loads(DBOpen.read())
        DBOpen.close()
        DBOpen = open(self.ConfigFile, "w+", encoding="utf-8")
        DBDict["Games"][GameName] = GameScore
        self.DB["Games"][GameName] = GameScore
        DBOpen.write(json.dumps(DBDict))
        return True
    def GetGameByName(self, GameName: str):
        DBOpen = open(self.ConfigFile, "r", encoding="utf-8")
        if DBOpen.read() == "":
            DBStart = open(self.ConfigFile, "w+", encoding="utf-8")
            DBStart.write("{}")
            DBStart.close()
        DBOpen.close()
        DBOpen = open(self.ConfigFile, "r", encoding="utf-8")
        DBDict = json.loads(DBOpen.read())
        DBOpen.close()
        if GameName in DBDict.keys():
            return DBDict["Games"][GameName]
        else:
            return False