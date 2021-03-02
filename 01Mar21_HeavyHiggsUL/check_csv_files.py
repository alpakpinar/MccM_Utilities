#!/usr/bin/env python

import os
import sys
import re
import csv

# Script to check the content of the CSV files for the Heavy Higgs requests.
def check_csv(infile):
    with open(infile, 'r') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            dataset_name = row['Dataset name']

            mass = float(re.findall('m(\d+)', dataset_name)[0])
            width = float(re.findall('w(\d+.\d+)', dataset_name)[0])

            print(dataset_name)

            if mass != 400:
                assert width / mass in [0.025, 0.1, 0.25] 
            else:
                assert width / mass in [0.025, 0.05, 0.1, 0.25] 

            count += 1
        
        # Additional width point for 2016
        if '2016' in infile:
            expectedcount = 2**3 * 3 * 6 + 8
        else:
            expectedcount = 2**3 * 3 * 6

        print('\nTotal number of requests: {}, expecting {} requests'.format(count, expectedcount))
        assert count == expectedcount
        print('DONE')

def main():
    infile = sys.argv[1]
    check_csv(infile)

if __name__ == '__main__':
    main()