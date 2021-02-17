import os
import csv

pjoin = os.path.join

# Data about each signal request
request_data = {
    'VBF' : {
        'fragment' : './fragments/vbf.py',
        'datasetName' : 'VBF_HToInvisible_M125_TuneCP5_PSweights_13TeV_powheg_pythia8',
        'gridpackPath' : '',
        'numEvents' : 1000000
    },
    'ggH' : {
        'fragment' : './fragments/ggh_with_filter.py',
        'datasetName' : 'GluGlu_HToInvisible_M125_HiggspTgt190_TuneCP5_PSweights_13TeV_powheg_pythia8',
        'gridpackPath' : '',
        'numEvents' : 2500000
    },
    'WminusH' : {
        'fragment' : './fragments/wminush.py',
        'datasetName' : 'WminusH_WToQQ_HToInvisible_M125_TuneCP5_PSweights_13TeV_powheg_pythia8',
        'gridpackPath' : '',
        'numEvents' : 1000000
    },
    'WplusH' : {
        'fragment' : './fragments/wplush.py',
        'datasetName' : 'WplusH_WToQQ_HToInvisible_M125_TuneCP5_PSweights_13TeV_powheg_pythia8',
        'gridpackPath' : '',
        'numEvents' : 1000000
    },
    'ZH' : {
        'fragment' : './fragments/zh.py',
        'datasetName' : 'ZH_ZToQQ_HToInvisible_M125_TuneCP5_PSweights_13TeV_powheg_pythia8',
        'gridpackPath' : '',
        'numEvents' : 1000000
    },
    'ggZH' : {
        'fragment' : './fragments/ggzh.py',
        'datasetName' : 'ggZH_ZToQQ_HToInvisible_M125_TuneCP5_PSweights_13TeV_powheg_pythia8',
        'gridpackPath' : '',
        'numEvents' : 1000000
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
        fwriter.writerow([
            dataset_name,
            data['numEvents'],
            fragment,
            'Powheg+Pythia8',
            dataset_name.split('_')
        ])

print('Requests saved to file:')
print(outpath)