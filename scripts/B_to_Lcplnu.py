#!/usr/bin/env python3

##########################################################################
# basf2 (Belle II Analysis Software Framework)                           #
# Author: The Belle II Collaboration                                     #
#                                                                        #
# See git log for contributors and copyright holders.                    #
# This file is licensed under LGPL-3.0, see LICENSE.md.                  #
##########################################################################

import os
import sys
import fei
import basf2 as b2
import modularAnalysis as ma
import vertex as vx
import variables.collections as vc
import variables.utils as vu
from stdCharged import stdK, stdPi, stdPr, stdE, stdMu
from stdV0s import stdKshorts
from stdPhotons import stdPhotons
from variables.MCGenTopo import mc_gen_topo
from variables import variables as vm


TAG_HAD = True
TAG_SL = False

def reco_fei(path):
        
    particles = fei.get_default_channels(
        B_extra_cut = None,
        hadronic = TAG_HAD,
        semileptonic = TAG_SL,
        KLong = False,
        baryonic = True,
        chargedB = True,
        neutralB = False,
        removeSLD = True,
    )

    # Set up FEI configuration specifying the FEI prefix
    configuration = fei.config.FeiConfiguration(
        prefix="FEIv1_2025_MC16ri_aldebaran_200", #FEIv4_2022_MC15_light-2205-abys
        training=False,
        monitor=False
    )
    
    # Get FEI path
    feistate = fei.get_path(particles, configuration)

    # Add FEI path to the path to be processed
    path.add_path(feistate.path)


# Create path
#path = b2.create_path()
path=b2.Path()


# Load input ROOT files, use for signal MC
input_files = sys.argv[2:]
base_path = 'signal_mc_scripts/example/production/' #input_files[0]
ma.inputMdstList(filelist=input_files, path=path)


'''
#for testing in bash via basf2 command
ma.inputMdstList(
   #filelist = ["/pnfs/desy.de/belle/local/belle/group/physics/SLME/sMC16rd_1263720001_26647/11180500/udst/sub00/11180500_00018_job522166834_00.udst.root"], #signMC
   filelist = ["/pnfs/desy.de/belle/local/belle/MC/light-2503-ceres/DB00003308/MC16rd_prompt/prod00051404/s00/e0033/4S/r00000/charged/11180500/udst/sub00/udst_000001_prod00051404_task320000001.root"], #BB
   path = path
)
'''


#path.add_module('RootInput') #for Grid submissions



# Load input ROOT file, use for batch
#if sys.argv[2][:2] == "MC":
#    base_path = "/pnfs/desy.de/belle/local/belle/MC/release-06-00-11/DB00002284/"
#else:
#    base_path = "/pnfs/desy.de/belle/local/belle/Data/release-06-01-12/DB00002058/"
#ma.inputMdst(os.path.join(base_path, sys.argv[2]), path=path)

# Add the necessary database
#os.environ["BELLE2_CONDB_METADATA"] = "/cvmfs/belle.cern.ch/conditions/database.sqlite"
b2.conditions.prepend_globaltag(ma.getAnalysisGlobaltag())

stdPr(path=path)
stdE(path=path)
stdMu(path=path)
stdPi(path=path)
stdK(path=path)
#stdKshorts(path=path)
stdPhotons(path=path)


#ma.fillParticleListFromMC('Sigma_c++:mc', '', path=path)
#ma.printMCParticles(path=path)


#if not base_path.startswith("/pnfs"):  # Only run FEI on signal MC
#reco_fei(path=path)                    # needed when testing outside of Grid

ma.applyCuts('e-:good', 'electronID > 0.9 and p > 0.3', path=path)
ma.applyCuts('mu-:good', 'muonID > 0.9 and p > 0.3', path=path)

#ma.cutAndCopyList('K_S0:my', 'K_S0:merged', '', path=path)
#ma.cutAndCopyList('gamma:my', 'gamma:loose', '', path=path)
#ma.reconstructDecay('pi0:my -> gamma:my gamma:my', '0.10 < InvM < 0.15', path=path)

