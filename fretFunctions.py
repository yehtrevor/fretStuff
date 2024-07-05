#FUNCTIONS FOR ANALYSIS#
########################
########################
########################

import pandas as pd
import numpy as np


### This function is used for traces that have been previously sorted into dynamic traces.
def sortTrajectories(traceInput, window_size = 3, skip = False, resolution = 2):
    #read in FRET by each frame; skip allows you to analyze
    if skip == True:
      df = pd.read_csv(traceInput, delimiter='\t', index_col=False, skiprows=lambda x: x % resolution != 0)
    else:
      df = pd.read_csv(traceInput, delimiter='\t', index_col=False)

    selected_columns = df.iloc[:, 1::4]

    #make array that is the same dimesntions as selected_columns
    dimensions = selected_columns.shape

    LMHvalues = pd.DataFrame(0,index=np.arange(dimensions[0]),columns=np.arange(dimensions[1]))

    FRETvalues = selected_columns.iloc[:,]

#range 1 - lo 0-0.35, mid 0.35-0.45, hi 0.45-1
#range 2 - lo 0-0.35, mid 0.35-0.55, hi 0.55-1
#range 3 - lo 0-0.3, mid 0.3-0.55, hi 0.55-1
#range 4 - lo 0-0.3, mid 0.3-0.45, hi 0.45-1
#range 5 - lo 0-0.35, mid 0.35-0.55, hi 0.55-1
#range 6 - lo 0-0.4, mid 0.4-0.55, hi 0.55-1
    for i in range(len(FRETvalues.columns)):
        for j in range(len(FRETvalues)):
            if 0 < FRETvalues.iloc[:, i][j] <= 0.4:
                LMHvalues.iloc[:, i][j] = 0
            elif 0.4 < FRETvalues.iloc[:, i][j] <= 0.55:
                LMHvalues.iloc[:, i][j] = 1
            elif 0.55 < FRETvalues.iloc[:, i][j] <= 1:
                LMHvalues.iloc[:, i][j] = 2
            else:
                LMHvalues.iloc[:, i][j] = np.nan
    #for i in range(len(LMHvalues.columns)):
    #    for j in range(len(LMHvalues)-1):
    #        if LMHvalues.iloc[j, i] == LMHvalues.iloc[j + 1, i]:
    #            LMHvalues.iloc[j, i] = np.nan
    #        else:
    #            break
    #
    #        if LMHvalues.iloc[-j, i] == LMHvalues.iloc[-j-1 , i]:
    #            LMHvalues.iloc[-j, i] = np.nan
    #        else:
    #            break

    AvgLMHvalues = pd.DataFrame(0,index=np.arange(dimensions[0]),columns=np.arange(dimensions[1]))
    AvgFRETvalues = pd.DataFrame(index=FRETvalues.index)

    #Boxcar average with window size of 3 to average FRET data. This is to remove events that may bounce back and forth bewtween states.

    for column in FRETvalues.columns:
        AvgFRETvalues[column] = FRETvalues[column].copy()  # Copy the column to avoid modifying the original data
        for i in range(1, window_size):
            AvgFRETvalues[column] += FRETvalues[column].shift(i)
        AvgFRETvalues[column] /= window_size


    for i in range(len(AvgFRETvalues.columns)):
      for j in range(len(AvgFRETvalues)):
          if 0 < AvgFRETvalues.iloc[:, i][j] <= 0.4:
              AvgLMHvalues.iloc[:, i][j] = 0
          elif 0.4 < AvgFRETvalues.iloc[:, i][j] <= 0.55:
              AvgLMHvalues.iloc[:, i][j] = 1
          elif 0.55 < AvgFRETvalues.iloc[:, i][j] <= 1:
              AvgLMHvalues.iloc[:, i][j] = 2
          else:
              AvgLMHvalues.iloc[:, i][j] = np.nan
    print("sortTrajectories is complete.")
    return selected_columns, FRETvalues, LMHvalues, AvgFRETvalues, AvgLMHvalues

