from math import e
import asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
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
from config import *

Tiempo = 60
rutaHistorial = os.path.join(rutaGlobal, 'HISTORIAL')
rutaComprasExitosas = os.path.join(rutaHistorial, 'COMPRAS_EXITOSAS')

init()

N1 = random.randint(1000, 1200)
N2 = random.randint(1000, 1200)
ErrorMD = False
Cerrado = False
MAX_WAIT_TIME = 10
US = ""

### CAMBIO DE CONFIGURACION SEGUN SISTEMA OPERATIVO ###
if platform.system() != "Windows":
    print("[Bot] Ejecutando version linux32. Forzando modo Headless local...")
    modo_headless = True  
    modo_uc = False           
    version_driver = "system" 
    modoPls = "none"  

    argumentos_extra = (
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disk-cache-size=1",
        "--media-cache-size=1",
        "--disable-gpu",
        "--single-process",
        "--disable-site-isolation-trials",
        "--user-data-dir=/dev/shm/chrome",
        "--disk-cache-dir=/dev/shm/cache",
        "--disable-renderer-backgrounding",
        "--disable-background-timer-throttling",
        "--disable-component-update",
        "--mute-audio",
        "--blink-settings=imagesEnabled=false",
        "--disable-software-rasterizer",
        "--disable-extensions",
        "--disable-features=AsmJsToWebAssembly",
        "--disable-features=WebAssembly",
        "--proxy-server=direct://",
        "--proxy-bypass-list=*",
        "--js-flags=--no-expose-wasm --max-semi-space-size=1 --max-old-space-size=256"
    )
    os_binary_location = "/usr/bin/chromium"
else:
    print("Ejecutando en Windows")
    modo_headless = False
    modo_uc = True            
    version_driver = "keep"
    modoPls = "none"
    argumentos_extra = [
        "--ignore-certificate-errors",
        "--ignore-ssl-errors",
        "--disable-web-security",
        "--disable-remote-fonts",
        "--enable-data-reduction-proxy-dev",
        "--disable-dev-shm-usage",
    ]
    os_binary_location = None 

PROXYS = {
    'local': None,
    'redmiNote12': 'socks5://100.67.185.66:1080',
    'ray' : 'socks5://100.78.148.101:1080',
    'ono1' : 'socks5://100.96.147.59:1080',
    'karen' : 'socks5://100.122.47.58:1080',
    'laptop_fernando' : 'socks5://100.80.146.29:1080'
}

driver = Driver(
    proxy=PROXYS['ono1'],
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
    driver_version=version_driver
)

wait = WebDriverWait(driver, MAX_WAIT_TIME)

# ==========================================
# GESTOR DE SESIÓN Y MONITOR ASÍNCRONO
# ==========================================
class MercantilSeleniumSession:
    _instance = None

    def __init__(self):
        self.driver = driver
        self.tarea_monitor = None
        self.running = False

    @classmethod
    async def get_instance(cls):
        if cls._instance is None:
            cls._instance = MercantilSeleniumSession()
        return cls._instance

    def iniciar_monitor(self):
        if not self.running:
            self.running = True
            self.tarea_monitor = asyncio.create_task(self._monitor_de_sesion())
            print("[Monitor] Monitor de sesión activado en segundo plano.")

    async def _monitor_de_sesion(self):
        """Monitorea modales de expiración en segundo plano usando Selenium"""
        xpath_error = '//*[@id="system-error"]/div/div[1]/div[1]'
        xpath_confirm_modal = '//*[@id="confirm-modal"]/div/div[2]/div[3]'
        xpath_btn_mantener = '//*[@id="confirm-modal"]/div/div[2]/div[4]/button[2]'

        try:
            while self.running:
                try:
                    detector = await asyncio.to_thread(self._detectar_modales, xpath_error, xpath_confirm_modal)

                    if detector in [
                        'El tiempo de tu sesión ha finalizado.',
                        'No has interactuado con nosotros en los últimos minutos.',
                        'Por tu seguridad hemos cerrado esta sesión.'
                    ]:
                        print('\n[Monitor] Sesión expirada detectada por el monitor.')

                    elif detector == '¿Deseas mantener tu sesión activa?':
                        print('\n[Monitor] Manteniendo sesión activa...')
                        await asyncio.to_thread(self._hacer_click, xpath_btn_mantener)

                except Exception:
                    pass

                await asyncio.sleep(3)

        except asyncio.CancelledError:
            print('[Monitor] Monitoreo detenido.')

    def _detectar_modales(self, xpath_err, xpath_conf):
        try:
            elems_err = self.driver.find_elements(By.XPATH, xpath_err)
            elems_conf = self.driver.find_elements(By.XPATH, xpath_conf)
            if elems_err and elems_err[0].is_displayed():
                return elems_err[0].text.strip()
            if elems_conf and elems_conf[0].is_displayed():
                return elems_conf[0].text.strip()
        except Exception:
            pass
        return ""

    def _hacer_click(self, xpath):
        try:
            btn = self.driver.find_element(By.XPATH, xpath)
            if btn.is_displayed():
                btn.click()
        except Exception:
            pass

    async def detener_monitor(self):
        self.running = False
        if self.tarea_monitor:
            self.tarea_monitor.cancel()
            await asyncio.gather(self.tarea_monitor, return_exceptions=True)


