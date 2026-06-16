import selenium.webdriver.common.by 
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
import FUNCIONES  

## Se usa para ingresar el monto y seleccionar las divisas en el modo madrugadita
montoIngresado = False


def seleccionarElemento(selector):
    # 1. Identifica si usa XPATH o CSS
    by = selenium.webdriver.common.by.By.XPATH if (selector.startswith('/') or selector.startswith('(')) else selenium.webdriver.common.by.By.CSS_SELECTOR
    
    try:
        # Se busca el overlay
        selenium.webdriver.support.ui.WebDriverWait(FUNCIONES.driver, 3).until(
            EC.invisibility_of_element_located((selenium.webdriver.common.by.By.CLASS_NAME, "overlay"))
        )
    except:
        # Si no existe el overlay o ya se quitó
        pass

    # 2. Espera que el elemento sea visible y lo selecciona
    elemento = FUNCIONES.wait.until(EC.visibility_of_element_located((by, selector)))
    
    # 3. Hace scroll para simular humano
    # FUNCIONES.driver.execute_script(
    #    "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", 
    #    elemento
    #)

    # 4. Verifica si es clickeable
    elemento = FUNCIONES.wait.until(EC.element_to_be_clickable((by, selector)))
    
    return elemento

import time
import random

def hacerClick(selector):
    try:
        elemento = seleccionarElemento(selector)
        
        # Pausa aleatoria
        time.sleep(random.uniform(0.1, 0.3))
        
        elemento.click()
    except Exception as e:
        print(f"Error al hacerClick en {selector}: {e}")
        obtenerMensajeError()

def escribir(selector, texto):
    try:
        elemento = seleccionarElemento(selector)
        
        # Se limpia el campo
        elemento.clear()
        
        
        elemento.send_keys(texto)
    except Exception as e:
        print(f"Error al escribir en {selector}: {e}")

def cerrarSesion():
    try:
        hacerClick("/html/body/app/melp-standard-layout/melp-header/div/div[3]/div/div/span")
        hacerClick("//span[text()='Cerrar sesión']")
        
        print("Se cierra la sesión")
    except Exception as e:
        print(f"No se pudo cerrar sesión: {e}")

def llenarFormularioCompra(Datos):
            '''
            try:
                ## Abre Select Desde Mi Cuenta
                hacerClick("#mat-select-0")
            except:
                print('no se presionó Select Desde Mi Cuenta')
            

            if Datos['cuenta'] == 'corriente':
                try:
                    ## Selecciona Cuenta Corriente
                    hacerClick("//div[@id='mat-select-0-panel']//*[contains(text(), 'Cuenta Corriente')]")
                except:
                    print('no se selecciono cuenta corriente')
                    ## Abre nuevamente Select Desde Mi Cuenta
                    hacerClick("#mat-select-0")

            if Datos['cuenta'] == 'ahorro':
                try:
                    ## Selecciona Cuenta Ahorro
                    hacerClick("//div[@id='mat-select-0-panel']//*[contains(text(), 'Cuenta Ahorro')]")
                except:
                    print('no se selecciono cuenta Ahorro')
                    ## Abre nuevamente Select Desde Mi Cuenta
                    hacerClick("#mat-select-3")
                    ##hacerClick("//mat-option//span[contains(text(), 'Fondos Propios')]")
            '''

            ################        ORIGREN DE LOS FONDOS        ################  
            

            try:
                ## Abre Select ORIGREN DE LOS FONDOS
                print("abre Origen de fondos")
                hacerClick('#mat-select-1')
            except:
                print('no se abrió Select ORIGREN DE LOS FONDOS')

            try:
                ## Selecciona Fondos Propios
                hacerClick("#mat-option-3")
            except:
                print('no se selecciono la opcion de Fondos Propios')

            ################        MOTIVO DE LA COMPRA        ################  


            try:
                ## Abre Select MOTIVO DE LA COMPRA 
                hacerClick('#mat-select-2')
            except:
                print('no se abrió select MOTIVO DE LA COMPRA ')

            try:
                hacerClick("//mat-option//*[contains(text(), 'Materia Prima')]")
            except:
                print('no se selecciono la opcion de Materia Prima')

                 
def validarDineroSuficiente(Datos):
            ###### ESCENARIO EN QUE NO TENGA SUFICIENTE DINERO EN LA CUENTA ######
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
                            hacerClick("//div[@id='mat-select-0-panel']//*[contains(text(), 'Cuenta de Ahorro')]")
                            print('se selecciono cuenta Ahorro')
                        except:
                            print('no se selecciono cuenta Ahorro')

                    if Datos['cuenta'] == 'ahorro':
                        try:
                            hacerClick("//div[@id='mat-select-0-panel']//*[contains(text(), 'Cuenta Corriente')]")
                            print('se selecciono cuenta Corriente')
                        except:
                            print('no se selecciono cuenta corriente')
            except:
                print(1)