#--------------------------#------------------------------#--------------------------------#---------------------------#--------------------------#
#--------------------------#------------------------------#--------------------------------#---------------------------#--------------------------#
#--------------------------#------------------------------#--------------------------------#---------------------------#--------------------------#

def traceClassification(df, threshold):
    jumpsPerTrace = []
    for i in range(len(df.columns)):
      new_jumps = 0
      previousValues=[]
      for j in range(len(df)):
        if j == 0:
          start = df.iloc[:, i][j] - threshold
          if start > 0:
            previousValues.append(1)
          else:
            previousValues.append(-1)
        else:
          if ((df.iloc[:, i][j] - threshold) / abs((df.iloc[:, i][j] - threshold))) == previousValues[j-1]:
            #print(((df.iloc[:, i][j] - threshold) / abs((df.iloc[:, i][j] - threshold))) == previousValues[j-1])
            previousValues.append(previousValues[j-1])
          else:
            previousValues.append(previousValues[j-1]*-1)
            new_jumps += 1
      jumpsPerTrace.append(new_jumps)
    return jumpsPerTrace


#--------------------------#------------------------------#--------------------------------#---------------------------#--------------------------#
#--------------------------#------------------------------#--------------------------------#---------------------------#--------------------------#
#--------------------------#------------------------------#--------------------------------#---------------------------#--------------------------#

#{ } Add the surivial lifetime of the dyes, fit to a falling exponential

### This function is used for traces that have been pre-selected using a user-specified filter in SPARTAN.
### This includes all FRET traces. This is just used to look at photobleaching. Resolution is in seconds.
def FRETLifetimes(LMHvalues,window = 3, avg =True, resolution = 0.1):
    Lifetimes = []
    counter = 0
    for i in range(len(LMHvalues.columns)):
        for j in range(len(LMHvalues)):
            if LMHvalues.iloc[:,i][j] == 0 or LMHvalues.iloc[:,i][j] == 1 or LMHvalues.iloc[:,i][j] == 2:
                counter += 1
        if avg == True:
            Lifetimes.append(counter * resolution / window)
        else:
            Lifetimes.append(counter * resolution)
        #print(counter)
        counter = 0
    print("FRETLifetimes is complete.")
    return Lifetimes

#--------------------------#------------------------------#--------------------------------#---------------------------#--------------------------#
#--------------------------#------------------------------#--------------------------------#---------------------------#--------------------------#
#--------------------------#------------------------------#--------------------------------#---------------------------#--------------------------#


###This function is used for traces that have been processed by the function sortTraces. This will give the Lo-Mid-Hi data. This is used to calculate the dwell times of each state.

#{ } Output dwell times of each state.

def LMHDistribution(LMHvalues, LMHnum, LMHOutput,resolution):
    counter = 0
    counterList = []
    counterListResolution = []

    for i in range(len(LMHvalues.columns)):
        for j in range(len(LMHvalues)):
            if LMHvalues.iloc[:, i][j] == float(LMHnum):
                counter += 1
            elif counter != 0:
                counterList.append(counter)
                counterListResolution.append(counter*resolution)
                counter = 0  # Reset counter only when encountering a different value

    # Append the last counter value if it's not zero after the loops
    if counter != 0:
        counterList.append(counter)
        counterListResolution.append(counter * resolution)
    with open(LMHOutput, 'w') as file:
        file.write(str(counterList))
    print("LMHDistribution is complete.")
    return counterList, counterListResolution

#--------------------------#------------------------------#--------------------------------#---------------------------#--------------------------#
#--------------------------#------------------------------#--------------------------------#---------------------------#--------------------------#
#--------------------------#------------------------------#--------------------------------#---------------------------#--------------------------#


### This function is used for counting transitions that occur.