Estadisticas = {
    'formulario' : 0,
    'metodos' : [],
    'horarios' : []
}

ip = None
US = None
inicioLinux = False

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
    from funciones_app import escribir, hacerClick
    global ip, US, inicioLinux
    US = UserAgent().random
    if not inicioLinux:
        driver.get("https://www30.mercantilbanco.com/login")
        inicioLinux = True

    print(f'{Fore.YELLOW} Ejecutando navegador con Agente: {Style.RESET_ALL} {US} ')
    
    driver.execute_cdp_cmd('Network.clearBrowserCookies', {})
    driver.execute_cdp_cmd('Network.clearBrowserCache', {})
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": US})

    driver.refresh()
    driver.get("about:blank") 
    driver.get("https://www30.mercantilbanco.com/login")
    driver.execute_script("document.body.style.zoom='50%'")

    try:
        print('iniciando sesion')
        if not escribir("#username", Inicio['usuario']):
            print('Error al ingresar el usuario')
            return False
            
        escribir("#password", Inicio['contrasena'])
        hacerClick(".button-wrapper__btn-primary")
        
        # Espera hasta 15 segundos a que carguen las preguntas de seguridad antes de continuar
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((
                By.XPATH, 
                '//*[@id="mat-input-3"] | //*[@id="question-1"] | //*[contains(text(), "El tiempo de tu sesión ha finalizado.")]'
            ))
        )
        return True

    except Exception as e:
        print(f'Error o timeout en inicio de sesión: {e}')
        return False

