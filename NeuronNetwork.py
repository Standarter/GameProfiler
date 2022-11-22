import copy
import time
import tkinter
from keras import models as KModel
from keras.layers import core as KSCode
from keras.models import load_model
from keras.optimizers import *
from keras.initializers.initializers_v2 import *
import tensorflow, numpy, functionstools, threading, os, gc
tensorflow.compat.v1.logging.set_verbosity(tensorflow.compat.v1.logging.ERROR)
from GameLib import GameConfigs
from UserLib import UserConfigs
from PredictLib import PredictCache
from matplotlib import pyplot
import random
class NeuronNetwork:
    UC = None
    GC = None
    PC = None
    NeuronModel = None
    FirstTrained = False
    BackgroundEvent = None
    BackroundThread = None
    BetterModel = None
    # NN Settings
    FirstNeurons = 5
    SecondNeurons = 3
    Batch_Size = 5
    LossFunc = "mse"
    ActFunc = "elu"
    Optimizer_NN = "adam"
    Initializer_NN = "RandomNormal"
    # NN End
    CurrentPath = "\\".join(__file__.split("\\")[:-1]) + "\\"
    LastFit = None
    ConfigDir = "DB" + "\\"
    def __init__(self, UC: UserConfigs, GC: GameConfigs, PC: PredictCache) -> None:
        self.UC = UC
        self.GC = GC
        self.PC = PC
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
        self.NeuronModel = KModel.Sequential()
        self.NeuronModel.add(KSCode.Dense(self.FirstNeurons, "elu"))
        self.NeuronModel.add(KSCode.Dense(self.SecondNeurons, "elu"))
        self.NeuronModel.add(KSCode.Dense(1, "elu"))
        self.NeuronModel.compile(optimizer="adam", loss="mse")
        if os.path.exists(self.CurrentPath + self.UC.GetUserName() + ".h5"):
            self.NeuronModel = load_model(self.CurrentPath + self.ConfigDir + self.UC.GetUserName() + ".h5")
    def format_data(self, data):
        for i in range(36, 48):
            data[i] /= 100
        data[49] -= 1900
        data[49] /= 200
        return data
    def load_network(self):
        self.NeuronModel = load_model(self.CurrentPath + self.ConfigDir + self.UC.GetUserName() + ".h5")
    def recreate_network(self):
        del self.NeuronModel
        self.NeuronModel = KModel.Sequential()
        self.NeuronModel.add(KSCode.Dense(self.FirstNeurons, "elu"))
        self.NeuronModel.add(KSCode.Dense(self.SecondNeurons, "elu"))
        self.NeuronModel.add(KSCode.Dense(1, "elu"))
        self.NeuronModel.compile(optimizer="adam", loss="mse")
    def network_train_first(self, force_train=False, max_time = 120, accuracy = 0.5, verbose = False):
        t0 = time.time()
        if os.path.exists(self.CurrentPath + self.ConfigDir + self.UC.GetUserName() + ".h5") == False or force_train:
            if force_train: os.remove(self.PC.ConfigFile)
            self.FirstTrained = False
            InputData = []
            OutputData = []
            MinLoss = 1000000000000000
            MaxLoss = -100000000000000
            for Game in self.UC.GetAllScoredGames():
                InputData.append(self.GC.GetGameByName(Game))
            for Game in self.UC.GetAllScoredGames():
                OutputData.append(self.UC.GetGameScore(Game))
            InputData = numpy.array(InputData, dtype=float)
            OutputData = numpy.array([[i] for i in OutputData])
            self.recreate_network()
            self.LastFit = self.NeuronModel.fit(InputData, OutputData, epochs=5, verbose=0)
            while self.LastFit.history["loss"][-1] > accuracy:
                self.recreate_network()
                self.LastFit = self.NeuronModel.fit(InputData, OutputData, epochs=5, verbose=0)
                while abs(self.LastFit.history["loss"][-1] - self.LastFit.history["loss"][-2]) > 0.01:
                    self.LastFit = self.NeuronModel.fit(InputData, OutputData, epochs=100, verbose=False, batch_size=self.Batch_Size)
                if time.time() - t0 > max_time: return 0
                if round(self.LastFit.history["loss"][-1], 3) < MinLoss:
                    MinLoss = round(self.LastFit.history["loss"][-1], 3)
                if round(self.LastFit.history["loss"][-1], 3) > MaxLoss:
                    MaxLoss = round(self.LastFit.history["loss"][-1], 3)
                print("Last loss:", 
                      round(self.LastFit.history["loss"][-1], 3), "|",
                      "Min loss:",
                      MinLoss, "|",
                      "Max loss:",
                      MaxLoss, "|", "Time:", round(time.time() - t0, 1), "s") if verbose else None
            self.NeuronModel.save(self.CurrentPath + self.ConfigDir + self.UC.GetUserName() + ".h5")
            print("Config: Saved") if verbose else None
        else:
            self.FirstTrained = True
            print("Config: Loaded")
            self.NeuronModel = load_model(self.CurrentPath + self.ConfigDir + self.UC.GetUserName() + ".h5")
    def network_train_first_mod(self, force_train=False, max_count = 25, accuracy = 0.2, verbose = False, label: tkinter.Label = None, label1: tkinter.Label = None, label_time: tkinter.Label = None):
        t0 = time.time()
        t_start = time.time()
        if os.path.exists(self.CurrentPath + self.ConfigDir + self.UC.GetUserName() + ".h5") == False or force_train:
            if force_train: 
                try: os.remove(self.PC.ConfigFile) 
                except: pass
            self.FirstTrained = False
            MinLoss = 10000000
            InputData = self.UC.GetAllScoredGames()
            OutputData = [self.UC.GetGameScore(n) for n in InputData]
            NNInput = [self.format_data(self.GC.GetGameByName(n)) for n in InputData]
            self.recreate_network()
            LF = self.NeuronModel.fit(NNInput, OutputData, epochs=100, verbose=0, batch_size=5)
            Count = 0
            while LF.history["loss"][-1] > accuracy and Count < max_count:
                self.recreate_network()
                LF = self.NeuronModel.fit(NNInput, OutputData, epochs=50, verbose=0, batch_size=5)
                print("Trying", Count)
                print("First: Initial weights")
                print("First time:", time.time() - t0)
                t0 = time.time()
                while LF.history["loss"][-1] - LF.history["loss"][-2] < -0.001:
                    print("Loss correction:", LF.history["loss"][-1] - LF.history["loss"][-2])
                    LF = self.NeuronModel.fit(NNInput, OutputData, epochs=100, verbose=0, batch_size=5)
                print("Corrected initial: Weights")
                print("Second time:", time.time() - t0)
                t0 = time.time()
                print(LF.history["loss"][-1])
                if LF.history["loss"][-1] < MinLoss:
                    MinLoss = LF.history["loss"][-1]
                    self.BetterModel = copy.deepcopy(self.NeuronModel.get_weights())
                    print("# Changed Neuron Model")
                if (LF.history["loss"][-1] < accuracy*2):
                    self.network_test(verbose=True)
                print("---------------------------")
                Count += 1
                if label != None:
                    label["text"] = "State: [Max accuracy: {0} ({1})]".format(1 - round(MinLoss, 3), Count)
                if label1 != None:
                    label1["text"] = "State: [Min Loss: {0} ({1})]".format(round(MinLoss, 3), Count)
                if label_time != None:
                    label_time["text"] = "Time: {0}s".format(time.time() - t_start)
            self.NeuronModel.set_weights(self.BetterModel)
            self.NeuronModel.save(self.CurrentPath + self.ConfigDir + self.UC.GetUserName() + ".h5")
            print("Less loss:", MinLoss)
            print("Config: Saved") if verbose else None
        else:
            self.FirstTrained = True
            print("Config: Loaded")
            self.NeuronModel = load_model(self.CurrentPath + self.ConfigDir + self.UC.GetUserName() + ".h5")
    def save_all(self):
        self.NeuronModel.save(self.CurrentPath + self.ConfigDir + self.UC.GetUserName() + ".h5")
    def network_train(self, event):
        if not self.BackgroundEvent.is_set():
            InputData = []
            OutputData = []
            for Game in self.UC.GetAllScoredGames():
                InputData.append(self.GC.GetGameByName(Game))
            for Game in self.UC.GetAllScoredGames():
                OutputData.append(self.UC.GetGameScore(Game))
            InputData = numpy.array(InputData, dtype=float)
            OutputData = numpy.array([[i] for i in OutputData])
            self.NeuronModel.fit(InputData, OutputData, epochs=1000, verbose=0)
            del InputData
            del OutputData
            gc.collect()
            self.network_train(event=event)
    def start_background_train(self):
        print("Started background learning")
        self.BackgroundEvent = threading.Event()
        self.BackroundThread = threading.Thread(target=self.network_train, args=(self.BackgroundEvent,))
        self.BackroundThread.start()
    def stop_background_train(self):
        print("Stopped background learning")
        self.BackgroundEvent.set()
        self.NeuronModel.save(self.CurrentPath + self.ConfigDir + self.UC.GetUserName() + ".h5")
        del self.BackroundThread
    def predict(self, GameName):
        return self.NeuronModel.predict(numpy.array([self.format_data(self.GC.GetGameByName(GameName=GameName))]), verbose=0)[0][0]
    @functionstools.functime(True)
    def predict_with_correlation(self, GameName):
        if not self.PC.GameInLib(GameName=GameName):
            Result = self.predict(GameName=GameName)-1
            if Result > 4:
                Result = 4
            elif Result < 0:
                Result = 0
            else:
                if Result + (5/100)*Result/2 < 5:
                    Result =  Result + (5/100)*Result/2
                else:
                    Result = Result
            self.PC.SetPredictScore(GameName=GameName, Score=round(25*Result, 2) if round(25*Result, 2) < 100 else 100)
            return round(25*Result, 2) if round(25*Result, 2) < 100 else 100
        else:
            return self.PC.GetPredictScore(GameName)
    def predict_with_correlation_np(self, GameName):
        Result = self.predict(GameName=GameName)
        if Result > 5:
            Result = 5
        elif Result < 1:
            Result = 1
        else:
            if Result + (5/100)*Result/2 < 5:
                Result =  Result + (5/100)*Result/2
            else:
                Result = Result
        return round(Result, 1)
    def show_loss_graph(self):
        pyplot.plot(self.LastFit.history["loss"])
        pyplot.show()
    def network_test(self, verbose = False, games_show=0):
        res = []
        for Game in (self.UC.GetAllScoredGames() if games_show == 0 else self.UC.GetAllScoredGames()[:games_show]):
            res.append(abs(self.UC.GetGameScore(Game) - self.predict(Game)))
            print("{2} [{0} | {1}]".format(self.UC.GetGameScore(Game), self.predict(Game), Game)) if verbose else None
        return sum(res)/len(res)
if __name__ == "__main__":
    UC = UserConfigs()
    GC = GameConfigs()
    PC = PredictCache()
    NN = NeuronNetwork(GC=GC, UC=UC, PC=PC)
    best = 1
    temp = 1000000000000
    print("Scored games:", len(UC.GetAllScoredGames()))
    """for j in range(3, 10):
        for k in range(1, 10):
            NN.FirstNeurons = j
            NN.SecondNeurons = k
            NN.recreate_network()
            for i in range(2, 4 + 1, 1):
                NN.Batch_Size = i
                t0 = time.time()
                NN.network_train_first(True)
                t1 = NN.network_test()
                print("Trained with (Batch_Size={0}; AVG_Loss={1}; Changed={2}; FH={3}; SH={4}):".format(i, t1, t1 < temp, NN.FirstNeurons, NN.SecondNeurons), time.time() - t0)
                if t1 < temp:
                    temp = t1
                    best = i
    """
    NN.recreate_network()
    NN.network_train_first_mod(True, max_count=100, accuracy=0.05, verbose=True)
    NN.network_test(True)  
    #print("Best batch:", best)
    #NN.show_loss_graph()