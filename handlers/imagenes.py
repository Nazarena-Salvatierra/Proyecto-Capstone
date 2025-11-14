import os
import tempfile
import google.generativeai as genai
import openai
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from dotenv import load_dotenv

# 🔑 Cargar variables de entorno desde .env
load_dotenv()

# Configuración de Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
modelo = genai.GenerativeModel("models/gemini-2.5-pro")  # multimodal

# Configuración de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ Handler para imágenes
async def manejar_imagen(update, context):
    await update.message.reply_text("📸 Recibí tu imagen. Procesándola...")

    try:
        # Descargar la foto
        file = await update.message.photo[-1].get_file()
        img_bytes = await file.download_as_bytearray()

        # Guardar temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_img:
            tmp_img.write(img_bytes)
            img_path = tmp_img.name

        descripcion = None

        try:
            # Subir imagen a Gemini
            uploaded_file = genai.upload_file(img_path)

            # ✅ Pedir descripción objetiva con Gemini
            respuesta = modelo.generate_content([
                "Describe esta imagen en un máximo de 5 frases simples, como si fuera un pedido de un producto en una panadería (pastel, torta, bizcochito, facturas, etc.). Evita adornos literarios, sé claro y directo.",
                uploaded_file
            ])
            descripcion = respuesta.text.strip()
            context.user_data["pedido"] = descripcion

        except Exception as e:
            print(f"Gemini falló: {e}")

        # ✅ Fallback con OpenAI Vision si Gemini no devuelve nada
        if not descripcion:
            try:
                with open(img_path, "rb") as f:
                    import base64
                    img_b64 = base64.b64encode(f.read()).decode()

                    response = openai.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "system",
                                "content": "Sos un asistente de panadería. Describe la imagen como un pedido sugerido, en máximo 5 frases simples, sin adornos literarios."
                            },
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "Describe esta imagen como si fuera un producto de panadería."},
                                    {"type": "image_url", "image_url": "data:image/jpeg;base64," + img_b64}
                                ]
                            }
                        ]
                    )
                descripcion = response.choices[0].message.content.strip()
                context.user_data["pedido"] = descripcion

            except Exception as e:
                print(f"OpenAI Vision falló: {e}")
                descripcion = "No pude procesar la imagen."

        pedido = (
            f"📋 Pedido sugerido:\n\n"
            f"En la imagen que me mandaste veo lo siguiente:\n{descripcion}\n\n"
            f"Si esta descripción corresponde con el pedido que querías realizar o el producto que te gustaría adquirir, escribí /confirmar.\n"
            f"Si querés cambiar algo, escribí /modificar."
        )

        await update.message.reply_text(pedido)

    except Exception as e:
        print(f"Error al manejar imagen: {e}")
        await update.message.reply_text("❌ Ocurrió un problema procesando tu imagen.")

# ✅ Handler para /modificar
async def modificar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.chat_data["esperando_modificacion"] = True
    await update.message.reply_text(
        "✏️ Perfecto, contame qué cambios querés hacer en tu pedido (ej. tamaño, sabor, decoración, etc.)."
    )

# ✅ Handler para guardar cambios escritos por el cliente
async def manejar_cambios(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.chat_data.get("modo_trabajador"):
        return
    if not context.chat_data.get("esperando_modificacion"):
        return

    nuevo_pedido = update.message.text.strip()
    context.user_data["pedido"] = nuevo_pedido
    context.chat_data["esperando_modificacion"] = False
    await update.message.reply_text(
        f"✅ Pedido actualizado:\n{nuevo_pedido}\n\nAhora podés confirmarlo con /confirmar."
    )

# ✅ Handler para /confirmar
async def confirmar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pedido = context.user_data.get("pedido")
    if not pedido:
        await update.message.reply_text(
            "No tengo un pedido para confirmar. Enviá una imagen primero para generar el pedido sugerido."
        )
        return

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    ticket = (
        "🎟️ *Ticket de Pedido*\n"
        "-------------------------\n"
        f"📅 Fecha: {fecha}\n"
        f"📝 Pedido: {pedido}\n"
        "-------------------------\n"
        "✅ Estado: Confirmado\n\n"
        "Te esperamos en el local para que retires tu pedido. ¡Gracias por elegirnos! 🥐🍰"
    )

    await update.message.reply_text(ticket, parse_mode="Markdown")
