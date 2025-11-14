import os
import tempfile
import subprocess
from telegram import Update
from telegram.ext import ContextTypes
from groq import Groq
from dotenv import load_dotenv


# 🔐 Cargar variables de entorno
load_dotenv()
API_KEY_GROQ = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=API_KEY_GROQ)

# ✅ Conversión con ffmpeg
def convertir_a_wav_ffmpeg(in_path: str, out_path: str) -> bool:
    try:
        cmd = [
            r"C:\Users\Estudiante\OneDrive\Documentos\ffmpeg\ffmpeg-8.0-full_build\bin\ffmpeg.exe",
            "-y", "-i", in_path,
            "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le",
            out_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception as e:
        print(f"Error ffmpeg convirtiendo a WAV: {e}")
        return False

# ✅ Transcripción con Whisper (Groq)
def transcribir_audio_con_groq(path_audio_wav: str) -> str | None:
    try:
        with open(path_audio_wav, "rb") as f:
            transcript = groq_client.audio.transcriptions.create(
                file=(os.path.basename(path_audio_wav), f, "audio/wav"),
                model="whisper-large-v3",
                language="es"
            )
        return getattr(transcript, "text", None) or (transcript.get("text") if isinstance(transcript, dict) else None)
    except Exception as e:
        print(f"Error al transcribir audio con Groq: {e}")
        return None

# ✅ Respuesta con LLM
def responder_con_llm_groq(texto_usuario: str) -> str | None:
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sos un asistente de una panadería. Respondé en español con claridad y cortesía. "
                        "Podés ayudar con pedidos, precios, horarios, tortas personalizadas y promociones."
                    ),
                },
                {"role": "user", "content": texto_usuario},
            ],
            temperature=0.6,
            max_tokens=600,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error al generar respuesta con Groq LLM: {e}")
        return None

# ✅ Handler para notas de voz
async def manejar_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎙️ Recibí tu audio. Procesándolo...")
    try:
        voice = update.message.voice
        if not voice:
            await update.message.reply_text("❌ No se encontró audio en el mensaje.")
            return

        file = await voice.get_file()
        ogg_bytes = await file.download_as_bytearray()

        # Guardar OGG temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp_ogg:
            tmp_ogg.write(ogg_bytes)
            ogg_path = tmp_ogg.name

        # Convertir a WAV con ffmpeg
        wav_path = ogg_path.replace(".ogg", ".wav")
        if not convertir_a_wav_ffmpeg(ogg_path, wav_path):
            await update.message.reply_text("❌ No pude convertir tu audio.")
            return

        # Transcribir
        texto = transcribir_audio_con_groq(wav_path)
        if not texto:
            await update.message.reply_text("❌ No pude transcribir tu audio.")
            return

        # Generar respuesta
        respuesta = responder_con_llm_groq(texto)
        if not respuesta:
            await update.message.reply_text("❌ No pude generar respuesta.")
            return

        await update.message.reply_text(f"📝 Transcripción:\n{texto}\n\n💬 Respuesta:\n{respuesta}")

    except Exception as e:
        print(f"Error general al manejar voice: {e}")
        await update.message.reply_text("❌ Ocurrió un problema procesando tu audio.")

# ✅ Handler para archivos de audio
async def manejar_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎧 Recibí tu archivo de audio. Procesándolo...")
    try:
        audio_obj = update.message.audio or update.message.document
        if not audio_obj:
            await update.message.reply_text("❌ No se encontró archivo de audio.")
            return

        file = await audio_obj.get_file()
        audio_bytes = await file.download_as_bytearray()

        # Guardar archivo temporal con extensión
        filename = getattr(audio_obj, "file_name", "audio_input")
        ext = os.path.splitext(filename)[1].lower() or ".bin"
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_in:
            tmp_in.write(audio_bytes)
            in_path = tmp_in.name

        # Convertir a WAV con ffmpeg
        wav_path = in_path.rsplit(".", 1)[0] + ".wav"
        if not convertir_a_wav_ffmpeg(in_path, wav_path):
            await update.message.reply_text("❌ No pude convertir tu archivo de audio.")
            return

        # Transcribir
        texto = transcribir_audio_con_groq(wav_path)
        if not texto:
            await update.message.reply_text("❌ No pude transcribir tu audio.")
            return

        # Responder con LLM
        respuesta = responder_con_llm_groq(texto)
        if not respuesta:
            await update.message.reply_text("❌ No pude generar respuesta.")
            return

        await update.message.reply_text(f"📝 Transcripción:\n{texto}\n\n💬 Respuesta:\n{respuesta}")

    except Exception as e:
        print(f"Error general al manejar audio: {e}")
        await update.message.reply_text("❌ Ocurrió un problema procesando tu audio.")
