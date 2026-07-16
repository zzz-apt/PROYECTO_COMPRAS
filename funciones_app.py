import selenium.webdriver.common.by 
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
import FUNCIONES  

## Se usa para ingresar el monto y seleccionar las divisas en el modo madrugadita
montoIngresado = False


def seleccionarElemento(selector, time=3):
    # 1. Identifica si usa XPATH o CSS
    by = selenium.webdriver.common.by.By.XPATH if (selector.startswith('/') or selector.startswith('(')) else selenium.webdriver.common.by.By.CSS_SELECTOR
    
    try:
        # Se busca el overlay
        selenium.webdriver.support.ui.WebDriverWait(FUNCIONES.driver, time).until(
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

def hacerClick(selector, show=True):
    
    try:
        elemento = seleccionarElemento(selector)
        
        # Pausa aleatoria
        time.sleep(random.uniform(0.1, 0.3))
        
        elemento.click()
        return True
    except Exception as e:
        if show:
            print(f"Error al hacerClick en {selector}: {e}")
        else:
            None
        return False
    
        
    

def escribir(selector, texto):
    try:
        elemento = seleccionarElemento(selector)
        
        # Se limpia el campo
        elemento.clear()
        
        
        elemento.send_keys(texto)
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

    ################        DESDE MI CUENTA        ################
  
    fecha_inicio = FUNCIONES.datetime.now()
    hora = fecha_inicio.hour
    minutos = fecha_inicio.minute
    segundos = fecha_inicio.second
    milesimas = fecha_inicio.microsecond // 1000
    try:
        msj_pass = seleccionarElemento('//*[@id="mat-select-value-0"]/span | //*[contains(text(), "En estos momentos no hay disponibilidad de divisas para realizar la operación.")] | //*[contains(text(), "Algo ha salido mal...")]' )

        
        if msj_pass.tag_name == 'span':
            msj_pass.click()

        if msj_pass.tag_name == 'div':
            print(f'{FUNCIONES.Fore.RED} {msj_pass.text} {FUNCIONES.datetime.now().hour}:{FUNCIONES.datetime.now().minute} {FUNCIONES.Style.RESET_ALL}')
            cerrarSesion()
            return False
                
    except:
        print('no se pudo hacer click en el select de DESDE MI CUENTA')
        input()
        
    if Datos['cuenta'] == 'corriente': #verifica si en Datos tiene el tipo de cuenta corriente o ahorro y la seleeciona
        try:
            hacerClick("//div[@id='mat-select-0-panel']//*[contains(text(), 'Cuenta Corriente')]")
        except:
                print('no se selecciono cuenta corriente')
                hacerClick('mat-select-0')

    if Datos['cuenta'] == 'ahorro':
        try:
            hacerClick("//div[@id='mat-select-0-panel']//*[contains(text(), 'Cuenta de Ahorro')]")
            print('se selecciono cuenta ahorro')
        except:
            print('no se selecciono cuenta ahorro')
            hacerClick('mat-select-0')

    
    ################        A MI CUENTA        ################
    if FUNCIONES.datetime.now().hour == 8: #seleccionar Cuenta extrajera SOLO cuando es hora de la venta de electronicos
        
        try:
            hacerClick("#mat-select-3") #hace click para elegir cuentas divisas
            #print('se selecciono btn para elegir cuenta en divisas')
        except:
            print('no se pudo abrir el select de A MI CUENTA')

        try:
            hacerClick('//mat-option//*[contains(text(), "Cuenta Moneda Extranjera USD - •")]') #hace click para elegir cuentas divisas
            #print('se selecciono cuenta moneda extranjera')
        except:
            print('no se pudo seleccionar la cuenta moneda extranjera')
    



            ################        ORIGREN DE LOS FONDOS        ################  


    try:
        ## Abre Select ORIGREN DE LOS FONDOS y click
        #print("abre Origen de fondos")
        FUNCIONES.driver.execute_script("""
            document.querySelector('#mat-select-1').click();
            document.querySelector('#mat-option-3').click();
        """)
    except:
        print('no se ejecuto el script ORIGREN DE LOS FONDOS')

    # try:
    #     ## Abre Select ORIGREN DE LOS FONDOS
    #     hacerClick('#mat-select-1')
    # except:
    #     print('no se abrió Select ORIGREN DE LOS FONDOS')

    # try:
    #     ## Selecciona Fondos Propios
    #     hacerClick("#mat-option-3")
    # except:
    #     print('no se selecciono la opcion de Fondos Propios')

    ################        MOTIVO DE LA COMPRA        ################  


    try:
        FUNCIONES.driver.execute_script("""
            document.querySelector('#mat-select-2').click();
            document.querySelector('#mat-option-14').click();
        """)
    except:
        print('no se ejecuto el script motivo de compra')

    # try:
    #     ## Abre Select MOTIVO DE LA COMPRA 
    #     hacerClick('#mat-select-2')
    # except:
    #     print('no se abrió select MOTIVO DE LA COMPRA ')

    # try:
    #     hacerClick("//mat-option//*[contains(text(), 'Materia Prima')]")
    # except:
    #     print('no se selecciono la opcion de Materia Prima')
    print(f"{fecha_inicio.second}    {FUNCIONES.datetime.now().second}")
    print(f"{abs(fecha_inicio.microsecond // 100 )}  {FUNCIONES.datetime.now().microsecond // 100}")
    formularioSelects = f'{FUNCIONES.datetime.now().second - fecha_inicio.second}.{abs(fecha_inicio.microsecond // 100 - FUNCIONES.datetime.now().microsecond // 100)} segundos'
    
    try:

        ################        DATOS DE LA OPERACION        ################  
        Monto_a_Comprar = seleccionarElemento('/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[1]/melp-data-transaction/div[1]/div/div[2]/div[2]/div').text
        Monto_a_Debitar = seleccionarElemento('/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[1]/melp-data-transaction/div/div/div[5]/div[2]/div').text
        TASA = seleccionarElemento('/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[1]/melp-data-transaction/div/div/div[1]/div[2]/div[1]').text
        print(f"{FUNCIONES.Fore.YELLOW}------- FORMULARIO ABIERTO ------ {FUNCIONES.datetime.now().hour}:{FUNCIONES.datetime.now().minute} ---\n {FUNCIONES.Style.RESET_ALL}")
        # print(f"--- DATOS DE LA OPERACION ---\nMonto a Comprar: {Monto_a_Comprar}$\nMonto a Debitar: {Monto_a_Debitar}bs\nTasa: {TASA}bs")
        if not hacerClick('/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[2]/melp-button-wrapper/div/div[2]/button[2]'): # btn continuar

                ###### ESCENARIO EN QUE NO TENGA SUFICIENTE DINERO EN LA CUENTA ######
            try:  
                seleccionarElemento("//*[contains(text(), 'El monto a comprar es mayor al saldo disponible de tu cuenta.')]")
                print(f"{FUNCIONES.Fore.RED} ------ El monto a comprar es mayor al saldo en la cuenta de {Datos['cuenta']} ------ {FUNCIONES.Style.RESET_ALL}")
                if Datos['2_Cuentas']: # Verifica si hay otra cuenta para intentar con esa, aprovechando el formulario    
                    print(FUNCIONES.Fore.YELLOW + '------ Cambiando Cuenta ------' + FUNCIONES.Style.RESET_ALL)
                        
                    try:
                        seleccionarElemento('//*[@id="mat-select-0"]').click()
                    except:
                        print('no se selecciono la primera casilla')
                    
                    if Datos['cuenta'] == 'corriente':
                        try:
                            hacerClick("//div[@id='mat-select-0-panel']//*[contains(text(), 'Cuenta de Ahorro')]")
                            print('se selecciono cuenta Ahorro')
                            if not hacerClick('/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[2]/melp-button-wrapper/div/div[2]/button[2]'): #btn aceptar
                                print(f"{FUNCIONES.Fore.RED} ------ No se pudo continuar con ningun tipo de cuenta debido a fondo insuficiente ------ {FUNCIONES.Style.RESET_ALL}")
                                verificacionBalance(Datos['nombre'])
                                cerrarSesion()
                                return False
                              
                        except:
                            print('no se selecciono cuenta Ahorro')

                    if Datos['cuenta'] == 'ahorro':
                        try:
                            hacerClick("//div[@id='mat-select-0-panel']//*[contains(text(), 'Cuenta Corriente')]")
                            print('se selecciono cuenta Corriente')
                            if not hacerClick('/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[2]/melp-button-wrapper/div/div[2]/button[2]'): #btn aceptar
                                FUNCIONES.Telegram("------ No se pudo continuar con ningun tipo de cuenta debido a fondo insuficiente ------")
                                print(f"{FUNCIONES.Fore.RED} ------ No se pudo continuar con ningun tipo de cuenta debido a fondo insuficiente ------ {FUNCIONES.Style.RESET_ALL}")
                                verificacionBalance(Datos['nombre'])
                                cerrarSesion()
                                return False
                        except:
                            print('no se selecciono cuenta corriente')
                else:
                    print(f"{FUNCIONES.Fore.RED} ------ No hay otra cuenta para intentar la compra ------ {FUNCIONES.Style.RESET_ALL}")
                    verificacionBalance(Datos['nombre'])
                    cerrarSesion()
                    return False
                        
                
            except:      
                print('hay dinero en la cuenta pero hubo un error el formulario')
        
    except:
        print('no se presionó el botonnn')
        input()

    try:
        hacerClick('/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[2]/melp-button-wrapper/div/div[2]/button[2]') #btn aceptar
    except:
        print('no se presionó el boton')
        input()
        

    try:
        FUNCIONES.driver.execute_script("document.evaluate('/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[1]/melp-exchange-market-statement/form/div/mat-checkbox//label', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();")
        #seleccionarElemento('//*[@id="mat-mdc-checkbox-0"]').click() #Casilla para marcar
    except:
        print('no se presionó el boton')
        input()

    try:
        hacerClick('/html/body/app/melp-standard-layout/div/div/melp-buy-foreign-currency/melp-standard-card-layout/div/div/div[1]/div[2]/melp-button-wrapper/div/div[2]/button[2]')  #ultimo btn aceptar
        FormularioLleno =f"Formulario completo lleno en {FUNCIONES.datetime.now().second - segundos}.{abs(FUNCIONES.datetime.now().microsecond // 100 - milesimas)} segundos"                           
    except:
        print('no se presionó el boton')
        input() 

    
    

    try:
        FUNCIONES.Telegram(f"🚀 --- FORMULARIO ABIERTO --- 🚀\n👤Usuario:{Datos['nombre']}\n 📋Cuenta: {Datos['cuenta']}\n💰 Monto a Comprar: {Monto_a_Comprar}$\n📉 Monto a Debitar: {Monto_a_Debitar}bs\n📊 Tasa: {TASA}bs\select llenos en {formularioSelects}\n{FormularioLleno}")
    except:
        print("Error al enviar mensaje a Telegram")
    
    print(FormularioLleno)
   




def verificacionBalance(Datos):
    try:
        seleccionarElemento("//*[contains(text(), 'Resumen financiero')]")
    except:
        FUNCIONES.driver.get("https://www30.mercantilbanco.com/summary")

    listaBalancesSucios = []
    Balances = []
    try:
        balance1 = seleccionarElemento("//*[@id='summary']/div/div[1]/melp-summary-all-products/melp-product-list-detail[1]/div/div[2]").text 
        listaBalancesSucios.append(balance1)
    except:
        pass 

    try:
        balance2 = seleccionarElemento("//*[@id='summary']/div/div[1]/melp-summary-all-products/melp-product-list-detail[1]/div/div[3]").text
        listaBalancesSucios.append(balance2)
    except:
        pass

    try:
        balance3 = seleccionarElemento("//*[@id='summary']/div/div[1]/melp-summary-all-products/melp-product-list-detail[1]/div/div[4]").text
        listaBalancesSucios.append(balance3)
    except:
        pass
    try:
        balanceUSD = (seleccionarElemento("//*[@id='summary']/div/div[1]/melp-summary-all-products/melp-product-list-detail[2]/div/div[3]").text).strip().split('\n')
        USD = (f"{balanceUSD[0]} -> Saldo: {balanceUSD[3]} $.")
    except:
        pass
    try: 
        
        ####################################
        '''
        Cada balance es una lista en donde:
        [0] = Nombre de la cuenta
        [1] = 'Más opciones'
        [2] = 'Bs.'
        [3] = Monto de la cuenta
        '''
        #####################################

        for balance_individual in listaBalancesSucios:

  
            lineas = [linea.strip() for linea in balance_individual.strip().split('\n') if linea.strip()]
            
     
            nombre_cuenta = lineas[0]
            monto_cuenta = lineas[3] 
            

            Balances.append(f"{nombre_cuenta} -> Saldo: {monto_cuenta} Bs.")

        balancesTotales = "\n".join(Balances)
        MSJ = f"--- BALANCE DE LA CUENTA {Datos['nombre']}--- \n{balancesTotales}\n{USD} "
        print(MSJ)
        FUNCIONES.Telegram(MSJ)
    except Exception as e:
        print(f"No se pudo verificar el balance: {e}")
        return False


def seleccionarTipoDivisas():
    xpath_dolares = "//*[contains(text(), 'Dólares')]"
    try:
        #print("click en Dólares...")
        Intentos = 0
        while not hacerClick(xpath_dolares, show=False) and Intentos < 3:
            if FUNCIONES.VerMensaje():
                return False
            print(f"Reintentado hacer click en Dólares... {Intentos + 1}/3")
            time.sleep(1)
            Intentos += 1
        return True
        
    except Exception as e:
        print(f"No se pudo hacer clic en Dólares: {e}")
        #driver.save_screenshot("error_click.png")
        elementoError = seleccionarElemento(".sub-title")
        print(f"Error: {elementoError.text}")
        FUNCIONES.VerMensaje()
        return False
    
def ingresarMonto(Datos):
    global montoIngresado
    if montoIngresado == False:
    
        # Primero selecciona el tipo de moneda o divisa
        if not seleccionarTipoDivisas():
            return False
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
            if FUNCIONES.inicio_sesion(cuenta['inicio']) == False:
                continue
            if FUNCIONES.ResolverPreguntasSeguridad(cuenta['preguntas']) == False:
                continue

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