# Lambda_c reconstruction
ma.reconstructDecay('Lambda_c+:11 -> p+:good K-:good pi+:good', '2.1 < InvM < 2.5', dmID=11, path=path)
#ma.reconstructDecay('Lambda_c+:12 -> p+:good K_S0:my', '2.1 < InvM < 2.5', dmID=12, path=path)
#ma.reconstructDecay('Lambda_c+:13 -> p+:good K_S0:my pi0:my', '2.1 < InvM < 2.5', dmID=13, path=path)
#ma.reconstructDecay('Lambda_c+:14 -> p+:good K-:good pi+:good pi0:my', '2.1 < InvM < 2.5', dmID=14, path=path)
ma.copyLists('Lambda_c+:all', ['Lambda_c+:11'], path=path)
#ma.reconstructDecay('Lambda_c+:12 -> p+:good K+:good pi-:good', '2.2 < InvM < 2.4', dmID=12, path=path)
#ma.copyLists('Lambda_c+:all', ['Lambda_c+:11', 'Lambda_c+:12'], path=path)



#test if MC have Sigma_c
#ma.fillParticleListFromMC('pi0:mc', '', path=path)
#ma.fillParticleListFromMC('pi+:mc', '', path=path)
#ma.fillParticleListFromMC('Lambda_c+:mc', '', path=path)

#ma.reconstructDecay('pi0:good -> gamma:all gamma:all', '0.080 < M < 0.200', path=path)

#ma.reconstructDecay('Sigma_c+:veto -> Lambda_c+:mc pi0:mc', '', path=path)
#ma.reconstructDecay('Sigma_c*+:veto -> anti-Lambda_c-:mc pi0:mc', '', path=path)
#ma.reconstructDecay('Sigma_c+:veto -> Lambda_c+:all pi0:good', '1.9 < M < 2.6', path=path)
#ma.reconstructDecay('Sigma_c*+:veto -> Lambda_c+:all pi0:good', '1.9 < M < 2.6', path=path)
#ma.reconstructDecay('Sigma_c++:Lcpi -> Lambda_c+:all pi+:good', '2.1 < M < 2.6', dmID=3, path=path)
#ma.reconstructDecay('Sigma_c++:veto -> Lambda_c+:mc pi+:mc', '1.9 < M < 2.6', path=path)
#ma.countInList('Sigma_c+:veto', 'nSigma_c+', path=path)
#ma.countInList('Sigma_c*+:veto', 'nSigma_cS+', path=path)
#ma.countInList('Sigma_c++:veto', 'nSigma_c++', path=path)
#ma.variableToSignalSideExtraInfo('Sigma_c+:veto', {'countInList(Sigma_c+:veto)': 'nSigma_cp'}, path=path)
#ma.variableToSignalSideExtraInfo('Sigma_c*+:veto', {'countInList(Sigma_c*+:veto)': 'nSigma_c*p'}, path=path)
#ma.variableToSignalSideExtraInfo('Sigma_c++:veto', {'countInList(Sigma_c++:veto)': 'nSigma_cpp'}, path=path)

#vm.addAlias('nSigma_cp', 'countInList(Sigma_c+:veto)')
#vm.addAlias('nSigma_cSp', 'countInList(Sigma_c*+:veto)')

#ma.rankByLowest('Sigma_c+:veto', 'abs(dM)', 1, path=path)
#ma.rankByLowest('Sigma_c*+:veto', 'abs(dM)', 1, path=path)
#ma.rankByLowest('Sigma_c++:veto', 'abs(dM)', 1, path=path)

#vx.treeFit('Sigma_c++:veto', conf_level=0, massConstraint=[], ipConstraint=False, updateAllDaughters=False, path=path)
#vx.treeFit('Sigma_c+:veto', conf_level=0, massConstraint=[], ipConstraint=False, updateAllDaughters=False, path=path)
#vx.treeFit('Sigma_c*+:veto', conf_level=0, massConstraint=[], ipConstraint=False, updateAllDaughters=False, path=path)

#ma.matchMCTruth('Sigma_c++:veto', path=path)
#ma.matchMCTruth('Sigma_c+:veto', path=path)
#ma.matchMCTruth('Sigma_c*+:veto', path=path)



