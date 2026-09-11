import io
import os
import re
import sys
import time
import uuid
import random
import platform
import cv2
import requests
import numpy as np
from datetime import datetime

from colorama import init, Fore, Style
from fake_useragent import UserAgent
from multiprocessing import Process

from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Importamos las dependencias locales
import FUNCIONES
import config
from funciones_app import (
    escribir,
    hacerClick,
    seleccionarElemento,
    ingresarMonto,
    clickComprar,
    llenarFormularioCompra,
    cerrarSesion
)

init()

# ==========================================
# 1. CONFIGURACIÓN DE CUENTAS Y PROXIES
# ==========================================
PROXYS = {
    'local': None,
    'ray': 'socks5://100.78.148.101:1080',
    'tecno': 'socks5://100.67.185.66:1080',
}

CUENTAS = [
    {
        'nombre_id': 'KAREN',
        'proxy': 'local',
        'activo': True,
        'datos': {
            '2_Cuentas': False, 'cuenta': 'corriente', 'nombre': 'KAREN',
            'CHAT_ID': '@none', 'Monto': 2000,
            'cuentaCash': 2311, 'cuentaElectronica': 3016,
            'mecanismo': {'menudeo': (None, 'C'), 'intervencion': 100000}
        },
        'inicio': {'usuario': 'karenlucena31', 'contrasena': 'Dios.1234', 'id': 'KAREN'},
        'preguntas': {'PreguntaUnica': True, 'RespuestaUnica': "karen"}
    },
    {
        'nombre_id': 'MIGUEL',
        'proxy': 'ray',
        'activo': True,
        'datos': {
            '2_Cuentas': False, 'cuenta': 'corriente', 'nombre': 'MIGUEL',
            'CHAT_ID': '@none',
            'cuentaCash': 5583, 'cuentaElectronica': 3768,
            'mecanismo': {'menudeo': (2000, 'C'), 'intervencion': None}
        },
        'inicio': {'usuario': 'arneirys14', 'contrasena': 'Arneirys35*', 'id': 'MIGUEL'},
        'preguntas': {'PreguntaUnica': True, 'RespuestaUnica': "miguel"}
    }
]

# ==========================================
# 2. TEMPORIZADOR DE ALTA PRECISIÓN NO BLOQUEANTE
# ==========================================
def esperar_hasta(hora_objetivo, min_objetivo, seg_objetivo=0):
    ahora = datetime.now()
    objetivo = ahora.replace(hour=hora_objetivo, minute=min_objetivo, second=seg_objetivo, microsecond=0)
    
    if ahora > objetivo:
        print(f"{Fore.CYAN}La hora {hora_objetivo:02d}:{min_objetivo:02d}:{seg_objetivo:02d} ya pasó hoy.{Style.RESET_ALL}")
        return

    print(f"{Fore.YELLOW}Esperando hora exacta: {hora_objetivo:02d}:{min_objetivo:02d}:{seg_objetivo:02d}...{Style.RESET_ALL}")
    
    while True:
        ahora = datetime.now()
        restante = (objetivo - ahora).total_seconds()
        if restante <= 0:
            break
        elif restante > 2:
            time.sleep(0.5)
        else:
            time.sleep(0.01)

# ==========================================
# 3. FUNCIONES AUXILIARES Y DE FLUJO
# ==========================================
def Telegram(MSG):
    token = "8167604613:AAFPFgIwMbZFBpnz4hO4p9FzK1-n52VSIIs"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    for cid in ["6231499420", "7781699329"]:
        try:
            requests.post(url, data={"chat_id": cid, "text": MSG})
        except Exception as e:
            print(f"Error enviando Telegram: {e}")

def img(Datos):
    try:
        png_bytes = FUNCIONES.driver.get_screenshot_as_png()
        nparr = np.frombuffer(png_bytes, np.uint8)
        imagen_cv2 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        is_success, buffer = cv2.imencode(".png", np.asarray(imagen_cv2))
        imagen_en_bytes = buffer.tobytes()

        TOKEN = "8167604613:AAFPFgIwMbZFBpnz4hO4p9FzK1-n52VSIIs"
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        
        destinatarios = [
            ("6231499420", f'💲 Compra Exitosa con {Datos["nombre"]}'), 
            ("7781699329", f'💲 Compra Exitosa con {Datos["nombre"]}')
        ]

        for chat_id, caption in destinatarios:
            try:
                foto_stream = io.BytesIO(imagen_en_bytes)
                payload = {"chat_id": chat_id, "caption": caption}
                files = {"photo": ("captura.png", foto_stream, "image/png")}
                requests.post(url, data=payload, files=files)
            except Exception as e:
                print(f"Error imagen Telegram: {e}")
    except Exception as e:
        print(f"No se pudo capturar/enviar imagen: {e}")

