#codigo de lucas 

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_first_name = update.effective_user.first_name
    user_username = update.effective_user.username
    await update.message.reply_text(
        f"¡Hola {user_first_name} (@{user_username})! 👋\n"
        "Bienvenido al Bot de la Panadería *El Buen Pan* 🥖\n\n"
        "📅 Horario:\nLunes a Viernes: 8:00 - 20:00\n"
        "Sábados: 8:00 - 18:00\nDomingos: Cerrado\n\n"
        "📦 Stock:\n- Pan de Trigo\n- Pan Integral\n- Pan de Centeno\n"
        "- Pan de Avena\n- Pan de Maíz\n- Pan de Papa\n\n"
        "💸 Promociones:\n- Pan Feliz (18:00 - 20:00)\n"
        "- Combo Completo\n- Frutas + Medialuna",
        parse_mode="Markdown"
    )

async def horario(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📅 *Horario de atención:*\n"
        "Lunes a Viernes: 8:00 - 20:00\n"
        "Sábados: 8:00 - 18:00\n"
        "Domingos: Cerrado",
        parse_mode="Markdown"
    )

async def stock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📦 *Stock disponible:*\n"
        "- Pan de Trigo\n- Pan Integral\n- Pan de Centeno\n"
        "- Pan de Avena\n- Pan de Maíz\n- Pan de Papa",
        parse_mode="Markdown"
    )

async def descuentos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "💸 *Promociones actuales:*\n"
        "- Pan Feliz (18:00 - 20:00)\n"
        "- Combo Completo\n- Frutas + Medialuna",
        parse_mode="Markdown"
    )

app = ApplicationBuilder().token("TOKEN").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("horario", horario))
app.add_handler(CommandHandler("stock", stock))
app.add_handler(CommandHandler("descuentos", descuentos))
