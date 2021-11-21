#thread.py file
#graph all threaded agents with the data from scraper.py

import scraper as scr
import matplotlib.pyplot as plt
import numpy as np
import threading
import time

class linReg:

    def __init__(self, col):
        self.col = col #defines which column on the database we need to work with

    def showPlot(self):
        plt.close()
        xpoints = []
        ypoints = []
        for i in scr.greenhouseDB.search():
            xpoints.append(i[0])
            ypoints.append(i[self.col])
        plt.scatter(xpoints, ypoints, color = 'b')

        coef = np.polyfit(xpoints, ypoints, 1)
        poly1d_fn = np.poly1d(coef)
        plt.plot(xpoints, ypoints, 'ro', xpoints, poly1d_fn(xpoints))
        plt.xlim(1979, 2020)
        agents = [" ", "CO2", "CH4", "N2O", "CFCs", "HCFCs", "HFCs"] #first element is placeholder
        plt.title(agents[self.col])
        plt.xlabel("YEAR")
        plt.ylabel("Global Radiative Forcing(W $\mathregular{m^{-2}}$ )")
        
        plt.show()


#xy = linReg(1)
#xy.showPlot()
lines = []

def plotLine(col):
    for i in range(6):
        col.append(linReg(i + 1))
        print("all plots made")

def showLine(col):
    for i in range(6):
        col[i].showPlot()
        print("Showing plots")

thread1 = threading.Thread(target=plotLine, args=(lines,)) #to create the graph
thread2 = threading.Thread(target=showLine, args=(lines,)) #to show the graph

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print("done")

