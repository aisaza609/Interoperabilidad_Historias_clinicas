import os
import sys
import random
import time

import yaml
import errno, stat, shutil
import Miscellaneus as MS
from colorama import Fore
from colorama import Style
from colorama import init
import subprocess
import warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
##andrea
init(convert=True)

def load_config():
    """Carga las configuraciones desde Config.yaml"""
    try:
        with open("Config.yaml", "r") as yamlfile:
            data = yaml.load(yamlfile, Loader=yaml.FullLoader)
            MS.printed(message="CONFIGURATION FILE LOADED SUCCESSFULLY", colour=Fore.GREEN, style=Style.BRIGHT)
        MS.kup = data[0]['Details']['KeepUp']
        MS.fu.cctipo = data[0]['Details']['SmartContract']
        MS.SCFolder = data[0]['Details']['SCFolder']
        MS.fu.vrs = data[0]['Details']['Version']
    except FileNotFoundError:
        MS.printed(message="CONFIG FILE NOT FOUND!", colour=Fore.RED, style=Style.BRIGHT)
        sys.exit(1)
    except yaml.YAMLError as exc:
        MS.printed(message=f"ERROR IN CONFIG FILE: {exc}", colour=Fore.RED, style=Style.BRIGHT)
        sys.exit(1)


load_config()

if MS.process_exists('Docker Desktop.exe'):
    MS.printed(message="DOCKER IS UP", colour=Fore.GREEN, style=Style.BRIGHT)
else:
    subprocess.Popen('C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe')
    MS.printed(message="OPENING UP DOCKER...", colour=Fore.LIGHTWHITE_EX, style=Style.BRIGHT)
    while not MS.process_exists('Docker Desktop.exe'):
        c = 1
    time.sleep(30)
    MS.printed("DOCKER IS UP", colour=Fore.GREEN, style=Style.BRIGHT)

if MS.kup.lower() == "keepup":
    MS.printed(message="THE BLOCKCHAIN NETWORK WILL NOT BE DELETED AT THE END OF THE PROCESS",
               colour=Fore.YELLOW, style=Style.BRIGHT)
else:
    MS.printed(message="THE BLOCKCHAIN NETWORK WILL BE DELETED AT THE END OF THE PROCESS",
               colour=Fore.YELLOW, style=Style.BRIGHT)

file1 = os.path.dirname(os.path.realpath(__file__)) + '\\vars\\chaincode\\' + MS.fu.cctipo
file2 = os.path.dirname(os.path.realpath(__file__)) + '\\vars\\chaincode'

random.seed(1)

MS.BCFolder = os.getcwd()+"\\vars\\chaincode"

if os.path.isdir(file2):
    if os.path.isdir(file1):
        MS.printed(message="BLOCKCHAIN NETWORK AND SMART CONTRACT SEEMS TO BE ALREADY DEPLOYED, SENDING TRANSACTIONS",
                   colour=Fore.GREEN, style=Style.BRIGHT)
        MS.chaincodefolder(new=False)
        MS.fu.copytree(MS.SCFolder, os.getcwd() + "\\chaincode")
    else:
        MS.printed(message="BLOCKCHAIN NETWORK SEEMS TO BE ALREADY DEPLOYED, INSTALLING CHAINCODE",
                   colour=Fore.LIGHTWHITE_EX, style=Style.BRIGHT)
        MS.deploychaincode()
else:
    MS.printed(message="BLOCKCHAIN NETWORK DO NOT SEEMS TO BE DEPLOYED", colour=Fore.YELLOW, style=Style.BRIGHT)
    MS.fu.deploybcnet()
    MS.deploychaincode()