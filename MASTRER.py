from FUNCIONES import *
# from funciones_app import *
from cuentas import CUENTAS
import schedule
import time
from datetime import datetime
from colorama import Fore, Style, init

init()


# --- BUCLE PRINCIPAL ---
ahora = datetime.now()
horaActual = ahora.hour

# MODO MADRUGADITA
if horaActual <= 5 or horaActual >= 22:

    print(Fore.CYAN + 'Modo Madrugadita Activo (06:04/06:05)' + Style.RESET_ALL)

    schedule.every().day.at("06:04").do(ejecutarCicloCuentas)
    while True:
        schedule.run_pending()
        time.sleep(1)
# HORARIO NORMAL
else:
    ejecutarCicloCuentas()

       