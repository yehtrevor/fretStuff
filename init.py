from fretFunctions import *
import warnings; warnings.simplefilter('ignore')
import time
import os
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog


newFileStorage = 'Test' #name this for folder output
outputName = 'test' #this is the output name for all your files
#Edit me!#
startDir = filedialog.askdirectory(initialdir="C:/Users/trevo/PycharmProjects/fretStuff")
root = tk.Tk()
root.withdraw()
traceInputTemp = filedialog.askopenfilenames()
traceInput = traceInputTemp[0].replace('\\','/')


if not os.path.exists(startDir +'/' + newFileStorage):
    os.mkdir(startDir +'/' + newFileStorage)

os.chdir(startDir +'/' +newFileStorage+'/') #moves you into the correct directory so all .txt files are properly stored
print(os.getcwd())


#Edit me!#


AllColumns, FRETvalues, LMHvalues, AvgFRETvalues, AvgLMHvalues = sortTrajectories(traceInput, window_size = 3, skip = False, resolution=2)
# # lo_LMH, lo_LMH_res = LMHDistribution(AvgLMHvalues, 0,f'lo_{outputName}.txt',resolution=0.150)
# # mid_LMH,mid_LMH_res = LMHDistribution(AvgLMHvalues, 1,f'mid_{outputName}.txt',resolution=0.150)
# # hi_LMH, hi_LMH_res = LMHDistribution(AvgLMHvalues, 2,f'hi_{outputName}.txt',resolution=0.150)
# # countTransitions(AvgLMHvalues,f'transitions_{outputName}.txt')
# # AvgFRETvalues.to_csv(f'FRETvalues_{outputName}.txt', sep='\t')
# # AvgLMHvalues.to_csv(f'LMHvalues_{outputName}.txt', sep='\t')
TotalTimes = sum(FRETLifetimes(LMHvalues))
completeOcclusions, jumps, unproductiveOcclusions,unproductiveOcclusionsTotal, OccFromZero, OccFromTwo=completeTransitions(AvgLMHvalues)
outputCompleteTransitions(outputName, completeOcclusions, jumps, unproductiveOcclusions, unproductiveOcclusionsTotal, TotalTimes, OccFromZero, OccFromTwo)
#
#
# # binwidth = 1
# # plt.subplot(1,3,1)
# # plt.hist(lo_LMH, bins=range(min(lo_LMH), max(lo_LMH) + binwidth, binwidth),color='red', edgecolor='black')
# # plt.xlabel('Frames')
# # plt.ylabel('Frequency')
# # plt.title('Lo')
# # plt.xlim((0,30))
# #
# # plt.subplot(1,3,2)
# # plt.hist(mid_LMH, bins=range(min(mid_LMH), max(mid_LMH) + binwidth, binwidth), color='white', edgecolor='black')
# # plt.xlabel('Frames')
# # plt.ylabel('Frequency')
# # plt.title('Mid')
# # plt.xlim((0,30))
# #
# # plt.subplot(1,3,3)
# # plt.hist(hi_LMH, bins=range(min(hi_LMH), max(hi_LMH) + binwidth, binwidth), edgecolor='black')
# # plt.xlabel('Frames')
# # plt.ylabel('Frequency')
# # plt.title('Hi')
# # plt.xlim((0,30))
# #
# #
# # # Display the plot
# # figure = plt.gcf() # get current figure
# # figure.set_size_inches(20, 6)
# # plt.savefig(f"{outputName}.jpg", transparent=True, dpi = 800)
# # plt.show()
