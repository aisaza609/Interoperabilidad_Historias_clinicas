import os
import re
import time
from os.path import exists

import ftputil
import csv
import sys
import glob
import subprocess
import psutil
import errno, stat, shutil
import pandas as pd
import numpy as np
import FabricUp as fu
from datetime import datetime
from colorama import Fore
from colorama import Style
from scipy.stats import zscore
from os import listdir
from tqdm import tqdm
tqdm.pandas()
import warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

SCFolder = ""
BCFolder = ""
# a_host = ftputil.FTPHost('93.188.167.110', 'dulcesFTP', 'UsuarioDulces')
sensors = []
var1 = ""
var2 = ""
var3 = ""
SmartContractGO = ""

bar = [
    "[=       ]",
    "[===     ]",
    "[====    ]",
    "[=====   ]",
    "[======  ]",
    "[======= ]",
    "[========]",
    "[ =======]",
    "[  ======]",
    "[   =====]",
    "[    ====]",
    "[     ===]",
    "[      ==]",
    "[       =]"
]
i = 0
kup = ""


def deploychaincode():
    printed(message="TRANSFERRING THE CHAINCODES TO THE BLOCKCHAIN INSTALLATION FOLDER",
                colour=Fore.LIGHTWHITE_EX, style=Style.BRIGHT)
    fu.copytree(SCFolder, BCFolder)
    chaincodefolder(new=True)
    fu.copytree(SCFolder, os.getcwd() + "\\chaincode")
    fu.installchaincodes(version=fu.vrs)


def chaincodefolder(new):
    if not os.path.isdir(os.getcwd() + "\\chaincode"):
        os.makedirs(os.getcwd() + "\\chaincode")
    else:
        shutil.rmtree(os.getcwd() + "\\chaincode",
                       onerror=lambda func, path, _: (os.chmod(path, stat.S_IWRITE), func(path)))
        os.makedirs(os.getcwd() + "\\chaincode")

    if not os.path.isdir(os.getcwd() + "\\chaincodeOld"):
        os.makedirs(os.getcwd() + "\\chaincodeOld")
    elif new:
        shutil.rmtree(os.getcwd() + "\\chaincodeOld",
                       onerror=lambda func, path, _: (os.chmod(path, stat.S_IWRITE), func(path)))
        os.makedirs(os.getcwd() + "\\chaincodeOld")


def lineupdater(file):
    max_length = 0
    max_len_line = ""
    for line in file:
        if len(line) > max_length:
            max_length = len(line)
            max_len_line = line
            index = max_len_line.find("payload")
            if index != -1:
                max_len_line = max_len_line[index:]
                max_len_line = max_len_line.replace('\\"', '')
                max_len_line = max_len_line.replace('Value', '')
                max_len_line = max_len_line.replace('[', '')
                max_len_line = max_len_line.replace('\\:', '')
                max_len_line = max_len_line.replace('payload:"', '')
                max_len_line = max_len_line.replace('Value', '')
                max_len_line = max_len_line.replace('\\', '')
                max_len_line = max_len_line.replace(']" \']0m', '')
                max_len_line = max_len_line.replace('}', '')
                max_len_line = max_len_line.replace('E', 'e')
                max_len_line = max_len_line.replace(',', ';')
    return max_len_line


def fileUpdate(Path):
    filenames = listdir(Path)
    for filename in filenames:
        filename = Path + "\\" + filename
        file = open(filename, "r")
        data = file.readlines()
        file.close()
        filename = filename.replace('.txt', '.csv')
        file = open(filename, "w")
        file.write(lineupdater(data))
        file.close()


def fileloader(Path):
    filelist = []
    filenames = listdir(Path)
    for filename in filenames:
        filename = Path + "\\" + filename
        file = open(filename, "r")
        data = file.readlines()
        file.close()
        if ".csv" in filename:
            filelist.append(filename)
        file = open(filename, "w")
        for line in data:
            file.write(line.replace(';', '\n'))
        file.close()
    return filelist


