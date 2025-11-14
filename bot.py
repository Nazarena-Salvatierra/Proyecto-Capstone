import os
from datetime import datetime
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
)
from groq import Groq
from dotenv import load_dotenv
# 🔑 Cargar variables de entorno desde .env
load_dotenv()

# Handlers de módulos existentes
from handlers.clientes import start, cliente_menu
from handlers.comandos import horario, descuentos, stock
from handlers.imagenes import manejar_imagen, modificar, manejar_cambios, confirmar
from handlers.trabajador import (
    trabajador, verificar_codigo_manual, manejar_opciones_trabajador, manejar_callback
)
from handlers.armar_torta import armar_torta, manejar_callback as manejar_callback_torta
from handlers.trabajador import manejar_callback as manejar_callback_trabajador
from handlers.audio import manejar_voice, manejar_audio
from handlers.reservas import (
    start as start_reservas,
    recetas,
    mostrar_receta,
    productos,
    reserva,
    guardar_reserva,
    ver_reservas
)

# ✅ Configuración con variables de entorno
TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY_GROQ = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=API_KEY_GROQ)

# ✅ Wrappers para filtrar correctamente
async def cambios_si_cliente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.chat_data.get("modo_trabajador"):
        await manejar_cambios(update, context)

async def mostrar_receta_si_cliente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.chat_data.get("modo_trabajador"):
        await mostrar_receta(update, context)

async def guardar_reserva_si_cliente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.chat_data.get("modo_trabajador"):
        await guardar_reserva(update, context)

async def verificar_codigo_si_trabajador(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.chat_data.get("esperando_codigo"):
        await verificar_codigo_manual(update, context)

async def opciones_si_trabajador(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.chat_data.get("modo_trabajador"):
        await manejar_opciones_trabajador(update, context)

# ✅ Función principal
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Menú principal
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cliente", cliente_menu))
    app.add_handler(CommandHandler("trabajador", trabajador))

    # Menú de reservas
    app.add_handler(CommandHandler("recetas", recetas))
    app.add_handler(CommandHandler("productos", productos))
    app.add_handler(CommandHandler("reserva", reserva))
    app.add_handler(CommandHandler("verreservas", ver_reservas))

    # Comandos rápidos
    app.add_handler(CommandHandler("armar_torta", armar_torta))
    app.add_handler(CommandHandler("horario", horario))
    app.add_handler(CommandHandler("descuentos", descuentos))
    app.add_handler(CommandHandler("stock", stock))

    # Manejo de imágenes
    app.add_handler(MessageHandler(filters.PHOTO, manejar_imagen))
    app.add_handler(CommandHandler("modificar", modificar))
    app.add_handler(CommandHandler("confirmar", confirmar))

    # ⚡ Handlers de trabajador primero
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, verificar_codigo_si_trabajador))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, opciones_si_trabajador))

    # ⚡ Handlers de cliente después
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cambios_si_cliente))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mostrar_receta_si_cliente))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guardar_reserva_si_cliente))

    # Botones inline / callbacks
    app.add_handler(CallbackQueryHandler(manejar_callback_torta, pattern="^(tipo_|relleno_|decoracion_|tamano_)"))
    app.add_handler(CallbackQueryHandler(manejar_callback_trabajador, pattern="^trabajador_"))
    app.add_handler(CallbackQueryHandler(manejar_callback))  # sin pattern

    # Handlers de audio
    app.add_handler(MessageHandler(filters.VOICE, manejar_voice))
    app.add_handler(MessageHandler(filters.AUDIO | filters.Document.ALL, manejar_audio))

    print("🤖 Bot de panadería LuNaTi iniciado. Esperando mensajes...")
    app.run_polling()

if __name__ == "__main__":
    main()
