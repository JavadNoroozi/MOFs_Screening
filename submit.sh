#!/bin/bash
#SBATCH --partition=General
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --job-name=Screening
#SBATCH --time=2:00:00

cd /home/jnoroozi/SCREENING/NotDone/metals/  # this is where GCMC inputs are 

shopt -s nullglob
dirs=(*/)
[[ $dirs ]] && var="${dirs[RANDOM%${#dirs[@]}]}"
echo "$var"

# this moves a random GCMC folder to loacl scratch for running 
mv "$var" /local_scratch/jnoroozi

# this goes into the folder and runs gcmc on it

cd /local_scratch/jnoroozi/$var
srun -t 1:55:00 python3 /home/jnoroozi/SCREENING/gcmc.py

cd ..
mv $var /home/jnoroozi/SCREENING/JobsRun/metals # Modify this to change where the jobs are returned to
