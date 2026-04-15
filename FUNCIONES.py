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

from colorama import init, Fore, Back, Style
import sys
Tiempo = 60
init()


N1 = random.randint(1000, 1200)
N2 = random.randint(1000, 1200)
ErrorMD = False
Cerrado = False
MAX_WAIT_TIME = 10
US = ""


driver = Driver(
    undetectable=True,
    uc=True,                # Activa undetected-chromedriver    
    block_images=True,
    window_size= f"{N1},{N2}",  
    headless1=False,
    chromium_arg="--ignore-certificate-errors,--ignore-ssl-errors,--disable-web-security, --disable-remote-fonts, --enable-data-reduction-proxy-dev",
    disable_csp=True,       # políticas de seguridad
    incognito=True,       
    # disable_cookies=True, # Se cuelga
    mobile=True,
    pls="eager",
    #user_data_dir="./cache",
    #ad_block=True,
)

wait = WebDriverWait(driver, MAX_WAIT_TIME)

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
    driver.get("https://www30.mercantilbanco.com/login")



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
    driver.get("https://www30.mercantilbanco.com/login")
    driver.execute_script("document.body.style.zoom='50%'")

    
    try:
        if  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, '//*[@id="system-error"]/div/div[1]/div[1]'))).text == '¡Lamentamos las molestias ocasionadas!':
            try:
                wait.until(EC.presence_of_element_located((By.ID, '//*[@id="system-error"]/div/div[1]/div[3]/button'))).click()
            except:
                print('no se encontro el boton')
    except:
        None

    try:
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(Inicio['usuario'])
        wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(Inicio['contrasena'])
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button-wrapper__btn-primary"))).click()
    except:
        print('no se encontro el objeto para ingresar el usuario')
        try:
            driver.get("https://www30.mercantilbanco.com/login")
        except:
            print("no se pudo acceder al sitio")
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(Inicio['usuario'])
        wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(Inicio['contrasena'])
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button-wrapper__btn-primary"))).click()
        return

    try:
        if wait.until(EC.presence_of_elements_located((By.XPATH, '//*[@id="system-error"]/div/div[1]/div[1]'))).text == 'El tiempo de tu sesión ha finalizado.':
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="system-error"]/div/div[1]/div[3]/button'))).click()
    except:
        None   

def preguntas_seguridad(Preguntas):

    try:
    
        try:

            if Preguntas['PreguntaUnica'] == True:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mat-input-2"))).send_keys(Preguntas['RespuestaUnica'])
                WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "mat-input-3"))).send_keys(Preguntas['RespuestaUnica'])

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
            return
     
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/app/melp-standard-layout/div/div/melp-secure-access/melp-standard-card-layout/div/div/div[1]/div/div/melp-connection-type/form/div/div[2]"))).click()

    except:
        print('hubo un problema ingresando las preguntas de seguridad')

def txt(mensaje):
    try:
        with open(rf'/home/yako/Documentos/python/PROYECTO_COMPRAS/HISTORIAL/{datetime.now().date()}.txt', 'a', encoding='utf-8') as archivo:
            archivo.write(f'\n{mensaje}\n')
    except Exception as e:
        print(f'error al escribir el archivo: {e}')

def excluir(usuario):
    with open(rf'/home/yako/Documentos/python/PROYECTO_COMPRAS/HISTORIAL/DATABASE.txt', "a", encoding="utf-8") as f:
        f.write(f"{usuario}\n")
        print(f"✅ {usuario} ha sido guardado en la base de datos y será excluido.")

