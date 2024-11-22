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

deliveredReg = 0
badTransaction = 0
SCFolder = ""
BCFolder = ""
FTPdir = ""
FTPName = ""
FTPPass = ""
# a_host = ftputil.FTPHost('93.188.167.110', 'dulcesFTP', 'UsuarioDulces')
sensors = []
var1 = ""
var2 = ""
var3 = ""


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
    printed(message="TRANSFERRING THE CHAINCODE TO THE BLOCKCHAIN INSTALLATION FOLDER",
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
    return file


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


def errorprint(process):
    for item in process.split("\n"):
        if "Error:" in item:
            printed(message=item.strip(), colour=Fore.RED, style=Style.BRIGHT)


def hypertx(command):
    process, error = subprocess.Popen(
        command, universal_newlines=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    if process.find('failed=0') == -1:
        errorprint(process)
        return 0
    else:
        return 1


def updatePatient(id, newData):
    cmd = "\"updatePatient\",\"{id}\",\"{newData}\""
    command = ["minifab.cmd", "invoke", "-n", fu.cctipo, "-p", cmd]
    if hypertx(command) == 0:
        #printed(message="ERROR! SMART CONTRACT NOT WORKING PROPERLY", colour=Fore.RED, style=Style.BRIGHT)
        sys.exit()
    else:
        printed(message="PATIENT DATA UPDATED SUCCESSFULLY", colour=Fore.GREEN, style=Style.BRIGHT)


def registerIPS(id, name):
    cmd = "\"registerIPS\",\"" + id + "\",\"" + name + "\""
    command = ["minifab.cmd", "invoke", "-n", fu.cctipo, "-p", cmd]
    if hypertx(command) == 0:
        #printed(message="ERROR! SMART CONTRACT NOT WORKING PROPERLY", colour=Fore.RED, style=Style.BRIGHT)
        sys.exit()
    else:
        printed(message="IPS REGISTERED SUCCESSFULLY", colour=Fore.GREEN, style=Style.BRIGHT)



def getPatientHistory(id):
    path = os.getcwd()
    folder = os.path.join(path, f"Patient_{id}_history")
    if not os.path.isdir(folder):
        os.makedirs(folder)
    printed(message="FETCHING PATIENT HISTORY, PLEASE WAIT...", colour=Fore.CYAN, style=Style.BRIGHT)
    
    cmd = f"\"getPatientHistory\",\"{id}\""
    command = ["minifab.cmd", "invoke", "-n", fu.cctipo, "-p", cmd]
    process, error = subprocess.Popen(
        command, universal_newlines=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    filename = os.path.join(folder, f"Patient_History_ID_{id}.txt")
    with open(filename, "w") as file:
        file.writelines(process)
    
    printed(message="PATIENT HISTORY SAVED SUCCESSFULLY", colour=Fore.GREEN, style=Style.BRIGHT)


def queryPatient(id):
    path = os.getcwd()
    folder = os.path.join(path, f"Patient_{id}_latest")
    if not os.path.isdir(folder):
        os.makedirs(folder)
    printed(message="FETCHING PATIENT DATA, PLEASE WAIT...", colour=Fore.CYAN, style=Style.BRIGHT)

    cmd = f"\"queryPatient\",\"{id}\""
    command = ["minifab.cmd", "invoke", "-n", fu.cctipo, "-p", cmd]
    process, error = subprocess.Popen(
        command, universal_newlines=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    filename = os.path.join(folder, f"Patient_ID_{id}.txt")
    with open(filename, "w") as file:
        file.writelines(process)
    
    printed(message="PATIENT DATA SAVED SUCCESSFULLY", colour=Fore.GREEN, style=Style.BRIGHT)

def registerPatient(id, name, ipsID):
    cmd = f"\"registerPatient\",\"{id}\",\"{name}\",\"{ipsID}\""
    command = ["minifab.cmd", "invoke", "-n", fu.cctipo, "-p", cmd]
    if hypertx(command) == 0:
        #printed(message="ERROR! SMART CONTRACT NOT WORKING PROPERLY", colour=Fore.RED, style=Style.BRIGHT)
        sys.exit()
    else:
        printed(message="PATIENT REGISTERED SUCCESSFULLY", colour=Fore.GREEN, style=Style.BRIGHT)


def writelatest(chaincode, var, folder):
    cmd = "\"latest\",\"" + var + "\""
    command = ["minifab.cmd", "invoke", "-n", chaincode, "-p", cmd]
    process, error = subprocess.Popen(
        command, universal_newlines=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    errorprint(process)
    filename = folder + '\\Patient_ID_' + var + '.txt'
    file = open(filename, "w")
    file.writelines(process)
    file.close()


def writehisyory2(chaincode, var, folder):
    cmd = "\"history\",\"" + var + "\""
    command = ["minifab.cmd", "invoke", "-n", chaincode, "-p", cmd]
    process, error = subprocess.Popen(
        command, universal_newlines=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    errorprint(process)
    filename = folder + '\\Patient_History_ID_' + var + '.txt'
    file = open(filename, "w")
    file.writelines(process)
    file.close()