#04-16-2024: Made a change at the end of each window, added else statement that takes care of when run into nan value - just break
def countTransitions(transitions, outputName):
    allTransitions = []

    for i in range(len(transitions.columns)):
        col = [0, 0, 0, 0, 0, 0]  # Initialize transition counters
        for p in range(0, len(transitions) - 1, 2):
            window1 = transitions.iloc[p:p+2, i].tolist()
            window2 = transitions.iloc[p+1:p+3, i].tolist()

            invalid_windows = [[0, 0], [1, 1], [2, 2], [0], [1], [2], []]

            if window1 not in invalid_windows:
                if window1 == [0, 1]:
                    col[0] += 1
                elif window1 == [1, 2]:
                    col[1] += 1
                elif window1 == [0, 2]:
                    col[2] += 1
                elif window1 == [2, 1]:
                    col[3] += 1
                elif window1 == [2, 0]:
                    col[4] += 1
                elif window1 == [1, 0]:
                    col[5] += 1


            if window2 not in invalid_windows:
                if window2 == [0, 1]:
                    col[0] += 1
                elif window2 == [1, 2]:
                    col[1] += 1
                elif window2 == [0, 2]:
                    col[2] += 1
                elif window2 == [2, 1]:
                    col[3] += 1
                elif window2 == [2, 0]:
                    col[4] += 1
                elif window2 == [1, 0]:
                    col[5] += 1


        allTransitions.append(col)
    allTransitionsCompiledDF = pd.DataFrame(allTransitions, columns=['LoMid', 'MidHi', 'LoHi', 'HiMid', 'HiLo', 'MidLo'])
    allTransitionsCompiledDF.to_csv(outputName, sep='\t')
    print("countTransitions is complete.")
    return allTransitionsCompiledDF

# def countTransitionsValidWindow(transitions, outputName):
#     allTransitions = []
#
#     for i in range(len(transitions.columns)):
#         col = [0, 0, 0, 0, 0, 0]  # Initialize transition counters
#         for p in range(0, len(transitions) - 1, 2):
#             window1 = transitions.iloc[p:p+2, i].tolist()
#             window2 = transitions.iloc[p+1:p+3, i].tolist()
#
#             valid_windows = [[0, 1], [1, 2], [0, 2], [2, 1], [2, 0], [1,0]]
#
#             if window1 in valid_windows:
#                 if window1 == [0, 1]:
#                     col[0] += 1
#                 elif window1 == [1, 2]:
#                     col[1] += 1
#                 elif window1 == [0, 2]:
#                     col[2] += 1
#                 elif window1 == [2, 1]:
#                     col[3] += 1
#                 elif window1 == [2, 0]:
#                     col[4] += 1
#                 elif window1 == [1, 0]:
#                     col[5] += 1
#
#             if window2 in valid_windows:
#                 if window2 == [0, 1]:
#                     col[0] += 1
#                 elif window2 == [1, 2]:
#                     col[1] += 1
#                 elif window2 == [0, 2]:
#                     col[2] += 1
#                 elif window2 == [2, 1]:
#                     col[3] += 1
#                 elif window2 == [2, 0]:
#                     col[4] += 1
#                 elif window2 == [1, 0]:
#                     col[5] += 1
#
#         allTransitions.append(col)
#     allTransitionsCompiledDF = pd.DataFrame(allTransitions, columns=['LoMid', 'MidHi', 'LoHi', 'HiMid', 'HiLo', 'MidLo'])
#     allTransitionsCompiledDF.to_csv(outputName, sep='\t')
#     return allTransitionsCompiledDF


#--------------------------#------------------------------#--------------------------------#---------------------------#--------------------------#
#--------------------------#------------------------------#--------------------------------#---------------------------#--------------------------#
#--------------------------#------------------------------#--------------------------------#---------------------------#--------------------------#

def energeticBarrierCalc(kConf, temp=298):
    energeticBarrier=-8.314*temp*np.log(6.626E-34*kConf/(1.38E-23*temp))*0.00023901
    print('Energetic barrier is ', energeticBarrier, ' kcal/mol')
    print('Energetic barrier is approximately ', energeticBarrier/5, ' hydrogen bonds.')
    return energeticBarrier


