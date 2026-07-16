from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
# import undetected_chromedriver as uc
from seleniumbase import Driver
from seleniumbase import SB
import urllib.request
import requests
from requests import get
import json
import random
import re
import time
from datetime import datetime
import cv2
from fake_useragent import UserAgent
import platform
from colorama import init, Fore, Back, Style
import sys
import os
import io
from io import BytesIO
import numpy as np
Tiempo = 60
rutaGlobal = r"C:\Users\medin\OneDrive\Documentos\ProyectosPython\mercantilDivisas\PROYECTO_COMPRAS" # Windows
# rutaGlobal = '/home/yako/Documentos/python/PROYECTO_COMPRAS' # Linux

rutaHistorial = rutaGlobal + r'/HISTORIAL'
rutaComprasExitosas = rutaHistorial + r'/COMPRAS_EXITOSAS'

init()


N1 = random.randint(1000, 1200)
N2 = random.randint(1000, 1200)
ErrorMD = False
Cerrado = False
MAX_WAIT_TIME = 10
US = ""


### CAMBIO DE CONFIGURACION SEGUN SISTEMA OPERATIVO y Kernel ###

if platform.system() != "Windows":
    print("[Bot] Ejecutando version linux32. Forzando modo Headless local...")
    modo_headless = True  
    modo_uc = False           
    version_driver = "system" 
    modoPls = "none"  

    # Agregamos flags críticos para optimizar RAM y evitar colapsos de pestañas
    argumentos_extra = (
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disk-cache-size=1",
        "--media-cache-size=1",
        "--disable-gpu",

        # --- ARGUMENTOS EXTREMOS (prueba) ---
        "--single-process",                 # Forza a Chromium a usar UN SOLO proceso (mata el 97% de CPU)
        "--disable-site-isolation-trials",  # Evita que aísle cada pestaña consumiendo más hilos
        "--user-data-dir=/dev/shm/chrome",  # Mueve el perfil temporal directo a la RAM (no lee disco duro)
        "--disk-cache-dir=/dev/shm/cache",  # Caché directo a la RAM
        "--disable-renderer-backgrounding", # Mantiene la prioridad de CPU al máximo en el login
        "--disable-background-timer-throttling",
        "--disable-component-update",        # No busca actualizaciones de Google al arrancar
        "--mute-audio",                      # Desactiva el módulo de sonido para ahorrar interrupciones}
        "--blink-settings=imagesEnabled=false",    # Bloquea la descarga de imágenes completamente
        "--disable-software-rasterizer",          # Evita que la CPU intente dibujar gráficos por software
        "--disable-extensions",                   # Desactiva cualquier extensión de fondo
        "--disable-features=AsmJsToWebAssembly",  # Desactiva traducciones pesadas de JS que ahogan CPUs viejas
        "--disable-features=WebAssembly",         # Corta scripts avanzados si el banco no los exige
        "--proxy-server=direct://",             # Salta la detección automática de proxies para conectar más rápido
        "--proxy-bypass-list=*",
        "--js-flags=--no-expose-wasm --max-semi-space-size=1 --max-old-space-size=256" # Limita la RAM interna de Javascript
    )
    os_binary_location = "/usr/bin/chromium"
else:
    print("Ejecutando en Windows")
    modo_headless = False 
    modo_uc = True            
    version_driver = "keep"
    modoPls = "none"
    argumentos_extra = (
        "--ignore-certificate-errors,--ignore-ssl-errors,--disable-web-security,"
        "--disable-remote-fonts,--enable-data-reduction-proxy-dev"
    )
    os_binary_location = None 

##########################################################################################

driver = Driver(
    undetectable=modo_uc,     
    uc=modo_uc,               
    block_images=True,
    window_size=f"{N1},{N2}",  
    headless1=modo_headless,  
    chromium_arg=argumentos_extra, 
    binary_location=os_binary_location, 
    disable_csp=True,       
    incognito=True,       
    mobile=False,
    pls=modoPls,
    driver_version=version_driver  # ("system" en Linux, "keep" en Windows)
)