def check(usuario):
  
    try:
        with open(rf'/home/yako/Documentos/python/PROYECTO_COMPRAS/HISTORIAL/DATABASE.txt', "r", encoding="utf-8") as f:
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

    img = cv2.imread(rf'/home/yako/Documentos/python/PROYECTO_COMPRAS/HISTORIAL/COMPRAS_EXITOSAS/{Datos["nombre"]} {datetime.now().date()}.png')
    
    y_inicio, y_fin = 190, 750 # alto
    x_inicio, x_fin = 300, 1210 # ancho
    cv2.line(img, (350, 558), (830, 558), (400, 400, 400), 40)
    cv2.line(img, (350, 270), (830, 270), (400, 400, 400), 20)
    img = img[y_inicio:y_fin, x_inicio:x_fin]


    cv2.imwrite(rf'/home/yako/Documentos/python/PROYECTO_COMPRAS/HISTORIAL/COMPRAS_EXITOSAS/{Datos["nombre"]} {datetime.now().date()}t.png', img)


    # --- Telegram ---
    TOKEN = '8167604613:AAFPFgIwMbZFBpnz4hO4p9FzK1-n52VSIIs' 
    CHAT_ID = Datos['CHAT_ID']    
    RUTA_IMAGEN = rf'/home/yako/Documentos/python/PROYECTO_COMPRAS/HISTORIAL/COMPRAS_EXITOSAS/{Datos["nombre"]} {datetime.now().date()}t.png' 
    TEXTO_DESCRIPCION = f'💲 Compra Exitosa 💲'

    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'


    with open(RUTA_IMAGEN, 'rb') as f:
        files = {'photo': f}
        data = {'chat_id': CHAT_ID, 'caption': TEXTO_DESCRIPCION}

 
        respuesta = requests.post(url, files=files, data=data)


    if respuesta.status_code == 200:
        print("Imagen enviada exitosamente")
        print(respuesta.json())
    else:
        print("Error al enviar la imagen")
        print(respuesta.status_code)
        print(respuesta.json())

    print()

    if not {Datos["nombre"]} == "Fernando":
        with open(RUTA_IMAGEN, 'rb') as f:
            files = {'photo': f}
            data = {'chat_id': 6231499420, 'caption': TEXTO_DESCRIPCION}
            respuesta = requests.post(url, files=files, data=data)

        if respuesta.status_code == 200:
            print("Imagen enviada exitosamente ADMIN")
            print(respuesta.json())
        else:
            print("Error al enviar la imagen")
            print(respuesta.status_code)
            print(respuesta.json())

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

def mantenimiento():
    driver.find_element(By.XPATH, "//*[text()='En este momento no podemos realizar tu operación']")
    print(Fore.RED + '------        VAYA         ------' + Style.RESET_ALL)
    Cerrado = False
    cerrar()
    return False
    
def vaya():
    global Cerrado
    driver.find_element(By.XPATH, "//*[text()='¡Vaya! En este momento no podemos realizar tu operación']")
    print(Fore.RED + '------        VAYA         ------' + Style.RESET_ALL)
    Cerrado = False
    cerrar()
    return False
   
def ups():

    global Cerrado, Tiempo
    driver.find_element(By.XPATH, "//*[text()='Algo ha salido mal...']")
    print(Fore.RED + '------        UPS         ------' + Style.RESET_ALL)
    cerrar()
    return False 
                         
def NoDivisas():
    global Cerrado
    global Estadisticas
    driver.find_element(By.XPATH, "//*[text()='En estos momentos no hay disponibilidad de divisas para realizar la operación.']") 
    print(f'{Fore.RED} ------    SIN DIVISAS    ------ {datetime.now().hour}:{datetime.now().minute} {Style.RESET_ALL}')
    txt(f' -------    SIN DIVISAS  :  {datetime.now().hour}:{datetime.now().minute}')
    cerrar()
  
    return True

def Formulario():
    nombre_archivo = "mi_documento.txt"
    texto_parcial = "Formulario Abierto"

    with open(rf'/home/yako/Documentos/python/PROYECTO_COMPRAS/HISTORIAL/{datetime.now().date()}.txt', 'r') as archivo:
        contenido = archivo.read()

    patron = r"Formulario Abierto.*:\s*(\d+:\d+)"

    horas_formulario = re.findall(patron, contenido)

    Horario = []

    for hora in horas_formulario:
        Horario.append(hora)
    return Horario
 
