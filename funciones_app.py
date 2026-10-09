import asyncio
import time
import random
import selenium.webdriver.common.by 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import FUNCIONES
from cuentas import CUENTAS

montoIngresado = False

def seleccionarElemento(selector, time_wait=3):
    by = selenium.webdriver.common.by.By.XPATH if (selector.startswith('/') or selector.startswith('(')) else selenium.webdriver.common.by.By.CSS_SELECTOR
    
    try:
        selenium.webdriver.support.ui.WebDriverWait(FUNCIONES.driver, time_wait).until(
            EC.invisibility_of_element_located((selenium.webdriver.common.by.By.CLASS_NAME, "overlay"))
        )
    except Exception:
        pass

    elemento = FUNCIONES.wait.until(EC.visibility_of_element_located((by, selector)))
    elemento = FUNCIONES.wait.until(EC.element_to_be_clickable((by, selector)))
    return elemento

def hacerClick(selector, show=True):
    try:
        elemento = seleccionarElemento(selector)
        time.sleep(random.uniform(0.1, 0.3))
        elemento.click()
        return True
    except Exception as e:
        if show:
            print(f"Error al hacerClick en {selector}: {e}")
        return False

def escribir(selector, texto):
    try:
        elemento = seleccionarElemento(selector)
        elemento.clear()
        elemento.send_keys(texto)
        return True
    except Exception as e:
        print(f"Error al escribir en {selector}: {e}")
        return False

def cerrarSesion():
    try:
        hacerClick("/html/body/app/melp-standard-layout/melp-header/div/div[3]/div/div/span")
        hacerClick("//span[text()='Cerrar sesión']")
        print("Se cierra la sesión")
    except Exception as e:
        print(f"No se pudo cerrar sesión: {e}")

