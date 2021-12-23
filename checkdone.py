import os
from datetime import date
import shutil

startdir = os.getcwd()
os.chdir('JobsRun')

inthisdir = os.listdir(os.getcwd())
finishedfile = "Finished.txt"
readytoanalyze = []
today = date.today()

for i in inthisdir:
    os.chdir(i)
    if os.path.isfile(finishedfile):
        readytoanalyze.append(i)
    else:
        pass
    os.chdir('..')

dirname = f"ReadyToProcess-{today}"
os.mkdir(dirname)

for j in readytoanalyze:
    shutil.move(j, dirname)

shutil.move(dirname, startdir)
