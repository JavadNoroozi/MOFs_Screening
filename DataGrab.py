import os
import re
import csv
import pandas as pd
import fnmatch
import shutil
import argparse

# Need to grab some stuff about the geometry


def GeometryExtractor():

    weight = 0.0
    geometry = []
    try:
        with open('FIELD', 'r') as f:
            for line in f:
                if 'Framework' in line:
                    supercell = int((next(f).strip().split(' ')[1]))
                    numatoms = int((next(f).strip().split(' ')[1]))
                    for i in range(numatoms):
                        geometry.append((next(f).strip()))
                else:
                    pass

            for j in geometry:
                weight += float(re.findall('\d+\.\d+', j)[0])

        return weight, supercell

    except:
        pass


parser = argparse.ArgumentParser()
parser.add_argument('--f', type=str, required=True)
args = parser.parse_args()
folder = args.f

os.chdir(folder)

ignore = ['compile_data.py', '.DS_Store', 'Finished.txt', 'celldensity.py', 'checkdone.py', 'submit2.sh']

folders = os.listdir(os.getcwd())
clean_dir = [f for f in folders if f not in ignore]
startdir = os.getcwd()

# Go into each MOF directory, get needed geometry info, split by binary/
# single component simulation. Get temp and pressures.

for mof in clean_dir:
    os.chdir(mof)
    print(mof)
    fastmcrun = f"faps_{mof}_fastmc"
    mofclipped = mof.split('_repeat')[0]
    co2binarydata = []
    n2binarydata = []
    co2monodata = []
    n2monodata = []
    os.chdir(fastmcrun)
    ignore = ['FIELD', 'CONFIG', 'T298.0P0.15', '.DS_Store']
    clean_fastmc = [f for f in os.listdir(os.getcwd()) if f not in ignore]
    weight, supercell = GeometryExtractor()
    for i in clean_fastmc:
        binaryjobs = []
        co2jobs = []
        n2jobs = []
        temp, p1, p2 = (re.findall('[A-Z][^A-Z]*', i))
        temp = float(temp.split('T')[1])
        p1 = float(p1.split('P')[1])
        p2 = float(p2.split('P')[1])
        if p1 != 0.0 and p2 != 0.0:
            binaryjobs.append(i)
        elif p1 != 0.0 and p2 == 0.0:
            co2jobs.append(i)
        else:
            n2jobs.append(i)

# parser for single component CO2 jobs

        for job in co2jobs:
            os.chdir(job)
            temp, p1, p2 = (re.findall('[A-Z][^A-Z]*', job))
            temp = float(temp.split('T')[1])
            p1 = float(p1.split('P')[1])
            p2 = float(p2.split('P')[1])
            co2results = []
            with open('OUTPUT', 'r', encoding="utf8", errors='ignore') as f:
                for line in f:
                    if 'Guest    1 pressure' in line:
                        co2fugpressure = (line.strip().split(' ')[-2])
                    elif 'final stats for guest  1   carbon dioxide' in line:
                        for i in range(18):
                            co2results.append(next(f).strip())
                        numco2guests = co2results[9].split(' ')[-1]
                        numco2guests_err = co2results[10].split(' ')[-1]
                        co2Hads = co2results[11].split(' ')[-1]
                        co2Hads_err = co2results[12].split(' ')[-1]
                        co2Cv = co2results[13].split(' ')[-1]
                        co2Cv_err = co2results[14].split(' ')[-1]
                        co2uptake = (float(numco2guests) / float(supercell))
                        co2uptake_err = (float(numco2guests_err) / float(supercell))
                        co2grav = 1000 * co2uptake / weight
                        co2grav_err = 1000 * co2uptake_err / weight
                    else:
                        pass

            co2_data = [temp, p1, co2uptake, co2grav, co2grav_err, co2Hads,
                        co2Hads_err, co2Cv, co2Cv_err, co2fugpressure, p1]

            co2monodata.append(co2_data)

            os.chdir('..')

# Parse for single component N2 jobs

        for job in n2jobs:
            os.chdir(job)
            temp, p1, p2 = (re.findall('[A-Z][^A-Z]*', job))
            temp = float(temp.split('T')[1])
            p1 = float(p1.split('P')[1])
            p2 = float(p2.split('P')[1])
            n2results = []
            with open('OUTPUT', 'r') as f:
                for line in f:
                    if 'Guest    2 pressure' in line:
                        n2fugpressure = (line.strip().split(' ')[-2])
                    elif 'final stats for guest  2   nitrogen in mofs' in line:
                        for i in range(18):
                            n2results.append(next(f).strip())
                        numn2guests = n2results[9].split(' ')[-1]
                        numn2guests_err = n2results[10].split(' ')[-1]
                        n2Hads = n2results[11].split(' ')[-1]
                        n2Hads_err = n2results[12].split(' ')[-1]
                        n2Cv = n2results[13].split(' ')[-1]
                        n2Cv_err = n2results[14].split(' ')[-1]
                        n2uptake = (float(numn2guests) / float(supercell))
                        n2uptake_err = (float(numn2guests_err) / float(supercell))
                        n2grav = 1000 * n2uptake / weight
                        n2grav_err = 1000 * n2uptake_err / weight
                    else:
                        pass
            n2_data = [temp, p2, n2uptake, n2grav, n2grav_err, n2Hads,
                       n2Hads_err, n2Cv, n2Cv_err, n2fugpressure, p2]

            n2monodata.append(n2_data)

            os.chdir('..')

