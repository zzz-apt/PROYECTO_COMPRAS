from FUNCIONES import *
import schedule
Tiempo = 60
hora_actual = datetime.now().hour
minuto_actual = datetime.now().minute
segundo_actual = datetime.now().second
x = True

DatosSh = {
     '2_Cuentas' : False,
     'cuenta' : 'corriente', 
     'nombre' : 'Sharynnel',
     'Error_MD' : 'False',
     'CHAT_ID' : '5766960410',
     'Monto' : 2000
}
InicioSh = {
     
          'usuario': 'Sharynnel2209',
          'contrasena' : 'Nicol2209*',

     }
PreguntasSh = {
          'PreguntaUnica' : False,
          'pregunta1' : '¿Cuál es su marca de carros preferida?',
          'respuesta1' : 'jeep',

          'pregunta2' : '¿Cuál es la profesión/ocupación de su madre?',
          'respuesta2' : 'maestra',

          'pregunta3' : '¿Cuál es el segundo nombre de su hermano(a) mayor?',
          'respuesta3' : 'Nicol',

          'pregunta4' : '¿Cuál es el nombre de su cantante/grupo favorito en la universidad?',
          'respuesta4' : 'Ariana Grande',

          'pregunta5' : '¿Cuál es el nombre de su mejor amigo(a) de infancia?',
          'respuesta5' : 'Valeria'

     }
def Shary():
  Compra2(InicioSh,DatosSh, PreguntasSh)


DatosNV = {
    
     '2_Cuentas' : False,
     'cuenta' : 'ahorro',
     'nombre' : 'Nathalia',
     'estado' : False,
     'CHAT_ID' : '6505930247',
     'Monto' : 2000


}
InicioNV =     {
    

          'usuario': 'hernalivargas',
          'contrasena' : 'Ximena.2025',
          'id' : 'Naty'

}
PreguntasNV = {
        
        'PreguntaUnica' : True,
        'RespuestaUnica' : "puerto",
        'pregunta1' : '¿Cuál es el apodo de su mejor amigo de la infancia?',
        'respuesta1' : 'puerto',

        'pregunta2' : '¿Cuál es el nombre de su cantante/grupo favorito en la universidad?',
        'respuesta2' : 'puerto',

        'pregunta3' : '¿Cuál es el nombre de su profesor favorito de universidad?',
        'respuesta3' : 'puerto',

        'pregunta4' : '¿Cuál es la profesión/ocupación de su madre?',
        'respuesta4' : 'puerto',

        'pregunta5' : '¿En qué ciudad nació su abuela materna?',
        'respuesta5' : 'puerto'

    }
def Naty():
    Compra2(InicioNV,DatosNV, PreguntasNV)

DatosAC = {
    
     '2_Cuentas' : False,
     'cuenta' : 'ahorro',
     'nombre' : 'Alexander',
     'CHAT_ID' : '6505930247',
     'Monto' : 2000


}
InicioAC =     {
    

          'usuario': 'alexcapri',
          'contrasena' : 'Xncv.2025',
          'id' : 'Alexander'

}
PreguntasAC = {
        'PreguntaUnica' : True,
        'RespuestaUnica' : "puerto",     
        'pregunta1' : '¿A qué hora del dia nació su hijo(a) mayor?',
        'respuesta1' : 'puerto',

        'pregunta2' : '¿Cuál es el nombre de su maestro(a) de primer grado de primaria?',
        'respuesta2' : 'puerto',

        'pregunta3' : '¿En qué ciudad nació su abuela materna?',
        'respuesta3' : 'puerto',

        'pregunta4' : '¿Cuál es la profesión/ocupación de su madre?',
        'respuesta4' : 'puerto',

        'pregunta5' : '¿Cuándo es el aniversario de boda de sus padres?',
        'respuesta5' : 'puerto'

    }
def Alexander():
    Compra2(InicioAC,DatosAC, PreguntasAC)

DatosFV = {
    
     '2_Cuentas' : True,
     'cuenta' : 'corriente',
     'nombre' : 'Fernando',
     'CHAT_ID' : '6231499420',
     'Monto' : 2000
     

     
}
InicioFV =     {
    
          'usuario': 'fernandovj7',
          'contrasena' : 'H600*diefer*',
          'id' : 'Fer'
}
PreguntasFV = {
        

        'PreguntaUnica' : True,
        'RespuestaUnica' : "Salsa",

        'pregunta1' : '¿Cuál es el nombre de su madrina de matrimonio?',
        'respuesta1' : 'salsa',

        'pregunta2' : '¿A qué hora del dia nació su hijo(a) mayor?',
        'respuesta2' : 'salsa',

        'pregunta3' : '¿En qué ciudad nació su abuelo paterno?',
        'respuesta3' : 'salsa',

        'pregunta4' : '¿En qué año conoció a su esposo(a)?',
        'respuesta4' : 'salsa',

        'pregunta5' : '¿Cuál es el nombre de su cantante/grupo favorito en la universidad?',
        'respuesta5' : 'salsa'

    }

