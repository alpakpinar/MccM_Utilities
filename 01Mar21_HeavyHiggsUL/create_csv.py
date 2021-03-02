#!/usr/bin/env python

import os
import csv
from itertools import product
from pprint import pprint

pjoin = os.path.join

def get_fragment_temp():
    fragmentfile = './fragment_temp.py'
    with open(fragmentfile, 'r') as f:
        fragment_temp = f.read()
    return fragment_temp

def create_csv():
    fragment_temp = get_fragment_temp()

    years = ['2016preAPV', '2016postAPV', '2017', '2018']
    numevents = {
        '2016preAPV'  : 250000,
        '2016postAPV' : 250000,
        '2017'        : 500000,
        '2018'        : 500000,
    }

    mass_points = [365, 400, 500, 600, 800, 1000]
    # Mass * width gives the actual width
    width_points = [0.025, 0.1, 0.25] 
    modes = ['ljets', 'll']

    # TODO: Need to update with actual cvmfs paths once they're uploaded
    gridpack_template = 'heavyhiggs_13TeV_{__MODE__}_m{__MASS__}_w{__WIDTH__}_{__INT__}_{__PSUEDO__}_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz'

    dataset_name_templates = {
        'INT' : {
            'll'    : 'H{__SCALAR__}ToTTTo2L2Nu_m{__MASS__}_w{__WIDTH__}_int_TuneCP5_13TeV-madgraph_pythia8',
            'ljets' : 'H{__SCALAR__}TTTo1L1Nu2J_m{__MASS__}_w{__WIDTH__}_int_TuneCP5_13TeV-madgraph_pythia8',
        },
        'RES' : {
            'll'    : 'H{__SCALAR__}ToTTTo2L2Nu_m{__MASS__}_w{__WIDTH__}_res_TuneCP5_13TeV-madgraph_pythia8',
            'ljets' : 'H{__SCALAR__}TTTo1L1Nu2J_m{__MASS__}_w{__WIDTH__}_res_TuneCP5_13TeV-madgraph_pythia8',
        },
    }

    outdir = './output'
    if not os.path.exists(outdir):
        os.makedirs(outdir)


    for year in years:
        masswidth_points = list(product(modes, mass_points, width_points))
        # Extra width point for 2016 only
        if '2016' in year:
            masswidth_points.append(('ll', 400, 0.05))
            masswidth_points.append(('ljets', 400, 0.05))

        # Output CSV files for the requests for this year/period
        outpath = pjoin(outdir, 'heavyhiggs_{}.csv'.format(year) )
        with open(outpath, 'w+') as f:
            writer = csv.writer(f)
            writer.writerow(['Dataset name', 'Number of events', 'Fragment', 'Generator', 'Notes'])
            
            for mode, mass, width in masswidth_points:
                _width = mass * width

                for _int in ['INT', 'RES']:
                    for _scalar in ['PSUEDO', 'SCALAR']:
                        gridpack_path = gridpack_template.format(
                            __MODE__ = mode,
                            __MASS__ = mass,
                            __WIDTH__ = _width,
                            __INT__ = _int,
                            __PSUEDO__ = _scalar,
                        )

                        fragment = fragment_temp.format(__GRIDPACK__ = gridpack_path)

                        dataset_name = dataset_name_templates[_int][mode].format(
                            __SCALAR__ = _scalar.lower(),
                            __MASS__   = mass,
                            __WIDTH__  = _width,
                        )

                        data = [
                            dataset_name,
                            numevents[year],
                            fragment,
                            'madgraph+pythia8',
                            dataset_name.split('_')
                        ]

                        writer.writerow(data)

        print('CSV file saved: {}'.format(outpath))

def main():
    create_csv()

if __name__ == '__main__':
    main()