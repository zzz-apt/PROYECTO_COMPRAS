import sys
import time
from FUNCIONES import Cierre_Programa
from FUNCIONES import Estadisticas
from datetime import datetime
import requests
import threading
import subprocess

from apscheduler.schedulers.blocking import BlockingScheduler


import requests
import json


from colorama import init, Fore, Back, Style
init()

def Telegram(MSG):
    token = "8167604613:AAFPFgIwMbZFBpnz4hO4p9FzK1-n52VSIIs"
    chat_id = "6231499420"
    mensaje = MSG
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": mensaje
    }

    response = requests.post(url, data=payload)
    #print(response.json())


X = {
     
     'fer' : False,
     'shary' : False,
     'naty' : False,
}

def BCV():
    respuesta = requests.get('https://api.dolarvzla.com/public/exchange-rate')
    datos = respuesta.json()
    tasas = datos['current']
    Tasa_bcv = tasas['usd']
    print(f'Actualmente la tasa BCV se encuentra en {Tasa_bcv} Bolivares')

def Intervenciones():
    respuesta = requests.get('https://api.dolarvzla.com/public/interventions')
    datos = respuesta.json()
    Intervenciones = datos['interventions']
    fecha = Intervenciones[0]
    fecha2 = fecha['date']

def cuenta_regresiva(MIN):
        
        tiempo_total_segundos = MIN*60
        # Itera desde el tiempo total de segundos hasta 0 (excluido)
        for segundos_restantes in range(tiempo_total_segundos, 0, -1):
            
            # 1. Calcular el formato MM:SS
            minutos = segundos_restantes // 60
            segundos = segundos_restantes % 60
            
            # Formatear el tiempo a MM:SS con ceros a la izquierda
            tiempo_formato = f"{minutos:02}:{segundos:02}"
            
            # 2. Mostrar y actualizar la línea
            # El caracter '\r' regresa el cursor al inicio de la línea.
            sys.stdout.write(f"\rCiclo de espera: {tiempo_formato}")
            
            # Asegura que el texto se muestre inmediatamente en la consola
            sys.stdout.flush() 
            
            # 3. Pausa de 1 segundo
            time.sleep(1) 
        
        # Finalización del contador
        # Borra la línea de conteo y muestra el mensaje final
        sys.stdout.write("\r" + " " * 30 + "\r") # Borra la línea
        sys.stdout.flush()
        print("Ciclo de espera terminado")

def temporizador():
    global temporizador_activo
    global tiempo_transcurrido
    
    

    if temporizador_activo:
        # with tiempo_lock:
            tiempo_total_segundos = 15*60
            for segundos_restantes in range(tiempo_total_segundos, 0, -1):
                minutos = segundos_restantes // 60
                segundos = segundos_restantes % 60
                

                tiempo_formato = f"{minutos:02}:{segundos:02}"

                
                global tiempo_transcurrido
                tiempo_transcurrido = tiempo_formato
                time.sleep(1) 
                

            tiempo_transcurrido = '00:00'

            temporizador_activo = False
            
            

            # Opcional: imprimir algo en consola para saber que sigue vivo
            # print(f"Contando... {tiempo_transcurrido}s")    
    
def iniciar_temporizador():
    """Inicia el hilo del temporizador."""
    global temporizador_activo, tiempo_transcurrido
    
    if not temporizador_activo:
        # Resetear el tiempo y activar la bandera
        tiempo_transcurrido = 0
        temporizador_activo = True
        
        # Crear y lanzar el hilo
        t = threading.Thread(target=temporizador)
        t.start()
        
    else:
        print("El temporizador ya está corriendo.")
    
def menu():
    
    print(
    f'''{Fore.GREEN}
    |0| Salir del Programa
    |1| Iniciar Programa
    |2| Tasa bcv
    |3| Ultima Intervencion Anunciada
    |4| Horario Del Mercado
    |5| Tiempo para Próxima Compra
    
    ''')
    
    while True:
        try:
            R = int(input(f'{Fore.YELLOW}ingrese opción: {Style.RESET_ALL} '))
            if R == 0:
                Cierre_Programa()
                exit()
            if R == 1:
                global scheduler
                print(Fore.YELLOW + '______________ INICIANDO ______________ ' + Style.RESET_ALL)
                subprocess.call('start cmd /k python FERNANDO.py', shell=True)
                subprocess.call('start cmd /k python Sharynnel.py', shell=True)
                subprocess.call('start cmd /k python Nathalia.py', shell=True)

            if R == 2:  
                BCV()
            if R == 3:
                Intervenciones()

            if R == 4:
                if Estadisticas['horario'] == []:
                    Estadisticas['horario'] = 0
                    Estadisticas['metodos'] = 0
                Telegram(f'''---- LAS COMPRAS HAN CERRADO ---- 
Horas que estuvieron abiertas las compras: {Estadisticas["horario"]} 
Metodos de compra que estuvieron disponibles: {Estadisticas["metodos"]}
Intentos Realizados: {Estadisticas["intentos"]}''')     
            if R == 5:
                print(tiempo_transcurrido)
            else:
                None
        except:
            None



     
titulo = '''

 ██████╗ ██╗   ██╗ █████╗ ███████╗██╗   ██╗███╗   ███╗██╗
██╔═══██╗╚██╗ ██╔╝██╔══██╗██╔════╝██║   ██║████╗ ████║██║
██║   ██║ ╚████╔╝ ███████║███████╗██║   ██║██╔████╔██║██║
██║   ██║  ╚██╔╝  ██╔══██║╚════██║██║   ██║██║╚██╔╝██║██║
╚██████╔╝   ██║   ██║  ██║███████║╚██████╔╝██║ ╚═╝ ██║██║
 ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝'''
logo = '''                                                                       
_______________________________________________________________________________________________________________________________________'''
hora = int(datetime.now().hour)
minuto = int(datetime.now().minute)
tiempo_transcurrido = f'{Fore.RED}Programa no Iniciado{Style.RESET_ALL}'


# scheduler = BlockingScheduler()
# scheduler.add_job(fer, 'interval', minutes=15)

#//////////////////////////////////////////////////////

print(Fore.GREEN + logo + titulo  + Style.RESET_ALL)
print(Fore.GREEN + '''________________________________________________________________________________________________________________________________________
       ''' + Style.RESET_ALL)

menu()




'''
while True:
    print(Fore.YELLOW + '______________ INICIANDO ______________ ' + Style.RESET_ALL)
    fer()
    cuenta_regresiva(15)

'''