# driver = Driver(
#     undetectable=True,
#     uc=True,                # Activa undetected-chromedriver    
#     block_images=True,
#     window_size= f"{N1},{N2}",  
#     headless1=False, # INTERFAZ
#     chromium_arg="--ignore-certificate-errors,--ignore-ssl-errors,--disable-web-security, --disable-remote-fonts, --enable-data-reduction-proxy-dev",
#     disable_csp=True,       # políticas de seguridad
#     incognito=True,       
#     # disable_cookies=True, # Se cuelga
#     mobile=True,
#     pls="eager",
#     #user_data_dir="./cache",
#     #ad_block=True,
#     driver_version="keep",
# )

wait = WebDriverWait(driver, MAX_WAIT_TIME)

from funciones_app import *

Estadisticas = {

    'formulario' : 0,
    'metodos' : [],
    'horarios' : []

}

ip=None
US=None




def cuenta_regresiva(MIN):
        
        tiempo_total_segundos = MIN
        for segundos_restantes in range(tiempo_total_segundos, 0, -1):

            minutos = segundos_restantes // 60
            segundos = segundos_restantes % 60
            
            tiempo_formato = f"{minutos:02}:{segundos:02}"
            sys.stdout.write(f"\rCiclo de espera: {tiempo_formato}")
            
            sys.stdout.flush() 
            time.sleep(1) 

        sys.stdout.write("\r" + " " * 30 + "\r")
        sys.stdout.flush()

def inicio_sesion(Inicio):
    # Cambiar el User Agent para la siguiente petición PUEDE QUE AYUDE A MEJORAR LAS COMPRAS
    global ip, US
    US = UserAgent().random
    ip = IP()
    

    print(f'{Fore.YELLOW} IP: {Fore.RED} {IP()}  {Style.RESET_ALL}')
    print(f'{Fore.YELLOW} Ejecutando navegador con Agente: {Style.RESET_ALL} {US} ')
    
    
    driver.execute_cdp_cmd('Network.clearBrowserCookies', {})
    driver.execute_cdp_cmd('Network.clearBrowserCache', {})
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": US
    })

    
    driver.refresh()
    driver.get("about:blank") 
  
    # driver.execute_cdp_cmd("Network.enable", {})


    # driver.execute_cdp_cmd(
    #     "Network.setBlockedURLs",
    #     {
    #         "urls": [
    #             "*.png",
    #             "*.jpg",
    #             "*.jpeg",
    #             "*.gif",
    #             "*.svg",
    #             "*.ico",  
    #             "*.woff",
    #             "*.woff2",
    #             "*.ttf",  
    #             "*google-analytics*",
    #             "*gtm.js*", 
    #         ]
    #     },
    # )
    driver.get("https://www30.mercantilbanco.com/login")
    driver.execute_script("document.body.style.zoom='50%'")

    
    
    # driver.execute_script(
    # """
    # document.querySelectorAll('style, link[rel="stylesheet"]').forEach(el => el.remove());
    # document.body.classList.add('no-animations');
    # """
    # )

    
   

        
   

    try:
        if escribir("#username", Inicio['usuario']) == False:
            return False
        escribir("#password", Inicio['contrasena'])
        hacerClick(".button-wrapper__btn-primary")
    except:
        print('no se encontro el objeto para ingresar el usuario')
        try:
            driver.get("https://www30.mercantilbanco.com/login")
        except:
            print("no se pudo acceder al sitio")
        escribir("#username", Inicio['usuario'])
        escribir("#password", Inicio['contrasena'])
        hacerClick(".button-wrapper__btn-primary")
        return

    try:
        if wait.until(EC.presence_of_elements_located((By.XPATH, '//*[@id="system-error"]/div/div[1]/div[1]'))).text == 'El tiempo de tu sesión ha finalizado.':
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="system-error"]/div/div[1]/div[3]/button'))).click()
    except:
        None   
    driver.execute_script(
        """
        let style = document.createElement('style');
        style.id = 'kill-animations';
        style.innerHTML = `
            *, *::before, *::after,
            .mat-checkbox-frame, .mat-checkbox-background,
            .mat-ripple-element, .mat-select-panel, .mat-option {
                transition: none !important;
                animation: none !important;
                transition-duration: 0s !important;
                animation-duration: 0s !important;
                animation-delay: 0s !important;
                transform: none !important;
            }
            .mat-ripple-element {
                display: none !important;
            }
        `;
        document.head.appendChild(style);
    """
    )
   
    