# Parser for binary jobs

        for job in binaryjobs:
            os.chdir(job)
            temp, p1, p2 = (re.findall('[A-Z][^A-Z]*', job))
            temp = float(temp.split('T')[1])
            p1 = float(p1.split('P')[1])
            p2 = float(p2.split('P')[1])
            co2results = []
            n2results = []
            with open('OUTPUT', 'r', encoding="utf8", errors='ignore') as f:
                for line in f:
                    if 'Guest    1 pressure' in line:
                        co2fugpressure = (line.strip().split(' ')[-2])
                    elif 'Guest    2 pressure' in line:
                        n2fugpressure = (line.strip().split(' ')[-2])
                    elif 'final stats for guest  1   carbon dioxide' in line:
                        for i in range(18):
                            co2results.append(next(f).strip())
                        numco2guests = co2results[9].split(' ')[-1]
                        numco2guests_err = co2results[10].split(' ')[-1]
                        co2Hads = co2results[11].split(' ')[-1]
                        co2Hads_err = co2results[12].split(' ')[-1]
                        co2Cv = co2results[13].split(' ')[-1]
                        co2Cv_err = co2results[14].split(' ')[-1]
                        co2uptake = (float(numco2guests) / float(supercell))
                        co2uptake_err = (float(numco2guests_err) / float(supercell))
                        co2grav = 1000 * co2uptake / weight
                        co2grav_err = 1000 * co2uptake_err / weight
                    elif 'final stats for guest  2   nitrogen in mofs' in line:
                        for i in range(18):
                            n2results.append(next(f).strip())
                        numn2guests = n2results[9].split(' ')[-1]
                        numn2guests_err = n2results[10].split(' ')[-1]
                        n2Hads = n2results[11].split(' ')[-1]
                        n2Hads_err = n2results[12].split(' ')[-1]
                        n2Cv = n2results[13].split(' ')[-1]
                        n2Cv_err = n2results[14].split(' ')[-1]
                        n2uptake = (float(numn2guests) / float(supercell))
                        n2uptake_err = (float(numn2guests_err) / float(supercell))
                        n2grav = 1000 * n2uptake / weight
                        n2grav_err = 1000 * n2uptake_err / weight
                    elif 'selectivity stats for guest  1/ 2' in line:
                        #next(f)
                        #next(f)
                        try:
                            selectresult = (next(f).strip().split(' '))
                            selectivity, selecterror = selectresult[6], selectresult[-1]
                        except IndexError:
                            next(f)
                            selectresult = (next(f).strip().split(' '))
                            selectivity, selecterror = selectresult[6], selectresult[-1]
                    else:
                        pass

                co2_data = [temp, p1, co2uptake, co2grav, co2grav_err, co2Hads,
                            co2Hads_err, co2Cv, co2Cv_err, selectivity,
                            selecterror, co2fugpressure, p1, p2]

                co2binarydata.append(co2_data)

                n2_data = [temp, p2, n2uptake, n2grav, n2grav_err, n2Hads,
                           n2Hads_err, n2Cv, n2Cv_err, selectivity,
                           selecterror, n2fugpressure, p1, p2]

                n2binarydata.append(n2_data)

            os.chdir('..')
    os.chdir('..')

