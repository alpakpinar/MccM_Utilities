#!/usr/bin/env python

import os
import csv

pjoin = os.path.join

# Data about each signal request
request_data = {
    'VBF' : {
        'fragment' : './fragments/vbf.py',
        'datasetName' : 'VBF_HToInvisible_M125_TuneCP5_withDipoleRecoil_PSweights_13TeV_powheg_pythia8',
        'gridpackPath' : '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/powheg/V2/VBF_H_slc7_amd64_gcc820_CMSSW_10_6_20_VBF_M125/v1/VBF_H_slc7_amd64_gcc820_CMSSW_10_6_20_VBF_M125.tgz',
        'numEvents' : 1000000
    },
    'ggH' : {
        'fragment' : './fragments/ggh_with_filter.py',
        'datasetName' : 'GluGlu_HToInvisible_M125_HiggspTgt190_TuneCP5_PSweights_13TeV_powheg_pythia8',
        'gridpackPath' : '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/powheg/V2/gg_H_quark-mass-effects_slc7_amd64_gcc820_CMSSW_10_6_20_ggH_M125/v1/gg_H_quark-mass-effects_slc7_amd64_gcc820_CMSSW_10_6_20_ggH_M125.tgz',
        'numEvents' : 2500000
    },
    'WminusH' : {
        'fragment' : './fragments/wminush.py',
        'datasetName' : 'WminusH_WToQQ_HToInvisible_M125_TuneCP5_PSweights_13TeV_powheg_pythia8',
        'gridpackPath' : '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/powheg/V2/HWJ_slc7_amd64_gcc820_CMSSW_10_6_20_HWminusJ_MH125/v1/HWJ_slc7_amd64_gcc820_CMSSW_10_6_20_HWminusJ_MH125.tgz',
        'numEvents' : 1000000
    },
    'WplusH' : {
        'fragment' : './fragments/wplush.py',
        'datasetName' : 'WplusH_WToQQ_HToInvisible_M125_TuneCP5_PSweights_13TeV_powheg_pythia8',
        'gridpackPath' : '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/powheg/V2/HWJ_slc7_amd64_gcc820_CMSSW_10_6_20_HWplusJ_M125/v1/HWJ_slc7_amd64_gcc820_CMSSW_10_6_20_HWplusJ_M125.tgz',
        'numEvents' : 1000000
    },
    'ZH' : {
        'fragment' : './fragments/zh.py',
        'datasetName' : 'ZH_ZToQQ_HToInvisible_M125_TuneCP5_PSweights_13TeV_powheg_pythia8',
        'gridpackPath' : '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/powheg/V2/HZJ_slc7_amd64_gcc820_CMSSW_10_6_20_HZJ_M125/v1/HZJ_slc7_amd64_gcc820_CMSSW_10_6_20_HZJ_M125.tgz',
        'numEvents' : 1000000
    },
    'ggZH' : {
        'fragment' : './fragments/ggzh.py',
        'datasetName' : 'ggZH_ZToQQ_HToInvisible_M125_TuneCP5_PSweights_13TeV_powheg_pythia8',
        'gridpackPath' : '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/powheg/V2/ggHZ_slc7_amd64_gcc820_CMSSW_10_6_20_ggHZ_M125/v1/ggHZ_slc7_amd64_gcc820_CMSSW_10_6_20_ggHZ_M125.tgz',
        'numEvents' : 1000000
    },
    'ttH' : {
        'fragment' : './fragments/tth.py',
        'datasetName' : 'ttH_HToInvisible_M125_TuneCP5_PSweights_13TeV_powheg_pythia8',
        'gridpackPath' : '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/powheg/V2/ttH_slc7_amd64_gcc820_CMSSW_10_6_20_ttH_M125/v1/ttH_slc7_amd64_gcc820_CMSSW_10_6_20_ttH_M125.tgz',
        'numEvents' : 6000000
    }
}

# Output CSV file to save requests
outdir = './output'
if not os.path.exists(outdir):
    os.makedirs(outdir)

outpath = pjoin(outdir, 'signal_requests.csv')

with open(outpath, 'w+') as csvf:
    fwriter = csv.writer(csvf)
    fwriter.writerow(['Dataset name', 'Total events', 'Fragment', 'Generator', 'Notes'])
    for signal, data in request_data.items():
        # Get the fragment template from the input files
        fragment_file = data['fragment']
        with open(fragment_file, 'r') as f:
            fragment_template = f.read()
        
        fragment = fragment_template.format(__GRIDPACK__ = data['gridpackPath'])
        dataset_name = data['datasetName']

        # Check dataset name, shouldn't be too long
        assert len(dataset_name) < 100

        fwriter.writerow([
            dataset_name,
            data['numEvents'],
            fragment,
            'Powheg+Pythia8',
            dataset_name.split('_')
        ])

print('Requests saved to file:')
print(outpath)