def fer():
    Compra2(InicioFV,DatosFV, PreguntasFV)

DatosE = {
    
     '2_Cuentas' : False,
     'cuenta' : 'corriente',
     'nombre' : 'Elizabeth',
     'CHAT_ID' : '@Ritz0810',
     'Monto' : 2000
     
}
InicioE =     {
    
          'usuario': 'Elizab10',
          'contrasena' : 'Augusto.13',
          'id' : 'Eli'
}
PreguntasE = {
     
        'pregunta1' : '¿Cuál es el segundo nombre de su hermano(a) mayor?',
        'respuesta1' : 'Agustin',

        'pregunta2' : '¿A qué hora del dia nació su hijo(a) mayor?',
        'respuesta2' : '11am',

        'pregunta3' : '¿En qué ciudad nació su abuelo materno?',
        'respuesta3' : 'Cartagena',

        'pregunta4' : '¿En qué año conoció a su esposo(a)?',
        'respuesta4' : '1990',

        'pregunta5' : '¿Cuál es el nombre de su cantante/grupo favorito en la universidad?',
        'respuesta5' : 'Chayanne'

    }
def Elizabeth():
    Compra2(InicioE,DatosE, PreguntasE)



DatosP = {
    
     '2_Cuentas' : True,
     'cuenta' : 'corriente',
     'nombre' : 'Perseo',
     'CHAT_ID' : '@Ritz0810',
     'Monto' : 2000
     
}
InicioP =     {
    
          'usuario': 'Perseo777',
          'contrasena' : 'Gnosis.29',
          'id' : 'Perseo'
}
PreguntasP = {

        'PreguntaUnica' : True,
        'RespuestaUnica' : "biologia",
     
        # 'pregunta1' : '¿Cuál es el nombre de su cantante/grupo favorito en la universidad?',
        # 'respuesta1' : 'biologia',

        # 'pregunta2' : '¿Cuál era el modelo de su primer carro?',
        # 'respuesta2' : 'biologia',

        # 'pregunta3' : '¿Cuál es la profesión/ocupación de su madre?',
        # 'respuesta3' : 'biologia',

        # 'pregunta4' : '¿En qué ciudad nació su abuelo paterno?',
        # 'respuesta4' : 'biologia',

        # 'pregunta5' : '¿A que hora del día nació usted?',
        # 'respuesta5' : 'biologia'

    }
def Perseo():
    Compra2(InicioP,DatosP, PreguntasP)






# RAYMOND
DatosDM = {
    
     '2_Cuentas' : False,
     'cuenta' : 'ahorro',
     'nombre' : 'Deleit',
     'estado' : False,
     'CHAT_ID' : None,
     'Monto' : 2000


}
InicioDM =     {
    

          'usuario': 'deleitmolina08',
          'contrasena' : 'Asterisc0*',
          'id' : 'Deleit'

}
PreguntasDM = {
        
        'PreguntaUnica' : True,
        'RespuestaUnica' : "Gera",

    }
def Deleit():
    Compra2(InicioDM, DatosDM, PreguntasDM)

DatospR = {
    
     '2_Cuentas' : True,
     'cuenta' : 'ahorro',
     'nombre' : 'pRAY',
     'CHAT_ID' : '@none',
     'Monto' : 2000
     
     }
IniciopR =     {
    
          'usuario': 'ramonm',
          'contrasena' : 'Haziel*2',
          'id' : 'pRAY'
}
PreguntaspR = {

        'PreguntaUnica' : True,
        'RespuestaUnica' : "ramon"
}
def pRAY():
   Compra2(IniciopR, DatospR, PreguntaspR)

DatosR = {
    
     '2_Cuentas' : False,
     'cuenta' : 'corriente',
     'nombre' : 'RAY',
     'CHAT_ID' : '@none',
     'Monto' : 2000
     
}
InicioR =     {
    
          'usuario': 'raymondm',
          'contrasena' : 'Haziel*2',
          'id' : 'RAY'
}
PreguntasR = {

        'PreguntaUnica' : True,
        'RespuestaUnica' : "marbelys"
}
def RAY():
  Compra2(InicioR, DatosR, PreguntasR)