def ResolverPreguntasSeguridad(Preguntas):
    from funciones_app import seleccionarElemento, escribir
    try:
        print('resolviendo Preguntas de Seguridad')
        try:
            if Preguntas['PreguntaUnica']:
                elemento = seleccionarElemento('//*[@id="mat-input-3"] | //*[contains(text(), "El tiempo de tu sesión ha finalizado.")] | //*[contains(text(), "¡Lamentamos las molestias ocasionadas!")] | //*[contains(text(), "Por tu seguridad hemos cerrado esta sesión.")]')
                if elemento.text in ['El tiempo de tu sesión ha finalizado.', '¡Lamentamos las molestias ocasionadas!', 'Por tu seguridad hemos cerrado esta sesión.']:
                    print(f'{Fore.RED} {elemento.text} {datetime.now().hour}:{datetime.now().minute} {Style.RESET_ALL}')
                    return False
                else:
                    elemento.send_keys(Preguntas['RespuestaUnica'])
                    escribir("#mat-input-2", Preguntas['RespuestaUnica'])
            else:
                elemento = seleccionarElemento('//*[@id="question-1"] | //*[contains(text(), "El tiempo de tu sesión ha finalizado.")] | //*[contains(text(), "¡Lamentamos las molestias ocasionadas!")] | //*[contains(text(), "Por tu seguridad hemos cerrado esta sesión.")]')

                if elemento.text in ['El tiempo de tu sesión ha finalizado.', '¡Lamentamos las molestias ocasionadas!', 'Por tu seguridad hemos cerrado esta sesión.']:
                    print(f'{Fore.RED} {elemento.text} {datetime.now().hour}:{datetime.now().minute} {Style.RESET_ALL}')
                    return False
                else:    
                    if elemento.text == Preguntas['pregunta1']:
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mat-input-2"))).send_keys(Preguntas['respuesta1'])
                    if elemento.text == Preguntas['pregunta2']:
                        wait.until(EC.presence_of_element_located((By.ID, "mat-input-2"))).send_keys(Preguntas['respuesta2'])
                    if elemento.text == Preguntas['pregunta3']:
                        wait.until(EC.presence_of_element_located((By.ID, "mat-input-2"))).send_keys(Preguntas['respuesta3'])
                    if elemento.text == Preguntas['pregunta4']:
                        wait.until(EC.presence_of_element_located((By.ID, "mat-input-2"))).send_keys(Preguntas['respuesta4'])
                    if elemento.text == Preguntas['pregunta5']:
                        wait.until(EC.presence_of_element_located((By.ID, "mat-input-2"))).send_keys(Preguntas['respuesta5'])

                    q2_text = wait.until(EC.presence_of_element_located((By.ID, 'question-2'))).text
                    if q2_text == Preguntas['pregunta1']:
                        wait.until(EC.presence_of_element_located((By.ID, "mat-input-3"))).send_keys(Preguntas['respuesta1'])
                    if q2_text == Preguntas['pregunta2']:
                        wait.until(EC.presence_of_element_located((By.ID, "mat-input-3"))).send_keys(Preguntas['respuesta2'])
                    if q2_text == Preguntas['pregunta3']:
                        wait.until(EC.presence_of_element_located((By.ID, "mat-input-3"))).send_keys(Preguntas['respuesta3'])
                    if q2_text == Preguntas['pregunta4']:
                        wait.until(EC.presence_of_element_located((By.ID, "mat-input-3"))).send_keys(Preguntas['respuesta4'])
                    if q2_text == Preguntas['pregunta5']:
                        wait.until(EC.presence_of_element_located((By.ID, "mat-input-3"))).send_keys(Preguntas['respuesta5'])

        except Exception:
            print('no encontro el elemento')
            VerMensaje()
            return False
     
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/app/melp-standard-layout/div/div/melp-secure-access/melp-standard-card-layout/div/div/div[1]/div/div/melp-connection-type/form/div/div[2]"))).click()
        return True
    except Exception:
        print('hubo un problema ingresando las preguntas de seguridad')
        return False

def txt(mensaje):
    try:
        with open(os.path.join(rutaHistorial, f'{datetime.now().date()}.txt'), 'a', encoding='utf-8') as archivo:
            archivo.write(f'\n{mensaje}\n')
    except Exception as e:
        print(f'error al escribir el archivo: {e}')

def excluir(usuario):
    with open(os.path.join(rutaGlobal, 'usuariosListos.txt'), "a", encoding="utf-8") as f:
        f.write(f"{usuario}\n")
        print(f"✅ {usuario} ha sido guardado en la base de datos y será excluido.")

def check(usuario):
    try:
        with open(os.path.join(rutaGlobal, 'usuariosListos.txt'), "r", encoding="utf-8") as f:
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
    try:
        png_bytes = driver.get_screenshot_as_png()
        nparr = np.frombuffer(png_bytes, np.uint8)
        imagen_cv2 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        imagen_recortada = imagen_cv2

        is_success, buffer = cv2.imencode(".png", np.asarray(imagen_recortada))
        imagen_en_bytes = buffer.tobytes()

        TOKEN = "8167604613:AAFPFgIwMbZFBpnz4hO4p9FzK1-n52VSIIs"
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        fer = "6231499420"
        ray = "7781699329"

        destinatarios = []
        if Datos["CHAT_ID"] != fer:
            destinatarios.append((fer, f'💲 Compra Exitosa 💲 con {Datos["nombre"]}'))
        if Datos["CHAT_ID"] != ray:
            destinatarios.append((ray, f'💲 Compra Exitosa 💲 con {Datos["nombre"]}'))
        destinatarios.append((Datos["CHAT_ID"], '💲 Compra Exitosa 💲'))

        for chat_id, caption in destinatarios:
            try:
                foto_stream = io.BytesIO(imagen_en_bytes)
                payload = {"chat_id": chat_id, "caption": caption}
                files = {"photo": ("captura.png", foto_stream, "image/png")}
                response = requests.post(url, data=payload, files=files)
                print(f"Enviado a {chat_id}: {response.json()}")
            except Exception as e:
                print(f"Error enviando a {chat_id}: {e}")
    except Exception:
        print('no se pudo enviar la imagen')

