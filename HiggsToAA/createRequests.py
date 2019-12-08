import csv
from fragments import *

import argparse
parser = argparse.ArgumentParser(prog="createRequests")
parser.add_argument("--years", type=str, choices=['2016','2017','2018'], nargs='*',
                              required=True, help="MC year condition (2016-2017-2018)" )
args = parser.parse_args()


years = args.years

for year in years:
    with open('HiggsTo_aa_4gamma_'+year+'.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['Dataset name','Events', 'fragment','notes','Generator'])

		# Iterate over all mass points
        for mass_point, nevents in mass_points_nevents.items():
            gridpacks = gridpacks_dict[year][mass_point] # NOTE: gridpacks_dict to be updated in fragments.py
			ds_name = dataset_names[year].format(str(mass_point).replace('.','p'))
			proc_card_link = gridpacks[year][1]
			gridpack_path = gridpacks[year][0]
			pythia_fragment = pythia_fragmets_dict[year]
			fragment = lhe_fragment.replace('__LINK__',proc_card_link).replace('__GRIDPACK__',gridpack_path).replace('__PYTHIA_FRAGMENT__',pythia_fragment)
			csvwriter.writerow([ds_name,nevents,fragment,ds_name.split('_'),'Madgraph+Pythia'])