# CHUCHO
DatosO = {
    
     '2_Cuentas' : False,
     'cuenta' : 'corriente',
     'nombre' : 'OLGA',
     'CHAT_ID' : '@none',
     'Monto' : 2000
     
}
InicioO =     {
    
          'usuario': 'ramoneilla',
          'contrasena' : 'Moak135*.',
          'id' : 'OLGA'
}
PreguntasO = {

        'PreguntaUnica' : False,

        'pregunta1' : '¿Cuál es el nombre de su profesor favorito de universidad?',
        'respuesta1' : 'Pedro chatarra',

        'pregunta2' : '¿Cuál es el nombre de su cantante/grupo favorito en la universidad?',
        'respuesta2' : 'Ricardo arjona',

        'pregunta3' : '¿Cuál es el apodo de su mejor amigo de la infancia?',
        'respuesta3' : 'Guanipita',
        
        'pregunta4' : '¿Cuál es el nombre de su abuela materna?',
        'respuesta4' : 'Agustina',

        'pregunta5' : '¿En qué ciudad nació su abuelo materno?',
        'respuesta5' : 'Carora',

        'pregunta' : '¿Cuál es el primer nombre de su primo(a) materno mayor?',
        'respuesta' : 'Douglas vasquez',
        
}
def Olga():
    Compra2(InicioO, DatosO, PreguntasO)

DatosRH = {
    
     '2_Cuentas' : False,
     'cuenta' : 'corriente',
     'nombre' : 'RH',
     'CHAT_ID' : '@none',
     'Monto' : 2000
     
}
InicioRH =     {
    
          'usuario': 'arvm1989',
          'contrasena' : 'Varmar-2026',
          'id' : 'RAY'
}
PreguntasRH = {

        'PreguntaUnica' : False,

        'pregunta1' : '¿Cuál es el nombre de su cantante/grupo favorito en la universidad?',
        'respuesta1' : 'Ricardo arjona',

        'pregunta2' : '¿A qué hora del dia nació su hijo(a) mayor?',
        'respuesta2' : 'dosycuarentaysiete',

        'pregunta3' : '¿Cuál es el segundo nombre de su hijo(a) mayor?',
        'respuesta3' : 'sharynnel',

        'pregunta4' : '¿Cuál es el segundo nombre de su padre?',
        'respuesta4' : 'vicente',

        'pregunta5' : '¿Cuál es su marca de carros preferida?',
        'respuesta5' : 'corsa',
        
}
def RH():
    Compra2(InicioRH,DatosRH, PreguntasRH)





def Compra2(inicio, datos, preguntas):
    resultado_compra = False
    
    if check(datos['nombre']) == True:
        return
    while not resultado_compra:
        ErrorMD = True
        print(f'{Fore.YELLOW}  ------  {datos["nombre"]} ------ {Style.RESET_ALL}')
        while ErrorMD:
            inicio_sesion(inicio)
            preguntas_seguridad(preguntas)
            ErrorMD = Ingreso()
        resultado_compra = compra(datos)
        cuenta_regresiva(20)
                


def StandBy():

     print( Fore.YELLOW + 'StandBy... ' + Style.RESET_ALL)
     ErrorMD = True
     print(Fore.YELLOW + ' ------ Ray ------' + Style.RESET_ALL)
     while ErrorMD:
          inicio_sesion(InicioR)
          preguntas_seguridad(PreguntasR)
          ErrorMD = Ingreso()
def compra1():
     global resultado_compra, x
     resultado_compra = compra(DatosR)
     print('compra madrugadita completada')
     x = False



if hora_actual <= 5 or hora_actual >= 22 :
    print( Fore.YELLOW + 'Ejecutando modo Madrugadita: ' + Style.RESET_ALL)
    Telegram(f'Ejecutando modo Madrugadita')
    schedule.every().day.at("06:04").do(StandBy)
    schedule.every().day.at("06:05").do(compra1)
    while x:
        schedule.run_pending()
        time.sleep(1) 


##################



##################

while True:
    try:
        Deleit()
        RAY()
        pRAY()
        Olga()


    

    except Exception as e:
        print(f'hubo un error al ejecutar el programa {e}')
        Telegram(f'hubo un error al ejecutar el programa {e}')
        Telegram(f'se ha detenido el programa')
        break