def contador(txt):

    with open(rf'/home/yako/Documentos/python/PROYECTO_COMPRAS/HISTORIAL/{datetime.now().date()}.txt', 'r') as archivo:
        contenido = archivo.read()

    contenido_lower = contenido.lower()
    texto_lower = txt.lower()

    conteo = contenido_lower.count(texto_lower)

    return conteo


def intentos():
    with open(rf'/home/yako/Documentos/python/PROYECTO_COMPRAS/HISTORIAL/{datetime.now().date()}.txt', 'r') as f:
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
    cerrar()

    return True

def cerrar():
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app/melp-standard-layout/melp-header/div/div[3]/div/div/span'))).click()
        time.sleep(3)
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app/melp-standard-layout/div/melp-sidebar/div[2]/melp-sidebar-logout/melp-button-menu/div/span'))).click()
        
    except:
        print('no se encontro algun objeto en cerrar()')

def Ingreso():
    

    global ErrorMD, Datos
    
    try:
    
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='step1']/div/div[1]/div[6]/div[2]//*[contains(text(), 'Mercado de divisas')]"))).click() 
    except: 
        print('no se pudo dar click mercado de divisas')
        try:
            ups()
        except:
            print('no se encontro el ups')
        return True 
        

                                            

    time.sleep(2)

    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='step1']/div/div[1]/div[12]/div/div[2]//*[contains(text(), 'Compra de divisas')]"))).click()
        return False
    except:
        print('no se pudo dar click compra')
        ups()
        return True 
    


def compra(Datos):
    print(Fore.GREEN + ' ------ INTENTANDO COMPRA ------' + Style.RESET_ALL)
    xpath_dolares = "//*[contains(text(), 'Dólares')]"
    try:
        boton = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpath_dolares))
        )

        driver.execute_script("arguments[0].click();", boton)

    except Exception as e:
        #print(f"No se pudo hacer clic en Dólares: {e}")
        driver.save_screenshot("error_click.png")
        ups() 
        return False

    try:
        driver.find_element(By.XPATH, '//input[starts-with(@id, "mat-input-")]').send_keys(Datos['Monto'])
    except:
        print('no se pudo ingresar el monto')
    

    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[2]/melp-button-wrapper/div/div[2]/button'))).click()
    except:
        print('no se pudo dar click en el segundo boton')
        return False
        


    ############################### COMPROBANDO ###############################################################################
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[1]/melp-data-transaction/div/div/div[4]/div[1]')))
        print(f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}')
        fecha_inicio = datetime.now()
        
    except:
        try:
            ups()
            return False
        except:
            try:
                NoDivisas()
                return True
            except:
                try:
                    MercadoCerrado()
                    driver.quit()
                    return False
                except:
                    try:
                        vaya()
                        return False
                    except:
                        None