def ResolverPreguntasSeguridad(Preguntas):

    try:
    
        try:

            seleccionarElemento("#mat-input-3") #verificando si esta en la pantalla de Preguntas de seguridad, si no esta, se va al except y se salta esta parte

            if Preguntas['PreguntaUnica'] == True:
                escribir("#mat-input-3", Preguntas['RespuestaUnica'])
                escribir("#mat-input-2", Preguntas['RespuestaUnica'])

            else:

                ########## PREGUNTA 1 ##########################
                if WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, 'question-1'))).text == Preguntas['pregunta1']:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mat-input-2"))).send_keys(Preguntas['respuesta1'])
                    

                if wait.until(EC.presence_of_element_located((By.ID, 'question-1'))).text == Preguntas['pregunta2']:
                    wait.until(EC.presence_of_element_located((By.ID, "mat-input-2"))).send_keys(Preguntas['respuesta2'])
                    
                            
                if wait.until(EC.presence_of_element_located((By.ID, 'question-1'))).text == Preguntas['pregunta3']:
                    wait.until(EC.presence_of_element_located((By.ID, "mat-input-2"))).send_keys(Preguntas['respuesta3'])
                    
                
                if wait.until(EC.presence_of_element_located((By.ID, 'question-1'))).text == Preguntas['pregunta4']:
                    wait.until(EC.presence_of_element_located((By.ID, "mat-input-2"))).send_keys(Preguntas['respuesta4'])
                    

                if wait.until(EC.presence_of_element_located((By.ID, 'question-1'))).text == Preguntas['pregunta5']:
                    wait.until(EC.presence_of_element_located((By.ID, "mat-input-2"))).send_keys(Preguntas['respuesta5'])
                    


                ########## PREGUNTA 2 ###############################
                if wait.until(EC.presence_of_element_located((By.ID, 'question-2'))).text == Preguntas['pregunta1']:
                    wait.until(EC.presence_of_element_located((By.ID, "mat-input-3"))).send_keys(Preguntas['respuesta1'])

                if wait.until(EC.presence_of_element_located((By.ID, 'question-2'))).text == Preguntas['pregunta2']:
                    wait.until(EC.presence_of_element_located((By.ID, "mat-input-3"))).send_keys(Preguntas['respuesta2'])
                            
                if wait.until(EC.presence_of_element_located((By.ID, 'question-2'))).text == Preguntas['pregunta3']:
                    wait.until(EC.presence_of_element_located((By.ID, "mat-input-3"))).send_keys(Preguntas['respuesta3'])
                
                if wait.until(EC.presence_of_element_located((By.ID, 'question-2'))).text == Preguntas['pregunta4']:
                    wait.until(EC.presence_of_element_located((By.ID, "mat-input-3"))).send_keys(Preguntas['respuesta4'])

                if wait.until(EC.presence_of_element_located((By.ID, 'question-2'))).text == Preguntas['pregunta5']:
                    wait.until(EC.presence_of_element_located((By.ID, "mat-input-3"))).send_keys(Preguntas['respuesta5'])

        except:
            print('no encontro el elemento')
            VerMensaje()
            return False
     
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/app/melp-standard-layout/div/div/melp-secure-access/melp-standard-card-layout/div/div/div[1]/div/div/melp-connection-type/form/div/div[2]"))).click()

    except:
        print('hubo un problema ingresando las preguntas de seguridad')

def txt(mensaje):
    try:
        with open(rf'{rutaHistorial}/{datetime.now().date()}.txt', 'a', encoding='utf-8') as archivo:
            archivo.write(f'\n{mensaje}\n')
    except Exception as e:
        print(f'error al escribir el archivo: {e}')

