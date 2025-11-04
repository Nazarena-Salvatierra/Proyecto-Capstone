from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = '8436141933:AAEpdkFJ2RiGOdYH6rL7VeyPCEWiydEwybU' 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"¡Hola, {user.mention_html()}! 👋\n"
        "Soy el Bot de la Panadería 'El Buen Pan'.\n"
        "Usa los siguientes comandos para información:\n"
        "**/horario**\n"
        "**/descuentos**\n"
        "**/stock**"
    )

async def horario(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mensaje = (
        "🍞 **Nuestro Horario:**\n"
        "Lunes a Sábado: 7:00 a 20:00\n"
        "Domingos: 8:00 a 13:00 (Solo panes y facturas)\n"
        "\n¡Te esperamos!"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

async def descuentos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    promociones = (
        "💰 **Promociones de Hoy:**\n"
        "1. **Hora Feliz (18:00 - 20:00):** 2x1 en Facturas y Criollos.\n"
        "2. **Miércoles de Pan Integral:** 20% de descuento en panes con semillas.\n"
        "3. **Desayuno Completo:** Café + Medialuna por $2.500.\n"
        "\n¡Aprovecha antes de que se acaben!"
    )
    await update.message.reply_text(promociones, parse_mode="Markdown")

async def stock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    disponibilidad = (
        "✅ **Stock Actual (Destacados):**\n"
        "**Panes:** Tira de Pan, Pan de Masa Madre, Pan Integral (disponible)\n"
        "**Facturas:** Medialuna de Manteca, Donas de Chocolate (¡recién hechos!)\n"
        "**Especialidad:** Tarta de Manzana (3 unidades restantes)\n"
        "\n_Nota: Para un stock más detallado, visita nuestra tienda._"
    )
    await update.message.reply_text(disponibilidad, parse_mode="Markdown")

def main() -> None:
    application = Application.builder().token(TOKEN).build()




    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("horario", horario))
    application.add_handler(CommandHandler("descuentos", descuentos)) 
    application.add_handler(CommandHandler("stock", stock)) 


    print("El bot de la panadería está escuchando...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