'''
vm.addAlias('nSigma_cpp', 'countInList(Sigma_c++:Lcpi)')
vm.addAlias('nSigma_cppmu', 'countInList(Sigma_c++:Lcmu)')
vm.addAlias('nSigma_cppe', 'countInList(Sigma_c++:Lce)')

#vm.addAlias('M_SigmaCmu', 'M')
vm.addAlias('dM_mu', 'M - daughter(0,M)')
vm.addAlias('muPID', 'daughter(1,muonID)')
vm.addAlias('piPID', 'daughter(1,pionID)')
vm.addAlias('ePID', 'daughter(1,electronID)')
vm.addAlias('lepPDG', 'daughter(1,mcPDG)')
vm.addAlias('S_decayMode', 'extraInfo(decayModeID)')



#ma.rankByLowest('Sigma_c++:veto', 'abs(dM_mu)', 1, path=path)
ma.matchMCTruth('Sigma_c++:veto', path=path)
#vm.addAlias('muon_Truth', 'isSignal')
'''


# B to Lc p l nu reconstruction
ma.reconstructDecay('B-:Lcpe -> Lambda_c+:all anti-p-:good e-:good', '', dmID=1, path=path)
ma.reconstructDecay('B-:Lcpmu -> Lambda_c+:all anti-p-:good mu-:good', '', dmID=2, path=path)
ma.copyLists('B-:sig', ['B-:Lcpe', 'B-:Lcpmu'], path=path)

vm.addAlias('hasMuB', 'countInList(B-:Lcpmu)')
vm.addAlias('hasEB',  'countInList(B-:Lcpe)')




#Sigma_c++ vetos
#ma.applyEventCuts('countInList(B-:sig) > 0', path=path)
#ma.fillSignalSideParticleList('Lambda_c+:sig', 'Upsilon(4S) -> [B- -> ^Lambda_c+ ...] B+', roe_path)
#ma.fillSignalSideParticleList('Lambda_c+:sig', 'B-:sig -> ^Lambda_c+ anti-p-:good ...', path)
ma.reconstructDecay('Sigma_c++:Lcpi -> Lambda_c+:all pi+:good', '2.2 < InvM < 2.6', dmID=103, path=path)
ma.reconstructDecay('Sigma_c++:Lcmu -> Lambda_c+:all mu+:good', '2.2 < InvM < 2.6', dmID=102, path=path)
ma.reconstructDecay('Sigma_c++:Lce -> Lambda_c+:all e+:good', '2.2 < InvM < 2.6', dmID=101, path=path)
ma.copyLists('Sigma_c++:veto', ['Sigma_c++:Lcpi', 'Sigma_c++:Lcmu', 'Sigma_c++:Lce'], path=path)

vm.addAlias('S_decayMode', 'extraInfo(decayModeID)')
vm.addAlias('dM_mu', 'M - daughter(0,M)')

ma.matchMCTruth('Sigma_c++:veto', path=path)

#ma.rankByLowest('Sigma_c++:veto', 'abs(dM)', 1, path=path)
'''
ma.variableToSignalSideExtraInfo('Sigma_c++:veto', 
    {
        #'M': 'Sigma_cppveto', 
        'countInList(Sigma_c++:Lcpi)': 'nSigma_cpp',
        'countInList(Sigma_c++:Lcmu)': 'nSigma_cppmu',
        'countInList(Sigma_c++:Lce)': 'nSigma_cppe',
        #'extraInfo(decayModeID)': 'S_decayMode'
    }, path=path)
'''



#validate Sigma_c veto
#ma.variableToSignalSideExtraInfo('Sigma_c++:vetomu', {'dmID': 'dmID_mu'}, path=path)
#ma.variableToSignalSideExtraInfo('B-:sig', {'nParticlesInList(Sigma_c+:veto)': 'hasSigmaC+'}, path=path)
#ma.variableToSignalSideExtraInfo('B-:sig', {'nParticlesInList(Sigma_c*+:veto)': 'hasSigmaC*+'}, path=path)
'''
ma.variableToSignalSideExtraInfo('B-:sig', {'nSigma_cpp': 'nSigma_cpp'}, path=path)
ma.variableToSignalSideExtraInfo('B-:sig', {'M_SigmaCmu': 'M_SigmaCmu'}, path=path)
ma.variableToSignalSideExtraInfo('B-:sig', {'muon_Truth': 'muon_Truth'}, path=path)
ma.variableToSignalSideExtraInfo('B-:sig', {'nSigma_cppmu': 'nSigma_cppmu'}, path=path)
'''

