from fretFunctions import *

traceInput = ''
import warnings; warnings.simplefilter('ignore')
AllColumns, FRETvalues, LMHvalues, AvgFRETvalues, AvgLMHvalues = sortTrajectories(traceInput, window_size = 3, skip = False, resolution=2)
FRETLifetimes(LMHvalues)