def dataframeLoader(Path):
    filenames = listdir(Path)
    filelist = []
    for idx, item in enumerate(filenames):
        filenames[idx] = Path + "\\" + item
        if ".csv" in filenames[idx]:
            filelist.append(filenames[idx])
    colnames = ['Data']
    df_list = [pd.read_csv(file, sep=';', names=colnames,
                            decimal='.', index_col=False, header=None) for file in filelist]
    # print("\n", len(df_list), "files were loaded\n")

    return df_list


def zeroadd(number):
    if number < 10:
        return "0" + str(number)
    else:
        return str(number)


def printed(message, colour, style):
    myobj = datetime.now()
    mytime = "[" + zeroadd(int(myobj.hour)) + ":" + zeroadd(int(myobj.minute)) + ":" + zeroadd(
        int(myobj.second)) + "] "
    print(mytime + colour + style + message + Style.RESET_ALL)


def buf_count_newlines_gen(fname):
    def _make_gen(reader):
        while True:
            b = reader(2 ** 16)
            if not b: break
            yield b

    with open(fname, "rb") as f:
        count = sum(buf.count(b"\n") for buf in _make_gen(f.raw.read))
    return count


def process_exists(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def checkmod(fileName, oldTime):
    newTime = int(os.path.getmtime(fileName))
    if newTime != oldTime:
        return False, newTime
    else:
        return True, oldTime


def closeProgram():
    if kup.lower() != "keepup":
        fu.clean()
    printed(message="DONE, GOOD BYE!", colour=Fore.YELLOW, style=Style.BRIGHT)
    sys.exit()


def hypertx(command):
    process, error = subprocess.Popen(
        command, universal_newlines=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if process.find('failed=0') == -1:
        return 0
    else:
        return 1


def transaction():
    fileList = []
    prList = []
    rdList = []
    rd = True

    if os.path.exists(os.getcwd() + "\\" + 'ProcessedFiles.txt'):
        with open(os.getcwd() + "\\" + 'ProcessedFiles.txt') as f:
            prList = f.readlines()
    else:
        rd = False

    a_host = ftputil.FTPHost(FTPdir, FTPName, FTPPass)

    for (dirname, subdirs, files) in a_host.walk("/home/dulcesFTP"):  # directory
        for f in files:
            if f.endswith('csv'):
                fileList.append(f)

    for i in range(len(fileList)):
        printed(message="PROCESSING FILE " + str(i + 1) + " OUT OF " +
                         str(len(fileList)) + " / FILE: " + fileList[i], colour=Fore.MAGENTA, style=Style.BRIGHT)
        if rd == True and fileList[i] not in prList:
            rdata(fileList[i])
            rdList.append(fileList[i])
        elif not rd:
            rdata(fileList[i])
            rdList.append(fileList[i])

    with open('ProcessedFiles.txt', 'a') as f:
        for item in rdList:
            f.write("%s\n" % item)

    fileList.clear()
    prList.clear()
    rdList.clear()


def sentTx(row):
    scvar1 = "Sensor_" + str(row['SensorId']) + "_date"
    scvar2 = "Sensor_" + str(row['SensorId']) + "_temp"
    scvar3 = "Sensor_" + str(row['SensorId']) + "_rh"
    cmd = "\"invoke\",\"" + scvar1 + "\"" + ",\"" + str(
        row['Time']) + "\"," + "\"" + scvar2 + "\"" + ",\"" + str(
        row['Temperature']) + "\"," + "\"" + scvar3 + "\"" + ",\"" + str(row['Humidity']) + "\""
    command = ["minifab.cmd", "invoke", "-n", fu.cctipo, "-p", cmd]
    if hypertx(command) == 0:
        printed(message="ERROR! SMART CONTRACT NOT WORKING PROPERLY", colour=Fore.RED, style=Style.BRIGHT)
        sys.exit()



def find_csv_filenames(path_to_dir, suffix=".csv"):
    filenames = listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]


def loaddata():
    directory = os.getcwd()
    filenames = find_csv_filenames(directory)
    datasets = (pd.read_csv(file) for file in filenames)
    return filenames, datasets


def uniq(lista):
    x = np.array(lista)
    sensorlist = np.unique(x)
    return sensorlist.tolist()