def excluir(usuario):
    with open(rf'{rutaGlobal}/usuariosListos.txt', "a", encoding="utf-8") as f:
        f.write(f"{usuario}\n")
        print(f"✅ {usuario} ha sido guardado en la base de datos y será excluido.")

def check(usuario):
  
    try:
        with open(rf'{rutaGlobal}/usuariosListos.txt', "r", encoding="utf-8") as f:
            excluidos = [linea.strip() for linea in f.readlines()]
            return usuario in excluidos
    except FileNotFoundError:
        return False
    
def Cierre_Programa():
    global driver
    print('cerrando programa')
    driver.quit()
    exit()

def img(Datos):

    png_bytes = driver.get_screenshot_as_png()

    # 2. bytes a formato de opencv
    nparr = np.frombuffer(png_bytes, np.uint8)
    imagen_cv2 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # aqui esta parte es para recortar la imagen, pero mientras las pruebas la dejo como esta (captura completa) 
    # el formato es [Y_inicio:Y_fin, X_inicio:X_fin] Ejemplo: [100:300, 150:650] 
    imagen_recortada = imagen_cv2  

    # bytes para Telegram
    is_success, buffer = cv2.imencode(".png", imagen_recortada)
    imagen_en_bytes = buffer.tobytes()

    # aqui envia la imagen a telegram sin guardarla localmente
    TOKEN = "8167604613:AAFPFgIwMbZFBpnz4hO4p9FzK1-n52VSIIs"
    TEXTO_DESCRIPCION = f'💲 Compra Exitosa 💲'
    TEXTO_DESCRIPCION_ADMIN = f'💲 Compra Exitosa 💲 con {Datos["nombre"]}'
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    fer = "6231499420"
    ray = "7781699329"

    payloadfer = {"chat_id": fer, "caption": f'💲 Compra Exitosa 💲 con {Datos["nombre"]}'}
    payloadray = {"chat_id": ray, "caption": f'💲 Compra Exitosa 💲 con {Datos["nombre"]}'}
    payload_User = {"chat_id": Datos["CHAT_ID"], "caption": f'💲 Compra Exitosa 💲'}

    files = {
        "photo": ("captura.png", io.BytesIO(imagen_en_bytes), "image/png")
    }

    # Realizamos los envios
    if not Datos["CHAT_ID"] == fer:
        try:
            response = requests.post(url, data=payloadfer, files=files)
            print(f"Enviado a Fer: {response.json()}")
        except Exception as e:
            print(f"Error enviando a Fer: {e}")

    if not Datos["CHAT_ID"] == ray:
        try:
            response = requests.post(url, data=payloadray, files=files)
            print(f"Enviado a Ray: {response.json()}")
        except Exception as e:
            print(f"Error enviando a Ray: {e}")
        
    try:
        response = requests.post(url, data=payload_User, files=files)
        print(f"Enviado a {Datos['nombre']}: {response.json()}")
    except Exception as e:
        print(f"Error enviando a {Datos['nombre']}: {e}")


def Telegram(MSG):
    token = "8167604613:AAFPFgIwMbZFBpnz4hO4p9FzK1-n52VSIIs"
    chat_id = "7781699329"
    chat_idFernando = "6231499420"
    mensaje = MSG
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_idFernando,
        "text": mensaje
    }
    payloadRaymond = {
        "chat_id": chat_id,
        "text": mensaje
    }

    response = requests.post(url, data=payload)
    response = requests.post(url, data=payloadRaymond)
    #print(response.json())

def mantenimiento():
    driver.find_element(By.XPATH, "//*[text()='En este momento no podemos realizar tu operación']")
    print(Fore.RED + '------        VAYA         ------' + Style.RESET_ALL)
    Cerrado = False
    cerrarSesion()
    return False
    
   
def ups():

    global Cerrado, Tiempo
    driver.find_element(By.XPATH, "//*[text()='Algo ha salido mal...']")
    print(Fore.RED + '------        UPS         ------' + Style.RESET_ALL)
    cerrarSesion()
    return False 
                         