############################################################################################################################ 


    try:
        try:
            try:
                porcentaje = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[1]/melp-data-transaction/div/div/div[4]/div[1]'))).text  
                print(porcentaje)
            except:
                print('no se encontro el porcentaje :(')
            
            try:
                metodo = ''

                if porcentaje == 'Comisión (0.2%) (Bs.)':
                    metodo = 'MENUDEO'
                    print('Activo Menudeo, 0,2')
                if porcentaje == 'Comisión (0.12%) (Bs.)':
                    metodo = 'MESA DE CAMBIO'
                    print('Activo Mesa de Cambio, 0.12')
                if porcentaje == 'Comisión (0.15%) (Bs.)':
                    metodo = 'INTERVENCIÓN'
                    print('Activo INTERVENCIÓN, 0.15')
                if porcentaje == None:
                    metodo = 'error'

            except:
                cerrar()
                print('no se hicieron las comprobaciones')
                return

            if metodo not in Estadisticas['metodos']:
                    Estadisticas['metodos'].append(metodo)
            if metodo not in Estadisticas['metodos']:
                    Estadisticas['metodos'].append(metodo)
            if metodo not in Estadisticas['metodos']:
                    Estadisticas['metodos'].append(metodo)

            txt(f' -------   Formulario Abierto ------ {metodo} :  {datetime.now().hour}:{datetime.now().minute}')
            Telegram(f'------ Formulario Abierto ------ {metodo} ------')
            print(f'{Fore.YELLOW} -----------  DATOS DE LA COMPRA  ------ {metodo} ----- {Style.RESET_ALL}')
                 
            
            
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'mat-select-0'))).click()
            except:
                print('no se selecciono la primera casilla')


            if Datos['cuenta'] == 'corriente':
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='mat-select-0-panel']//*[contains(text(), 'Cuenta Corriente')]"))).click()
                except:
                        print('no se selecciono cuenta corriente')
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'mat-select-0'))).click()

            if Datos['cuenta'] == 'ahorro':
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='mat-select-0-panel']//*[contains(text(), 'Cuenta de Ahorro')]"))).click()
                    print('se selecciono cuenta ahorro')
                except:
                    print('no se selecciono cuenta ahorro')
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'mat-select-0'))).click()


            ################        ORIGREN DE LOS FONDOS        ################  
            

            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'mat-select-2'))).click()
            except:
                print('no se selecciono la segunda casilla')

            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='mat-select-2-panel']//*[contains(text(), 'Fondos Propios')]"))).click()
            except:
                print('no se selecciono la opcion de la segunda casilla  ')

            ################        MOTIVO DE LA COMPRA        ################  


            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'mat-select-3'))).click()
            except:
                print('no se selecciono la tercera casilla')

            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='mat-select-3-panel']//*[contains(text(), 'Materia Prima')]"))).click()
            except:
                print('no se selecciono la opcion de la tercera casilla ')

                    
            ######             ESCENARIO EN QUE NO TENGA SUFICIENTE DINERO EN LA CUENTA             ######
            try:
                if driver.find_element(By.XPATH, '//*[@id="mat-mdc-error-13"]').text == 'El monto a comprar es mayor al saldo disponible de tu cuenta.':
                    print(f"{Fore.RED} ------ El monto a comprar es mayor al saldo disponible de tu cuenta {Datos['cuenta']} ------ {Style.RESET_ALL}")
                    print(Fore.YELLOW + '------ Cambiando Cuenta ------' + Style.RESET_ALL)
                        
                    try:
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'mat-select-0'))).click()
                    except:
                        print('no se selecciono la primera casilla')

                    
                    if Datos['cuenta'] == 'corriente':
                        try:
                            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='mat-select-0-panel']//*[contains(text(), 'Cuenta de Ahorro')]"))).click()
                            print('se selecciono cuenta Ahorro')
                        except:
                            print('no se selecciono cuenta Ahorro')

                    if Datos['cuenta'] == 'ahorro':
                        try:
                            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='mat-select-0-panel']//*[contains(text(), 'Cuenta Corriente')]"))).click()
                            print('se selecciono cuenta Corriente')
                        except:
                            print('no se selecciono cuenta corriente')
            except:
                print(1)
            
            try:
                    driver.save_screenshot('PRUEBA_DE_Monto.png')
            except:
                    print("no se pudo hacer la captura")
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[2]/melp-button-wrapper/div/div[2]/button[2]'))).click()
            except:
                print('no se presionó el boton1')
                Telegram('ERROR CON FORMULARIO ABIERTO')
                time.sleep(60)
                
                
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[2]/melp-button-wrapper/div/div[2]/button[2]'))).click()
            except:
                print('no se presionó el boton2')
                Telegram('ERROR CON FORMULARIO ABIERTO')
                time.sleep(60)

                
            driver.save_screenshot('PRUEBA DE ESTATUS.png')
            try:
                wait.until(EC.presence_of_element_located((By.ID, 'mat-mdc-checkbox-0-input'))).click()
            except Exception as e:
                print('no se presionó el boton3')
                Telegram('ERROR CON FORMULARIO ABIERTO')
                Telegram(e)
                time.sleep(60)

            try:
                wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[2]/melp-button-wrapper/div/div[2]/button[2]'))).click()
            except:
                print('no se presionó el boton4')
                Telegram('ERROR CON FORMULARIO ABIERTO')
                time.sleep(60)


            segundos_transcurridos = (datetime.now() - fecha_inicio).total_seconds()
            print(f"Segundos transcurridos relleno formulario: {segundos_transcurridos} segundos")
            try:
                driver.save_screenshot('PRUEBA_DE_ESTATUS2.png')
            except:
                print("no se pudo hacer la captura")

            try:
                ups()
                Telegram("error UPS al llenar formulario, se recomienda cambiar de ip")
                print("error UPS al llenar formulario, se recomienda cambiar de ip")
                return False
            except:
                None
            ##### COMPRA NO EXITOSA #####
            try:
                global Tiempo
                wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'La compra no fue exitosa.')]")))
                segundos_transcurridos = (datetime.now() - fecha_inicio).total_seconds()
                print(f"Segundos transcurridos: {segundos_transcurridos} segundos")
                print(f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}')
                #'En este momento no es posible realizar tu operación de Mercado de Divisas. Código 10'
                #'La operación no se pudo realizar. Has alcanzado el límite de transacciones permitidas. Código 15'
                try:
                    Tipo_Error = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[1]/melp-finalize-transaction/div/div[2]/div/div[3]/div'))).text
                    print(Tipo_Error)
                except:
                    print('la primera ubicacion es incorrecta')
                    try:
                        Tipo_Error = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[1]/melp-finalize-transaction/div/div[2]/div/div[3]/div/div"))).text
                        print(Tipo_Error)
                    except:
                        print('la segunda ubicacion es incorrecta')
                
                print(f"{Fore.RED} ---- la compra con {Datos['nombre']} no fue exitosa:{Fore.YELLOW}{Tipo_Error} - - - - {datetime.now().hour}:{datetime.now().minute} - - - -    {Style.RESET_ALL}")
                Telegram(f"---- la compra con {Datos['nombre']} no fue exitosa:{Tipo_Error} - - - - ")   
                Telegram(f"ip:{ip} agente{US}")
                Tiempo = 1
                cerrar()
                # CloneMac()
                return False
                
            except:
                None

            driver.save_screenshot('PRUEBA DE ESTATUS3.png')

            ##### COMPRA EXITOSA #####
            try:
                WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '¡Listo! Tu compra fue exitosa.')]")))
                print(f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}')
                segundos_transcurridos = (datetime.now() - fecha_inicio).total_seconds()
                print(f"Segundos transcurridos: {segundos_transcurridos} segundos")
                print(f"{Fore.GREEN} - - - - la compra con {Datos['nombre']} fue exitosa {Style.RESET_ALL} - - - - {datetime.now().hour}:{datetime.now().minute} - - - - ")
                driver.save_screenshot(rf"/home/yako/Documentos/python/PROYECTO_COMPRAS/HISTORIAL/COMPRAS_EXITOSAS/{Datos['nombre']} {datetime.now().date()}.png")  
                Telegram(f"------ Compra Exitosa con {Datos['nombre']} ------")
                Telegram(f"ip:{ip} agente{US}")
                img(Datos)
                excluir(Datos['nombre'])  
                cerrar()
                # CloneMac()
                return True

            except:
                cerrar()
        except:
            print(Fore.RED +  '______ ERROR AL SELECCIONAR CUENTAS _______' + Style.RESET_ALL)
            
            return
    except:
        print('hubo problema con la pagina de compra')
        print('cerrando sesion')
        cerrar()

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
