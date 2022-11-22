import tkinter, json
from GameLib import GameConfigs
from UserLib import UserConfigs

class DBProgram:
    DB = None
    CurrentPath = "\\".join(__file__.split("\\")[:-1]) + "\\"
    ConfigName = "GameConfig.db"
    ConfigFile = CurrentPath + "DB\\" + ConfigName
    def LoadDB(self):
        DBOpen = open(self.ConfigFile, "r", encoding="utf-8")
        if DBOpen.read() == "":
            DBStart = open(self.ConfigFile, "w+", encoding="utf-8")
            DBStart.write("{}")
            DBStart.close()
        DBOpen.close()
        DBOpen = open(self.ConfigFile, "r", encoding="utf-8")
        self.DB = json.loads(DBOpen.read())
        DBOpen.close()
    def __init__(self):
        GameConfigs()
        self.LoadDB()
        DB = self.DB
        MainWindow = tkinter.Tk()
        MainWindow.title("DBConfigurator")
        MainWindow.geometry("800x400")
        MainWindow.resizable(False, False)
        def DBCheck(GameName):
            UC = UserConfigs()
            if GameName in DB[UC.GetUserName()]["Games"].keys():
                FoundLabel.set("Game name: ({0})".format("Found [You]"))
                GC = GameConfigs()
                GameData = GC.GetGameByUserName(UserName=UC.GetUserName(), GameName=GameName)
                print(GameData)
                for i in range(len(All_Genres)):
                    if GameData[i] >= 0.5:
                        All_Genres[i].set(True)
                    else:
                        All_Genres[i].set(False)
                for i in range(len(All_Genres), 
                            len(All_Genres) + len(All_Platforms)):
                    if GameData[i] >= 0.5:
                        All_Platforms[i - len(All_Genres)].set(True)
                    else:
                        All_Platforms[i - len(All_Genres)].set(False)
                for i in range(len(All_Genres) + len(All_Platforms), 
                            len(All_Genres) + len(All_Platforms) + len(All_Qualities)):
                    All_Qualities[i - (len(All_Genres) + len(All_Platforms))].set(GameData[i])
                for i in range(len(All_Genres) + len(All_Platforms) + len(All_Qualities), 
                            len(All_Genres) + len(All_Platforms) + len(All_Qualities) + len(All_Addictional)):
                    All_Addictional[i - (len(All_Genres) + len(All_Platforms) + len(All_Qualities))].set(GameData[i])
            else:
                GC = GameConfigs()
                FoundLabel.set("Game name: ({0})".format("Found [All]" if GC.GameInDB(GameName=GameName) else "Not found [All]"))
                GameData = GC.GetGameByName(GameName=GameName)
                for i in range(len(All_Genres)):
                    if GameData[i] >= 0.5:
                        All_Genres[i].set(True)
                    else:
                        All_Genres[i].set(False)
                for i in range(len(All_Genres), 
                            len(All_Genres) + len(All_Platforms)):
                    if GameData[i] >= 0.5:
                        All_Platforms[i - len(All_Genres)].set(True)
                    else:
                        All_Platforms[i - len(All_Genres)].set(False)
                for i in range(len(All_Genres) + len(All_Platforms), 
                            len(All_Genres) + len(All_Platforms) + len(All_Qualities)):
                    All_Qualities[i - (len(All_Genres) + len(All_Platforms))].set(GameData[i])
                for i in range(len(All_Genres) + len(All_Platforms) + len(All_Qualities), 
                            len(All_Genres) + len(All_Platforms) + len(All_Qualities) + len(All_Addictional)):
                    All_Addictional[i - (len(All_Genres) + len(All_Platforms) + len(All_Qualities))].set(GameData[i])
            return True
        Action_Genre = tkinter.BooleanVar()
        Adventure_Genre = tkinter.BooleanVar()
        Platformer_Genre = tkinter.BooleanVar()
        Shooter_Genre = tkinter.BooleanVar()
        Fighting_Genre = tkinter.BooleanVar()
        Stealth_Genre = tkinter.BooleanVar()
        Survival_Genre = tkinter.BooleanVar()
        Rhythm_Genre = tkinter.BooleanVar()
        Horror_Genre = tkinter.BooleanVar()
        Quest_Genre = tkinter.BooleanVar()
        Novel_Genre = tkinter.BooleanVar()
        InterractiveFilm_Genre = tkinter.BooleanVar()
        RP_Genre = tkinter.BooleanVar()
        RPG_Genre = tkinter.BooleanVar()
        MMO_Genre = tkinter.BooleanVar()
        OpenWorld_Genre = tkinter.BooleanVar()
        Simulator_Genre = tkinter.BooleanVar()
        Strategy_Genre = tkinter.BooleanVar()
        Sport_Genre = tkinter.BooleanVar()
        Racing_Genre = tkinter.BooleanVar()
        COOP_Genre = tkinter.BooleanVar()
        LANCOOP_Genre = tkinter.BooleanVar()
        Logical_Genre = tkinter.BooleanVar()
        Sandbox_Genre = tkinter.BooleanVar()
        All_Genres = [Action_Genre, Adventure_Genre, Platformer_Genre,
                      Shooter_Genre, Fighting_Genre, Stealth_Genre,
                      Survival_Genre, Rhythm_Genre, Horror_Genre,
                      Quest_Genre, Novel_Genre, InterractiveFilm_Genre,
                      RP_Genre, RPG_Genre, MMO_Genre, OpenWorld_Genre,
                      Simulator_Genre, Strategy_Genre, Sport_Genre, Racing_Genre,
                      COOP_Genre, LANCOOP_Genre, Logical_Genre, Sandbox_Genre]
        #
        MacOS = tkinter.BooleanVar()
        WindowsOS = tkinter.BooleanVar()
        LinuxOS = tkinter.BooleanVar()
        IOSOS = tkinter.BooleanVar()
        AndroidOS = tkinter.BooleanVar()
        Xbox360OS = tkinter.BooleanVar()
        PS3OS = tkinter.BooleanVar()
        XboxOneOS = tkinter.BooleanVar()
        PS4OS = tkinter.BooleanVar()
        XboxXOS = tkinter.BooleanVar()
        PS5OS = tkinter.BooleanVar()
        NintendoSwitchOS = tkinter.BooleanVar()
        All_Platforms = [MacOS, WindowsOS, LinuxOS, IOSOS, 
                         AndroidOS, Xbox360OS, XboxOneOS, XboxXOS,
                         PS3OS, PS4OS, PS5OS, NintendoSwitchOS]
        #
        Quality_Graphics = tkinter.IntVar()
        Quality_Sound = tkinter.IntVar()
        Quality_Interface = tkinter.IntVar()
        Quality_Style = tkinter.IntVar()
        
        Mechanics_Gameplay = tkinter.IntVar()
        Mechanics_Difficulty = tkinter.IntVar()
        Mechanics_AI = tkinter.IntVar()
        Mechanics_Diversity = tkinter.IntVar()
        
        History_Story = tkinter.IntVar()
        History_Logic = tkinter.IntVar()
        History_Thoroughness = tkinter.IntVar()
        History_Atmosphere = tkinter.IntVar()
        
        All_Qualities = [Quality_Graphics, Quality_Sound, Quality_Interface, Quality_Style,
                         Mechanics_Gameplay, Mechanics_Difficulty, Mechanics_AI, Mechanics_Diversity,
                         History_Story, History_Logic, History_Thoroughness, History_Atmosphere]
        #
        AVG_Time = tkinter.IntVar()
        Game_Year = tkinter.IntVar()
        CompanyPopularity = tkinter.IntVar()
        Difficulty = tkinter.IntVar()
        Tension = tkinter.IntVar()
        Regularity = tkinter.IntVar()
        Scary = tkinter.IntVar()
        Emotionality = tkinter.IntVar()
        SingleQuality = tkinter.IntVar()
        OnlineQuality = tkinter.IntVar()
        
        All_Addictional = [AVG_Time, Game_Year, CompanyPopularity, 
                           Difficulty, Tension, Regularity, Scary, 
                           Emotionality, SingleQuality, OnlineQuality]
        #
        FoundLabel = tkinter.StringVar()
        FoundLabel.set("Game name:")
        GameCheck = (MainWindow.register(DBCheck), "%P")
        SearchFrame = tkinter.LabelFrame(MainWindow)
        SearchFrame.place(x = 10, y = 10, width=250, height=50)
        TextEntry = tkinter.Entry(SearchFrame, validatecommand=GameCheck, validate="key")
        TextEntry.pack(side="bottom", fill="x", pady=3, padx=5)
        Label = tkinter.Label(SearchFrame, textvariable=FoundLabel)
        Label.pack(side="top", fill="both", expand=True)
        Genre_Frame = tkinter.LabelFrame(MainWindow, text="Genres")
        Genre_Frame.place(x = 10, y = 60, width=250, height=320)
        Genre_First = tkinter.Frame(Genre_Frame, width=150)
        Genre_First.pack(side="left", fill="y")
        Genre_Second = tkinter.Frame(Genre_Frame, width=150)
        Genre_Second.pack(side="left", fill="y")
        tkinter.Checkbutton(Genre_First, text="Action", variable=Action_Genre).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Genre_First, text="Adventure", variable=Adventure_Genre).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Genre_First, text="Platformer", variable=Platformer_Genre).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Genre_First, text="Shooter", variable=Shooter_Genre).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Genre_First, text="Fighting", variable=Fighting_Genre).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Genre_First, text="Stealth", variable=Stealth_Genre).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Genre_First, text="Survival", variable=Survival_Genre).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Genre_First, text="Rhythm", variable=Rhythm_Genre).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Genre_First, text="Horror", variable=Horror_Genre).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Genre_First, text="Quest", variable=Quest_Genre).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Genre_First, text="Visual Novel", variable=Novel_Genre).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Genre_First, text="Interractive Film", variable=InterractiveFilm_Genre).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Genre_Second, text="Role Play (RP)", variable=RP_Genre).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Genre_Second, text="RPG", variable=RPG_Genre).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Genre_Second, text="MMO", variable=MMO_Genre).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Genre_Second, text="Open World", variable=OpenWorld_Genre).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Genre_Second, text="Simulator", variable=Simulator_Genre).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Genre_Second, text="Strategy", variable=Strategy_Genre).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Genre_Second, text="Sport", variable=Sport_Genre).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Genre_Second, text="Racing", variable=Racing_Genre).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Genre_Second, text="COOP", variable=COOP_Genre).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Genre_Second, text="LAN COOP", variable=LANCOOP_Genre).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Genre_Second, text="Logical", variable=Logical_Genre).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Genre_Second, text="Sandbox", variable=Sandbox_Genre).pack(side="top", anchor="nw")
        #
        Platform_Frame = tkinter.LabelFrame(MainWindow, width=300, text="Platform")
        Platform_Frame.place(x = 270, y = 60, height=320)
        tkinter.Checkbutton(Platform_Frame, text="MacOS", variable=MacOS).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Platform_Frame, text="Windows", variable=WindowsOS).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Platform_Frame, text="Linux", variable=LinuxOS).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Platform_Frame, text="IOS", variable=IOSOS).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Platform_Frame, text="Android", variable=AndroidOS).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Platform_Frame, text="Xbox 360", variable=Xbox360OS).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Platform_Frame, text="Xbox One", variable=XboxOneOS).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Platform_Frame, text="Xbox X", variable=XboxXOS).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Platform_Frame, text="PS 3", variable=PS3OS).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Platform_Frame, text="PS 4", variable=PS4OS).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Platform_Frame, text="PS 5", variable=PS5OS).pack(side="top", anchor="nw")
        tkinter.Checkbutton(Platform_Frame, text="Nintendo Swith", variable=NintendoSwitchOS).pack(side="top", anchor="nw")
        GraphicsFrame = tkinter.LabelFrame(MainWindow, text="Quality (1% - 100%)")
        TF = tkinter.Frame(GraphicsFrame)
        TL = tkinter.Label(TF, text="Graphics")
        TL.pack(side="left")
        TE = tkinter.Entry(TF, width=5, textvariable=Quality_Graphics)
        TE.pack(side="right", padx=3)
        TF.pack(side="top", fill="x", padx=5)
        TF = tkinter.Frame(GraphicsFrame)
        TL = tkinter.Label(TF, text="Sound")
        TL.pack(side="left")
        TE = tkinter.Entry(TF, width=5, textvariable=Quality_Sound)
        TE.pack(side="right", padx=3)
        TF.pack(side="top", fill="x", padx=5)
        TF = tkinter.Frame(GraphicsFrame)
        TL = tkinter.Label(TF, text="Interface")
        TL.pack(side="left")
        TE = tkinter.Entry(TF, width=5, textvariable=Quality_Interface)
        TE.pack(side="right", padx=3)
        TF.pack(side="top", fill="x", padx=5)
        TF = tkinter.Frame(GraphicsFrame)
        TL = tkinter.Label(TF, text="Style")
        TL.pack(side="left")
        TE = tkinter.Entry(TF, width=5, textvariable=Quality_Style)
        TE.pack(side="right", padx=3)
        TF.pack(side="top", fill="x", padx=5)
        GraphicsFrame.place(x = 395, y = 60, width=150, height=105)
        MechanicsFrame = tkinter.LabelFrame(MainWindow, text="Mechanics (1% - 100%)")
        TF = tkinter.Frame(MechanicsFrame)
        TL = tkinter.Label(TF, text="Gameplay")
        TL.pack(side="left")
        TE = tkinter.Entry(TF, width=5, textvariable=Mechanics_Gameplay)
        TE.pack(side="right", padx=3)
        TF.pack(side="top", fill="x", padx=5)
        TF = tkinter.Frame(MechanicsFrame)
        TL = tkinter.Label(TF, text="Difficulty")
        TL.pack(side="left")
        TE = tkinter.Entry(TF, width=5, textvariable=Mechanics_Difficulty)
        TE.pack(side="right", padx=3)
        TF.pack(side="top", fill="x", padx=5)
        TF = tkinter.Frame(MechanicsFrame)
        TL = tkinter.Label(TF, text="AI")
        TL.pack(side="left")
        TE = tkinter.Entry(TF, width=5, textvariable=Mechanics_AI)
        TE.pack(side="right", padx=3)
        TF.pack(side="top", fill="x", padx=5)
        TF = tkinter.Frame(MechanicsFrame)
        TL = tkinter.Label(TF, text="Diversity")
        TL.pack(side="left")
        TE = tkinter.Entry(TF, width=5, textvariable=Mechanics_Diversity)
        TE.pack(side="right", padx=3)
        TF.pack(side="top", fill="x", padx=5)
        MechanicsFrame.place(x = 395, y = 166, width=150, height=105)
        HistoryFrame = tkinter.LabelFrame(MainWindow, text="History (1% - 100%)")
        TF = tkinter.Frame(HistoryFrame)
        TL = tkinter.Label(TF, text="Story")
        TL.pack(side="left")
        TE = tkinter.Entry(TF, width=5, textvariable=History_Story)
        TE.pack(side="right", padx=3)
        TF.pack(side="top", fill="x", padx=5)
        TF = tkinter.Frame(HistoryFrame)
        TL = tkinter.Label(TF, text="Logics")
        TL.pack(side="left")
        TE = tkinter.Entry(TF, width=5, textvariable=History_Logic)
        TE.pack(side="right", padx=3)
        TF.pack(side="top", fill="x", padx=5)
        TF = tkinter.Frame(HistoryFrame)
        TL = tkinter.Label(TF, text="Detail")
        TL.pack(side="left")
        TE = tkinter.Entry(TF, width=5, textvariable=History_Thoroughness)
        TE.pack(side="right", padx=3)
        TF.pack(side="top", fill="x", padx=5)
        TF = tkinter.Frame(HistoryFrame)
        TL = tkinter.Label(TF, text="Atmosphere")
        TL.pack(side="left")
        TE = tkinter.Entry(TF, width=5, textvariable=History_Atmosphere)
        TE.pack(side="right", padx=3)
        TF.pack(side="top", fill="x", padx=5)
        HistoryFrame.place(x = 395, y = 276, width=150, height=105)
        Addictional_Frame = tkinter.LabelFrame(MainWindow, width=300, text="Addictional (1% - 100%)")
        TF = tkinter.Frame(Addictional_Frame)
        TL = tkinter.Label(TF, text="Average time (In hours)")
        TL.pack(side="left")
        TE = tkinter.Entry(TF, width=5, textvariable=AVG_Time)
        TE.pack(side="right", padx=3)
        TF.pack(side="top", fill="x", padx=5)
        TF = tkinter.Frame(Addictional_Frame)
        TL = tkinter.Label(TF, text="Game year (1900-2XXX)")
        TL.pack(side="left")
        TE = tkinter.Entry(TF, width=5, textvariable=Game_Year)
        TE.pack(side="right", padx=3)
        TF.pack(side="top", fill="x", padx=5)
        TF = tkinter.Frame(Addictional_Frame)
        TL = tkinter.Label(TF, text="Company popularity")
        TL.pack(side="left")
        TE = tkinter.Entry(TF, width=5, textvariable=CompanyPopularity)
        TE.pack(side="right", padx=3)
        TF.pack(side="top", fill="x", padx=5)
        TF = tkinter.Frame(Addictional_Frame)
        TL = tkinter.Label(TF, text="Difficulty")
        TL.pack(side="left")
        TE = tkinter.Entry(TF, width=5, textvariable=Difficulty)
        TE.pack(side="right", padx=3)
        TF.pack(side="top", fill="x", padx=5)
        TF = tkinter.Frame(Addictional_Frame)
        TL = tkinter.Label(TF, text="Tension ")
        TL.pack(side="left")
        TE = tkinter.Entry(TF, width=5, textvariable=Tension)
        TE.pack(side="right", padx=3)
        TF.pack(side="top", fill="x", padx=5)
        TF = tkinter.Frame(Addictional_Frame)
        TL = tkinter.Label(TF, text="Regularity ")
        TL.pack(side="left")
        TE = tkinter.Entry(TF, width=5, textvariable=Regularity)
        TE.pack(side="right", padx=3)
        TF.pack(side="top", fill="x", padx=5)
        TF = tkinter.Frame(Addictional_Frame)
        TL = tkinter.Label(TF, text="Scary ")
        TL.pack(side="left")
        TE = tkinter.Entry(TF, width=5, textvariable=Scary)
        TE.pack(side="right", padx=3)
        TF.pack(side="top", fill="x", padx=5)
        TF = tkinter.Frame(Addictional_Frame)
        TL = tkinter.Label(TF, text="Emotionality ")
        TL.pack(side="left")
        TE = tkinter.Entry(TF, width=5, textvariable=Emotionality)
        TE.pack(side="right", padx=3)
        TF.pack(side="top", fill="x", padx=5)
        TF = tkinter.Frame(Addictional_Frame)
        TL = tkinter.Label(TF, text="Single Quality ")
        TL.pack(side="left")
        TE = tkinter.Entry(TF, width=5, textvariable=SingleQuality)
        TE.pack(side="right", padx=3)
        TF.pack(side="top", fill="x", padx=5)
        TF = tkinter.Frame(Addictional_Frame)
        TL = tkinter.Label(TF, text="Online Quality ")
        TL.pack(side="left")
        TE = tkinter.Entry(TF, width=5, textvariable=OnlineQuality)
        TE.pack(side="right", padx=3)
        TF.pack(side="top", fill="x", padx=5)
        Addictional_Frame.place(x = 560, y = 60, height=320, width= 220)
        def DBAddButtonCallback(event):
            GameConfiguration = []
            for element in All_Genres:
                GameConfiguration.append(int(element.get()))
            for element in All_Platforms:
                GameConfiguration.append(int(element.get()))
            for element in All_Qualities:
                GameConfiguration.append(int(element.get()))
            for element in All_Addictional:
                GameConfiguration.append(int(element.get()))
            UC = UserConfigs()
            GC = GameConfigs()
            GC.AddToConfig(UC.GetUserName(), str(TextEntry.get()), GameConfiguration)
        DBAddButton = tkinter.Button(Addictional_Frame, text="Add To Database")
        DBAddButton.bind("<Button-1>", DBAddButtonCallback)
        DBAddButton.pack(side="bottom", pady=10)
        MainWindow.mainloop()
DBProgram()