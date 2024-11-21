import os
import random
import time
import sys
import argparse
#holaa
import yaml
import Miscellaneus as MS
from colorama import Fore
from colorama import Style
from colorama import init
import subprocess
import warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

parser = argparse.ArgumentParser(
            prog='myprogram',
            description='''Universidad del Cauca - MINTIC Datos a la U''',
            epilog="""Soluciones Innovadoras con Datos Abiertos.""", allow_abbrev=False)
parser.add_argument('-s', '-S', metavar='\b', help='Guardar. Uso -s/S id_del_paciente diagnostico medicamentos control')
parser.add_argument('-c', '-C', metavar='\b', help='Consultar. Uso -c/C id_del_paciente')
parser.add_argument('-hi', '-HI', metavar='\b', help='Historia. Uso -hi/HI id_del_paciente')
parser.add_argument('-sispro', '-SISPRO', metavar='\b', help='IPS/EPS. Uso -sispro/SISPRO id_SISPRO nombre')
args = parser.parse_args()


def configfileload():
    with open("Config.yaml", "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
        MS.printed(message="CONFIGURATION FILE LOADED SUCCESSFULLY", colour=Fore.GREEN, style=Style.BRIGHT)

    MS.kup = data[0]['Details']['KeepUp']
    MS.fu.cctipo = data[0]['Details']['SmartContract']
    MS.SCFolder = data[0]['Details']['SCFolder']
    MS.fu.vrs = data[0]['Details']['Version']

if __name__ == "__main__":
    keys = ('diagnostico', 'medicamentos', 'control')
    datos = dict.fromkeys(keys)

    if "-s" in sys.argv[0] or "-S" in sys.argv[0]:
        configfileload()
        datos['diagnostico'] = sys.argv[2]
        datos['medicamentos'] = sys.argv[3]
        datos['control'] = sys.argv[4]
        MS.updatepatient(sys.argv[1], datos)

    elif "-c" in sys.argv[0] or "-C" in sys.argv[0]:
        configfileload()
        MS.patientconsult(sys.argv[1])

    elif "-hi" in sys.argv[0] or "-HI" in sys.argv[0]:
        configfileload()
        MS.patienhistory(sys.argv[1])

    elif "-sispro" in sys.argv[0] or "-SISPRO" in sys.argv[0]:
        configfileload()
        MS.addIEPS(sys.argv[1], sys.argv[2])

    elif "" in sys.argv[0] or "-h" in sys.argv[0] or "--help" in sys.argv[0]:
        parser.print_help()

