🥖 Bot de Panadería LuNaTi
Bot de Telegram que simula la gestión de una panadería llamada LuNaTi. Permite a los clientes realizar pedidos y reservas, y a los trabajadores acceder a un menú interno para gestionar stock y pedidos.

📌 Características principales
✔️ Menú interactivo para clientes

✔️ Sistema de reservas

✔️ Lectura y análisis de imágenes con IA

✔️ Menú privado para trabajadores

✔️ Gestión de stock y pedidos

✔️ Persistencia de datos en data.json

🚀 Instalación
1. Clonar el repositorio
bash
git clone https://github.com/tuusuario/Panaderia-LuNaTi.git
cd Panaderia-LuNaTi
2. Instalar dependencias
bash
pip install python-telegram-bot==20.3 google-generativeai openai groq python-dotenv
3. Configurar claves en .env
Crea un archivo .env en la raíz del proyecto con las siguientes variables:

Código
TELEGRAM_TOKEN=tu_token_de_telegram
GROQ_API_KEY=tu_api_key_de_groq
OPENAI_API_KEY=tu_api_key_de_openai
GEMINI_API_KEY=tu_api_key_de_google
⚠️ El archivo .env está ignorado en .gitignore para proteger tus claves.

4. Ejecutar el bot
bash
python bot.py
👤 Modo Cliente
Comandos disponibles:

/inicio → menú inicial

/recetas → lista de recetas

Número de receta → muestra ingredientes/pasos

/productos → lista con precios

/reserva → guía para pedir

Nombre - Producto - Cantidad → genera reserva

/verreservas → muestra reservas

Enviar imagen → sugerencia de pedido con IA

/modificar → edita el pedido solicitado

/confirmar → confirma el pedido y genera ticket

🧑‍🍳 Modo Trabajador
Acceso:

Enviar /trabajador

Ingresar código: panaderia2025

Opciones del menú interno:

📋 Ver pedidos

📦 Ver stock

También funciona por texto:

ver pedidos

ver stock

📂 Estructura del proyecto
Código
Panaderia-LuNaTi/
│── bot.py
│── handlers/
│   ├── reservas.py
│   ├── imagenes.py
│   ├── trabajador.py
│   ├── comandos.py
│   ├── audio.py
│   ├── clientes.py
│── data.json
│── README.md
│── .env
│── .gitignore
🎯 Ejemplos de uso
Cliente
bash
/start
/productos
Juan Pérez - Pan Casero - 2
/verreservas
Trabajador
bash
/trabajador
panaderia2025
ver pedidos
ver stock
💾 Archivo de datos
data.json: almacena todas las reservas, pedidos y stock para mantener persistencia entre ejecuciones.

🛠️ Tecnologías utilizadas
Python 3.10+

python-telegram-bot 20.3

API de OpenAI

Groq

IA generativa de Google

python-dotenv para gestión segura de claves

📜 Licencia
Este proyecto se encuentra bajo licencia MIT. Podés modificarlo y adaptarlo libremente.

💬 Autores
María Nazarena Salvatierra Gómez

Lucas Carrizo

Ticiano Carrasco

✨ Estudiantes apasionados por IA, automatización y desarrollo de bots.
![alt text](<imagen ilustracion LuNaTi.png>)
