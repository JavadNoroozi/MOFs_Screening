import os
import subprocess
import fnmatch
import shutil
import random
import argparse

start = "Started.txt"
done = "Finished.txt"
gcmc = "/opt/ohpc/pub/fastmc/1.4.0/bin/gcmc.x"


def Restart():
    files = ['OUTPUT', 'jobcontrol.in']
    try:
        shutil.rmtree('branch01')
    except:
        pass
    for i in files:
        try:
            os.remove(i)
        except:
            pass
    subprocess.run([gcmc])
    shutil.rmtree('branch01')
    os.remove('CONFIG')
    os.remove('CONTROL')
    os.remove('FIELD')
    os.remove('jobcontrol.in')
    os.remove(start)
    with open(done, 'w') as f:
        f.write("Done.")

def Start():
    files = ['CONFIG', 'CONTROL', 'FIELD', 'jobcontrol.in', start]
    with open(start, 'w') as f:
        f.write("Started.")
    subprocess.run([gcmc])
    shutil.rmtree('branch01')
    for i in files:
        os.remove(i)
    with open(done, "w") as f:
        f.write("Done.")

def RunGCMC():
    mofname = os.getcwd().split('/')[-1]
    with open(start, "w") as f:
        f.write("Started.")
    gcmc_folder = f"faps_{mofname}_fastmc"
    os.chdir(gcmc_folder)
    ignore = ['T298.0P0.15', 'FIELD', 'CONFIG']
    gcmc = [f for f in os.listdir(os.getcwd()) if f not in ignore]
    for job in gcmc:
        os.chdir(job)
        if os.path.isfile(done):
            pass
        elif os.path.isfile(start) == True and os.path.isfile("OUTPUT") == True:
            Restart()
        else:
            Start()
        os.chdir('..')
    os.chdir('..')
    os.remove(start)
    with open(done, "w") as f:
        f.write("Done")

def main():
    RunGCMC()

if __name__ == "__main__":
    main()

