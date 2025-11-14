🥖 Bot de Panadería LuNaTi
Este proyecto es un bot de Telegram que simula la gestión de una panadería llamada LuNaTi. Permite a clientes hacer pedidos y reservas, y a trabajadores acceder a un menú privado con stock y pedidos.
🚀 Instalación y ejecución
1.	Clonar el repositorio.
2.	Instalar dependencias: pip install python-telegram-bot==20.3 google-generativeai openai groq
3.	Configurar claves: TOKEN, API_KEY_GROQ, openai.api_key, genai.configure().
4.	Ejecutar: python bot.py
👤 Modo Cliente
•	/start → muestra el menú inicial.
•	/recetas → lista recetas disponibles.
•	Número de receta → muestra ingredientes y pasos.
•	/productos → lista productos con precios.
•	/reserva → explica cómo hacer un pedido.
•	Nombre - Producto - Cantidad → guarda la reserva.
•	/verreservas → muestra todas las reservas.
•	Enviar imagen → el bot sugiere un pedido con IA.
•	/modificar → editar el pedido sugerido.
•	/confirmar → confirmar el pedido y generar ticket.
🧑‍🍳 Modo Trabajador
/trabajador → solicita el código.
Ingresar: panaderia2025.
Menú de trabajo:
• Ver pedidos
• Ver stock
📂 Archivos principales
•	bot.py → archivo principal, registra todos los handlers.
•	reservas.py → recetas, productos y reservas.
•	imagenes.py → pedidos a partir de imágenes con IA.
•	trabajador.py → acceso de trabajadores y menú.
•	comandos.py → comandos rápidos.
•	audio.py → manejo de audios.
•	clientes.py → menú inicial para clientes.
🎯 Ejemplo de uso
Cliente:
/start
/productos
Juan Pérez - Pan Casero - 2
/verreservas
Trabajador:
/trabajador
panaderia2025
Ver pedidos
Ver stock
💡 Nota final
•	Los clientes pueden hacer pedidos y reservas.
•	Los trabajadores tienen un menú privado con stock y pedidos.
•	La información se guarda en data.json.
![alt text](<imagen ilustracion LuNaTi.png>)