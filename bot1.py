import json
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🥖 Bienvenido a la Panadería Delicias 🥐\n\n"
        "📜 /recetas\n🛍️ /productos\n🧾 /reserva\n📋 /verreservas"
    )

async def recetas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = "🍞 *Recetas disponibles:*\n\n"
    for i, r in enumerate(data["recetas"], start=1):
        mensaje += f"{i}. {r['nombre']}\n"
    mensaje += "\nEnviá el número de la receta para verla 🍰"
    await update.message.reply_text(mensaje, parse_mode="Markdown")

async def mostrar_receta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    if texto.isdigit():
        num = int(texto)
        if 1 <= num <= len(data["recetas"]):
            r = data["recetas"][num - 1]
            detalle = (
                f"👩‍🍳 *{r['nombre']}*\n\n"
                f"🧂 Ingredientes:\n- " + "\n- ".join(r["ingredientes"]) +
                "\n\n🍽️ Pasos:\n" + "\n".join([f"{i+1}. {p}" for i, p in enumerate(r["pasos"])]) +
                f"\n\n⏱️ Tiempo total: {r['tiempo']}\n💡 Consejo: {r['consejo']}"
            )
            await update.message.reply_text(detalle, parse_mode="Markdown")

async def productos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = "🧺 *Productos disponibles:*\n\n"
    for i, p in enumerate(data["productos"], start=1):
        mensaje += f"{i}. {p['nombre']} - 💲{p['precio']}\n"
    mensaje += "\nUsá /reserva para hacer un pedido."
    await update.message.reply_text(mensaje, parse_mode="Markdown")

async def reserva(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 Ingresá tu pedido con el formato:\n\n"
        "`Nombre - Producto - Cantidad`\n\n"
        "Ejemplo:\n`Juan Pérez - Pan Casero - 2`",
        parse_mode="Markdown"
    )

async def guardar_reserva(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    if "-" in texto:
        partes = [p.strip() for p in texto.split("-")]
        if len(partes) == 3:
            nombre, producto, cantidad = partes
            cantidad = cantidad.replace("unidades", "").strip()
            producto_info = next((p for p in data["productos"] if p["nombre"].lower() == producto.lower()), None)
            if not producto_info:
                await update.message.reply_text("❌ Producto no encontrado. Usá /productos para ver los disponibles.")
                return
            total = int(cantidad) * producto_info["precio"]
            nueva_reserva = {
                "cliente": nombre,
                "producto": producto_info["nombre"],
                "cantidad": cantidad,
                "total": total,
                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            data["reservas"].append(nueva_reserva)
            with open("data.json", "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            await update.message.reply_text(
                f"✅ *Reserva registrada:*\n"
                f"👤 {nombre}\n"
                f"🥐 {producto_info['nombre']} x{cantidad}\n"
                f"💰 Total: ${total}",
                parse_mode="Markdown"
            )

async def ver_reservas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not data["reservas"]:
        await update.message.reply_text("📭 No hay reservas registradas.")
        return
    mensaje = "📋 *Reservas actuales:*\n\n"
    for i, r in enumerate(data["reservas"], start=1):
        mensaje += f"{i}. 👤 {r['cliente']} - {r['producto']} x{r['cantidad']} 💰 ${r['total']} ({r['fecha']})\n"
    await update.message.reply_text(mensaje, parse_mode="Markdown")

TOKEN = "TU_TOKEN_DEL_BOT"
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("recetas", recetas))
app.add_handler(CommandHandler("productos", productos))
app.add_handler(CommandHandler("reserva", reserva))
app.add_handler(CommandHandler("verreservas", ver_reservas))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mostrar_receta))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guardar_reserva))
app.run_polling()