def llenarFormularioCompra(Datos):
    fecha_inicio = FUNCIONES.datetime.now()
    segundos = fecha_inicio.second
    milesimas = fecha_inicio.microsecond // 1000

    try:
        msj_pass = seleccionarElemento('//*[@id="mat-select-value-0"]/span | //*[contains(text(), "En estos momentos no hay disponibilidad de divisas para realizar la operación.")] | //*[contains(text(), "Algo ha salido mal...")] | //*[contains(text(), "En este momento el Mercado de divisas se encuentra cerrado")] | //*[contains(text(), "El tiempo de tu sesión ha finalizado.")] | //*[contains(text(), "¡Lamentamos las molestias ocasionadas!")] ')

        if msj_pass.tag_name == 'span':
            msj_pass.click()

        if msj_pass.tag_name == 'div':
            print(f'{FUNCIONES.Fore.RED} {msj_pass.text} {FUNCIONES.datetime.now().hour}:{FUNCIONES.datetime.now().minute} {FUNCIONES.Style.RESET_ALL}')
            cerrarSesion()
            return False
    except Exception:
        print('no se pudo hacer click en el select de DESDE MI CUENTA')

    if Datos['cuenta'] == 'corriente':
        try:
            hacerClick("//div[@id='mat-select-0-panel']//*[contains(text(), 'Cuenta Corriente')]")
        except Exception:
            print('no se selecciono cuenta corriente')

    if Datos['cuenta'] == 'ahorro':
        try:
            hacerClick("//div[@id='mat-select-0-panel']//*[contains(text(), 'Cuenta de Ahorro')]")
        except Exception:
            print('no se selecciono cuenta ahorro')

    try:
        mecanismo = seleccionarElemento('//*[contains(text(), "Comisión (0,50%) (Bs.)")] | //*[contains(text(), "Comisión (0,20%) (Bs.)")]').text

        if mecanismo == "Comisión (0,50%) (Bs.)":
            print('Activa Intervencion Electronica')
            try:
                FUNCIONES.driver.execute_script(f"""            
            document.querySelector('#mat-select-1').click();
            document.querySelector('#mat-option-3').click();
            
            document.querySelector('#mat-select-2').click();
            document.querySelector('#mat-option-14').click();
            """)
            except Exception:
                print('no se ejecuto el script ORIGEN DE LOS FONDOS')
        elif mecanismo == "Comisión (0,20%) (Bs.)":
            print('Formulario Menudeo')    
            CtaUsd = 'Cuenta Moneda Extranjera USD - ••••'
            if Datos['mecanismo']['menudeo'][1] == 'C':
                CtaUsd += str(Datos['cuentaCash'])
            elif Datos['usarCuenta'] == 'E':
                CtaUsd += str(Datos['cuentaElectronica'])
            try:
                FUNCIONES.driver.execute_script(f"""
        document.querySelector('#mat-select-value-3').click();  
        document.evaluate('//mat-option//*[contains(text(), "{CtaUsd}")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();
        
        document.querySelector('#mat-select-1').click();
        document.querySelector('#mat-option-3').click();
        
        document.querySelector('#mat-select-2').click();
        document.querySelector('#mat-option-14').click();
        """)
            except Exception:
                print('no se ejecuto el script ORIGEN DE LOS FONDOS')
    except Exception as e:
        print(f'error except: {e}')

    

    try:
        if not hacerClick('/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[2]/melp-button-wrapper/div/div[2]/button[2]'):
            print('no se pudo presionar el boton de continuar')
            try:  
                seleccionarElemento("//*[contains(text(), 'El monto a comprar es mayor al saldo disponible de tu cuenta.')]")
                print(f"{FUNCIONES.Fore.RED} ------ El monto a comprar es mayor al saldo en la cuenta de {Datos['cuenta']} ------ {FUNCIONES.Style.RESET_ALL}")
                if Datos.get('2_Cuentas'):
                    print(FUNCIONES.Fore.YELLOW + '------ Cambiando Cuenta ------' + FUNCIONES.Style.RESET_ALL)
                    try:
                        seleccionarElemento('//*[@id="mat-select-0"]').click()
                    except Exception:
                        pass
                    
                    if Datos['cuenta'] == 'corriente':
                        try:
                            hacerClick("//div[@id='mat-select-0-panel']//*[contains(text(), 'Cuenta de Ahorro')]")
                            if not hacerClick('/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[2]/melp-button-wrapper/div/div[2]/button[2]'):
                                verificacionBalance(Datos)
                                cerrarSesion()
                                return False
                        except Exception:
                            pass

                    if Datos['cuenta'] == 'ahorro':
                        try:
                            hacerClick("//div[@id='mat-select-0-panel']//*[contains(text(), 'Cuenta Corriente')]")
                            if not hacerClick('/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[2]/melp-button-wrapper/div/div[2]/button[2]'):
                                FUNCIONES.Telegram("------ No se pudo continuar por fondo insuficiente ------")
                                verificacionBalance(Datos)
                                cerrarSesion()
                                return False
                        except Exception:
                            pass
                else:
                    verificacionBalance(Datos)
                    cerrarSesion()
                    return False
            except Exception:      
                print('hay dinero en la cuenta pero hubo un error el formulario')
    except Exception:
        print('no se presionó el boton')

    try:
        hacerClick('/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[2]/melp-button-wrapper/div/div[2]/button[2]')
    except Exception:
        pass

    try:
        FUNCIONES.driver.execute_script("""const click = path => new Promise(res => {
  const i = setInterval(() => {
    const el = document.evaluate(path, document, null, 9, null).singleNodeValue;
    if (el) { clearInterval(i); el.click(); res(); }
  }, 100);
});

(async () => {
  await click('//*[@id="mat-mdc-checkbox-0-input"]');
  await click('/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[2]/melp-button-wrapper/div/div[2]/button[2]');
})();""")
    except Exception:
        pass

    return True

def verificacionBalance(Datos):
    try:
        seleccionarElemento("//*[contains(text(), 'Resumen financiero')]")
    except Exception:
        FUNCIONES.driver.get("https://www30.mercantilbanco.com/summary")

    listaBalancesSucios = []
    Balances = []
    for idx in range(2, 5):
        try:
            bal = seleccionarElemento(f"//*[@id='summary']/div/div[1]/melp-summary-all-products/melp-product-list-detail[1]/div/div[{idx}]").text 
            listaBalancesSucios.append(bal)
        except Exception:
            pass

    USD = ""
    try:
        balanceUSD = (((seleccionarElemento("//*[@id='summary']/div/div[1]/melp-summary-all-products/melp-product-list-detail[2]/div/div[3]").text).strip())).split('\n')
        USD = f"{balanceUSD[0]} -> Saldo: {balanceUSD[3]} $."
    except Exception:
        pass

    try:
        for balance_individual in listaBalancesSucios:
            lineas = [linea.strip() for linea in balance_individual.strip().split('\n') if linea.strip()]
            nombre_cuenta = lineas[0]
            monto_cuenta = lineas[3] 
            Balances.append(f"{nombre_cuenta} -> Saldo: {monto_cuenta} Bs.")

        balancesTotales = "\n".join(Balances)
        MSJ = f"--- BALANCE DE LA CUENTA {Datos['nombre']}--- \n{balancesTotales}\n{USD}"
        print(MSJ)
        FUNCIONES.Telegram(MSJ)
    except Exception as e:
        print(f"No se pudo verificar el balance: {e}")

