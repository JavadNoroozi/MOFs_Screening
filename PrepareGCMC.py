import os, shutil, argparse, fnmatch, random, subprocess

homedir = "/home/jnoroozi/SCREENING"

parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, required=True)
parser.add_argument('-n', type=int, required=True)
args = parser.parse_args()
folder = args.f
numfiles = args.n
tar = f"{folder}.tar"


# Mover creates a directory based on the given name (-n) and then moves the specified number of files into the directory
def Mover():
    dest = folder
    subprocess.run(['mkdir', dest])
    pattern = "*.cif"
    cif_files = []
    for filename in os.listdir('.'):
        if fnmatch.fnmatch(filename, pattern):
            cif_files.append(filename)
    for x in range(numfiles):
        j = random.choice(cif_files)
        try:
            shutil.move(j, dest)
        except:
            pass
        
# Create a folder for each cif and move the cif into folder
def MakeFolder():
    file_list = os.listdir('.')
    pattern = '*.cif'
    cif_files = []
    cif_directory = {}
    
    for filename in file_list:
        if fnmatch.fnmatch(filename, pattern):
            folder_name = filename.split('.cif')[0]
            cif_directory[folder_name] = filename

    for key in cif_directory:
        try:
            os.makedirs(key)
            shutil.move(cif_directory[key], key)
        except:
            pass

# Run FAPS on each directory to create the inputs for the GCMC simulations (see ~/.faps/fapsnosub.fap)
def CreateFaps():
    for i in os.listdir(os.getcwd()):
        os.chdir(i)
        subprocess.run(['faps', '-s', '-j', 'fapsnosub', i])
        os.chdir('..')

# Create the inputs, tar the directory, and clean up
def main():
    os.chdir('/home/jnoroozi/SCREENING/NotDone/functionalgroups')
    Mover()
    os.chdir(folder)
    MakeFolder()
    CreateFaps()
    os.chdir('..')
    shutil.move(folder, homedir)
    os.chdir(homedir)
    subprocess.run(['tar', '-cvhf', tar, folder])
    shutil.rmtree(folder)

if __name__ == "__main__":
    main()

