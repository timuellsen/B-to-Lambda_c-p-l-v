import os
import sys
import glob
import time
#import subprocess

# Argumente prüfen
if len(sys.argv) < 2:
    print("Usage: python3 SignMC_process.py <start_index>")
    sys.exit(1)



steering_file = 'B_to_Lcplnu.py'
dir = '/pnfs/desy.de/belle/local/belle/group/physics/SLME/sMC16rd_1263720001_26647/11180500/udst/sub00/'
#project_name = "Lcplnu"
#release = "release-09-00-06"
evt_type_str = "signMC"

exclude_numbers = {345, 346, 347, 348, 349, 350}

start=int(sys.argv[1])
end=start+50

root_files = sorted(glob.glob(os.path.join(dir, "*.root")))
files_to_process = root_files[start:end]

i=1
for sig in files_to_process:
    filename = os.path.basename(sig)
    
    number = int(filename.split("_")[1])

    if number in exclude_numbers:
        print(f"Skip file {filename} (Number {number})")
        continue

    output_name = f"/data/dust/user/timmue/project/signMC/{evt_type_str}_{number}_cut_output_4.root"

    if os.path.exists(output_name):
        print(f"Skip {filename} → output already exists")
        continue
    
    #command = 'basf2 ' + steering_file + ' -p ' + project_name + ' -i ' + sig + ' -s ' + release + ' --cputime 100 ' + ' --basf2opt=\" -- ' + evt_type_str  + '_output.root \"' 
    #command = 'basf2 ' + steering_file + ' -p ' + project_name + ' -i ' + sig + ' -s ' + release + ' --cputime 100 ' + ' --basf2opt=\" -- ' + evt_type_str  + '_output.root \"' 
    
    command = f"basf2 {steering_file} {output_name} {sig}"

    print(str(i)+". root file is processed")
    print(command)
    os.system(command)
    i=i+1
    time.sleep(1)