vx.treeFit('B-:sig', conf_level=0, massConstraint=[], ipConstraint=True, updateAllDaughters=True, path=path)

ma.buildEventShape('', path=path)

ma.applyCuts('B-:sig', '-3 < cosThetaBetweenParticleAndNominalB < 2', path=path)
ma.applyCuts('B-:sig', 'foxWolframR2 < 0.5', path=path)



#ma.rankByHighest("B-:sig", "chiProb", numBest=1, path=path)

#ma.buildEventShape('', path=path)



#for SignalMC, run FEI
#if not base_path.startswith("/pnfs"):
#if TAG_HAD: ma.copyList('B+:hadtag', 'B+:generic', path=path)
#if TAG_SL: ma.copyList('B+:sltag', 'B+:semileptonic', path=path)
#else:
if TAG_HAD: ma.copyList('B+:hadtag', 'B+:feiHadronic', path=path)
if TAG_SL: ma.copyList('B+:sltag', 'B+:feiSL', path=path)



'''
ma.buildRestOfEvent(target_list_name='B-:sig', path=path)

roe_path = b2.Path()
deadEndPath = b2.Path()

ma.signalSideParticleFilter('B-:sig', '', roe_path, deadEndPath)

#ma.fillParticleList('gamma:roe', 'isInRestOfEvent == 1 and E > 0.050', path=roe_path)                   
#ma.reconstructDecay('pi0:roe -> gamma:roe gamma:roe', '0.080 < M < 0.200', path=roe_path)
#ma.fillParticleList('pi-:roe', 'isInRestOfEvent == 1 and E > 0.050', path=roe_path)
ma.fillParticleList('pi+:roe', 'isInRestOfEvent == 1 and E > 0.050', path=roe_path)
ma.fillParticleList('e+:roe', 'isInRestOfEvent == 1 and E > 0.050', path=roe_path)
ma.fillParticleList('mu+:roe', 'isInRestOfEvent == 1 and E > 0.050', path=roe_path)
#ma.fillParticleList('Lambda_c+:sig', 'isSignalSide == 1 and abs(pdg) == 4122', path=roe_path)

ma.fillSignalSideParticleList('Lambda_c+:sig', 'B-:sig -> ^Lambda_c+ ...', roe_path)

#ma.fillSignalSideParticleList('Lambda_c+:fromLcpe', 'B-:Lcpe -> ^Lambda_c+ anti-p-:good e-:good', roe_path)
#ma.fillSignalSideParticleList('Lambda_c+:fromLcpmu', 'B-:Lcpmu -> ^Lambda_c+ anti-p-:good mu-:good', roe_path) 
#ma.copyLists('Lambda_c+:sig', ['Lambda_c+:fromLcpe', 'Lambda_c+:fromLcpmu'], path=roe_path)

#ma.reconstructDecay('Sigma_c+:veto -> Lambda_c+:all pi0:roe', '1.9 < M < 2.6', path=roe_path)     
ma.reconstructDecay('Sigma_c++:Lcpi -> Lambda_c+:sig pi+:roe', '2.1 < M < 2.6', dmID=3, path=roe_path)
ma.reconstructDecay('Sigma_c++:Lcmu -> Lambda_c+:sig mu+:roe', '2.1 < M < 2.6', dmID=2, path=roe_path)
ma.reconstructDecay('Sigma_c++:Lce -> Lambda_c+:sig e+:roe', '2.1 < M < 2.6', dmID=1, path=roe_path)
ma.copyLists('Sigma_c++:veto', ['Sigma_c++:Lcpi', 'Sigma_c++:Lcmu', 'Sigma_c++:Lce'], path=roe_path)
#ma.reconstructDecay('Sigma_c*+:veto -> Lambda_c+:all pi0:roe', '1.9 < M < 2.6', path=roe_path)
#ma.rankByLowest('Sigma_c+:veto', 'abs(dM)', 1, path=roe_path)
ma.rankByLowest('Sigma_c++:veto', 'abs(dM)', 1, path=roe_path)
#ma.rankByLowest('Sigma_c*+:veto', 'abs(dM)', 1, path=roe_path)
#ma.mathMCTruth('Sigma_c++:veto', path=roe_path)
#ma.variableToSignalSideExtraInfo('Sigma_c+:veto', {'M': 'Sigma_c+veto'}, path=roe_path)
ma.variableToSignalSideExtraInfo('Sigma_c++:veto', 
    {
        'M': 'Sc++veto', 
        'countInList(Sigma_c++:Lcpi)': 'nSigma_cpp',
        'countInList(Sigma_c++:Lcmu)': 'nSigma_cppmu',
        'countInList(Sigma_c++:Lce)': 'nSigma_cppe',
        'extraInfo(decayModeID)': 'S_decayMode'
    }, path=roe_path)
#ma.variableToSignalSideExtraInfo('Sigma_c*+:veto', {'M': 'Sigma_c*+veto'}, path=roe_path)

path.for_each('RestOfEvent', 'RestOfEvents', roe_path)
'''


