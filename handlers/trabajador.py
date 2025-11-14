from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

CODIGO_TRABAJADOR = "panaderia2025"

# 🧑‍🍳 Comando /trabajador: solicita el código
async def trabajador(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🔐 Ingresá el código de acceso para trabajadores:")
    context.chat_data["esperando_codigo"] = True

# 🔐 Verifica el código ingresado
async def verificar_codigo_manual(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.chat_data.get("esperando_codigo"):
        code = update.message.text.strip()
        if code == CODIGO_TRABAJADOR:
            context.chat_data["modo_trabajador"] = True
            context.chat_data["esperando_codigo"] = False

            teclado = InlineKeyboardMarkup([
                [InlineKeyboardButton("📋 Ver pedidos", callback_data="ver_pedidos")],
                [InlineKeyboardButton("📦 Ver stock", callback_data="ver_stock")]
            ])

            await update.message.reply_text(
                "✅ Acceso autorizado 👷\n\n"
                "Este es tu menú de trabajo:",
                reply_markup=teclado
            )
        else:
            context.chat_data["modo_trabajador"] = False
            context.chat_data["esperando_codigo"] = False
            await update.message.reply_text("❌ Código incorrecto. Volvé al menú principal con /start.")

# 📲 Maneja los botones inline
async def manejar_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if not context.chat_data.get("modo_trabajador"):
        await query.edit_message_text("🔒 Esta función es solo para trabajadores.")
        return

    if query.data == "ver_pedidos":
        await ver_pedidos(update, context)
    elif query.data == "ver_stock":
        await ver_stock(update, context)

# 🧾 Maneja opciones escritas por el trabajador
async def manejar_opciones_trabajador(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.chat_data.get("modo_trabajador"):
        opcion = update.message.text.strip().lower()
        if opcion == "ver pedidos":
            await ver_pedidos(update, context)
        elif opcion == "ver stock":
            await ver_stock(update, context)

# 📋 Muestra los pedidos guardados
async def ver_pedidos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pedidos = context.chat_data.get("pedidos", [])
    mensaje = "📭 No hay pedidos registrados aún." if not pedidos else \
        "📋 Pedidos registrados:\n\n" + "\n\n".join([f"{i+1}. {p}" for i, p in enumerate(pedidos)])

    if update.callback_query:
        await update.callback_query.message.reply_text(mensaje)
    else:
        await update.message.reply_text(mensaje)

# 📦 Muestra el stock disponible
async def ver_stock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    stock_items = [
        "Pan Casero - 20 unidades",
        "Facturas surtidas - 15 unidades",
        "Tortas de chocolate - 5 unidades"
    ]

    mensaje = "📦 Stock disponible:\n\n" + "\n".join([f"- {item}" for item in stock_items])

    if update.callback_query:
        await update.callback_query.message.reply_text(mensaje)
    else:
        await update.message.reply_text(mensaje)
