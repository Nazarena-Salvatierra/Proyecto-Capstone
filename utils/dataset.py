import json

def cargar_dataset(path="json_preguntas.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def buscar_en_dataset(pregunta, dataset):
    pregunta = pregunta.strip().lower()
    for item in dataset:
        if item["pregunta"].strip().lower() == pregunta:
            return item["respuesta"]
    return None
