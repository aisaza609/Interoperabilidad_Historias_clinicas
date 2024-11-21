import os
import sys
import argparse
import yaml
from colorama import Fore, Style
import Miscellaneus as MS

def load_config():
    """Carga las configuraciones desde Config.yaml"""
    try:
        with open("Config.yaml", "r") as yamlfile:
            data = yaml.load(yamlfile, Loader=yaml.FullLoader)
            MS.printed(message="CONFIGURATION FILE LOADED SUCCESSFULLY", colour=Fore.GREEN, style=Style.BRIGHT)
            print(MS.__file__)
            return data[0]['Details']
    except FileNotFoundError:
        MS.printed(message="CONFIG FILE NOT FOUND!", colour=Fore.RED, style=Style.BRIGHT)
        sys.exit(1)
    except yaml.YAMLError as exc:
        MS.printed(message=f"ERROR IN CONFIG FILE: {exc}", colour=Fore.RED, style=Style.BRIGHT)
        sys.exit(1)

def main():
    """Punto de entrada principal del script"""
    # Definimos los argumentos CLI disponibles
    parser = argparse.ArgumentParser(
        prog='SentTransaction',
        description='''Universidad del Cauca - MINTIC Datos a la U''',
        epilog="""Soluciones Innovadoras con Datos Abiertos."""
    )
    parser.add_argument('-rp', metavar=('\b', '\b', '\b'), nargs=3, help='Registrar paciente. Uso: -rp id_paciente nombre id_ips')
    parser.add_argument('-c', metavar='\b', help='Consultar. Uso: -c id_paciente')
    parser.add_argument('-hi', metavar='\b', help='Historial. Uso: -hi id_paciente')
    parser.add_argument('-sispro', metavar=('\b', '\b'), nargs=2, help='Registrar IPS/EPS. Uso: -sispro id nombre')
    args = parser.parse_args()

    # Cargamos configuraciones
    config = load_config()

    # Lógica basada en los argumentos
    if args.rp:
        try:
            MS.registerPatient(args.rp[0], args.rp[1], args.rp[2])
        except Exception as e:
            MS.printed(message=f"ERROR REGISTERING PATIENT: {e}", colour=Fore.RED, style=Style.BRIGHT)
            sys.exit(1)

    elif args.c:
        try:
            MS.queryPatient(args.c)
        except Exception as e:
            MS.printed(message=f"ERROR QUERYING PATIENT: {e}", colour=Fore.RED, style=Style.BRIGHT)
            sys.exit(1)

    elif args.hi:
        try:
            MS.getPatientHistory(args.hi)
        except Exception as e:
            MS.printed(message=f"ERROR FETCHING PATIENT HISTORY: {e}", colour=Fore.RED, style=Style.BRIGHT)
            sys.exit(1)

    elif args.sispro:
        try:
            MS.registerIPS(args.sispro[0], args.sispro[1])
        except Exception as e:
            MS.printed(message=f"ERROR REGISTERING IPS: {e}", colour=Fore.RED, style=Style.BRIGHT)
            sys.exit(1)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
