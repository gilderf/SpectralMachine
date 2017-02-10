#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
*********************************************
*
* TrainingDataMaker
* Adds spectra to Training File
* version: 20170120a
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************
'''

print(__doc__)

import numpy as np
from sklearn import svm
import sys, os.path

#**********************************************
''' main '''
#**********************************************

def main():
    try:
        makeFile(sys.argv[1], sys.argv[2], sys.argv[3])
    except:
        usage()
    sys.exit(2)

#**********************************************
''' Make Map file '''
#**********************************************
def makeFile(mapFile, sampleFile, param):
    
    #**********************************************
    ''' Open and process training data '''
    #**********************************************
    
    try:
        with open(sampleFile, 'r') as f:
            En = np.loadtxt(f, unpack = True, usecols=range(0,1))
            print(' Number of points in the sample dataset: ' + str(En.shape[0]))
    except:
        print('\033[1m' + ' Sample data file not found \n' + '\033[0m')
        return

    with open(sampleFile, 'r') as f:
        R = np.loadtxt(f, unpack = True, usecols=range(1,2))

    try:
        with open(mapFile, 'r') as f:
            M = np.loadtxt(f, unpack =False)
            EnT = np.delete(np.array(M[0,:]),np.s_[0:1],0)
            if EnT.shape[0] == En.shape[0]:
                print(' Number of points in the map dataset: ' + str(EnT.shape[0]))
            else:
                print('\033[1m' + ' Mismatch in datapoints: map: ' + str(EnT.shape[0]) + '; sample = ' +  str(En.shape[0]) + '\033[0m')
                R = np.interp(EnT, En, R)
                print('\033[1m' + ' Mismatch corrected: datapoints in sample: ' + str(R.shape[0]) + '\033[0m')
    except:
        print('\033[1m' + ' Map data file not found \n' + '\033[0m')
        return


    if os.path.exists(mapFile):
        print('\n Adding spectra to ' + mapFile + '\n')
        newMap = np.append(float(param),R).reshape(1,-1)
    else:
        print('\n' + mapFile + ' does not exist. Creating...' + '\n')
        newMap = np.append([0], En)
        newMap = np.vstack((newMap, np.append(float(param),R)))

    with open(mapFile, 'ab') as f:
        np.savetxt(f, newMap, delimiter='\t', fmt='%10.6f')


#************************************
''' Lists the program usage '''
#************************************
def usage():
    print('\n Usage:')
    print('  python TrainingDataMaker.py <trainingfile> <spectrafile> <parameter>\n')

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
