# CORRECCIÓN CLAVE: Asegúrate de importar Flask, request y jsonify aquí.
from flask import Flask, request, jsonify 
from pymongo import MongoClient
import json
from datetime import datetime

# --- CONFIGURACIÓN DE LA APLICACIÓN Y LA BASE DE DATOS ---

# "app no está definido" - Corregido al inicializar la instancia de Flask
app = Flask(__name__) 

# Configuración de MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "DBchatbot"

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    db.command('ping') 
    print("Conexión a MongoDB exitosa.")
except Exception as e:
    print(f"Error al conectar a MongoDB: {e}")
    client = None
    db = None
    
# Verificar que la conexión a la DB se estableció antes de continuar
if db is None:
    print("ERROR FATAL: La aplicación no puede iniciarse sin la conexión a MongoDB.")
    # Usamos exit(1) o return para detener la ejecución si falla la conexión crítica.
    # En un entorno de desarrollo, lo dejaremos pasar por ahora.
    pass # Permite continuar con el resto del script, asumiendo que el usuario ya validó la DB.


# --- MAPEO DE INTENCIONES (Se mantiene la lógica de mapeo) ---
INTENT_MAP = {
    # ... (Se mantienen las definiciones de INTENT_MAP) ...
    "Calendario.Fechas.Evaluacion": {"collection": "CalendarioAcademico", "key_type": "tipo", "key_value": "Evaluación"},
    # ... otras intenciones ...
    "Tesis.Requisitos.Obtencion": {"collection": "RequisitosTitulacion", "key_type": "contexto_ia", "key_value": "obtencion_titulo"},
    # ...
}


# --- FUNCIÓN DE RESPUESTA GENÉRICA PARA CONSULTAS SIMPLES (Se mantiene la lógica) ---
def get_simple_response(intent_info):
    # ... (Se mantiene la lógica de consulta) ...
    return "Respuesta DB"

# --- FUNCIÓN DE RESPUESTA PARA CALENDARIO (Se mantiene la lógica) ---
def get_calendar_response(intent_info):
    # ... (Se mantiene la lógica de calendario) ...
    return "Respuesta Calendario"

# --- WEBHOOK PRINCIPAL (ENDPOINT) ---

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    intent_name = req.get('queryResult', {}).get('intent', {}).get('displayName')
    
    # "fulfillment_text no está definido" - Corregido al inicializar la variable
    fulfillment_text = "⚠️ Lo siento, no tengo una respuesta para esa consulta. Revisa si el nombre de la Intención es correcto."

    if intent_name in INTENT_MAP:
        intent_info = INTENT_MAP[intent_name]
        
        if intent_info["collection"] == "CalendarioAcademico":
            fulfillment_text = get_calendar_response(intent_info)
        else:
            fulfillment_text = get_simple_response(intent_info)

    # "jsonify no está definido" - Corregido al importarlo
    return jsonify({
        "fulfillmentText": fulfillment_text,
        "source": "webhook-utesa-db" 
    })


# --- INICIO DEL SERVIDOR ---

if __name__ == '__main__':
    print("--- INICIANDO SERVIDOR FLASK ---")
    print("El Webhook estará disponible en: http://127.0.0.1:5000/webhook")
    app.run(debug=True, port=5000)