import asyncio
from FUNCIONES import *
from funciones_app import ejecutarCicloCuentas
from colorama import Fore, Style, init

init()

if __name__ == '__main__':
    print(Fore.RED, Fore.LIGHTWHITE_EX, '\n -------- INICIANDO COMPRAS --------', Style.RESET_ALL)
    try:
        asyncio.run(ejecutarCicloCuentas())
    except KeyboardInterrupt:
        print("\n SISTEMA INTERRUMPIDO POR EL USUARIO. cerrando...")