cleanMask = (
    "cleanMask",
    "pt > 0.1 and thetaInCDCAcceptance and abs(dz) < 4.0 and dr < 2.0",
    "E > 0.1 and thetaInCDCAcceptance",
    )
 

if TAG_HAD:
    ma.buildRestOfEvent(target_list_name='B-:sig', path=path)
    ma.appendROEMasks(list_name="B-:sig", mask_tuples=[cleanMask], path=path)
    ma.buildContinuumSuppression(list_name="B-:sig", roe_mask="cleanMask", path=path)

    ma.buildRestOfEvent(target_list_name='B+:hadtag', path=path)
    ma.appendROEMasks(list_name="B+:hadtag", mask_tuples=[cleanMask], path=path)
    ma.buildContinuumSuppression(list_name="B+:hadtag", roe_mask="cleanMask", path=path)
    

    # FEI selection cuts aligned with calibration
    ma.applyCuts("B+:hadtag", "Mbc >= 5.272", path=path)
    ma.applyCuts("B+:hadtag", "-0.150 <= deltaE <= 0.100", path=path)
    ma.applyCuts("B+:hadtag", "cosTBTO <= 0.9", path=path)
    ma.applyCuts("B+:hadtag", "extraInfo(SignalProbability) > 0.001", path=path)
    ma.rankByHighest("B+:hadtag", "extraInfo(SignalProbability)", numBest=1, path=path)
    ma.reconstructDecay('Upsilon(4S):hadtag -> B+:hadtag B-:sig', '', path=path)
    ma.matchMCTruth(list_name='Upsilon(4S):hadtag', path=path)
    ma.buildRestOfEvent(target_list_name='Upsilon(4S):hadtag', path=path)

    ma.appendROEMasks(list_name="Upsilon(4S):hadtag", mask_tuples=[cleanMask], path=path)
    ma.buildContinuumSuppression(list_name="Upsilon(4S):hadtag", roe_mask="cleanMask", path=path)
    
    ma.applyCuts('Upsilon(4S):hadtag', 'nROE_Charged() < 2', path=path)

if TAG_SL:
    '''
    ma.buildRestOfEvent(target_list_name='B-:sig', path=path)
    ma.appendROEMasks(list_name="B-:sig", mask_tuples=[cleanMask], path=path)
    ma.buildContinuumSuppression(list_name="B-:sig", roe_mask="cleanMask", path=path)

    ma.buildRestOfEvent(target_list_name='B+:sltag', path=path)
    ma.appendROEMasks(list_name="B+:sltag", mask_tuples=[cleanMask], path=path)
    ma.buildContinuumSuppression(list_name="B+:sltag", roe_mask="cleanMask", path=path)
    '''

    ma.applyCuts("B+:sltag", "-8 < cosThetaBetweenParticleAndNominalB < 2", path=path)
    ma.rankByHighest("B+:sltag", "extraInfo(SignalProbability)", numBest=1, path=path)
    ma.reconstructDecay('Upsilon(4S):sltag -> B+:sltag B-:sig', '', path=path)
    ma.matchMCTruth(list_name='Upsilon(4S):sltag', path=path)
    ma.buildRestOfEvent(target_list_name='Upsilon(4S):sltag', path=path)

    
    #ma.appendROEMasks(list_name="Upsilon(4S):sltag", mask_tuples=[cleanMask], path=path)
    #ma.buildContinuumSuppression(list_name="Upsilon(4S):sltag", roe_mask="cleanMask", path=path)
    
    ma.applyCuts('Upsilon(4S):sltag', 'nROE_Charged() < 2', path=path)


