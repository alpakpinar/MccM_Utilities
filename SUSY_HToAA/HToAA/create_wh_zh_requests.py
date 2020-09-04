import os
from request_creator import RequestCreator

pjoin = os.path.join

# =======================================================================
# Dump the WH and ZH requests configuration into csv files for all three years. 
# =======================================================================

# Fragment template (both for WH and ZH)
fragment_temp = '''import FWCore.ParameterSet.Config as cms

# link to cards:
# https://github.com/cms-sw/genproductions/pull/2670, https://github.com/cms-sw/genproductions/pull/2705
externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('{__GRIDPACK__}'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(1),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.),
                         HepMCFilter = cms.PSet(
                             filterName = cms.string('EmbeddingHepMCFilter'),
                             filterParameters = cms.PSet(
                                 ElElCut = cms.string('El1.Pt > 22 && El2.Pt > 10 && El1.Eta < 2.6 && El2.Eta < 2.6'),
                                 ElHadCut = cms.string('El.Pt > 6 && Had.Pt > 16 && El.Eta < 2.6 && Had.Eta < 2.7'),
                                 ElMuCut = cms.string('Mu.Pt > 4 && El.Pt > 6 && El.Eta < 2.6 && Mu.Eta < 2.5'),
                                 HadHadCut = cms.string('Had1.Pt > 16 && Had2.Pt > 16 && Had1.Eta < 2.5 && Had2.Eta < 2.5'),
                                 MuHadCut = cms.string('Mu.Pt > 4 && Had.Pt > 16 && Mu.Eta < 2.5 && Had.Eta < 2.7'),
                                 MuMuCut = cms.string('Mu1.Pt > 17 && Mu2.Pt > 8 && Mu1.Eta < 2.5 && Mu2.Eta < 2.5'),
                                 Final_States = cms.vstring(
                                     'ElHad',
                                     'ElMu',
                                     'HadHad',
                                     'MuHad'
                                 ),
                                 BosonPDGID = cms.int32(36)
                             )
                         ),
                         PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock, 
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PSweightsSettings'
                                    )
        )
                         )

ProductionFilterSequence = cms.Sequence(generator)
'''

def create_wh_requests():
    '''Create CSV files containing configuration of the WH requests'''
    # Gridpack locations 
    # TODO: Put gridpack location here once they are on CVMFS
    gridpack_location_temp = ''

    dataset_name_temp = 'SUSYWlepHToAA_AToBB_AToTauTau_M-{__MASS__}_FilterTauTauReco_TuneCP5_13TeV_madgraph_pythia8'

    # List of several quantities
    mass_points = [12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
    years = [2016, 2017, 2018]
    filter_effs = [0.2]*5 + [0.25]*6
    # Number of events before filter for each mass point
    num_events = [150000]*11
    
    template_dict = {
        'Dataset name': dataset_name_temp, 
        'Gridpack path': gridpack_location_temp, 
        'Fragment': fragment_temp 
    }
    
    # Dump the request to csv files
    r = RequestCreator(
        template_dict=template_dict, 
        mass_points=mass_points,
        filter_effs=filter_effs,
        filter_effs=filter_effs,
        num_events=num_events,
        years=years, tag='wh'
    )
    
    r.dump_to_csv()

def create_zh_requests():
    '''Create CSV files containing configuration of the ZH requests'''
    # Gridpack locations 
    # TODO: Put gridpack location here once they are on CVMFS
    gridpack_location_temp = ''

    dataset_name_temp = 'SUSYZlepHToAA_AToBB_AToTauTau_M-{__MASS__}_FilterTauTauReco_TuneCP5_13TeV_madgraph_pythia8'

    # List of several quantities
    mass_points = [12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
    years = [2016, 2017, 2018]
    filter_effs = [0.2]*5 + [0.25]*6
    # Number of events before filter for each mass point
    num_events = [150000]*11 
    
    template_dict = {
        'Dataset name': dataset_name_temp, 
        'Gridpack path': gridpack_location_temp, 
        'Fragment': fragment_temp 
    }
    
    # Dump the request to csv files
    r = RequestCreator(
        template_dict=template_dict, 
        mass_points=mass_points,
        filter_effs=filter_effs,
        filter_effs=filter_effs,
        num_events=num_events,
        years=years, tag='zh'
    )
    
    r.dump_to_csv()

def main():
    create_wh_requests()
    create_zh_requests()

if __name__ == '__main__':
    main()