#--------------------------#------------------------------#--------------------------------#---------------------------#--------------------------#
#--------------------------#------------------------------#--------------------------------#---------------------------#--------------------------#
#--------------------------#------------------------------#--------------------------------#---------------------------#--------------------------#

def countAllStates(df):
    counterList = []
    for i in range(len(df.columns)):
        for j in range(len(df)):
            if df.iloc[:, i][j] <= 0:
              pass
            else:
              counterList.append(df.iloc[:, i][j])
    with open('StateHistogramDat.txt', 'w') as file:
        file.write(str(counterList))
    return counterList

#--------------------------#------------------------------#--------------------------------#---------------------------#--------------------------#
#--------------------------#------------------------------#--------------------------------#---------------------------#--------------------------#
#--------------------------#------------------------------#--------------------------------#---------------------------#--------------------------#


def completeTransitions(transitions):

    """0 to 1^n to 2
       2 to 1^n to 0

       These are productive transitions if we fully reach max/min states.

       Code goal is to understand unproductive occlusions before a full
       transition (i.e. 0-101101-2) or 2-121212221-0.

       Need to count complete transistions (0-2 or 2-0) and number of occlusions."""

    complete_transitions_count = [0] * len(transitions.columns)
    jump_transitions_count = [0] * len(transitions.columns)

    # Updated part: List of lists to hold occlusions before each complete transition
    occlusions_before_transition_total= [[] for _ in transitions.columns]
    occlusions_before_transition = [[] for _ in transitions.columns]
    occlusionsFromZeroState = [[] for _ in transitions.columns]
    occlusionsFromTwoState = [[] for _ in transitions.columns]
    jump_windows = [[0, 2], [2, 0]]
    no_change_windows = [[0, 0], [1, 1], [2, 2]]
    zero_occlusions = [[1, 0]]
    two_occlusions = [[1, 2]]

    for i in range(len(transitions.columns)):
        zero_state = False
        two_state = False
        # Reset occlusion counter for each column
        occlusionsFromZero = 0
        occlusionFromTwo = 0
        occlusions = 0
        for p in range(0, len(transitions) - 1):  # Adjusted range to avoid index out of range
            #reminder that p:p+2 returns windows of two int. 0:2 gives index 0 and 1, noninclusive of 2
            window = transitions.iloc[p:p+2, i].tolist()

            if zero_state == False and two_state == False:
                if 0 in window:
                    zero_state = True
                if 2 in window:
                    two_state = True

                continue

            if window in no_change_windows:
                continue

            if window in jump_windows:
                jump_transitions_count[i] += 1

                # When a jump window occurs, we reset the occlusion count
                occlusions_before_transition_total[i].append(occlusionFromTwo + occlusionsFromZero)
                occlusions_before_transition[i].append(occlusions)
                occlusionsFromZeroState[i].append(occlusionsFromZero)
                occlusionsFromTwoState[i].append(occlusionFromTwo)
                occlusions = 0
                occlusionsFromZero = 0
                occlusionFromTwo = 0

                if window == [0, 2]:
                    two_state = True
                    zero_state = False
                else:
                    zero_state = True
                    two_state = False

                continue
            if (two_state and window in two_occlusions or zero_state and window in zero_occlusions):
                occlusions += 1
            if two_state and window in two_occlusions:
                occlusionFromTwo += 1
            if zero_state and window in zero_occlusions:
                occlusionsFromZero += 1


            # Complete transition logic
            if (two_state and window == [1, 0]) or (zero_state and window == [1, 2]):
                complete_transitions_count[i] += 1
                occlusions_before_transition_total[i].append(occlusionFromTwo + occlusionsFromZero)
                occlusions_before_transition[i].append(occlusions)
                occlusionsFromZeroState[i].append(occlusionsFromZero)
                occlusionsFromTwoState[i].append(occlusionFromTwo)
                occlusions = 0
                occlusionsFromZero = 0
                occlusionFromTwo = 0

                two_state = not two_state
                zero_state = not zero_state
                continue
    print("completeTransitions is complete.")
    return complete_transitions_count, jump_transitions_count, occlusions_before_transition, occlusions_before_transition_total, occlusionsFromZeroState, occlusionsFromTwoState

