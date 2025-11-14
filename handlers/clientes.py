from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🌙🥐 <b>Bienvenido a Panadería Lunati</b> 🥐🌙\n"
        "<i>Pan y Repostería Artesanal</i>\n\n\n"
        "Ahora podés hablarme directamente 🎙️:\n"
        "Mandá una nota de voz con tu pedido o consulta y te responderé al instante.\n\n"
        "También podés enviarme una 📸 foto:\n"
        "Mostrame tu torta soñada o una idea de decoración, y te ayudaré a armarla.\n\n"
        "Si preferís usar el teclado, estos son los comandos disponibles:\n\n"
        "🛍️ <b>Clientes:</b>\n"
        "• /cliente — Soy cliente\n\n"
        "👷 <b>Personal:</b>\n"
        "• /trabajador — Soy trabajador\n\n"
        "📌 <b>Comandos rápidos:</b>\n"
        "• /horario — Ver horario 📅\n"
        "• /descuentos — Ver descuentos 💸\n"
        "• /stock — Ver stock 📦",
        parse_mode="HTML"
    )

async def cliente_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👩‍🍳 <b>Menú del Cliente:</b>\n\n"
        "📜 /recetas - Ver recetas disponibles\n"
        "🧺 /productos - Ver productos y precios\n"
        "🧾 /reserva - Hacer una reserva\n"
        "📋 /verreservas - Ver reservas actuales\n"
        "⏰ /horario - Consultar horarios\n"
        "💸 /descuentos - Ver descuentos\n"
        "📦 /stock - Consultar stock\n"
        "🎂 /armar_torta - Armar tu torta personalizada\n"
        "🖼️ Mandá una foto para que te sugiera un pedido\n"
        "✏️ /modificar - Cambiar tu pedido\n"
        "✅ /confirmar - Confirmar tu pedido",
        parse_mode="HTML"
    )
