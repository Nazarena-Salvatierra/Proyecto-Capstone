🥖 Bot de Panadería LuNaTi








Bot de Telegram que simula la gestión de una panadería llamada LuNaTi.
Permite a los clientes hacer pedidos y reservas, y a los trabajadores acceder a un menú interno con stock y pedidos.

📌 Características principales

✔️ Menú interactivo para clientes
✔️ Sistema de reservas
✔️ Lectura y análisis de imágenes con IA
✔️ Menú privado para trabajadores
✔️ Gestión de stock y pedidos
✔️ Persistencia de datos en data.json

🚀 Instalación

Clonar el repositorio

git clone https://github.com/tuusuario/Panaderia-LuNaTi.git
cd Panaderia-LuNaTi


Instalar dependencias

pip install python-telegram-bot==20.3 google-generativeai openai groq


Configurar claves
En tu archivo de configuración o directamente en el código:

TOKEN (Telegram Bot)

API_KEY_GROQ

openai.api_key

genai.configure(api_key=...)

Ejecutar el bot

python bot.py

👤 Modo Cliente

Comandos disponibles:

/start → menú inicial

/recetas → lista recetas

Número de receta → muestra ingredientes/pasos

/productos → lista con precios

/reserva → guía para pedir

Nombre - Producto - Cantidad → genera reserva

/verreservas → muestra reservas

Enviar imagen → sugerencia de pedido con IA

/modificar → edita el pedido sugerido

/confirmar → confirma el pedido y genera ticket

🧑‍🍳 Modo Trabajador

Acceso restringido:

Enviar /trabajador

Ingresar código → panaderia2025

Opciones del menú interno:

📋 Ver pedidos

📦 Ver stock

También funciona por texto:

ver pedidos

ver stock

📂 Estructura del proyecto
Panaderia-LuNaTi/
│── bot.py
│── reservas.py
│── imagenes.py
│── trabajador.py
│── comandos.py
│── audio.py
│── clientes.py
│── data.json
│── README.md

🎯 Ejemplos de uso
Cliente
/start
/productos
Juan Pérez - Pan Casero - 2
/verreservas

Trabajador
/trabajador
panaderia2025
Ver pedidos
Ver stock

💾 Archivo de datos: data.json

Todas las reservas, pedidos y stock se almacenan en este archivo para mantener persistencia entre ejecuciones.

🛠️ Tecnologías utilizadas

Python 3.10+

python-telegram-bot 20.3

OpenAI API

Groq

Google Generative AI

📜 Licencia

Este proyecto se encuentra bajo licencia MIT.
Podés modificarlo y adaptarlo libremente.

💬 Autores 

Maria Nazarena Salvatierra Gomez 
Lucas Carrizo
Ticiano Carrasco
✨
Estudiantes apasionados por IA, automatización y desarrollo de bots.
![alt text](<imagen ilustracion LuNaTi.png>)
