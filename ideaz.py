import argparse
from argparse import RawTextHelpFormatter

import numpy as np
import sys
from random_list import RandomList

class Ideaz(object):
    def __init__(self, filenames, N_layers):
        self.oneList = IdeazOneList(filenames, N_layers)
        self.multipleLists = IdeazMultipleLists(filenames)
        self.setList(N_layers)
            
    def setList(self, N_layers):
        if N_layers == 0:
            self.currentList = self.multipleLists
        else:
            self.oneList.setNrOfLayers(N_layers)
            self.currentList = self.oneList
            
    def step(self):
        return self.currentList.step()
        
    def getNrOfLayers(self):
        return self.currentList.getNrOfLayers()

class IdeazOneList(object):
    def __init__(self, filenames, N_layers):
        self.data = self.parseCommandLine(filenames)
        self.setNrOfLayers(N_layers)
        
    def setNrOfLayers(self, N_layers):
        self.N_layers = N_layers
        self.N_combinations = np.prod(len(self.data)-np.arange(N_layers))
        self.candidates = RandomList(self.N_combinations)
        
    def parseCommandLine(self, filenames):
        data = []
        for fn in filenames:
            data += [line.strip() for line in open(fn, 'r')]
        return data
    
    def getRawIndices(self, candidate):
        N = len(self.data);
        rawIndices = np.array([np.mod(candidate, N)], dtype=np.uint32)
        for i in np.arange(self.N_layers-1):
            candidate = np.uint32(candidate/(N-i))
            rawIndices = np.append(rawIndices, np.mod(candidate, N-i-1))
        return rawIndices
        
    def getFineIndices(self, rawIndices):
        allIndices = np.arange(self.N_combinations)
        fineIndices = np.array([], dtype=np.uint32)
        for i in np.arange(self.N_layers):
            fineIndices = np.append(fineIndices, allIndices[rawIndices[i]])
            allIndices = np.delete(allIndices, rawIndices[i])
        return fineIndices
        
    def getSelectedData(self, fineIndices):
        selectedData = []
        for i in fineIndices:
            selectedData.append(self.data[i])
        return selectedData
        
    def step(self):
        rawIndices = self.getRawIndices(self.candidates.step())
        fineIndices = self.getFineIndices(rawIndices)
        return self.getSelectedData(fineIndices)
        
    def getNrOfLayers(self):
        return self.N_layers

        
class IdeazMultipleLists(object):
    '''
    - This class takes a list of text files from the commandline.
    - Each text file i stores N_i lines.
    - By calling step(), one item from each file is selected and returned as a list of strings.
    - There are in total \prod_i N_i combinations.
    - Algorithm:
    -- There are \prod_i N_i combinations
    -- A candidate is randomly selected from the range 0..N_combinations-1
    -- A candidate is represented as a linear combination 
       candidate = i + N_i*j + N_i * N_j*k + ...
    -- i, j, k are computed by alternating mod and division
    '''
    def __init__(self, filenames):
        self.filenames = filenames
        self.data, self.list_lengths = self.parseCommandLine(filenames)
        N_combinations = np.prod(self.list_lengths)
        self.candidates = RandomList(N_combinations)

    def parseCommandLine(self, filenames):
        data = []
        list_lengths = []
        for fn in filenames:
            data.append([line.strip() for line in open(fn, 'r')])
            list_lengths.append(len(data[-1]))
        return data, list_lengths

    def getRawIndices(self, candidate):
        rawIndices = np.array([np.mod(candidate, self.list_lengths[0])], dtype=np.uint32)
        for i, length in enumerate(self.list_lengths[:-1]):
            candidate = np.uint32(candidate/length)
            rawIndices = np.append(rawIndices, np.mod(candidate, self.list_lengths[i+1]))
        return rawIndices

    def getSelectedData(self, data, rawIndices):
        selectedData = []
        for i, rawIndex in enumerate(rawIndices):
            selectedData.append(data[i][rawIndex])
        return selectedData

    def step(self):
        rawIndices = self.getRawIndices(self.candidates.step())
        return self.getSelectedData(self.data, rawIndices)
        
    def getNrOfLayers(self):
        return len(self.filenames)

if __name__ == '__main__':
    descr = \
    """
    -------------------------
    Whip up ideas in no time!
    -------------------------
    """
    parser = argparse.ArgumentParser(description=descr, formatter_class=RawTextHelpFormatter)

    parser.add_argument('filename', nargs='+', type=str, help='file name')
    parser.add_argument('-N_layers', nargs='?', type=int, default=0)
    
    args = parser.parse_args()
    
    ideaz = Ideaz(args.filename, args.N_layers)
