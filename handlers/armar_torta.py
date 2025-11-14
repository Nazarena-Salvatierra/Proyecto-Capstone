from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Paso 1: iniciar armado de torta
async def armar_torta(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🍫 Chocolate", callback_data="tipo_chocolate"),
         InlineKeyboardButton("🍦 Vainilla", callback_data="tipo_vainilla")],
        [InlineKeyboardButton("❤️ Red Velvet", callback_data="tipo_red_velvet"),
         InlineKeyboardButton("🥕 Zanahoria", callback_data="tipo_zanahoria")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎂 Elegí el *tipo* de torta:", reply_markup=reply_markup, parse_mode="Markdown")

# Paso 2: manejar las selecciones
async def manejar_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Selección de tipo
    if query.data.startswith("tipo_"):
        context.user_data["tipo"] = query.data.replace("tipo_", "")
        keyboard = [
            [InlineKeyboardButton("🥛 Crema", callback_data="relleno_crema"),
             InlineKeyboardButton("🍫 Ganache", callback_data="relleno_ganache")],
            [InlineKeyboardButton("🍓 Mermelada", callback_data="relleno_mermelada"),
             InlineKeyboardButton("🍯 Dulce de leche", callback_data="relleno_dulce_de_leche")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🧁 Ahora elegí el *relleno*:", reply_markup=reply_markup, parse_mode="Markdown")

    # Selección de relleno
    elif query.data.startswith("relleno_"):
        context.user_data["relleno"] = query.data.replace("relleno_", "")
        keyboard = [
            [InlineKeyboardButton("🍓 Frutilla", callback_data="decoracion_frutilla"),
             InlineKeyboardButton("🍫 Chocolate", callback_data="decoracion_chocolate")],
            [InlineKeyboardButton("🥣 Granola", callback_data="decoracion_granola"),
             InlineKeyboardButton("🧈 Buttercream", callback_data="decoracion_buttercream")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("✨ Elegí la *decoración*:", reply_markup=reply_markup, parse_mode="Markdown")

    # Selección de decoración
    elif query.data.startswith("decoracion_"):
        context.user_data["decoracion"] = query.data.replace("decoracion_", "")
        keyboard = [
            [InlineKeyboardButton("📏 Chica: 1Kg", callback_data="tamano_chica"),
             InlineKeyboardButton("📐 Mediana: 2Kg", callback_data="tamano_mediana"),
             InlineKeyboardButton("🎉 Grande: 3kg", callback_data="tamano_grande")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📏 Elegí el *tamaño*:", reply_markup=reply_markup, parse_mode="Markdown")

    # Selección de tamaño y confirmación final
    elif query.data.startswith("tamano_"):
        context.user_data["tamano"] = query.data.replace("tamano_", "")
        tipo = context.user_data.get("tipo")
        relleno = context.user_data.get("relleno")
        decoracion = context.user_data.get("decoracion")
        tamano = context.user_data.get("tamano")

        await query.edit_message_text(
            f"🎂 Tu torta está lista:\n"
            f"- Tipo: {tipo}\n"
            f"- Relleno: {relleno}\n"
            f"- Decoración: {decoracion}\n"
            f"- Tamaño: {tamano}\n\n"
            "✅ Pedido confirmado 🕒 Podés retirar tu torta dentro de *12 horas* en nuestro local 🥐\n, ¡gracias por elegir Panadería Lunati! 🥐"
        )
