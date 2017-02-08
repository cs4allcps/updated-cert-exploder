# coding: utf-8

import csv
import pandas as pd
import sys
import os
from cert_exploder.py import explode, parse_args


def main(filename):
	'''
	Takes an Excel report of CPS employees with teaching licenses and  
    CS endorsements or other endorsements/certification applicable to CS and
    generates a .csv report showing counts of teachers with CS endorsements
    and counts of other credentials for each cs4all school(*).

    **If there is not a file named 'Cohorts 1-3 rolodex.xlsx' in the working 
      directory containing a list of cs4all schools, the report will instead 
      contain counts for all schools at which there are teachers with CS
      certifications.

    Input: filename of Excel file (to avoid raising an error, the file 
            needs the column names 'Accomplishment' and 'Certification')
	'''


if __name__ == '__main__':
    if len(sys.argv) > 1:
        args = parse_args(sys.argv)
        filename = args.input_filename[0]
        usingDefault = False 
    else:
        print("no input file passed as argument... Attempting to use default")
        filename  = 'SAW2611689 - Computer Science Teachers - 2017-02-06.xlsx' #default
        usingDefault = True 
    if os.path.isfile(filename):
        if usingDefault:
            print('Using default')
        main(filename)
    else:
        if usingDefault:
            print('Default file not in working directory')
        else:
            print('Input file not found')