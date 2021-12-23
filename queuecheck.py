import os
import subprocess


def GetJobs():

    ''' Check the queue and return the number of queued and running jobs '''

    runningjobs = []
    queuedjobs = []
    jobids = []

    p = subprocess.run(['squeue', '-u', 'jnoroozi'], check=True,
                       stdout=subprocess.PIPE, universal_newlines=True)
    output = p.stdout

    with open("JobLog.txt", "w") as f:
        f.write(output)

    with open("JobLog.txt", "r") as f:
        next(f)
        for line in f:
            if(line.strip().split(' ')[7]) == 'R':
                runningjobs.append(line.strip().split(' ')[0])
                jobids.append(line.strip().split(' ')[0])
            elif(line.strip().split(' ')[6]) == 'PD':
                queuedjobs.append(line.strip().split(' ')[0])
                jobids.append(line.strip().split(' ')[0])

    with open("job_ids.txt", 'w') as f:
        for j in jobids:
            f.write(j)
            f.write("\n")
    os.remove("JobLog.txt")

    return str(len(runningjobs)), str(len(queuedjobs))


def main():
    running, queued = GetJobs()

    print("There are: " + running + " jobs running!")
    print("There are: " + queued + " jobs queued!")


if __name__ == "__main__":
    main()