def NoDivisas():
    global Cerrado
    global Estadisticas
    driver.find_element(By.XPATH, "//*[text()='En estos momentos no hay disponibilidad de divisas para realizar la operación.']") 
    print(f'{Fore.RED} ------    SIN DIVISAS    ------ {datetime.now().hour}:{datetime.now().minute} {Style.RESET_ALL}')
    txt(f' -------    SIN DIVISAS  :  {datetime.now().hour}:{datetime.now().minute}')
    cerrarSesion()
  
    return True

def Formulario():
    nombre_archivo = "mi_documento.txt"
    texto_parcial = "Formulario Abierto"

    with open(rf'{rutaHistorial}/{datetime.now().date()}.txt', 'r') as archivo:
        contenido = archivo.read()

    patron = r"Formulario Abierto.*:\s*(\d+:\d+)"

    horas_formulario = re.findall(patron, contenido)

    Horario = []

    for hora in horas_formulario:
        Horario.append(hora)
    return Horario
 
def contador(txt):

    with open(rf'{rutaHistorial}/{datetime.now().date()}.txt', 'r') as archivo:
        contenido = archivo.read()

    contenido_lower = contenido.lower()
    texto_lower = txt.lower()

    conteo = contenido_lower.count(texto_lower)

    return conteo


def intentos():
    with open(rf'{rutaGlobal}/HISTORIAL/{datetime.now().date()}.txt', 'r') as f:
        line_count = sum(1 for _ in f)
    return int(line_count /2)

def MercadoCerrado():
    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//*[text()='En este momento el Mercado de divisas se encuentra cerrado']"))) 
    print(f'{Fore.RED} ------  CERRÓ EL MERCADO  ------ {Style.RESET_ALL}')
    txt(f' -------   CERRÓ EL MERCADO  :  {datetime.now().hour}:{datetime.now().minute}')
    
    Telegram(f'''🚫 LAS COMPRAS HAN CERRADO  🚫
             
📋 Veces que abrio el Formulario: {contador("Formulario Abierto")} 
💵 Metodo de compra: Menudeo

🕐 Horarios del Formulario : {Formulario()}

 ''') 
    # Intentos Realizados: {intentos()}
    global Cerrado
    Cerrado = True
    Tiempo = 1
    cerrarSesion()

    return True



def MercadoDivisas():
    global ErrorMD, Datos
    
    # --- PASO 1: Clic en el Menú Principal ---
    try:
        respuesta = requests.head("https://www30.mercantilbanco.com/")

        horaServidorRaw = respuesta.headers['Date']

        # aqui se convierte a formato de fecha local porque los servidores siempre responden en GMT/UTC
        hora_servidor = datetime.strptime(horaServidorRaw, '%a, %d %b %Y %H:%M:%S %Z')

        # print(f'Hora del servidor: {hora_servidor}')
        # print("hora impresa en pagina: " + FUNCIONES.seleccionarElemento('//*[@id="navigation"]/div/div[1]/span[1]').text)
        # print(f"hora local: {datetime.now()}")
        xpath_mercado = "//*[contains(text(), 'Mercado de divisas')]"
        boton_mercado = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, xpath_mercado))
        )
        # Clic forzado para desplegar opciones
        driver.execute_script("arguments[0].click();", boton_mercado)
        print(f'{Fore.CYAN}Desplegado: Mercado de Divisas{Style.RESET_ALL}')

        
    except Exception as e:
        try: 
            VerMensaje()
        except: 
            print(f'{Fore.RED}Fallo en menú principal: {e}{Style.RESET_ALL}')
            return False
        

    # Pequeña pausa para que el submenú se renderice en el DOM
    time.sleep(1.5)

    # --- PASO 2: Clic en la Opción Específica ---
    try:
        xpath_compra = "//*[contains(text(), 'Compra de divisas')]"
        boton_compra = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, xpath_compra))
        )
        # Clic forzado para entrar al formulario
        driver.execute_script("arguments[0].click();", boton_compra)
        print(f'{Fore.GREEN}Éxito: Entrando a Compra de Divisas{Style.RESET_ALL}')
        
        return True  # Indica que TODO SALIÓ BIEN (ErrorMD = False)

    except Exception as e:
        print(f'{Fore.RED}No se pudo dar click en el botón de compra: {e}{Style.RESET_ALL}')
        try: ups()
        except: pass
        return True # Indica que hubo un error

