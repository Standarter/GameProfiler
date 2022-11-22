from UserLib import UserConfigs
import os, json, numpy
from numba import njit
import functionstools
class GameConfigs:
    CurrentPath = "\\".join(__file__.split("\\")[:-1]) + "\\"
    ConfigName = "GameConfig.db"
    ConfigDir = "DB" + "\\"
    ConfigFile = CurrentPath + ConfigDir + ConfigName
    ArrayLenght = 58
    DB = None
    def __init__(self) -> None:
        UC = UserConfigs()
        UserName = UC.GetUserName()
        if os.path.exists(self.ConfigFile) == False:
            DBCreate = open(self.ConfigFile, "w+", encoding="utf-8")
            DBCreate.write("{}")
            DBCreate.close()
            del DBOpen
        DBOpen = open(self.ConfigFile, "r", encoding="utf-8")
        if DBOpen.read() == "":
            DBStart = open(self.ConfigFile, "w+", encoding="utf-8")
            DBStart.write("{}")
            DBStart.close()
            del DBOpen
        DBOpen.close()
        del DBOpen
        DBOpen = open(self.ConfigFile, "r", encoding="utf-8")
        DBDict = json.loads(DBOpen.read())
        DBOpen.close()
        del DBOpen
        DBOpen = open(self.ConfigFile, "w+", encoding="utf-8")
        if UserName not in DBDict.keys():
            DBDict[UserName] = {"Games": {}}
        DBOpen.write(json.dumps(DBDict))
        DBOpen.close()
        del DBOpen
        DBOpen = open(self.ConfigFile, "r", encoding="utf-8")
        self.DB = json.loads(DBOpen.read())
        DBOpen.close()
        del DBOpen
    def AddToConfig(self, UserName, GameName, GameStats):
        if len(GameStats) == self.ArrayLenght:
            DBOpen = open(self.ConfigFile, "w+", encoding="utf-8")
            if UserName not in self.DB.keys():
                self.DB[UserName] = {}
            self.DB[UserName]["Games"][GameName] = [GameStats]
            DBOpen.write(json.dumps(self.DB))
            return True
        return False
    def GetGameByName(self, GameName):
        Result = []
        for C_User in self.DB.keys():
            if GameName in self.DB[C_User]["Games"].keys():
                Result.append(numpy.array(self.DB[C_User]["Games"][GameName]))
        try:
            return (sum(Result)/len(Result)).tolist()[0]
        except:
            return [0]*self.ArrayLenght
    def GetGameUserscore(self, GameName):
        Data = self.GetGameByName(GameName=GameName)
        return sum(Data[36:48])/len(Data[36:48])
    def GetGameYear(self, GameName):
        Data = self.GetGameByName(GameName=GameName)
        return Data[49]
    def GetGameByUserName(self, UserName, GameName):
        if UserName in self.DB.keys() and GameName in self.DB[UserName]["Games"].keys():
            return self.DB[UserName]["Games"][GameName][0]
        else:
            return self.GetGameByName(GameName=GameName)
    def GameInDB(self, GameName):
        for Names in self.DB.keys():
            if GameName in self.DB[Names]["Games"]:
                return True
        return False
    @functionstools.functime(True)
    def GetAllGamesInDB(self):
        Result = []
        for Names in self.DB.keys():
            for Game in self.DB[Names]["Games"].keys():
                if Game not in Result:
                    Result.append(Game)
        return Result
    def GetAllPlatforms(self, Gamename):
        Platforms = self.GetGameByName(GameName=Gamename)[24:37]
        Result = []
        if Platforms[0] == 1:
            Result.append("MacOS")
        if Platforms[1] == 1:
            Result.append("Windows")
        if Platforms[2] == 1:
            Result.append("Linux")
        if Platforms[3] == 1:
            Result.append("IOS")
        if Platforms[4] == 1:
            Result.append("Android")
        if Platforms[5] == 1:
            Result.append("Xbox 360")
        if Platforms[6] == 1:
            Result.append("Xbox One")
        if Platforms[7] == 1:
            Result.append("Xbox Series X")
        if Platforms[8] == 1:
            Result.append("PS3")
        if Platforms[9] == 1:
            Result.append("PS4")
        if Platforms[10] == 1:
            Result.append("PS5")
        if Platforms[11] == 1:
            Result.append("NS")
        TempResult = " ".join(Result)
        if len(TempResult) > 25:
            for i in range(len(Result)):
                if Result[i] == "Xbox 360":
                    Result[i] = "X360"
                if Result[i] == "Windows":
                    Result[i] = "Win"
                if Result[i] == "Xbox One":
                    Result[i] = "XOne"
                if Result[i] == "Xbox Series X":
                    Result[i] = "XboxSX"
                if Result[i] == "MacOS":
                    Result[i] = "Mac"
        return " ".join(Result)
    def GetAllPlatformsList(self, Gamename):
        return self.GetGameByName(GameName=Gamename)[24:37]
    def Update(self):
        self.__init__()
if __name__ == "__main__":
    GC = GameConfigs()
    print(GC.GetGameByName("Pragmata"))