def transitionProbability(unproductiveOcclusion):
    occlusionBeforeTransition = []
    for x in range(0, len(unproductiveOcclusion)):
        for y in range(0, len(unproductiveOcclusion[x])):
            occlusionBeforeTransition.append(unproductiveOcclusion[x][y])
    return occlusionBeforeTransition

def outputCompleteTransitions(nameOfFile, completeOcclusions, jumps, unproductiveOcclusions,occlusions_before_transition_total , TotalTimes, occlusionsFromZeroState, occlusionsFromTwoState):
    with open(nameOfFile+"_transitionsStats.txt", "a") as f:
        print("Complete:", completeOcclusions, file=f)
        print("Jump:", jumps, file=f)
        print("Occ Per Complete:", unproductiveOcclusions, file=f)
        print("Total Time:", TotalTimes, file=f)
        totalOcc = 0
        totalOcc2 = 0
        totalZeroState = 0
        totalTwoState = 0
        totalJump = 0
        totalComplete = 0
        for ele in range(0, len(jumps)):
            totalComplete = totalComplete + completeOcclusions[ele]
        for ele in range(0, len(jumps)):
            totalJump = totalJump + jumps[ele]

        for ele in range(0, len(unproductiveOcclusions)):
            for ele2 in range(0, len(unproductiveOcclusions[ele])):
                totalOcc = totalOcc + unproductiveOcclusions[ele][ele2]

        for ele in range(0, len(occlusionsFromZeroState)):
            for ele2 in range(0, len(occlusionsFromZeroState[ele])):
                totalZeroState = totalZeroState + occlusionsFromZeroState[ele][ele2]

        for ele in range(0, len(occlusionsFromTwoState)):
            for ele2 in range(0, len(occlusionsFromTwoState[ele])):
                totalTwoState = totalTwoState + occlusionsFromTwoState[ele][ele2]


        for ele in range(0, len(occlusions_before_transition_total)):
            for ele2 in range(0, len(occlusions_before_transition_total[ele])):
                totalOcc2 = totalOcc2 + occlusions_before_transition_total[ele][ele2]
        print("Jump:", totalJump, file=f)
        print("Jump+Occ:", totalJump + totalOcc, file=f)
        print("Total Unproductive Occ: ", totalOcc, file=f)
        print("Total Unproductive Occ from Sum: ", totalOcc2, file=f)
        print("Total Productive occ: ", totalComplete, file=f)
        print("Total Productive/sec: ", totalComplete / TotalTimes, file=f)
        print("Ratio of Productive to Unproductive; ", totalComplete / totalOcc, file=f)
        print("Unproductive Occlusion from Zero State: ", totalZeroState,file=f)
        print("Unproductive Occlusion from Two State: ", totalTwoState,file=f)



def midStateProbability(transitions):
    zero_occlusions = [[1, 0]]
    two_occlusions = [[1, 2]]
    occlusionsFromZero = 0
    occlusionFromTwo = 0
    for i in range(len(transitions.columns)):
        zero_state = False
        two_state = False
        # Reset occlusion counter for each column
        for p in range(0, len(transitions) - 1):  # Adjusted range to avoid index out of range
            #reminder that p:p+2 returns windows of two int. 0:2 gives index 0 and 1, noninclusive of 2
            window = transitions.iloc[p:p+2, i].tolist()
            if window in zero_occlusions:
                occlusionsFromZero += 1
            if window in two_occlusions:
                occlusionFromTwo += 1

    print("completeTransitions is complete.")
    return occlusionsFromZero, occlusionFromTwo