def obtener_ip_publica_navegador(nombre_id):
    """Obtiene y muestra la IP pública activa en la sesión del bot al inicio."""
    try:
        FUNCIONES.driver.get("https://api.ipify.org?format=json")
        body_text = FUNCIONES.wait.until(EC.presence_of_element_located((By.TAG_NAME, "pre"))).text
        ip_detectada = re.search(r'\d+\.\d+\.\d+\.\d+', body_text).group(0)
        print(f"{Fore.MAGENTA}🌐 [{nombre_id}] IP PÚBLICA ACTIVA: {ip_detectada}{Style.RESET_ALL}")
        return ip_detectada
    except Exception as e:
        print(f"{Fore.YELLOW}[{nombre_id}] No se pudo obtener IP pública inicial: {e}{Style.RESET_ALL}")
        return "Desconocida"

def inicio_sesion_local(Inicio):
    US = UserAgent().random
    print(f"{Fore.YELLOW}[{Inicio['id']}] Agente:{Style.RESET_ALL} {US}")
    
    FUNCIONES.driver.get("https://www30.mercantilbanco.com/login")
    
    try:
        print(f"[{Inicio['id']}] Ingresando credenciales...")
        if escribir("#username", Inicio['usuario']) == False:
            return False
        escribir("#password", Inicio['contrasena'])
        hacerClick(".button-wrapper__btn-primary")
    except Exception as e:
        print(f"Reintentando login para {Inicio['id']}: {e}")
        FUNCIONES.driver.get("https://www30.mercantilbanco.com/login")
        escribir("#username", Inicio['usuario'])
        escribir("#password", Inicio['contrasena'])
        hacerClick(".button-wrapper__btn-primary")

    try:
        FUNCIONES.driver.execute_script("""
            let style = document.createElement('style');
            style.id = 'kill-animations';
            style.innerHTML = `*, *::before, *::after { transition: none !important; animation: none !important; }`;
            document.head.appendChild(style);
        """)
    except Exception:
        pass

    return True

def ResolverPreguntasSeguridad_local(Preguntas):
    try:
        print('Resolviendo Preguntas de Seguridad')
        
        mensajes_error = [
            'El tiempo de tu sesión ha finalizado.',
            '¡Lamentamos las molestias ocasionadas!',
            'Por tu seguridad hemos cerrado esta sesión.'
        ]

        try:
            # CASO 1: PREGUNTA ÚNICA
            if Preguntas.get('PreguntaUnica') is True:
                elemento = seleccionarElemento(
                    '//*[@id="mat-input-3"] | '
                    '//*[contains(text(), "El tiempo de tu sesión ha finalizado.")] | '
                    '//*[contains(text(), "¡Lamentamos las molestias ocasionadas!")] | '
                    '//*[contains(text(), "Por tu seguridad hemos cerrado esta sesión.")]'
                )
                
                if elemento.text.strip() in mensajes_error:
                    print(f'{Fore.RED}{elemento.text.strip()} {datetime.now().strftime("%H:%M")}{Style.RESET_ALL}')
                    return False
                else:
                    elemento.clear()
                    elemento.send_keys(Preguntas['RespuestaUnica'])
                    escribir("#mat-input-2", Preguntas['RespuestaUnica'])

            # CASO 2: PREGUNTAS MÚLTIPLES
            else:
                elemento = seleccionarElemento(
                    '//*[@id="question-1"] | '
                    '//*[contains(text(), "El tiempo de tu sesión ha finalizado.")] | '
                    '//*[contains(text(), "¡Lamentamos las molestias ocasionadas!")] | '
                    '//*[contains(text(), "Por tu seguridad hemos cerrado esta sesión.")]'
                )

                if elemento.text.strip() in mensajes_error:
                    print(f'{Fore.RED}{elemento.text.strip()} {datetime.now().strftime("%H:%M")}{Style.RESET_ALL}')
                    return False

                # Mapa dinámico de preguntas -> respuestas
                mapa_respuestas = {
                    Preguntas.get(f'pregunta{i}'): Preguntas.get(f'respuesta{i}')
                    for i in range(1, 6)
                    if Preguntas.get(f'pregunta{i}') and Preguntas.get(f'respuesta{i}')
                }

                # --- PROCESAR PREGUNTA 1 ---
                texto_p1 = elemento.text.strip()
                if texto_p1 in mapa_respuestas:
                    input_p1 = FUNCIONES.wait.until(EC.presence_of_element_located((By.ID, "mat-input-2")))
                    input_p1.clear()
                    input_p1.send_keys(mapa_respuestas[texto_p1])

                # --- PROCESAR PREGUNTA 2 ---
                q2_elem = FUNCIONES.wait.until(EC.presence_of_element_located((By.ID, 'question-2')))
                texto_p2 = q2_elem.text.strip()
                
                if texto_p2 in mapa_respuestas:
                    input_p2 = FUNCIONES.wait.until(EC.presence_of_element_located((By.ID, "mat-input-3")))
                    input_p2.clear()
                    input_p2.send_keys(mapa_respuestas[texto_p2])

        except Exception as e:
            print(f'No encontró el elemento o falló al ingresar respuestas: {e}')
            return False

        # --- BOTÓN DE ENVIAR / CONTINUAR ---
        xpath_boton = "/html/body/app/melp-standard-layout/div/div/melp-secure-access/melp-standard-card-layout/div/div/div[1]/div/div/melp-connection-type/form/div/div[2]"
        btn_continuar = FUNCIONES.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_boton)))
        btn_continuar.click()
        return True

    except Exception as e:
        print(f'Hubo un problema ingresando las preguntas de seguridad: {e}')
        return False