def VerMensaje():
    Mensaje = (WebDriverWait(driver, 1).until(EC.any_of(
        EC.presence_of_element_located((By.XPATH, "/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/melp-in-card-error/div[1]/div[1]")),
        EC.presence_of_element_located((By.XPATH, "//*[@id='system-error']/div/div[1]/div[1]"))
    )).text).strip()
    print(f'{Fore.RED} {Mensaje} {datetime.now().hour}:{datetime.now().minute} {Style.RESET_ALL}')
    
    if any(frase in Mensaje for frase in ['En estos momentos no hay disponibilidad de divisas para realizar la operación. Código 9021', 'Algo ha salido mal...']):
        cerrarSesion()
        return True

    if Mensaje == 'El tiempo de tu sesión ha finalizado.' or Mensaje == '¡Lamentamos las molestias ocasionadas!':
        try:
            return True
        except:
            print('no se encontro el boton')
    
    return False


def compra(Datos):
    print(f"{Fore.GREEN} ------ INTENTANDO COMPRA: {Datos['nombre']} ------ {Style.RESET_ALL}")
    
    # 1. Ingresar Monto y seleccionar divisa
    if ingresarMonto(Datos) == False:
        return False
    
    clickComprar()
    try:
        fecha_inicio = datetime.now()
        if llenarFormularioCompra(Datos) == False:
            return False
        

        # 5. Verificación de resultados (Éxito o Fracaso)
        return verificar_finalizacion(Datos, fecha_inicio)

    except Exception as e:
        print(f"Error en flujo de compra: {e}")
        obtenerMensajeError()
        return False

def verificar_finalizacion(Datos, fecha_inicio):
    """Verifica si la compra fue exitosa o rechazada usando tus validaciones."""

    try: ### ver si el elemento de exito o error se encuentra y extraer el texto para determinar el resultado como "resultadoCompra" pero durando la misma cantidad de tiempo en ver si alguno de los dos estan
        resultadoCompra = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '¡Listo! Compra realizada') | //*[contains(text(), 'fue exitosa')] | //*[contains(text(), 'no fue exitosa')]"))
        ).text
        print(resultadoCompra)
        ###  ya que se extrajo la informacion, procedemos a procesar el texto de "resultadoCompra" para determinar si fue exitoso o no
        if resultadoCompra == "¡Listo! Compra realizada" or resultadoCompra == "¡Listo! Tu compra fue exitosa.":
            segundos = (datetime.now() - fecha_inicio).total_seconds()
            print(f"{Fore.GREEN} ¡ÉXITO! {Datos['nombre']} compró en {segundos}s {Style.RESET_ALL}")
            
            driver.save_screenshot(rf"{rutaComprasExitosas}/{Datos['nombre']} {datetime.now().date()}.png")
            Telegram(f"------ Compra Exitosa con {Datos['nombre']} ------")
            img(Datos)
            #excluir(Datos['nombre'])
            cerrarSesion()
            return True
        else:
            try:
                xpath_err_1 = '/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[1]/melp-finalize-transaction/div/div[2]/div/div[3]/div'
                tipo_error = driver.find_element(By.XPATH, xpath_err_1).text
                print(f"{Fore.RED} Compra no exitosa para {Datos['nombre']}: {tipo_error} {Style.RESET_ALL}")
                Telegram(f"❌ Compra no exitosa para {Datos['nombre']}: {tipo_error}")
            except:
                if VerMensaje():
                    return False
                print("No se pudo capturar el texto del error final.")
                
            cerrarSesion()
            return False
    except:
        
        print("No se encontró el resultado de la compra.")
       

    # try:
    #     # Intentar detectar ÉXITO (Wait corto para no perder tiempo) se amplió el tiempo de espera para detectar el mensaje de éxito, ya que a veces tarda un poco más en aparecer
    #     WebDriverWait(driver, 15).until(
    #         EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '¡Listo! Tu compra fue exitosa.')]"))
    #     )
    #     segundos = (datetime.now() - fecha_inicio).total_seconds()
    #     print(f"{Fore.GREEN} ¡ÉXITO! {Datos['nombre']} compró en {segundos}s {Style.RESET_ALL}")
        
    #     driver.save_screenshot(rf"{rutaComprasExitosas}/{Datos['nombre']} {datetime.now().date()}.png")
    #     Telegram(f"------ Compra Exitosa con {Datos['nombre']} ------")
    #     #img(Datos)
    #     #excluir(Datos['nombre'])
    #     cerrarSesion()
    #     return True

    # except:
    #     # Si no fue exitosa, buscamos el mensaje de error de COMPRA NO EXITOSA
    #     try:
    #         # Usamos tus XPaths de error
    #         xpath_err_1 = '/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[1]/melp-finalize-transaction/div/div[2]/div/div[3]/div'
    #         tipo_error = driver.find_element(By.XPATH, xpath_err_1).text
    #         print(f"{Fore.RED} Compra no exitosa para {Datos['nombre']}: {tipo_error} {Style.RESET_ALL}")
    #         Telegram(f"Compra no exitosa para {Datos['nombre']}: {tipo_error}")
    #     except:
    #         print("No se pudo capturar el texto del error final.")
            
    #     cerrarSesion()
    #     return False