'''
if TAG_HAD:
    # FEI selection cuts aligned with calibration
    #ma.buildRestOfEvent(target_list_name='B+:hadtag', path=path)
    ma.appendROEMasks(list_name="Upsilon(4S):hadtag", mask_tuples=[cleanMask], path=path)
    ma.buildContinuumSuppression(list_name="Upsilon(4S):hadtag", roe_mask="cleanMask", path=path)
    #ma.applyCuts("Upsilon(4S):hadtag", "cosTBTO <= 0.9", path=path)
if TAG_SL:
    #ma.buildRestOfEvent(target_list_name='B+:sltag', path=path)
    ma.appendROEMasks(list_name="Upsilon(4S):sltag", mask_tuples=[cleanMask], path=path)
    ma.buildContinuumSuppression(list_name="Upsilon(4S):sltag", roe_mask="cleanMask", path=path)
'''







track_variables = ['p', 'useCMSFrame(p)', 'cosTheta', 'phi', "charge", 'isSignal', 'chiProb', 'electronID', 'muonID', 'pionID', 'kaonID', 'protonID', 'deuteronID', 'mcPDG', 'mcMother(PDG)']
composite_variables = ['InvM', 'isSignal', 'isSignalAcceptMissing', 'isSignalAcceptMissingGamma', 'isSignalAcceptMissingMassive', 'isSignalAcceptMissingNeutrino', 'mcErrors', 'chiProb', 'extraInfo(decayModeID)', 'p', 'useCMSFrame(p)', 'cosTheta', 'phi', 'charge', 'dM', 'mcPDG', 'nMCDaughters', 'mcMother(PDG)']
B_variables = [
        'cosThetaBetweenParticleAndNominalB', 
        'daughterInvM(0, 1)', 
        'daughterInvM(0, 2)', 
        'daughterInvM(1, 2)', 
        #'daughterAngle(0, 1)', 
        #'daughterAngle(0, 2)', 
        #'daughterAngle(1, 2)', 
        #'daughterAngle(0, 1, 2)', 
        'recQ2Bh', 
        'recQ2BhSimple',
        'deltaE',
        'Mbc',
        'mcDaughter(0, PDG)',
        'mcDaughter(1, PDG)',
        'mcDaughter(2, PDG)',
        'mcDaughter(3, PDG)',
        'mcDaughter(4, PDG)',
        'foxWolframR2'
    ]
Y_variables = [
        'isContinuumEvent', 
        'isUnmixedBEvent', 
        'isChargedBEvent', 
        'isMC',
        'm2RecoilSignalSide'
    ]
tag_variables = [
        'extraInfo(SignalProbability)',
        'extraInfo(decayModeID)',
        'Mbc',
        'deltaE',
        'cosThetaBetweenParticleAndNominalB'
        ]
event_variables = vc.roe_multiplicities + vc.event_shape

CS_variables = [
    "R2",
    "thrustBm",
    "thrustOm",
    "cosTBTO",
    "cosTBz",
    "KSFWVariables(et)",
    "KSFWVariables(mm2)",
    "KSFWVariables(hso00)",
    "KSFWVariables(hso01)",
    "KSFWVariables(hso02)",
    "KSFWVariables(hso03)",
    "KSFWVariables(hso04)",
    "KSFWVariables(hso10)",
    "KSFWVariables(hso12)",
    "KSFWVariables(hso14)",
    "KSFWVariables(hso20)",
    "KSFWVariables(hso22)",
    "KSFWVariables(hso24)",
    "KSFWVariables(hoo0)",
    "KSFWVariables(hoo1)",
    "KSFWVariables(hoo2)",
    "KSFWVariables(hoo3)",
    "KSFWVariables(hoo4)",
    "CleoConeCS(1)",
    "CleoConeCS(2)",
    "CleoConeCS(3)",
    "CleoConeCS(4)",
    "CleoConeCS(5)",
    "CleoConeCS(6)",
    "CleoConeCS(7)",
    "CleoConeCS(8)",
    "CleoConeCS(9)",
]

