#!/usr/bin/env python
# -*- coding: utf-8 -*-

#gb2_ds_search collection --get_metadata /belle/collection/MC/S16_MC16rd-proc16_4S_udsctau_skim_74000100_v2

import os
import sys
import glob
import time

################################################################################################################################
################################################################################################################################

# Here we define the steering file we want to use and the release we want 
steering_file = 'B_to_Lcplnu.py'
release = 'release-08-01-05'

# Here we define the collections
# MC16rd+proc16 just included qq and BB (include tau)



coll_dict_skim = {
    'BB_proc_had': '/belle/collection/MC/S16_MC16rd-proc16_4S_BB_skim_11180500_v6', #hadronic
    #'BB_proc_sl': '/belle/collection/MC/S16_MC16rd-proc16_4S_BB_skim_11180600_v3', #semi-leptonic
    #'udsctau_proc_had': '/belle/collection/MC/S16_MC16rd-proc16_4S_udsctau_skim_11180500_v6', #hadronic
    #'udsctau_proc_sl': '/belle/collection/MC/S16_MC16rd-proc16_4S_udsctau_skim_11180600_v3', #semi-leptonic
    #'BB_prompt_had': '/belle/collection/MC/S16_MC16rd-prompt_4S_BB_skim_11180500_v6 ', #hadronic
    #'BB_prompt_sl': '/belle/collection/MC/S16_MC16rd-prompt_4S_BB_skim_11180600_v1 ', #semi-leptonic
    #'udsctau_prompt_had': '/belle/collection/MC/S16_MC16rd-prompt_4S_udsctau_skim_11180500_v6 ', #hadronic, skim
    #'udsctau_prompt_sl': '/belle/collection/MC/S16_MC16rd-prompt_4S_udsctau_skim_11180600_v1 ', #semi-leptonic, skim
    #'signMC_had': '/pnfs/desy.de/belle/local/belle/group/physics/SLME/sMC16rd_1263720001_26647/11180500/udst/sub00/*.root', #hadronic
    #'signMC_sl': '/pnfs/desy.de/belle/local/belle/group/physics/SLME/sMC16rd_1263720001_26647/11180500/udst/sub00/*.root', #semi-leptonic

}


coll_dict_skim_data = {
    #'skim_data_2': '/belle/collection/Data/S16_proc16_4S_skim_11180500_v3/', #hadronic
    #'skim_data_1': '/belle/collection/Data/S16_prompt_4S_skim_11180500_v1/',
    #'skim_data_2': '/belle/collection/Data/S16_proc16_4S_skim_11180600_v3/', #semi-leptonic
    #'skim_data_1': '/belle/collection/Data/S16_prompt_4S_skim_11180600_v1/',
}

test = {
    'test': '/belle/MC/light-2503-ceres/DB00003308/MC16rd_prompt/prod00051404/s00/e0033/4S/r00000/charged/11180500/udst/sub00/udst_000001_prod00051404_task320000001.root'
    
    #'/pnfs/desy.de/belle/local/belle/group/physics/SLME/sMC16rd_1263720001_26647/11180500/udst/sub00/11180500_00000_job522166816_00.udst.root' signalMC

    #'/belle/MC/light-2503-ceres/DB00003307/MC16rd_proc16/prod00051442/s00/e0024/4S/r00000/mixed/11180500/udst/sub00/udst_000001_prod00051442_task230000001.root' BB or udsctau
    #/belle/MC/light-2503-ceres/DB00003308/MC16rd_prompt/prod00051404/s00/e0033/4S/r00000/charged/11180500/udst/sub00/udst_000001_prod00051404_task320000001.root
}



coll_dict = coll_dict_skim #coll_dict_skim, coll_dict_skim_data or test



for evt_type_str, coll in coll_dict.items():

    # Here you define the prefix of the project
    project_name = 'B_Lcplnu_' + evt_type_str + '_v8' 

    
    # This is the main command to submit to the grid
    # we use the steering_file and release defined and the created project name
    # cputime must be defined individually, I think it is 20* real time in minutes if ran locally
    # munu-munux1-e0-r0-sub00.root is the file name, each file gets a individual file name, e.g. munu-munux1-e0-r0-sub00_00194_job389659631_13.root
    command = 'gbasf2 ' + steering_file + ' -p ' + project_name + ' -i ' + coll + ' -s ' + release + ' --cputime 100 ' + ' --basf2opt=\" -- ' + evt_type_str  + '_output.root \"' 
    
    
    print(command)
    os.system(command)
    time.sleep(1)

    #command = 'gbasf2 ' + steering_file + ' -p ' + project_name + ' -i ' + coll + ' -s ' + release + ' --cputime 100 ' + ' --basf2opt=\" -- ' + evt_type_str  + '_output.root \"' 
    #
    #gbasf2 steeringfile.py -p dalitz_uubar_exp20-26_v2_topoana -i /belle/MC/release-06-00-11/DB00002284/MC15rd_b/prod00028008/s00/e0020/4S/r00429/uubar/mdst/sub00/mdst_000001_prod00028008_task19428000001.root -s release-08-01-05 --cputime 100  --basf2opt=" -- uubar_exp20-26_output.root "

    #/MC/release-06-00-11/DB00002284/MC15rd_b/prod00028010/s00/e0020/4S/r00597/ccbar/mdst/sub00/mdst_000001_prod00028010_task19596000001.root
#skim one file
#/belle/MC/build-light-2411a/DB00003307/MC16rd_proc16/prod00048161/s00/e0014/4S/r00000/charged/None/74000100/mdst/sub00/mdst_000001_prod00048161_task130000001.root

# gbasf2 steeringfile.py -p dalitz_skim_test_v1 -i /belle/MC/build-light-2411a/DB00003307/MC16rd_proc16/prod00048161/s00/e0014/4S/r00000/charged/None/74000100/mdst/sub00/mdst_000001_prod00048161_task130000001.root -s release-08-01-05 --cputime 100  --basf2opt=" -- skimtest_output.root "
# gb2_ds_search collection --list_all_collections /belle/collection/MC/* | grep "S16" | grep "74000100"