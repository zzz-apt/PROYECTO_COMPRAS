from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ApplicationBuilder, MessageHandler, filters, ConversationHandler
import logging
from telegram import Update



from telegram import Bot
import requests
import json
from datetime import datetime
import re
from FUNCIONES import *
import subprocess

tasa_bcv = 0
def BCV_():
    global tasa_bcv
    respuesta = requests.get('https://api.dolarvzla.com/public/exchange-rate')
    datos = respuesta.json()
    tasas = datos['current']
    Tasa_bcv = float(tasas['usd'])
    return Tasa_bcv




ESPERANDO_RESPUESTA = 0

async def inicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde al comando /inicio y pide el input."""
    await update.message.reply_text("¡Hola! ¿Cómo te llamas?")
    # Le decimos a Telegram que el siguiente paso es esperar la respuesta
    return ESPERANDO_RESPUESTA

async def procesar_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recibe el texto, lo usa como input y termina la conversación."""
    user_input = update.message.text
    
    # Aquí es donde usas el input para lo que necesites
    await update.message.reply_text(f"Mucho gusto, {user_input}. He guardado tu nombre.")
    
    # Finaliza el ConversationHandler
    return ConversationHandler.END

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancela la conversación actual."""
    await update.message.reply_text("Operación cancelada.")
    return ConversationHandler.END




async def ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'LA IP ES {IP()}')

async def mac(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'CAMBIANDO MAC DEL DISPOSITIVO')
    CloneMac()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'REINICIAR MODEM MANUALMENTE')
    
async def compra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'INICIANDO COMPRAS')
    comando = "terminology -e /home/yako/Documentos/python/PROYECTO_COMPRAS/venv/bin/python /home/yako/Documentos/python/PROYECTO_COMPRAS/MASTRER.py"
    subprocess.Popen(comando, shell=True)

    
async def oyasumi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Hola, con que cuentas quieres trabajar?')
    try:
        with open(rf'/home/yako/Documentos/python/PROYECTO_COMPRAS/sys/usuarios.txt', 'a', encoding='utf-8') as archivo:
            archivo.write(f'\nhola\n')
    except Exception as e:
        print(f'error al escribir el archivo: {e}')



   
async def intentos(update: Update, context: ContextTypes.DEFAULT_TYPE):
     with open(rf'/home/yako/Documentos/python/PROYECTO_COMPRAS/HISTORIAL/{datetime.now().date()}.txt', 'r') as f:
        line_count = sum(1 for _ in f)
        p = f'se han hecho un total de {int(line_count /2)} intentos'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=p)   
async def estado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='''si, estoy vivo y operando ¿que necesitas?''')
async def BCV(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respuesta = requests.get('https://api.dolarvzla.com/public/exchange-rate')
    datos = respuesta.json()
    tasas = datos['current']
    Tasa_bcv = tasas['usd']
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Actualmente la tasa BCV se encuentra en {Tasa_bcv} Bolivares')

async def Intervencion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respuesta = requests.get('https://api.dolarvzla.com/public/interventions')
    datos = respuesta.json()
    Intervenciones = datos['interventions']
    fecha = Intervenciones[0]
    fecha2 = fecha['date']
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Ultima Intervencion Anunciada: {fecha2[0:10]}')
    
async def Horarios(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre_archivo = "mi_documento.txt"
    texto_parcial = "Formulario Abierto ------ MENUDEO"

    with open(rf'/home/yako/Documentos/python/PROYECTO_COMPRAS/HISTORIAL/{datetime.now().date()}.txt', 'r') as archivo:
        contenido = archivo.read()

    patron = r"Formulario Abierto ------ MENUDEO.*:\s*(\d+:\d+)"

    horas_formulario = re.findall(patron, contenido)

    Horario = []

    for hora in horas_formulario:
        Horario.append(hora)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'🧾Formuario estuvo activo en las horas: {Horario}')



def main() -> None:
     # Reemplaza 'TU_TOKEN_AQUI' con el token que te dio BotFather
    TOKEN = '8167604613:AAFPFgIwMbZFBpnz4hO4p9FzK1-n52VSIIs'
    
    # Crea la aplicación y pásale el token
    application = ApplicationBuilder().token(TOKEN).build()

    # Añade los manejadores (handlers) para diferentes tipos de actualizaciones
    # Manejador para el comando '/start'
  
    #application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('BCV', BCV))
    application.add_handler(CommandHandler('INT', Intervencion))
    application.add_handler(CommandHandler('formulario', Horarios))
    application.add_handler(CommandHandler('estado', estado))
    #application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler('intentos', intentos))
    application.add_handler(CommandHandler('ip', ip))
    application.add_handler(CommandHandler('mac', mac))
    application.add_handler(CommandHandler('compra', compra))
    # application.add_handler(conv_handler)
    '''# Manejador para mensajes de texto (que no sean comandos)
    # filters.TEXT & ~filters.COMMAND asegura que solo maneje texto plano
    echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    application.add_handler(echo_handler)'''
    
    # Inicia el bot, que se mantendrá escuchando por mensajes
    logging.info("El bot está escuchando (long polling)...")
    application.run_polling(poll_interval=3.0)
     # Configuramos el manejador de conversación
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("inicio", inicio)],
        states={
            ESPERANDO_RESPUESTA: [MessageHandler(filters.TEXT & ~filters.COMMAND, procesar_input)]
        },
        fallbacks=[CommandHandler("cancelar", cancelar)]
    )

if __name__ == '__main__':
    main()
