sigma_event_variables = [
    'countInList(Sigma_c++:Lcpi)',
    'countInList(Sigma_c++:Lcmu)',
    'countInList(Sigma_c++:Lce)'
]

sigma_variables = [
    'M',
    'InvM',
    'dM',
    'p',
    #'useCMSFrame(p)',
    #'cosTheta',
    #'phi',
    #'chiProb',
    #'isSignal',
    'mcPDG',
    'mcMother(PDG)',
    'mcErrors',
    'mcDaughter(0,PDG)',
    'mcDaughter(1,PDG)',
    'nMCDaughters',
    #'nSigma_cp',
    #'nSigma_cSp',
    'extraInfo(nSigma_cpp)',
    'extraInfo(nSigma_cppmu)',
    'extraInfo(nSigma_cppe)',
    'dM_mu',
    #'muPID',
    #'ePID',
    #'piPID',
    'hasMuB',
    'hasEB',
    #'lepPDG',
    'S_decayMode',
    #'extraInfo(decayModeID)'
    #'nSigma_window'
    #'massDifference(0,1)'
]



# B to Lc p l nu variables
variables_tracks_Lcpl = vu.create_aliases_for_selected(list_of_variables=track_variables, decay_string='Upsilon(4S) -> B+ [B- -> [Lambda_c+ -> ^p+ ^K- ^pi+] ^anti-p- ^mu-]')
variables_composite_Lcpl = vu.create_aliases_for_selected(list_of_variables=composite_variables, decay_string='^Upsilon(4S) -> B+ [^B- -> [^Lambda_c+ -> p+ K- pi+] anti-p- mu-]')
variables_B_Lcpl = vu.create_aliases_for_selected(list_of_variables=B_variables + CS_variables, decay_string='Upsilon(4S) -> B+ ^B-') # + CS_variables
variables_Y = vu.create_aliases_for_selected(list_of_variables=Y_variables + CS_variables, decay_string='^Upsilon(4S) -> B+ B-') # + CS_variables
variables_tag = vu.create_aliases_for_selected(list_of_variables=tag_variables + CS_variables, decay_string='Upsilon(4S) -> ^B+ B-', prefix='Btag') # + CS_variables


output_file="output.root" #output_had_test6.root

if TAG_HAD:
    
    ma.variablesToNtuple(
            decayString='Upsilon(4S):hadtag', 
            variables=variables_tracks_Lcpl + variables_composite_Lcpl + variables_B_Lcpl + event_variables + variables_Y + variables_tag + sigma_event_variables + mc_gen_topo(200),
            #filename= output_file, 
            filename=sys.argv[1],
            treename='hadronic',
            path=path
    )
    
    ma.variablesToNtuple(
            decayString='Sigma_c++:veto',
            variables=sigma_variables,
            #filename= output_file, 
            filename= sys.argv[1],
            treename='veto',
            path=path
    )
    '''
    ma.variablesToNtuple(
            decayString='Sigma_c+:veto',
            variables=sigma_variables,
            filename=sys.argv[1],
            treename='Sigma_cp_veto',
            path=path
    )

    ma.variablesToNtuple(
            decayString='Sigma_c*+:veto',
            variables=sigma_variables,
            filename=sys.argv[1],
            treename='Sigma_cstarp_veto',
            path=path
    )
    
    ma.variablesToNtuple(
            decayString='Sigma_c++:veto2',
            variables=sigma_variables,
            filename=sys.argv[1],
            treename='Sigma_cpp_veto2',
            path=path
    )
    '''

if TAG_SL:
    ma.variablesToNtuple(
            decayString='Upsilon(4S):sltag', 
            variables=variables_tracks_Lcpl + variables_composite_Lcpl + variables_B_Lcpl + event_variables + variables_Y + variables_tag + mc_gen_topo(200),
            filename= output_file, #sys.argv[1],
            treename='semileptonic',
            path=path
    )
    '''
    ma.variablesToNtuple(
            decayString='Sigma_c++:veto',
            variables=sigma_variables,
            filename=output_file, #sys.argv[1],
            treename='Sigma_cpp_veto',
            path=path
    )
    '''

b2.process(path) #, event_max=500)
print(b2.statistics)