def MercadoDivisas_local():
    try:
        xpath_mercado = "//*[contains(text(), 'Mercado de divisas')]"
        boton_mercado = FUNCIONES.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_mercado)))
        FUNCIONES.driver.execute_script("arguments[0].click();", boton_mercado)
        time.sleep(1)

        xpath_compra = "//*[contains(text(), 'Compra de divisas')]"
        boton_compra = FUNCIONES.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_compra)))
        FUNCIONES.driver.execute_script("arguments[0].click();", boton_compra)
        print(f"{Fore.GREEN}Pantalla Compra de Divisas alcanzada.{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}Fallo navegación a Mercado: {e}{Style.RESET_ALL}")
        return False

def verificar_finalizacion_local(Datos, fecha_inicio):
    """
    Validación estricta de resultado para evitar falsos positivos por Código 10 o rechazos.
    """
    try: 
        elemento_resultado = FUNCIONES.wait.until(
            EC.presence_of_element_located((
                By.XPATH, 
                "//*[contains(text(), '¡Listo! Compra realizada') or "
                "contains(text(), 'La compra no fue exitosa') or "
                "contains(text(), 'no es posible realizar tu operación') or "
                "contains(text(), 'Código 10')]"
            ))
        )
        texto_resultado = elemento_resultado.text.strip()
        texto_pagina = FUNCIONES.driver.find_element(By.TAG_NAME, "body").text

        # REGLA 1: Descarte de rechazos o Código 10
        if "no fue exitosa" in texto_pagina.lower() or "código 10" in texto_pagina.lower() or "no es posible realizar" in texto_pagina.lower():
            print(f"{Fore.RED}❌ ERROR EN COMPRA [{Datos['nombre']}]: La operación falló (Código 10 o rechazo detectado).{Style.RESET_ALL}")
            return False

        # REGLA 2: Confirmación estricta de éxito
        if "¡listo! compra realizada" in texto_resultado.lower() or "operación exitosa" in texto_resultado.lower():
            segundos = (datetime.now() - fecha_inicio).total_seconds()
            print(f"{Fore.GREEN}¡ÉXITO CONFIRMADO! {Datos['nombre']} compró en {segundos:.2f}s{Style.RESET_ALL}")
            img(Datos)
            Telegram(f"------ Compra Exitosa con {Datos['nombre']} ------")
            return True

        print(f"{Fore.RED}No se pudo confirmar éxito explícito para {Datos['nombre']}. Texto: {texto_resultado}{Style.RESET_ALL}")
        return False

    except Exception as e:
        print(f"{Fore.RED}Excepción al verificar resultado de la compra: {e}{Style.RESET_ALL}")
        return False