# Write out the data to csvs, sort, and separate them

    binaryheader = ['Temp', 'p', 'molc', 'mmol/g', 'stdev',
                    'HOA', 'stdev', 'Cv', 'stdev', 'S(g1)',
                    'S(g1)_err', 'f/bar', 'p(g1)', 'p(g2)']

    monoheader = ['Temp', 'p', 'molc', 'mmol/g', 'stdev',
                  'HOA', 'stdev', 'Cv', 'stdev', 'f/bar', 'p(g1)']

    mono298 = [298, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    mono333 = [333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    mono393 = [393, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    bi298 = [298.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0]

    bi333 = [333.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0]

    bi393 = [393.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0]

    with open('tempBiCO2data.csv', 'w', newline='') as csvfile:
        write = csv.writer(csvfile)
        write.writerow(binaryheader)
        write.writerow(bi298)
        write.writerow(bi333)
        write.writerow(bi393)
        write.writerows(co2binarydata)

    binaryCO2data = pd.read_csv('tempBiCO2data.csv')
    bico2_298 = binaryCO2data[binaryCO2data.Temp == 298]
    bico2_333 = binaryCO2data[binaryCO2data.Temp == 333]
    bico2_393 = binaryCO2data[binaryCO2data.Temp == 393]
    bico2_298_sort = bico2_298.sort_values(by=['p'])
    bico2_333_sort = bico2_333.sort_values(by=['p'])
    bico2_393_sort = bico2_393.sort_values(by=['p'])

    bico2_298_sort.to_csv(f"{mofclipped}-Binary-CO2-298K.csv", index=False)
    bico2_333_sort.to_csv(f"{mofclipped}-Binary-CO2-333K.csv", index=False)
    bico2_393_sort.to_csv(f"{mofclipped}-Binary-CO2-393K.csv", index=False)

    with open('tempBiN2data.csv', 'w', newline='') as csvfile:
        write = csv.writer(csvfile)
        write.writerow(binaryheader)
        write.writerow(bi298)
        write.writerow(bi333)
        write.writerow(bi393)
        write.writerows(n2binarydata)

    binaryN2data = pd.read_csv('tempBiN2data.csv')
    bin2_298 = binaryN2data[binaryN2data.Temp == 298]
    bin2_333 = binaryN2data[binaryN2data.Temp == 333]
    bin2_393 = binaryN2data[binaryN2data.Temp == 393]
    bin2_298_sort = bin2_298.sort_values(by=['p'])
    bin2_333_sort = bin2_333.sort_values(by=['p'])
    bin2_393_sort = bin2_393.sort_values(by=['p'])

    bin2_298_sort.to_csv(f"{mofclipped}-Binary-N2-298K.csv", index=False)
    bin2_333_sort.to_csv(f"{mofclipped}-Binary-N2-333K.csv", index=False)
    bin2_393_sort.to_csv(f"{mofclipped}-Binary-N2-393K.csv", index=False)

    with open('tempMonoCO2data.csv', 'w', newline='') as csvfile:
        write = csv.writer(csvfile)
        write.writerow(monoheader)
        write.writerow(mono298)
        write.writerow(mono333)
        write.writerow(mono393)
        write.writerows(co2monodata)

    singleCO2data = pd.read_csv('tempMonoCO2data.csv')
    co2_298 = singleCO2data[singleCO2data.Temp == 298]
    co2_333 = singleCO2data[singleCO2data.Temp == 333]
    co2_393 = singleCO2data[singleCO2data.Temp == 393]
    co2_298_sort = co2_298.sort_values(by=['p'])
    co2_333_sort = co2_333.sort_values(by=['p'])
    co2_393_sort = co2_393.sort_values(by=['p'])

    co2_298_sort.to_csv(f"{mofclipped}-SingleComp-CO2-298K.csv", index=False)
    co2_333_sort.to_csv(f"{mofclipped}-SingleComp-CO2-333K.csv", index=False)
    co2_393_sort.to_csv(f"{mofclipped}-SingleComp-CO2-393K.csv", index=False)

    with open('tempMonoN2data.csv', 'w', newline='') as csvfile:
        write = csv.writer(csvfile)
        write.writerow(monoheader)
        write.writerow(mono298)
        write.writerow(mono333)
        write.writerow(mono393)
        write.writerows(n2monodata)

    singleN2data = pd.read_csv('tempMonoN2data.csv')
    n2_298 = singleN2data[singleN2data.Temp == 298]
    n2_333 = singleN2data[singleN2data.Temp == 333]
    n2_393 = singleN2data[singleN2data.Temp == 393]
    n2_298_sort = n2_298.sort_values(by=['p'])
    n2_333_sort = n2_333.sort_values(by=['p'])
    n2_393_sort = n2_393.sort_values(by=['p'])

    n2_298_sort.to_csv(f"{mofclipped}-SingleComp-N2-298K.csv", index=False)
    n2_333_sort.to_csv(f"{mofclipped}-SingleComp-N2-333K.csv", index=False)
    n2_393_sort.to_csv(f"{mofclipped}-SingleComp-N2-393K.csv", index=False)

# Clean up temporary files

    tempfiles = ['tempBiN2data.csv', 'tempBiCO2data.csv', 'tempMonoN2data.csv',
                 'tempMonoCO2data.csv']

    for tempfile in tempfiles:
        os.remove(tempfile)

# Make a directory to put all the csvs in
    dirname = f"{mofclipped}-GCMC_data"
    os.mkdir(dirname)
    csvs = []
    filelist = os.listdir('.')
    pattern = "*.csv"

    for item in filelist:
        if fnmatch.fnmatch(item, pattern):
            csvs.append(item)

    for datafile in csvs:
        try:
            shutil.move(datafile, dirname)
        except:
            pass

    shutil.move(dirname, startdir)

    os.chdir('..')