def seleccionarTipoDivisas():
    xpath_dolares = "//*[contains(text(), 'Dólares')]"
    try:
        hacerClick(xpath_dolares)

    except Exception as e:
        print(f"No se pudo hacer clic en Dólares: {e}")
        #driver.save_screenshot("error_click.png")
        #ups() 
        elementoError = seleccionarElemento(".sub-title")
        print(f"Error: {elementoError.text}")

        cerrarSesion()
        return False
    
def ingresarMonto(Datos):
    global montoIngresado
    if montoIngresado == False:
    
        # Primero selecciona el tipo de moneda o divisa
        seleccionarTipoDivisas()
        try:
            escribir("#buy-foreign-currency-form-first input", Datos['Monto'])
            return True
            
        except:
            print('no se pudo ingresar el monto')
            return False
    
    return True
        
        
def clickComprar():
    try:
        hacerClick('/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[2]/melp-button-wrapper/div/div[2]/button')
        return True
    except:
        print('no se pudo dar click en el botón luego de colocar el monto')
        try:
            obtenerMensajeError()
            return False
        except Exception as e:
            print(f"no se pudo obtener el error {e}")
            return False

    

from cuentas import CUENTAS

def ejecutarCicloCuentas():
    """Procesa las cuentas activas siguiendo la lógica de éxito (True) y error (False)."""
    cuentasActivas = [c for c in CUENTAS if c.get('activo', False)]

    global montoIngresado
    
    if not cuentasActivas:
        return

    for cuenta in cuentasActivas:
        nombre = cuenta['datos']['nombre']
        
        # 1. Verificación de compra previa
        if FUNCIONES.check(nombre):
            continue
            
        print(f'\n{FUNCIONES.Fore.YELLOW} ------ {nombre} ------ {FUNCIONES.Style.RESET_ALL}')
   
        try:
            # 2. Proceso de entrada (Inicio de sesión y navegación)
            FUNCIONES.inicio_sesion(cuenta['inicio'])
            FUNCIONES.ResolverPreguntasSeguridad(cuenta['preguntas'])
            
            # Si MercadoDivisas devuelve False, algo falló (ej: botón no clicable o página caída)
            if not FUNCIONES.MercadoDivisas():
                print(f"Error al entrar a Mercado Divisas para {nombre}")
                cerrarSesion() 
                continue 
            
            montoIngresado = False

            # 3. Sincronización de horario 
            ahora = FUNCIONES.datetime.now()
            if ahora.hour == 6 and ahora.minute < 5:

                ## Se ingresa el monto y se selecciona el tipo de divisa
                if ingresarMonto(cuenta['datos']) == False:
                    return False
                
                montoIngresado = True

                print(f"Esperando apertura (06:05) para {nombre}...")
                while FUNCIONES.datetime.now().minute < 5:
                    time.sleep(1)
            
            # 4. Proceso de compra
            # compra() debe retornar True si fue exitosa o False si falló algo
            exito = FUNCIONES.compra(cuenta['datos'])
            
            if exito:
                print(f"Ciclo completado con éxito para {nombre}")
            else:
                print(f"No se pudo completar la compra para {nombre}")

        except Exception as e:
            print(f"Error crítico en el ciclo de {nombre}: {e}")
            # Si algo explota fuera de los try-except internos, forzamos cierre para no bloquear la siguiente cuenta
            try:
                cerrarSesion()
            except:
                pass
            continue 

    print(f"\n{FUNCIONES.Fore.CYAN}--- Finalizado Ciclo de Cuentas ---{FUNCIONES.Style.RESET_ALL}")
    ejecutarCicloCuentas()


def obtenerMensajeError():
    error = seleccionarElemento(".title").text
    try:
        codigoError = seleccionarElemento('.error-code').text
    except Exception:
        # Si no existe, busca el subtítulo
        codigoError = seleccionarElemento('.subtitle').text

    print(f"Error: {error} {codigoError}")
    cerrarSesion()
    return True 

def tipoMercado():
    # 2. Esperar y detectar el porcentaje/método (Usando tu XPath original)
    xpath_comision = '/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[1]/melp-data-transaction/div/div/div[4]/div[1]'
        
    elemento_porcentaje = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath_comision))
    )
    porcentaje = elemento_porcentaje.text
    print(f"Porcentaje detectado: {porcentaje}")

    # Mapeo de métodos según el texto capturado
    metodos_dict = {
        'Comisión (0,20%) (Bs.)': 'MENUDEO',
        'Comisión (0,12%) (Bs.)': 'MESA DE CAMBIO',
        'Comisión (0,15%) (Bs.)': 'INTERVENCIÓN'
    }
    metodo = metodos_dict.get(porcentaje, 'DESCONOCIDO')
        
    # Registro en estadísticas y logs
    if metodo not in Estadisticas['metodos']:
        Estadisticas['metodos'].append(metodo)

    txt(f' ------- Abierto ------ {metodo} : {datetime.now().hour}:{datetime.now().minute}')
    Telegram(f'------ Formulario Abierto ------ {metodo} ------ Texto porcentaje: {porcentaje}')
    print(f'{Fore.YELLOW} ----------- DATOS DE LA COMPRA ------ {metodo} ----- {Style.RESET_ALL}')