def Telegram(MSG):
    token = "8167604613:AAFPFgIwMbZFBpnz4hO4p9FzK1-n52VSIIs"
    chat_id = "7781699329"
    chat_idFernando = "6231499420"
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    requests.post(url, data={"chat_id": chat_idFernando, "text": MSG})
    requests.post(url, data={"chat_id": chat_id, "text": MSG})

def mantenimiento():
    from funciones_app import cerrarSesion
    driver.find_element(By.XPATH, "//*[text()='En este momento no podemos realizar tu operación']")
    print(Fore.RED + '------        VAYA         ------' + Style.RESET_ALL)
    cerrarSesion()
    return False

def ups():
    from funciones_app import cerrarSesion
    driver.find_element(By.XPATH, "//*[text()='Algo ha salido mal...']")
    print(Fore.RED + '------        UPS         ------' + Style.RESET_ALL)
    cerrarSesion()
    return False 

def NoDivisas():
    from funciones_app import cerrarSesion
    driver.find_element(By.XPATH, "//*[text()='En estos momentos no hay disponibilidad de divisas para realizar la operación.']") 
    print(f'{Fore.RED} ------    SIN DIVISAS    ------ {datetime.now().hour}:{datetime.now().minute} {Style.RESET_ALL}')
    txt(f' -------    SIN DIVISAS  :  {datetime.now().hour}:{datetime.now().minute}')
    cerrarSesion()
    return True

def Formulario():
    with open(os.path.join(rutaHistorial, f'{datetime.now().date()}.txt'), 'r') as archivo:
        contenido = archivo.read()
    patron = r"Formulario Abierto.*:\s*(\d+:\d+)"
    return re.findall(patron, contenido)

def contador(txt_search):
    with open(os.path.join(rutaHistorial, f'{datetime.now().date()}.txt'), 'r') as archivo:
        contenido = archivo.read()
    return contenido.lower().count(txt_search.lower())

def intentos():
    with open(os.path.join(rutaHistorial, f'{datetime.now().date()}.txt'), 'r') as f:
        line_count = sum(1 for _ in f)
    return int(line_count / 2)

def MercadoCerrado():
    from funciones_app import cerrarSesion
    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//*[text()='En este momento el Mercado de divisas se encuentra cerrado']"))) 
    print(f'{Fore.RED} ------  CERRÓ EL MERCADO  ------ {Style.RESET_ALL}')
    txt(f' -------   CERRÓ EL MERCADO  :  {datetime.now().hour}:{datetime.now().minute}')
    
    Telegram(f'''🚫 LAS COMPRAS HAN CERRADO  🚫
             
📋 Veces que abrio el Formulario: {contador("Formulario Abierto")} 
💵 Metodo de compra: Menudeo

🕐 Horarios del Formulario : {Formulario()}
''') 
    global Cerrado, Tiempo
    Cerrado = True
    Tiempo = 1
    cerrarSesion()
    return True

def MercadoDivisas():
    global ErrorMD
    from funciones_app import cerrarSesion
    try:
        respuesta = requests.head("https://www30.mercantilbanco.com/")
        xpath_mercado = "//*[contains(text(), 'Mercado de divisas')]"
        boton_mercado = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, xpath_mercado))
        )
        driver.execute_script("arguments[0].click();", boton_mercado)
        print(f'{Fore.CYAN}Desplegado: Mercado de Divisas{Style.RESET_ALL}')
    except Exception as e:
        try: 
            VerMensaje()
        except Exception: 
            print(f'{Fore.RED}Fallo en menú principal: {e}{Style.RESET_ALL}')
            return False

    time.sleep(1.5)

    try:
        xpath_compra = "//*[contains(text(), 'Compra de divisas')]"
        boton_compra = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, xpath_compra))
        )
        driver.execute_script("arguments[0].click();", boton_compra)
        print(f'{Fore.GREEN}Éxito: Entrando a Compra de Divisas{Style.RESET_ALL}')
        return True

    except Exception as e:
        print(f'{Fore.RED}No se pudo dar click en el botón de compra: {e}{Style.RESET_ALL}')
        try: ups()
        except Exception: pass
        return True

