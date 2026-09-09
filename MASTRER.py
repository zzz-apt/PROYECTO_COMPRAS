from FUNCIONES import *
# from funciones_app import *
from cuentas import CUENTAS
import time
from datetime import datetime
from colorama import Fore, Style, init

init()


# --- BUCLE PRINCIPAL ---
ahora = datetime.now()
horaActual = ahora.hour
minutoActual = ahora.minute
modoMadrugadita = True 



if __name__ == '__main__':
    print(Fore.RED, Fore.LIGHTWHITE_EX, '\n -------- INICIANDO --------', Style.RESET_ALL )
    ejecutarCicloCuentas()