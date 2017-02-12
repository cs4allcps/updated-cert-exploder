# coding: utf-8

import csv
import pandas as pd
import sys
import os
from cert_exploder import explode, parse_args, mkdir_p
import requests
import json


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
    endorsements, certifications, teachers = explode(filename)
    #remove teachers who aren't assigned to schools
    teachers = teachers[teachers['DeptType'] == 'ES' or teachers['DeptType'] == 'HS']
    #remove teachers at non-cs4all schools
    if os.path.isfile('Cohorts 1-3 rolodex.xlsx'):
        #get school codes for all cs4all schools
        cs4all_schools = pd.read_excel('Cohorts 1-3 rolodex.xlsx', sheetname = 'master')
        cs4all_school_names = cs4all_schools["School"].tolist()
        #Request school data from city data portal
        url = "https://data.cityofchicago.org/resource/76dk-7ieb.json"
        resp = requests.get(url)
        schools = resp.json() #List of dicts representing each cps school
        name_to_id = {}
        for school in schools:
            name_to_id[row['short_name']] = row['school_id']
        cs4all_school_ids = [name_to_id[name] for name in cs4all_school_names]
        #remove teachers with school id not in list of cs4all school codes
        teachers = teacher[teachers['Deptid'] in cs4all_school_ids]
    #now remove endorsements and certifications that don't belong to shortened list of teachers
    IDs = teachers['teacherID'].tolist()
    endorsements = endorsements[endorsements['teacherID'] in IDs]
    certifications = certifications[certifications['teacherID'] in IDs]
    #write counts for each school in question
    schools = list(set(teachers['Department'].tolist()))
    mkdir_p('reports')
    with open('reports/school_counts.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(['School,' 'CS Endorsements', 'Other Credentials'])
        for school in schools:
            teachs_at_school = teachers[teachers['Department'] == school]
            IDs = teachs_at_school['teacherID'].tolist()
            endorsements = 
            '''
            function incomplete
            '''
            w.writerow([school, endor_ct, cred_ct])



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