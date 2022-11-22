import re
import time
import copy
import numpy
import random
import tkinter
import threading
import functionstools
from GameLib import GameConfigs
from UserLib import UserConfigs
from PredictLib import PredictCache
from NeuronNetwork import NeuronNetwork
from ConfigLib import ProgramConfig
from LangLib import LangConfig
from TkinterAddictional import VerticalScrolledFrame
numpy.set_printoptions(suppress=True)
class PredictProgram:
    GC = None
    UC = None
    PC = None
    NN = None
    PConfig = None
    LConfig = None
    Geometry = "800x600"
    Title = "Game Profiler"
    ItemsPerPage = 10
    PageSelected = 1
    CurrentWindow = None
    sort_alg = None
    #
    WindowsPlatform = None
    LinuxPlatform = None
    MacOSPlatform = None
    AndroidPlatform = None
    IOSPlatform = None
    Xbox360Platform = None
    XboxOnePlatform = None
    XboxSeriasXPlatform = None
    PS3Platform = None
    PS4Platform = None
    PS5Platform = None
    NintendoSwitchPlatform = None
    AllPlatforms = []
    #
    def DestroyAllChildren(self, Window):
        if len(Window.winfo_children()) > 0:
            for Children in Window.winfo_children():
                self.DestroyAllChildren(Children)
        else:
            Window.destroy()
    def DestroyAllFrameChildren(self, Frame):
        for Children in Frame.winfo_children():
                self.DestroyAllChildren(Children)
    @functionstools.functime(True)
    def SortAlgoritmByScore(self, Gamename):
        sorttype = self.sort_alg.get()
        if len(self.UC.GetAllScoredGames()) > 0:
            print(sorttype)
            if sorttype=="minmax": return -self.NN.predict_with_correlation(GameName=Gamename)
            if sorttype=="maxmin": return self.NN.predict_with_correlation(GameName=Gamename)
            if sorttype=="name": return Gamename[0]
            if sorttype=="userscore": return -self.GC.GetGameUserscore(GameName=Gamename)
            if sorttype=="year": return -self.GC.GetGameYear(GameName=Gamename)
        return 1
    def SortAlgoritmForRecommends(self, Gamename):
        GameScore = self.GC.GetGameUserscore(GameName=Gamename)
        GamePredict = self.NN.predict_with_correlation(GameName=Gamename)
        return -(GameScore+GamePredict)/2
    @functionstools.functime(True)
    def SearchAlgoritm(self, event, ResultsFrame, SearchText: tkinter.Entry):
        [self.DestroyAllFrameChildren(ResultsFrame) for i in range(10)]
        for Game in self.GC.GetAllGamesInDB():
            if re.match(".*" + SearchText.get() + ".*", Game, flags=re.IGNORECASE) != None:
                GameFrame = tkinter.LabelFrame(ResultsFrame)
                GameLabel = tkinter.Label(GameFrame, text=Game)
                GameLabel.pack(fill="x", expand=True)
                MainBlock = tkinter.LabelFrame(GameFrame)
                ScaleBlock = tkinter.Scale(MainBlock, length=250, orient="horizontal", from_=1, to=5, )
                if self.UC.GetGameScore(GameName=Game) != False:
                    ScaleBlock.set(self.UC.GetGameScore(GameName=Game))
                else:
                    ScaleBlock.set(3)
                ScaleBlock.pack()
                ApplyButton = tkinter.Button(MainBlock, text="Apply")
                ApplyButton.pack(anchor="ne", side="right", fill="y", expand=True) 
                if self.UC.GetGameScore(Game) != False:
                    ApplyButton["text"] = "Change"
                ApplyButton.bind("<Button-1>", lambda event, GameLabel=GameLabel, ScoreFrame=ScaleBlock: self.SetGameScoreAlgoritm(GameLabel=GameLabel, ScoreFrame=ScoreFrame))
                MainBlock.pack(fill="x", expand=True)
                BottomBlock = tkinter.Frame(GameFrame)
                Text1 = tkinter.Label(BottomBlock, text="{0}: ".format(self.LConfig.GetTextByName("Platforms") + self.GC.GetAllPlatforms(Game)))
                Text1.pack(side="left", anchor="nw")
                Text2 = tkinter.Label(BottomBlock, text="{0}: ".format(self.LConfig.GetTextByName("NeuroScore")))
                Text2.pack(side="right", anchor="nw")
                Text2["text"] = "{0}: ".format(self.LConfig.GetTextByName("NeuroScore")) + str(self.NN.predict_with_correlation(GameLabel.cget("text"))) + "%"
                BottomBlock.pack(fill="x", expand=True)
                GameFrame.pack(fill="x", expand=True, pady=10, padx=25)
    @functionstools.functime(True)
    def SearchAlgoritmMyGames(self, event, ResultsFrame, SearchText: tkinter.Entry):
        [self.DestroyAllFrameChildren(ResultsFrame) for i in range(10)]
        for Game in self.UC.GetAllScoredGames():
            if re.match(".*" + SearchText.get() + ".*", Game, flags=re.IGNORECASE) != None:
                GameFrame = tkinter.LabelFrame(ResultsFrame)
                GameLabel = tkinter.Label(GameFrame, text=Game)
                GameLabel.pack(fill="x", expand=True)
                MainBlock = tkinter.LabelFrame(GameFrame)
                ScaleBlock = tkinter.Scale(MainBlock, length=250, orient="horizontal", from_=1, to=5, )
                if self.UC.GetGameScore(GameName=Game) != False:
                    ScaleBlock.set(self.UC.GetGameScore(GameName=Game))
                else:
                    ScaleBlock.set(3)
                ScaleBlock.pack()
                ApplyButton = tkinter.Button(MainBlock, text="Apply")
                ApplyButton.pack(anchor="ne", side="right", fill="y", expand=True) 
                if self.UC.GetGameScore(Game) != False:
                    ApplyButton["text"] = "Change"
                ApplyButton.bind("<Button-1>", lambda event, GameLabel=GameLabel, ScoreFrame=ScaleBlock: self.SetGameScoreAlgoritm(GameLabel=GameLabel, ScoreFrame=ScoreFrame))
                MainBlock.pack(fill="x", expand=True)
                BottomBlock = tkinter.Frame(GameFrame)
                Text1 = tkinter.Label(BottomBlock, text="{0}: ".format(self.LConfig.GetTextByName("Platforms") + self.GC.GetAllPlatforms(Game)))
                Text1.pack(side="left", anchor="nw")
                Text2 = tkinter.Label(BottomBlock, text="{0}: ".format(self.LConfig.GetTextByName("NeuroScore")))
                Text2.pack(side="right", anchor="nw")
                Text2["text"] = "Network Predict: " + str(self.NN.predict_with_correlation(GameLabel.cget("text"))) + "%"
                BottomBlock.pack(fill="x", expand=True)
                GameFrame.pack(fill="x", expand=True, pady=10, padx=25)
    def SetGameScoreAlgoritm(self, GameLabel: tkinter.Label, ScoreFrame: tkinter.Scale):
        self.UC.SetGameScore(GameName=GameLabel.cget("text"), GameScore=ScoreFrame.get())
    @functionstools.functime(True)
    def ScoredGamesWindow(self, Window: tkinter.Frame | tkinter.LabelFrame, SelectedPage = 1):
        if self.CurrentWindow != "ScoredGamesWindow": self.PageSelected = 1
        self.CurrentWindow = "ScoredGamesWindow"
        [self.DestroyAllFrameChildren(Window) for i in range(10)]
        SearchFrame = tkinter.Frame(Window)
        SearchFrame.pack(fill="x", padx=25, pady=10)
        SearchButton = tkinter.Button(SearchFrame, text=self.LConfig.GetTextByName("Search"))
        SearchButton.pack(side="right", anchor="nw", fill="y", ipadx=10)
        SearchEntry = tkinter.Entry(SearchFrame)
        SearchEntry.pack(side="left", anchor="nw", fill="both", expand=True)
        ResultsFrame = tkinter.LabelFrame(Window)
        SortingFrame = tkinter.Frame(ResultsFrame, height=30)
        SortingFrame.pack(anchor="ne", side="top")
        SortButton1 = tkinter.Button(SortingFrame, text=self.LConfig.GetTextByName("Sort1"))
        SortButton2 = tkinter.Button(SortingFrame, text=self.LConfig.GetTextByName("Sort2"))
        SortButton3 = tkinter.Button(SortingFrame, text=self.LConfig.GetTextByName("Sort3"))
        SortButton4 = tkinter.Button(SortingFrame, text=self.LConfig.GetTextByName("Sort4"))
        SortButton5 = tkinter.Button(SortingFrame, text=self.LConfig.GetTextByName("Sort5"))
        def change_algorithm(mode):
            self.sort_alg.set(mode)
            self.ScoredGamesWindow(Window=Window)
        SortButton1.bind("<Button-1>", lambda event, data="minmax": change_algorithm(data))
        SortButton2.bind("<Button-1>", lambda event, data="maxmin": change_algorithm(data))
        SortButton3.bind("<Button-1>", lambda event, data="name": change_algorithm(data))
        SortButton4.bind("<Button-1>", lambda event, data="userscore": change_algorithm(data))
        SortButton5.bind("<Button-1>", lambda event, data="year": change_algorithm(data))
        SortButton1.pack(side="left", padx=5)
        SortButton2.pack(side="left", padx=5)
        SortButton3.pack(side="left", padx=5)
        SortButton4.pack(side="left", padx=5)
        SortButton5.pack(side="left", padx=5)
        ResultsFrameFinal = VerticalScrolledFrame(ResultsFrame)
        ResultsFrameFinal.pack(fill="both", expand=True)
        Games = self.UC.GetAllScoredGames()
        Games = sorted(Games, key=self.SortAlgoritmByScore)
        PageSelectFrame = tkinter.Frame(Window)
        PageSelectFrame2 = tkinter.Frame(PageSelectFrame)
        GoToLabel = tkinter.Label(PageSelectFrame2, text="{1} {0}".format(" (" + str(self.PageSelected) + " / " + str(len(Games)//self.ItemsPerPage) + ")", self.LConfig.GetTextByName("GTSP")))
        GoToLabel.pack(side="left", anchor="nw", fill="both")
        GoToEntry = tkinter.Entry(PageSelectFrame2)
        GoToEntry.insert(0, str(self.PageSelected))
        GoToEntry.pack(side="left", anchor="nw", fill="both")
        def GoToButtonCallback(event, Entry=SelectedPage):
            self.PageSelected = int(Entry.get())
            self.ScoredGamesWindow(Window=Window)
        GoToButton = tkinter.Button(PageSelectFrame2, text=self.LConfig.GetTextByName("Go"))
        GoToButton.pack(side="left", anchor="nw", fill="both")
        GoToButton.bind("<Button-1>", lambda event, Entry=GoToEntry: GoToButtonCallback(event=event, Entry=Entry))
        PageSelectFrame2.pack(anchor="center", side="bottom")
        PageSelectFrame.pack(side="bottom", fill="both")
        SearchButton.bind("<Button-1>", lambda event, ResultsFrame=ResultsFrameFinal.interior, SearchText=SearchEntry: self.SearchAlgoritmMyGames(event=event, ResultsFrame=ResultsFrame, SearchText=SearchEntry))
        for Game in Games[(self.PageSelected - 1)*10 : (self.PageSelected)*10 if len(Games[(self.PageSelected - 1)*10:]) >= 10 else len(Games[(self.PageSelected - 1)*10:])]:
            GameFrame = tkinter.LabelFrame(ResultsFrameFinal.interior)
            GameLabel = tkinter.Label(GameFrame, text=Game)
            GameLabel.pack(fill="x", expand=True)
            MainBlock = tkinter.LabelFrame(GameFrame)
            ScaleBlock = tkinter.Scale(MainBlock, length=250, orient="horizontal", from_=1, to=5, )
            if self.UC.GetGameScore(GameName=Game) != False:
                ScaleBlock.set(self.UC.GetGameScore(GameName=Game))
            else:
                ScaleBlock.set(3)
            ScaleBlock.pack()
            ApplyButton = tkinter.Button(MainBlock, text="Apply")
            ApplyButton.pack(anchor="ne", side="right", fill="y", expand=True) 
            if self.UC.GetGameScore(Game) != False:
                ApplyButton["text"] = "Change"
            ApplyButton.bind("<Button-1>", lambda event, GameLabel=GameLabel, ScoreFrame=ScaleBlock: self.SetGameScoreAlgoritm(GameLabel=GameLabel, ScoreFrame=ScoreFrame))
            MainBlock.pack(fill="x", expand=True)
            BottomBlock = tkinter.Frame(GameFrame)
            Text1 = tkinter.Label(BottomBlock, text="{0}: ".format(self.LConfig.GetTextByName("Platforms") + self.GC.GetAllPlatforms(Game)))
            Text1.pack(side="left", anchor="nw")
            Text2 = tkinter.Label(BottomBlock, text="{0}: ".format(self.LConfig.GetTextByName("NeuroScore")))
            Text2.pack(side="right", anchor="nw")
            if (len(self.UC.GetAllScoredGames()) > 0):
                Text2["text"] = "{0}: ".format(self.LConfig.GetTextByName("NeuroScore")) + str(self.NN.predict_with_correlation(GameLabel.cget("text"))) + "%"    
            else:
                Text2["text"] = "No games scored"
            BottomBlock.pack(fill="x", expand=True)
            GameFrame.pack(fill="x", expand=True, pady=10, padx=25)
        ResultsFrame.pack(fill="both", expand=True, padx=5, pady=5)
    @functionstools.functime(True)
    def RecommendedGamesWindow(self, Window: tkinter.Frame | tkinter.LabelFrame, SelectedPage = 1):
        if self.CurrentWindow != "RecommendedGamesWindow": self.PageSelected = 1
        self.CurrentWindow = "RecommendedGamesWindow"
        [self.DestroyAllFrameChildren(Window) for i in range(10)]
        SearchFrame = tkinter.Frame(Window)
        SearchFrame.pack(fill="x", padx=25, pady=10)
        SearchButton = tkinter.Button(SearchFrame, text=self.LConfig.GetTextByName("Search"))
        SearchButton.pack(side="right", anchor="nw", fill="y", ipadx=10)
        SearchEntry = tkinter.Entry(SearchFrame)
        SearchEntry.pack(side="left", anchor="nw", fill="both", expand=True)
        ResultsFrame = tkinter.LabelFrame(Window)
        SortingFrame = tkinter.Frame(ResultsFrame, height=30)
        SortingFrame.pack(anchor="ne", side="top")
        SortButton1 = tkinter.Button(SortingFrame, text=self.LConfig.GetTextByName("Sort1"))
        SortButton2 = tkinter.Button(SortingFrame, text=self.LConfig.GetTextByName("Sort2"))
        SortButton3 = tkinter.Button(SortingFrame, text=self.LConfig.GetTextByName("Sort3"))
        SortButton4 = tkinter.Button(SortingFrame, text=self.LConfig.GetTextByName("Sort4"))
        SortButton5 = tkinter.Button(SortingFrame, text=self.LConfig.GetTextByName("Sort5"))
        def change_algorithm(mode):
            self.sort_alg.set(mode)
            self.RecommendedGamesWindow(Window=Window)
        SortButton1.bind("<Button-1>", lambda event, data="minmax": change_algorithm(data))
        SortButton2.bind("<Button-1>", lambda event, data="maxmin": change_algorithm(data))
        SortButton3.bind("<Button-1>", lambda event, data="name": change_algorithm(data))
        SortButton4.bind("<Button-1>", lambda event, data="userscore": change_algorithm(data))
        SortButton5.bind("<Button-1>", lambda event, data="year": change_algorithm(data))
        SortButton1.pack(side="left", padx=5)
        SortButton2.pack(side="left", padx=5)
        SortButton3.pack(side="left", padx=5)
        SortButton4.pack(side="left", padx=5)
        SortButton5.pack(side="left", padx=5)
        ResultsFrameFinal = VerticalScrolledFrame(ResultsFrame)
        ResultsFrameFinal.pack(fill="both", expand=True)
        Games = list(set(self.GC.GetAllGamesInDB()) - set(self.UC.GetAllScoredGames()))
        Games = list(filter(lambda x: round(self.NN.predict_with_correlation(x)) >= 60, Games))
        if sum(self.GetPlatforms()) != 0:
            Games = list(filter(lambda x: self.ExprToShow(self.GC.GetAllPlatformsList(Gamename=x)) > 0, Games))
        Games = sorted(Games, key=self.SortAlgoritmForRecommends)
        PageSelectFrame = tkinter.Frame(Window)
        PageSelectFrame2 = tkinter.Frame(PageSelectFrame)
        GoToLabel = tkinter.Label(PageSelectFrame2, text="{1} {0}".format(" (" + str(self.PageSelected) + " / " + str(len(Games)//self.ItemsPerPage) + ")", self.LConfig.GetTextByName("GTSP")))
        GoToLabel.pack(side="left", anchor="nw", fill="both")
        GoToEntry = tkinter.Entry(PageSelectFrame2)
        GoToEntry.insert(0, str(self.PageSelected))
        GoToEntry.pack(side="left", anchor="nw", fill="both")
        def GoToButtonCallback(event, Entry=SelectedPage):
            self.PageSelected = int(Entry.get())
            self.RecommendedGamesWindow(Window=Window)
        GoToButton = tkinter.Button(PageSelectFrame2, text=self.LConfig.GetTextByName("Go"))
        GoToButton.pack(side="left", anchor="nw", fill="both")
        GoToButton.bind("<Button-1>", lambda event, Entry=GoToEntry: GoToButtonCallback(event=event, Entry=Entry))
        PageSelectFrame2.pack(anchor="center", side="bottom")
        PageSelectFrame.pack(side="bottom", fill="both")
        SearchButton.bind("<Button-1>", lambda event, ResultsFrame=ResultsFrameFinal.interior, SearchText=SearchEntry: self.SearchAlgoritmMyGames(event=event, ResultsFrame=ResultsFrame, SearchText=SearchEntry))
        for Game in Games[(self.PageSelected - 1)*10 : (self.PageSelected)*10 if len(Games[(self.PageSelected - 1)*10:]) >= 10 else len(Games[(self.PageSelected - 1)*10:])]:
            GameFrame = tkinter.LabelFrame(ResultsFrameFinal.interior)
            GameLabel = tkinter.Label(GameFrame, text=Game)
            GameLabel.pack(fill="x", expand=True)
            MainBlock = tkinter.LabelFrame(GameFrame)
            ScaleBlock = tkinter.Scale(MainBlock, length=250, orient="horizontal", from_=1, to=5, )
            if self.UC.GetGameScore(GameName=Game) != False:
                ScaleBlock.set(self.UC.GetGameScore(GameName=Game))
            else:
                ScaleBlock.set(3)
            ScaleBlock.pack()
            ApplyButton = tkinter.Button(MainBlock, text="Apply")
            ApplyButton.pack(anchor="ne", side="right", fill="y", expand=True) 
            if self.UC.GetGameScore(Game) != False:
                ApplyButton["text"] = "Change"
            ApplyButton.bind("<Button-1>", lambda event, GameLabel=GameLabel, ScoreFrame=ScaleBlock: self.SetGameScoreAlgoritm(GameLabel=GameLabel, ScoreFrame=ScoreFrame))
            MainBlock.pack(fill="x", expand=True)
            BottomBlock = tkinter.Frame(GameFrame)
            Text1 = tkinter.Label(BottomBlock, text="{0}: ".format(self.LConfig.GetTextByName("Platforms")) + self.GC.GetAllPlatforms(Game))
            Text1.pack(side="left", anchor="nw")
            Text2 = tkinter.Label(BottomBlock, text="{0}: ".format(self.LConfig.GetTextByName("NeuroScore")))
            Text2.pack(side="right", anchor="nw")
            if (len(self.UC.GetAllScoredGames()) > 0):
                Text2["text"] = "{0}: ".format(self.LConfig.GetTextByName("NeuroScore")) + str(self.NN.predict_with_correlation(GameLabel.cget("text"))) + "%"    
            else:
                Text2["text"] = "No games scored"
            BottomBlock.pack(fill="x", expand=True)
            GameFrame.pack(fill="x", expand=True, pady=10, padx=25)
        ResultsFrame.pack(fill="both", expand=True, padx=5, pady=5)
    @functionstools.functime(True)
    def SearchWindow(self, Window: tkinter.Frame | tkinter.LabelFrame, SelectedPage = 1):
        if self.CurrentWindow != "SearchWindow": self.PageSelected = 1
        self.CurrentWindow = "SearchWindow"
        [self.DestroyAllFrameChildren(Window) for i in range(10)]
        SearchFrame = tkinter.Frame(Window)
        SearchFrame.pack(fill="x", padx=25, pady=10)
        SearchButton = tkinter.Button(SearchFrame, text=self.LConfig.GetTextByName("Search"))
        SearchButton.pack(side="right", anchor="nw", fill="y", ipadx=10)
        SearchEntry = tkinter.Entry(SearchFrame)
        SearchEntry.pack(side="left", anchor="nw", fill="both", expand=True)
        ResultsFrame = tkinter.LabelFrame(Window)
        SortingFrame = tkinter.Frame(ResultsFrame, height=30)
        SortingFrame.pack(anchor="ne", side="top")
        SortButton1 = tkinter.Button(SortingFrame, text=self.LConfig.GetTextByName("Sort1"))
        SortButton2 = tkinter.Button(SortingFrame, text=self.LConfig.GetTextByName("Sort2"))
        SortButton3 = tkinter.Button(SortingFrame, text=self.LConfig.GetTextByName("Sort3"))
        SortButton4 = tkinter.Button(SortingFrame, text=self.LConfig.GetTextByName("Sort4"))
        SortButton5 = tkinter.Button(SortingFrame, text=self.LConfig.GetTextByName("Sort5"))
        def change_algorithm(mode):
            self.sort_alg.set(mode)
            self.SearchWindow(Window=Window)
        SortButton1.bind("<Button-1>", lambda event, data="minmax": change_algorithm(data))
        SortButton2.bind("<Button-1>", lambda event, data="maxmin": change_algorithm(data))
        SortButton3.bind("<Button-1>", lambda event, data="name": change_algorithm(data))
        SortButton4.bind("<Button-1>", lambda event, data="userscore": change_algorithm(data))
        SortButton5.bind("<Button-1>", lambda event, data="year": change_algorithm(data))
        SortButton1.pack(side="left", padx=5)
        SortButton2.pack(side="left", padx=5)
        SortButton3.pack(side="left", padx=5)
        SortButton4.pack(side="left", padx=5)
        SortButton5.pack(side="left", padx=5)
        ResultsFrameFinal = VerticalScrolledFrame(ResultsFrame)
        ResultsFrameFinal.pack(fill="both", expand=True)
        Games = list(set(self.GC.GetAllGamesInDB()) - set(self.UC.GetAllScoredGames()))
        if sum(self.GetPlatforms()) != 0:
            Games = list(filter(lambda x: self.ExprToShow(self.GC.GetAllPlatformsList(Gamename=x)) > 0, Games))
        Games = sorted(Games, key=self.SortAlgoritmByScore)
        PageSelectFrame = tkinter.Frame(Window)
        PageSelectFrame2 = tkinter.Frame(PageSelectFrame)
        GoToLabel = tkinter.Label(PageSelectFrame2, text="{1} {0}".format(" (" + str(self.PageSelected) + " / " + str(len(Games)//self.ItemsPerPage) + ")", self.LConfig.GetTextByName("GTSP")))
        GoToLabel.pack(side="left", anchor="nw", fill="both")
        GoToEntry = tkinter.Entry(PageSelectFrame2)
        GoToEntry.insert(0, str(self.PageSelected))
        GoToEntry.pack(side="left", anchor="nw", fill="both")
        def GoToButtonCallback(event, Entry=SelectedPage):
            self.PageSelected = int(Entry.get())
            self.SearchWindow(Window=Window)
        GoToButton = tkinter.Button(PageSelectFrame2, text=self.LConfig.GetTextByName("Go"))
        GoToButton.pack(side="left", anchor="nw", fill="both")
        GoToButton.bind("<Button-1>", lambda event, Entry=GoToEntry: GoToButtonCallback(event=event, Entry=Entry))
        PageSelectFrame2.pack(anchor="center", side="bottom")
        PageSelectFrame.pack(side="bottom", fill="both")
        SearchButton.bind("<Button-1>", lambda event, ResultsFrame=ResultsFrameFinal.interior, SearchText=SearchEntry: self.SearchAlgoritm(event=event, ResultsFrame=ResultsFrame, SearchText=SearchEntry))
        for Game in Games[(self.PageSelected - 1)*10 : (self.PageSelected)*10 if len(Games[(self.PageSelected - 1)*10:]) >= 10 else len(Games[(self.PageSelected - 1)*10:])]:
            GameFrame = tkinter.LabelFrame(ResultsFrameFinal.interior)
            GameLabel = tkinter.Label(GameFrame, text=Game)
            GameLabel.pack(fill="x", expand=True)
            MainBlock = tkinter.LabelFrame(GameFrame)
            ScaleBlock = tkinter.Scale(MainBlock, length=250, orient="horizontal", from_=1, to=5, )
            if self.UC.GetGameScore(GameName=Game) != False:
                ScaleBlock.set(self.UC.GetGameScore(GameName=Game))
            else:
                ScaleBlock.set(3)
            ScaleBlock.pack()
            ApplyButton = tkinter.Button(MainBlock, text="Apply")
            ApplyButton.pack(anchor="ne", side="right", fill="y", expand=True) 
            if self.UC.GetGameScore(Game) != False:
                ApplyButton["text"] = "Change"
            ApplyButton.bind("<Button-1>", lambda event, GameLabel=GameLabel, ScoreFrame=ScaleBlock: self.SetGameScoreAlgoritm(GameLabel=GameLabel, ScoreFrame=ScoreFrame))
            MainBlock.pack(fill="x", expand=True)
            BottomBlock = tkinter.Frame(GameFrame)
            Text1 = tkinter.Label(BottomBlock, text="{0}: ".format(self.LConfig.GetTextByName("Platforms")) + self.GC.GetAllPlatforms(Game))
            Text1.pack(side="left", anchor="nw")
            Text2 = tkinter.Label(BottomBlock, text="{0}: ".format(self.LConfig.GetTextByName("NeuroScore")))
            Text2.pack(side="right", anchor="nw")
            if (len(self.UC.GetAllScoredGames()) > 0):
                Text2["text"] = "{0}: ".format(self.LConfig.GetTextByName("NeuroScore")) + str(self.NN.predict_with_correlation(GameLabel.cget("text"))) + "%"    
            else:
                Text2["text"] = "No games scored"
            BottomBlock.pack(fill="x", expand=True)
            GameFrame.pack(fill="x", expand=True, pady=10, padx=25)
        ResultsFrame.pack(fill="both", expand=True, padx=5, pady=5)
    @functionstools.functime(True)
    def OptionsWindow(self, Window: tkinter.Frame | tkinter.LabelFrame, SelectedPage = 1):
        if self.CurrentWindow != "OptionsWindow": self.PageSelected = 1
        self.CurrentWindow = "OptionsWindow"
        [self.DestroyAllFrameChildren(Window) for i in range(10)]
        Platform_Options = tkinter.LabelFrame(Window, text=self.LConfig.GetTextByName("Platforms"))
        Platform1 = tkinter.Checkbutton(Platform_Options, text="Windows", variable=self.WindowsPlatform)
        Platform1.pack(anchor="nw", padx=10)
        Platform1 = tkinter.Checkbutton(Platform_Options, text="MacOS", variable=self.MacOSPlatform)
        Platform1.pack(anchor="nw", padx=10)
        Platform1 = tkinter.Checkbutton(Platform_Options, text="Linux", variable=self.LinuxPlatform)
        Platform1.pack(anchor="nw", padx=10)
        Platform1 = tkinter.Checkbutton(Platform_Options, text="Android", variable=self.AndroidPlatform)
        Platform1.pack(anchor="nw", padx=10)
        Platform1 = tkinter.Checkbutton(Platform_Options, text="IOS", variable=self.IOSPlatform)
        Platform1.pack(anchor="nw", padx=10)
        Platform1 = tkinter.Checkbutton(Platform_Options, text="Xbox 360", variable=self.Xbox360Platform)
        Platform1.pack(anchor="nw", padx=10)
        Platform1 = tkinter.Checkbutton(Platform_Options, text="Xbox One", variable=self.XboxOnePlatform)
        Platform1.pack(anchor="nw", padx=10)
        Platform1 = tkinter.Checkbutton(Platform_Options, text="Xbox Series X", variable=self.XboxSeriasXPlatform)
        Platform1.pack(anchor="nw", padx=10)
        Platform1 = tkinter.Checkbutton(Platform_Options, text="Play Station 3", variable=self.PS3Platform)
        Platform1.pack(anchor="nw", padx=10)
        Platform1 = tkinter.Checkbutton(Platform_Options, text="Play Station 4", variable=self.PS4Platform)
        Platform1.pack(anchor="nw", padx=10)
        Platform1 = tkinter.Checkbutton(Platform_Options, text="Play Station 5", variable=self.PS5Platform)
        Platform1.pack(anchor="nw", padx=10)
        Platform1 = tkinter.Checkbutton(Platform_Options, text="Nintendo Switch", variable=self.NintendoSwitchPlatform)
        Platform1.pack(anchor="nw", padx=10)
        Platform_Options.place(x=10, y=10, width=200, height=330)
    def ProfileWindow(self, Window):
        if self.CurrentWindow != "ProfileWindow": self.PageSelected = 1
        self.CurrentWindow = "ProfileWindow"
        [self.DestroyAllFrameChildren(Window) for i in range(10)]
        Games = list(set(self.GC.GetAllGamesInDB()) - set(self.UC.GetAllScoredGames()))
        Label = tkinter.Label(Window, text="{0}: ".format(self.LConfig.GetTextByName("Nickname")) + self.UC.GetUserName())
        Label.pack(side="top", anchor="nw", padx=10, pady=2)
        Label = tkinter.Label(Window, text="{0}: ".format(self.LConfig.GetTextByName("GamesLike")) + str(len(self.UC.DB["Games"])))
        Label.pack(side="top", anchor="nw", padx=10, pady=2)
        Label = tkinter.Label(Window, text="{0}: ".format(self.LConfig.GetTextByName("AVGScore")) + str(round(self.UC.GetAvgGamesScore(), 2)))
        Label.pack(side="top", anchor="nw", padx=10, pady=2)
        Label = tkinter.Label(Window, text="{0}: ".format(self.LConfig.GetTextByName("RandomGame")) + str(Games[random.randint(0, len(Games) - 1)]))
        Label.pack(side="top", anchor="nw", padx=10, pady=2)
    def ChangeMainFrame(self, MainFrame: tkinter.Frame | tkinter.LabelFrame, Window, event="enabled"):
        if event != "disabled":
            self.DestroyAllFrameChildren(MainFrame)
            Window(MainFrame)
    def GetPlatforms(self):
        return [n.get() for n in self.AllPlatforms]
    def MultipleArrays(self, array1: list, array2: list):
        for i in range(len(array1)):
            array1[i] *= array2[i]
        return array1
    def ExprToShow(self, array: list):
        return sum(self.MultipleArrays(self.GetPlatforms(), array))
    def MainWindow(self):
        Root = tkinter.Tk()
        self.sort_alg = tkinter.StringVar()
        self.sort_alg.set("minmax")
        Root.geometry(self.Geometry)
        Root.title(self.Title)
        Root.resizable(False, False)
        NeuronNetworkState = tkinter.StringVar()
        self.WindowsPlatform = tkinter.BooleanVar()
        self.LinuxPlatform = tkinter.BooleanVar()
        self.MacOSPlatform = tkinter.BooleanVar()
        self.AndroidPlatform = tkinter.BooleanVar()
        self.IOSPlatform = tkinter.BooleanVar()
        self.Xbox360Platform = tkinter.BooleanVar()
        self.XboxOnePlatform = tkinter.BooleanVar()
        self.XboxSeriasXPlatform = tkinter.BooleanVar()
        self.PS3Platform = tkinter.BooleanVar()
        self.PS4Platform = tkinter.BooleanVar()
        self.PS5Platform = tkinter.BooleanVar()
        self.NintendoSwitchPlatform = tkinter.BooleanVar()
        self.AllPlatforms = [self.MacOSPlatform, self.WindowsPlatform, self.LinuxPlatform, 
                             self.IOSPlatform, self.AndroidPlatform, self.Xbox360Platform, 
                             self.XboxOnePlatform, self.XboxSeriasXPlatform, self.PS3Platform, 
                             self.PS4Platform, self.PS5Platform, self.NintendoSwitchPlatform]
        NeuronNetworkState.set("Neuron Network (State): No NN")
        MenuFrame = tkinter.LabelFrame(Root, text=self.LConfig.GetTextByName("Menu"))
        ProfileButton = tkinter.Button(MenuFrame, text=self.LConfig.GetTextByName("Profile"))
        ProfileButton.pack(fill="x", padx=10, pady=5)
        ProfileButton.bind("<Button-1>", lambda event: self.ChangeMainFrame(MainFrame, self.ProfileWindow, event.widget["state"]))
        BrowserButton = tkinter.Button(MenuFrame, text=self.LConfig.GetTextByName("GameBrowser"))
        BrowserButton.pack(fill="x", padx=10, pady=5)
        BrowserButton["state"] = "disable"
        BrowserButton.bind("<Button-1>", lambda event: self.ChangeMainFrame(MainFrame, self.SearchWindow, event.widget["state"]))
        ScoredGamesButton = tkinter.Button(MenuFrame, text=self.LConfig.GetTextByName("ScoredGames"))
        ScoredGamesButton.pack(fill="x", padx=10, pady=5)
        ScoredGamesButton.bind("<Button-1>", lambda event: self.ChangeMainFrame(MainFrame, self.ScoredGamesWindow, event.widget["state"]))
        ScoredGamesButton = tkinter.Button(MenuFrame, text=self.LConfig.GetTextByName("RecommendedGames"))
        ScoredGamesButton.pack(fill="x", padx=10, pady=5)
        ScoredGamesButton.bind("<Button-1>", lambda event: self.ChangeMainFrame(MainFrame, self.RecommendedGamesWindow, event.widget["state"]))
        ScoredGamesButton = tkinter.Button(MenuFrame, text=self.LConfig.GetTextByName("Options"))
        ScoredGamesButton.pack(fill="x", padx=10, pady=5, side="bottom")
        ScoredGamesButton.bind("<Button-1>", lambda event: self.ChangeMainFrame(MainFrame, self.OptionsWindow, event.widget["state"]))
        MenuFrame.place(x=10, y=0, width=250, height=390)
        MainFrame = tkinter.LabelFrame(Root, text=self.LConfig.GetTextByName("Profile"))
        MainFrame.place(x=270, y=0, width=520, height=590)
        TrainFrame = tkinter.LabelFrame(Root, text=self.LConfig.GetTextByName("TS"))
        TrainLabel = tkinter.Label(TrainFrame, textvariable=NeuronNetworkState)
        TrainLabel.pack(anchor="nw", padx=5)
        TrainTime = tkinter.Label(TrainFrame, text="{1}: 0 {0}".format(self.LConfig.GetTextByName("Seconds"), self.LConfig.GetTextByName("Time")))
        TrainTime.pack(anchor="nw", padx=5)
        CacheTime = tkinter.Label(TrainFrame, text="{1}: {0}s".format(0.047*len(self.GC.GetAllGamesInDB()), self.LConfig.GetTextByName("CacheTime")))
        CacheTime.pack(anchor="nw", padx=5)
        LearnState1 = tkinter.Label(TrainFrame, text=self.LConfig.GetTextByName("LSN"))
        LearnState1.pack(anchor="nw", padx=5)
        LearnState2 = tkinter.Label(TrainFrame, text=self.LConfig.GetTextByName("LSN"))
        LearnState2.pack(anchor="nw", padx=5)
        ReTrainButton = tkinter.Button(TrainFrame, text=self.LConfig.GetTextByName("ReTrainNetwork"))
        ReTrainButton.pack(anchor="nw", padx=5, pady=5, side="bottom")
        def NetworkLoad():
            if len(self.UC.GetAllScoredGames()) > 0: 
                BrowserButton["state"] = "disabled"
                ReTrainButton["state"] = "disabled"
                NeuronNetworkState.set(self.LConfig.GetTextByName("NNLoading"))
                TStart = time.time()
                self.NN.network_train_first_mod()
                TrainTime["text"] = "{0}: ".format(self.LConfig.GetTextByName("Time")) + str(round(time.time() - TStart, 2)) + " seconds"
                BrowserButton["state"] = "active"
                NeuronNetworkState.set(self.LConfig.GetTextByName("NNL"))
                ReTrainButton["state"] = "active"
                BrowserButton["state"] = "active"
            else:
                ReTrainButton["state"] = "active"
                BrowserButton["state"] = "active"
        def RetrainNetwork():
            if self.CurrentWindow != "ProfileWindow":
                self.ChangeMainFrame(MainFrame=MainFrame, Window=self.ProfileWindow)
            self.PC.Delete()
            BrowserButton["state"] = "disabled"
            ReTrainButton["state"] = "disabled"
            NeuronNetworkState.set(self.LConfig.GetTextByName("NNLoading"))
            TStart = time.time()
            self.NN.network_train_first_mod(True, accuracy=self.PConfig.AllData["max_loss"], max_count=self.PConfig.AllData["max_try"], label=LearnState1, label1=LearnState2, label_time=TrainTime)
            TrainTime["text"] = "{0}: ".format(self.LConfig.GetTextByName("Time")) + str(round(time.time() - TStart, 2)) + " " + self.LConfig.GetTextByName("Seconds")
            BrowserButton["state"] = "active"
            NeuronNetworkState.set(self.LConfig.GetTextByName("NNL"))
            ReTrainButton["state"] = "active"
            BrowserButton["state"] = "active"
        threading.Thread(target=NetworkLoad).start()
        ReTrainButton.bind("<Button-1>", lambda event: threading.Thread(target=RetrainNetwork).start())
        TrainFrame.place(x=10, y=400, width=250, height=190)
        self.ChangeMainFrame(MainFrame, self.ProfileWindow)
        Root.mainloop()
    def __init__(self) -> None:
        self.GC = GameConfigs()
        self.UC = UserConfigs()
        self.PC = PredictCache()
        self.PConfig = ProgramConfig()
        self.LConfig = LangConfig()
        self.NN = NeuronNetwork(UC=self.UC, GC=self.GC, PC=self.PC)
        self.MainWindow()
PredictProgram()