def seleccionarTipoDivisas():
    xpath_dolares = "//*[contains(text(), 'Dólares')]"
    try:
        Intentos = 0
        while not hacerClick(xpath_dolares, show=False) and Intentos < 3:
            if FUNCIONES.VerMensaje():
                return False
            time.sleep(1)
            Intentos += 1
        return True
    except Exception:
        return False

def ingresarMonto(Datos):
    global montoIngresado
    if not montoIngresado:
        if not seleccionarTipoDivisas():
            return False
        try:
            escribir("#buy-foreign-currency-form-first input", str(Datos))
            return True
        except Exception:
            return False
    return True

def clickComprar():
    try:
        hacerClick('/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[2]/melp-button-wrapper/div/div[2]/button')
        return True
    except Exception:
        return False


# FUNCIONES ASYNCRONAS

async def ingresoPuntualAsync(hora, minuto=0, nombre='alguien', cuenta=None):
    ahora = FUNCIONES.datetime.now()

    if (cuenta['datos']['mecanismo']['intervencion'] is None and cuenta['datos']['mecanismo']['menudeo'][0] is not None) or \
       (cuenta['datos']['mecanismo']['intervencion'] is not None and cuenta['datos']['mecanismo']['menudeo'][0] is None):

        if ahora.hour < hora or (ahora.hour == hora and ahora.minute <= minuto):
            print(f"Instancia iniciada, esperando para iniciar sesion a las {hora}:{minuto} con {nombre}...")
            while (FUNCIONES.datetime.now().hour < 6) or \
                  (FUNCIONES.datetime.now().hour <= 6 and FUNCIONES.datetime.now().minute < minuto) or \
                  (FUNCIONES.datetime.now().hour < hora) or \
                  (FUNCIONES.datetime.now().hour == hora and FUNCIONES.datetime.now().minute < minuto): 
                await asyncio.sleep(1)
        return

    if cuenta['datos']['mecanismo']['intervencion'] is not None and cuenta['datos']['mecanismo']['menudeo'][0] is not None:
        if (ahora.hour == hora and ((minuto - 3) <= ahora.minute <= minuto)) or ahora.hour < 6 or (ahora.hour == 6 and ahora.minute < 5):
            print(f"Instancia iniciada, esperando para iniciar sesion a las {hora}:{minuto} con {nombre}...")
            while (FUNCIONES.datetime.now().hour <= 5) or (FUNCIONES.datetime.now().hour == 6 and FUNCIONES.datetime.now().minute < minuto):
                await asyncio.sleep(1)

async def compraPuntualAsync(hora, minuto, nombre, monto):
    global montoIngresado
    
    ahora = FUNCIONES.datetime.now()

    # Si estamos en la hora esperada y aun no hemos llegado al minuto de apertura (osea: son las 8:20 y abren a las 8:30)
    if ahora.hour == hora and ahora.minute < minuto:
        # 1. se ingresa el monto para estar ready
        if not ingresarMonto(monto):
            return False

        montoIngresado = True
        print(f"{FUNCIONES.Fore.YELLOW}Esperando apertura de las {hora}:{minuto:02d} para {nombre}...{FUNCIONES.Style.RESET_ALL}")

        # 2. Bucle asyncrono para que no afecte al monitor de sesion activa
        while True:
            momento_actual = FUNCIONES.datetime.now()
            if momento_actual.hour > hora or (momento_actual.hour == hora and momento_actual.minute >= minuto):
                print(f"{FUNCIONES.Fore.GREEN} Procediendo con la compra...{FUNCIONES.Style.RESET_ALL}")
                break
            await asyncio.sleep(1)

    # si de casualidad la función se ejecuta justo en el minuto o después, se asegura el monto. Uno es salado, hay que prevenir
    elif ahora.hour == hora and ahora.minute >= minuto:
        if not ingresarMonto(monto):
            return False
        montoIngresado = True

