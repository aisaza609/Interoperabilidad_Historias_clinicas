import os
import subprocess
import shutil
import sys

import Miscellaneus as MS
from colorama import Fore
from colorama import Style
from zipfile import ZipFile
from os.path import basename
import warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

cctipo = ""
vrs = 1.0

def clean():
    cleanup()


def zipSC(directory, dirName, name):
    shutil.make_archive(directory+"\\"+name, 'zip', dirName)


def consolExec(command, verbose = True):
    process, error = subprocess.Popen(
        command, universal_newlines=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if verbose:
        if process.find('failed=0') == -1:
            MS.printed(message="FAILED", colour=Fore.RED, style=Style.BRIGHT)
            MS.printed(message=process, colour=Fore.RED, style=Style.BRIGHT)
            sys.exit()
        else:
            MS.printed(message="SUCCESSFULL", colour=Fore.GREEN, style=Style.BRIGHT)
            # sys.stdout.write("... DONE")
 

def consolExec2(command):
    process, error = subprocess.Popen(
        command, universal_newlines=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()


def deploybcnet():
    MS.printed(message="DEPLOYING THE NETWORK", colour=Fore.LIGHTWHITE_EX, style=Style.BRIGHT)
    command = ["minifab.cmd", "up", "-e", "true"]
    consolExec(command)

    MS.printed(message="CREATING THE TEST CHANNEL", colour=Fore.LIGHTWHITE_EX, style=Style.BRIGHT)
    command = ["minifab.cmd", "create", "-c", "testchannel"]
    consolExec(command)

    MS.printed(message="JOINING TO THE TEST CHANNEL", colour=Fore.LIGHTWHITE_EX, style=Style.BRIGHT)
    command = ["minifab.cmd", "join"]
    consolExec(command)

    MS.printed(message="PERFORMING CHANNEL QUERY", colour=Fore.LIGHTWHITE_EX, style=Style.BRIGHT)
    command = ["minifab.cmd", "channelquery"]
    consolExec(command)

    editjsonfile()
    MS.printed(message="PERFORMING CHANNEL SIGN", colour=Fore.LIGHTWHITE_EX, style=Style.BRIGHT)
    command = ["minifab.cmd", "channelsign"]
    consolExec(command)

    MS.printed(message="PERFORMING CHANNEL UPDATE", colour=Fore.LIGHTWHITE_EX, style=Style.BRIGHT)
    command = ["minifab.cmd", "channelupdate"]
    consolExec(command)

    MS.printed(message="DEPLOYING HYPERLEDGER EXPLORER", colour=Fore.LIGHTWHITE_EX, style=Style.BRIGHT)
    command = ["minifab.cmd", "explorerup"]
    consolExec(command)

    ##MS.printed(message="DEPLOYING METRICS TOOLS USING PROMETHEUS", colour=Fore.LIGHTWHITE_EX, style=Style.BRIGHT)
    ##command = ["docker", "rm", "-f", "$(docker ps -a -q)"]
    ##consolExec(command, verbose=False)

    ##command = ["docker-compose", "-f", "docker-monitoring.yaml", "up", "-d"]
    ##consolExec(command, verbose=False)

    ##command = ["docker", "network", "connect", "mysite", "prometheus"]
    ##consolExec(command, verbose=False)
    
    MS.printed(message="DEPLOYMENT COMPLETED", colour=Fore.GREEN, style=Style.BRIGHT)


def editjsonfile():
    filename = os.path.dirname(os.path.realpath(__file__)) + '\\vars\\testchannel_config.json'
    file = open(filename, "r")
    data = file.readlines()
    file.close()
    file = open(filename, "w")
    for line in data:
        if "max_message_count" in line:
            line = line.replace("10", "50")
        elif "\"timeout\"" in line:
            line = line.replace("2s", "20s")
        file.write(line)
    file.close()


def discover():
    MS.printed(message="DISCOVERING THE INSTALLED CHAINCODE", colour=Fore.LIGHTWHITE_EX, style=Style.BRIGHT)
    command = ["minifab.cmd", "discover"]
    consolExec(command)


def installchaincodes(version):
    MS.printed(message="INSTALLING " + cctipo.upper() + " CHAINCODE", colour=Fore.LIGHTWHITE_EX, style=Style.BRIGHT)
    command = ["minifab.cmd", "install,approve,commit", "-n", cctipo, "-v", str(version), "-p", "\"init\""]
    consolExec(command)
    discover()

    MS.printed(message="INITIALIZING " + cctipo.upper() + " CHAINCODE", colour=Fore.LIGHTWHITE_EX, style=Style.BRIGHT)
    command = ["minifab.cmd", "initialize", "-n", cctipo, "-p", "\"init\""]
    consolExec(command)


def cleanup():
    MS.printed(message="CLEANING UP THE NETWORK", colour=Fore.LIGHTWHITE_EX, style=Style.BRIGHT)
    command = ["minifab.cmd", "cleanup"]
    consolExec(command)


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
