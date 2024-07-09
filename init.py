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


newFileStorage = 'Y59F_BestFRET' #name this for folder output
outputName = 'Y59F_BestFRET' #this is the output name for all your files



#Edit me!#
startDir = filedialog.askdirectory(initialdir=r"C:\Users\tyeh\Desktop\fretStuff")
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
# lo_LMH, lo_LMH_res = LMHDistribution(AvgLMHvalues, 0,f'lo_{outputName}.txt',resolution=0.150)
# mid_LMH,mid_LMH_res = LMHDistribution(AvgLMHvalues, 1,f'mid_{outputName}.txt',resolution=0.150)
# hi_LMH, hi_LMH_res = LMHDistribution(AvgLMHvalues, 2,f'hi_{outputName}.txt',resolution=0.150)
# countTransitions(AvgLMHvalues,f'transitions_{outputName}.txt')
# AvgFRETvalues.to_csv(f'FRETvalues_{outputName}.txt', sep='\t')
AvgLMHvalues.to_csv(f'LMHvalues_{outputName}.txt', sep='\t')
# TotalTimes = sum(FRETLifetimes(LMHvalues))
completeOcclusions, jumps, unproductiveOcclusions,unproductiveOcclusionsTotal, OccFromZero, OccFromTwo=completeTransitions(AvgLMHvalues)
completeOcclusions2, jumps2, unproductiveOcclusions2,unproductiveOcclusionsTotal2, OccFromZero2, OccFromTwo2, zeroToTwo, twoToZero =newcompleteTransitions(AvgLMHvalues)

FromZero = sum(transitionProbability(OccFromZero2))
FromTwo = sum(transitionProbability(OccFromTwo2))
# print(FromZero)
# print(FromTwo)
# print(sum(zeroToTwo))
# print(sum(twoToZero))
print('PO, P(1 -> 2 | 0): ', sum(zeroToTwo)/(FromZero+sum(zeroToTwo)))
print('UO, P(1 -> 0 | 0): ', 1-(sum(zeroToTwo)/(FromZero+sum(zeroToTwo))))
print('PO, P(1 -> 0 | 2): ', sum(twoToZero)/(FromTwo+sum(twoToZero)))
print('UO, P(1 -> 2 | 2): ', 1-(sum(twoToZero)/(FromTwo+sum(twoToZero))))


# print(sum(completeOcclusions) == sum(zeroToTwo)+sum(twoToZero))
# print(sum(completeOcclusions))
# print(sum(completeOcclusions2))
# print(completeOcclusions2)
# print(zeroToTwo)
# print(twoToZero)
#outputCompleteTransitions(outputName, completeOcclusions, jumps, unproductiveOcclusions, unproductiveOcclusionsTotal, TotalTimes, OccFromZero, OccFromTwo)
# transitionProb = transitionProbability(unproductiveOcclusions)
# with open(f"UnprodOccBeforeTransition_{outputName}", 'w') as file:
#     file.write(str(transitionProb))
#
# zeroStates, twoStates = midStateProbability(AvgLMHvalues)
# print('Percentage of Mid to Lo',zeroStates/(zeroStates+twoStates))
# print('Percentage of Mid to Hi',twoStates/(zeroStates+twoStates))

# binwidth = 1
# plt.subplot(1,3,1)
# plt.hist(lo_LMH, bins=range(min(lo_LMH), max(lo_LMH) + binwidth, binwidth),color='red', edgecolor='black')
# plt.xlabel('Frames')
# plt.ylabel('Frequency')
# plt.title('Lo')
# plt.xlim((0,30))
#
#
# plt.subplot(1,3,2)
# plt.hist(mid_LMH, bins=range(min(mid_LMH), max(mid_LMH) + binwidth, binwidth), color='white', edgecolor='black')
# plt.xlabel('Frames')
# plt.ylabel('Frequency')
# plt.title('Mid')
# plt.xlim((0,30))
#
# plt.subplot(1,3,3)
# plt.hist(hi_LMH, bins=range(min(hi_LMH), max(hi_LMH) + binwidth, binwidth), edgecolor='black')
# plt.xlabel('Frames')
# plt.ylabel('Frequency')
# plt.title('Hi')
# plt.xlim((0,30))
#
#
# # Display the plot
# figure = plt.gcf() # get current figure
# figure.set_size_inches(20, 6)
# plt.savefig(f"{outputName}_LMH_Histograms.jpg", transparent=True, dpi = 800)
# plt.show()
#
# plt.hist(transitionProb, density = True, cumulative=True,histtype="step", bins=range(min(transitionProb), max(transitionProb) + binwidth, binwidth), edgecolor='black')
# plt.xlim(-.5, max(transitionProb))
# plt.xlabel('Unproductive Occlusion')
# plt.ylabel('CDF')
# plt.title('Cumulative Distribution of Unproductive Occlusions')
# figure = plt.gcf() # get current figure
# figure.set_size_inches(8, 6)
# plt.savefig(f"{outputName}_CumulativeSum_UnprodOcc.jpg", transparent=True, dpi = 800)
# plt.show()
