import os
import shutil

destination = "/home/smaley/ForHTPS4"
os.chdir('JobsRun')

in_dir = os.listdir(os.getcwd())

for i in in_dir:
    os.chdir(i)
    if os.path.isfile("Started.txt"):
        os.remove("Started.txt")
    else:
        pass
    os.chdir('..')
    try:
        shutil.move(i, destination)
    except shutil.Error:
        shutil.rmtree(i)