def VerMensaje():
    from funciones_app import cerrarSesion
    try:
        Mensaje = (WebDriverWait(driver, 1).until(EC.any_of(
            EC.presence_of_element_located((By.XPATH, "/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/melp-in-card-error/div[1]/div[1]")),
            EC.presence_of_element_located((By.XPATH, "//*[@id='system-error']/div/div[1]/div[1]"))
        )).text).strip()
        print(f'{Fore.RED} {Mensaje} {datetime.now().hour}:{datetime.now().minute} {Style.RESET_ALL}')
        
        if any(frase in Mensaje for frase in ['En estos momentos no hay disponibilidad de divisas para realizar la operación. Código 9021', 'Algo ha salido mal...']):
            cerrarSesion()
            return True

        if Mensaje in ['El tiempo de tu sesión ha finalizado.', '¡Lamentamos las molestias ocasionadas!', 'Por tu seguridad hemos cerrado esta sesión.']:
            return True

        return False
    except Exception:
        return False

def compra(Datos):
    from funciones_app import ingresarMonto, clickComprar, llenarFormularioCompra
    print(f"{Fore.GREEN} ------ INTENTANDO COMPRA: {Datos['nombre']} ------ {Style.RESET_ALL}")
    
    if Datos['mecanismo']['menudeo'][0] is not None:
        if not ingresarMonto(Datos['mecanismo']['menudeo'][0]):
            return False
    elif Datos['mecanismo']['intervencion'] is not None:
        if not ingresarMonto(Datos['mecanismo']['intervencion']):
            return False
    else:
        print('no se selecciono fondo en ningun mecanismo')
    
    clickComprar()
    try:
        fecha_inicio = datetime.now()
        if not llenarFormularioCompra(Datos):
            return False

        return verificar_finalizacion(Datos, fecha_inicio)
    except Exception as e:
        print(f"Error en flujo de compra: {e}")
        obtenerMensajeError()
        return False

def verificar_finalizacion(Datos, fecha_inicio):
    from funciones_app import cerrarSesion
    try: 
        try:
            resultadoCompra = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '¡Listo! Compra realizada') or contains(text(), 'fue exitosa') or contains(text(), 'no fue exitosa')]"))
            ).text
            print(resultadoCompra)
        except Exception:
            print('no se encontro resultado compra')
            resultadoCompra = ""

        if resultadoCompra in ["¡Listo! Compra realizada", "¡Listo! Tu compra fue exitosa."]:
            segundos = (datetime.now() - fecha_inicio).total_seconds()
            print(f"{Fore.GREEN} ¡ÉXITO! {Datos['nombre']} compró en {segundos}s {Style.RESET_ALL}")
            driver.execute_script("document.body.style.zoom='100%'")
            driver.save_screenshot(os.path.join(rutaComprasExitosas, f"{Datos['nombre']} {datetime.now().date()}.png"))
            Telegram(f"------ Compra Exitosa con {Datos['nombre']} ------")
            img(Datos)
            cerrarSesion()
            return True
        else:
            try:
                xpath_err_1 = '/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[1]/melp-finalize-transaction/div/div[2]/div/div[3]/div'
                tipo_error = driver.find_element(By.XPATH, xpath_err_1).text
                print(f"{Fore.RED} Compra no exitosa para {Datos['nombre']}: {tipo_error} {Style.RESET_ALL}")
            except Exception:
                if VerMensaje():
                    return False
                print("No se pudo capturar el texto del error final.")
                
            cerrarSesion()
            return False
    except Exception:
        print("No se encontró el resultado de la compra.")
        return False

MACid = 0

def RandomMac():
    mac = [random.randint(0x00, 0xff) for _ in range(6)]
    return ":".join(f"{b:02X}" for b in mac)

def IP():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        return response.json()['ip']
    except Exception:
        print('hubo un error al consultar la ip')

def ipProxys():
    try:
        driver.get('https://api.ipify.org')
        return driver.get_text("body").strip()
    except Exception:
        print('hubo un error al consultar la ip')

def obtenerMensajeError():
    from funciones_app import cerrarSesion, seleccionarElemento
    error = seleccionarElemento(".title").text
    try:
        codigoError = seleccionarElemento('.error-code').text
    except Exception:
        codigoError = seleccionarElemento('.subtitle').text

    print(f"Error: {error} {codigoError}")
    cerrarSesion()
    return True