MACid = 0

def CloneMac():
    driver.get("http://192.168.16.1/login.asp")
    try:
        driver.get("http://192.168.16.1/admin/more.html")
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "macClone"))).click()
        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.ID, "cloneinpt"))).send_keys(Keys.CONTROL + "a")
        wait.until(EC.presence_of_element_located((By.ID, "cloneinpt"))).send_keys(Keys.BACKSPACE)
        MAC = RandomMac()
        wait.until(EC.presence_of_element_located((By.ID, "cloneinpt"))).send_keys(MAC)
        wait.until(EC.presence_of_element_located((By.ID, "mac_apply"))).click()
        
        print(f'CAMBIANDO MAC DEL DISPOSITIVO A: {MAC}')
        print(f'REINICIAR MODEM MANUALMENTE')
        print(IP())
        time.sleep(70)
        print(f'REINICIO EXTISOSO')
        Telegram("REINICIO EXTISOSO")
    except:
        wait.until(EC.presence_of_element_located((By.ID, "login_pwd"))).send_keys("papillo.")
        wait.until(EC.presence_of_element_located((By.ID, "loginin"))).click()
        # WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/script[1]")))
        driver.get("http://192.168.16.1/admin/more.html")
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "macClone"))).click()
        time.sleep(2)
        global MACid
        MACid = wait.until(EC.presence_of_element_located((By.ID, "cloneinpt"))).text
        
        wait.until(EC.presence_of_element_located((By.ID, "cloneinpt"))).send_keys(Keys.CONTROL + "a")
        wait.until(EC.presence_of_element_located((By.ID, "cloneinpt"))).send_keys(Keys.BACKSPACE)
        MAC = RandomMac()
        wait.until(EC.presence_of_element_located((By.ID, "cloneinpt"))).send_keys(MAC)
        wait.until(EC.presence_of_element_located((By.ID, "mac_apply"))).click()
        Telegram(f'CAMBIANDO MAC DEL DISPOSITIVO DE {MACid} A {MAC}')
        Telegram(f'POR FAVOR, REINICIAR MODEM MANUALMENTE')
        print(f'CAMBIANDO MAC DEL DISPOSITIVO DE {MACid} A {MAC}')
        print(f'POR FAVOR, REINICIAR MODEM MANUALMENTE')
        print(IP())
        Telegram("REINICIO EXTISOSO")
def IP():
    # Usamos un servicio externo sencillo para leer la IP
    try:
        ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        return ip
    except:
        print('hubo un error al consultar la ip')

def RandomMac():
    
    mac = [random.randint(0x00, 0xff) for _ in range(6)]
    return ":".join(f"{b:02X}" for b in mac)