async def ejecutarCicloCuentas():
    """La misma funcion para procesar las cuentas pero asyncrona para que no afecte al monitor"""
    global montoIngresado

    cuentasActivas = [
        c for c in CUENTAS 
        if c.get('activo', False) and not FUNCIONES.check(c.get('nombre_id'))
    ]

    if not cuentasActivas:
        print('No hay cuentas activas, finalizando el programa...')
        return

    session_bot = await FUNCIONES.MercantilSeleniumSession.get_instance()

    for cuenta in cuentasActivas[:]:
        nombre = cuenta['datos']['nombre']

        if FUNCIONES.check(nombre):
            continue

        if cuenta['datos']['mecanismo']['intervencion'] is None and cuenta['datos']['mecanismo']['menudeo'][0] is None:
            print(f'{FUNCIONES.Fore.RED}No hay monto ingresado para ningún mecanismo en la cuenta de {nombre}{FUNCIONES.Style.RESET_ALL}')
            cuentasActivas.remove(cuenta)
            continue

        print(f'{FUNCIONES.Fore.YELLOW}IP:{FUNCIONES.Fore.RED}{FUNCIONES.ipProxys()}{FUNCIONES.Style.RESET_ALL}')
        await ingresoPuntualAsync(6, 3, nombre, cuenta)

        if cuenta['datos']['mecanismo']['intervencion'] is not None and cuenta['datos']['mecanismo']['menudeo'][0] is None:
            await ingresoPuntualAsync(8, 20, nombre, cuenta)

        print(f'\n{FUNCIONES.Fore.YELLOW} ------ {nombre} ------ {FUNCIONES.Style.RESET_ALL}')

        try:
            #Inicio de sesión
            login_exito = await asyncio.to_thread(FUNCIONES.inicio_sesion, cuenta['inicio'])
            
            if not login_exito:
                print(f"{FUNCIONES.Fore.RED}Falló el inicio de sesión para {nombre}. Pasando a la siguiente cuenta.{FUNCIONES.Style.RESET_ALL}")
                continue

            # Preguntas de seguridad
            preguntas_exito = await asyncio.to_thread(FUNCIONES.ResolverPreguntasSeguridad, cuenta['preguntas'])
            
            if not preguntas_exito:
                print(f"{FUNCIONES.Fore.RED}Falló la resolución de preguntas de seguridad para {nombre}.{FUNCIONES.Style.RESET_ALL}")
                continue

            # INICIANDO MONITOR DE SESION ACTIVA
            session_bot.iniciar_monitor()

            # Mercado Divisas
            if not await asyncio.to_thread(FUNCIONES.MercadoDivisas):
                print(f"{FUNCIONES.Fore.RED}Error al entrar a Mercado Divisas para {nombre}{FUNCIONES.Style.RESET_ALL}")
                await asyncio.to_thread(cerrarSesion)
                continue 

            montoIngresado = False

            # Esperas de horario y Compra
            await compraPuntualAsync(6, 5, nombre, cuenta['datos']['mecanismo']['menudeo'][0])

            if cuenta['datos']['mecanismo']['intervencion'] is not None:
                await compraPuntualAsync(8, 30, nombre, cuenta['datos']['mecanismo']['intervencion'])

            print("[4] Ejecutando formulario y confirmación de compra...")
            exito = await asyncio.to_thread(FUNCIONES.compra, cuenta['datos'])

            if exito:
                print(f"{FUNCIONES.Fore.GREEN}¡Ciclo completado con éxito para {nombre}!{FUNCIONES.Style.RESET_ALL}")
                cuentasActivas.remove(cuenta)
            else:
                print(f"{FUNCIONES.Fore.RED}No se pudo completar la compra para {nombre}{FUNCIONES.Style.RESET_ALL}")

        except Exception as e:
            print(f"{FUNCIONES.Fore.RED}Error crítico en el ciclo de {nombre}: {e}{FUNCIONES.Style.RESET_ALL}")
            try:
                await asyncio.to_thread(cerrarSesion)
            except Exception:
                pass
            continue 

    # Detener monitor al completar la ronda de la lista
    await session_bot.detener_monitor()

    if not cuentasActivas:
        print(f'{FUNCIONES.Fore.BLUE}No hay más cuentas activas, finalizando el programa...{FUNCIONES.Style.RESET_ALL}')
        return

    print(f"\n{FUNCIONES.Fore.CYAN}--- Finalizado Ciclo de Cuentas ---{FUNCIONES.Style.RESET_ALL}")
    
    # Siguiente ciclo
    await ejecutarCicloCuentas()