def preparacion_y_disparo_compra(Datos):
    # 1. CARGA PREVIA DEL MONTO (ANTES DE 06:05 AM)
    m_menudeo = Datos['mecanismo']['menudeo']
    if m_menudeo and m_menudeo[0] is not None:
        print(f"[{Datos['nombre']}] Ingresando monto: {m_menudeo[0]} USD...")
        if ingresarMonto(m_menudeo[0]) == False:
            return False
    
    print(f"{Fore.CYAN}[{Datos['nombre']}] Formulario listo. Aguardando 06:05:00 AM para el click simultáneo...{Style.RESET_ALL}")
    
    # 2. ESPERA PRECISA A LAS 06:05:00 AM
    esperar_hasta(hora_objetivo=6, min_objetivo=5, seg_objetivo=0)

    # 3. DISPARO SIMULTÁNEO
    print(f"{Fore.GREEN}🚀 [{Datos['nombre']}] ¡CLICK EN COMPRAR! ({datetime.now().strftime('%H:%M:%S.%f')}){Style.RESET_ALL}")
    clickComprar()
    fecha_inicio = datetime.now()
    
    # 4. FINALIZAR FORMULARIO
    if llenarFormularioCompra(Datos) == False:
        return False

    return verificar_finalizacion_local(Datos, fecha_inicio)

# ==========================================
# 4. WORKER DE CADA NAVEGADOR (VENTANA ÚNICA)
# ==========================================
def worker_bot(cuenta_config):
    nombre = cuenta_config['nombre_id']
    proxy_clave = cuenta_config['proxy']
    proxy_url = PROXYS.get(proxy_clave)
    
    instancia_id = str(uuid.uuid4())[:8]
    modo_headless = False

    chrome_args = [
        "--no-first-run",
        "--no-service-autorun",
        "--password-store=basic",
        "--disable-blink-features=AutomationControlled"
    ]

    if platform.system() != "Windows":
        version_driver = "system"
        chrome_args.extend([
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            f"--user-data-dir=/tmp/chrome_{instancia_id}"
        ])
        os_binary_location = "/usr/bin/chromium"
    else:
        version_driver = "keep"
        chrome_args.extend([
            "--ignore-certificate-errors",
            "--disable-web-security"
        ])
        os_binary_location = None

    N1, N2 = random.randint(1000, 1200), random.randint(800, 1000)

    # EVITA DUPLICADOS CON uc_subprocess=False
    driver_instancia = Driver(
        proxy=proxy_url,
        uc=True,
        uc_subprocess=False,
        block_images=False,
        window_size=f"{N1},{N2}",
        headless=modo_headless,
        chromium_arg=",".join(chrome_args),
        binary_location=os_binary_location,
        disable_csp=True,
        incognito=True,
        pls="none",
        driver_version=version_driver
    )

    wait_instancia = WebDriverWait(driver_instancia, 15)

    # Asignación de variables al módulo global de funciones
    FUNCIONES.driver = driver_instancia
    FUNCIONES.wait = wait_instancia

    try:
        # 1. REGISTRO DE IP PÚBLICA EN LOGS AL ARRANCAR
        obtener_ip_publica_navegador(nombre)

        print(f"[{nombre}] Navegador listo. Esperando hora de login (06:03 AM)...")
        esperar_hasta(hora_objetivo=6, min_objetivo=3, seg_objetivo=0)

        print(f"[{nombre}] Iniciando sesión...")
        if inicio_sesion_local(cuenta_config['inicio']):
            if ResolverPreguntasSeguridad_local(cuenta_config['preguntas']):
                if MercadoDivisas_local():
                    preparacion_y_disparo_compra(cuenta_config['datos'])
    except Exception as e:
        print(f"[{nombre}] Error durante la ejecución: {e}")
    finally:
        print(f"[{nombre}] Cerrando ventana de navegador...")
        try:
            cerrarSesion()
        except Exception:
            pass
        driver_instancia.quit()

# ==========================================
# 5. INICIO DE PROCESOS
# ==========================================
if __name__ == '__main__':
    procesos = []

    print("Iniciando procesos concurrentes...")
    for cta in CUENTAS:
        if cta['activo']:
            p = Process(target=worker_bot, args=(cta,))
            procesos.append(p)
            p.start()

    for p in procesos:
        p.join()

    print("Ejecución finalizada.")