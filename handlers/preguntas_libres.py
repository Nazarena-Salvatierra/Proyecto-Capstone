from telegram import Update
from telegram.ext import ContextTypes
from utils.dataset import cargar_dataset, buscar_en_dataset

faq_dataset = cargar_dataset()

async def responder_pregunta(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pregunta_usuario = update.message.text
    respuesta = buscar_en_dataset(pregunta_usuario, faq_dataset)

    if respuesta:
        await update.message.reply_text(respuesta)
    else:
        await update.message.reply_text("😕 No encontré una respuesta para eso. Probá con otra pregunta o usá /start.")
