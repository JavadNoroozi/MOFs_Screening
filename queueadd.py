import subprocess
import time
import argparse
from queuecheck import GetJobs

parser = argparse.ArgumentParser()
parser.add_argument('-r', type=int, required=True)
parser.add_argument('-s', type=int, required=True)
parser.add_argument('-l', type=int, required=True)
args = parser.parse_args()

_range = args.r
sleep = args.s
lim = args.l


def AddJobs():

    ''' Determines how many jobs can be added to the queue and submits jobs '''

    running, queued = GetJobs()
    queue_limit = lim
    total_jobs = int(running) + int(queued)
    diff = (queue_limit - total_jobs)

    if diff > 0:
        for i in range(diff):
            subprocess.run(['sbatch', 'submit.sh'])
    else:
        pass


def main():
    for i in range(_range):
        AddJobs()
        subprocess.run(['rm', 'slurm*'])
        time.sleep(sleep)


if __name__ == "__main__":
    main()
