from pymongo import MongoClient

# 1. Conexión al servidor local de MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['UTESA_Chatbot'] # Nombre de tu base de datos

# 2. Definición de los Datasets (Módulos Lógicos)
# Aquí organizamos la información según tu tabla de "Módulo Lógico"

datasets = {
    "RequisitosTitulacion": [
        {
            "articulo": "Requisitos de Grado",
            "contexto": "obtencion_titulo",
            "detalle": [
                "Haber aprobado todas las asignaturas del pensum.",
                "Completar las horas de servicio social requeridas.",
                "Estar al día con los pagos administrativos."
            ],
            "tema": "Graduación"
        }
    ],
    "ReglamentosDisciplinarios": [
        {
            "articulo": "Faltas Gravísimas",
            "contexto": "disciplina_gravisimas",
            "detalle": [
                "Falsificación de documentos oficiales.",
                "Agresión física dentro del recinto.",
                "Uso de sustancias prohibidas."
            ],
            "sancion_asociada": "Expulsión definitiva o suspensión por 2 años.",
            "tema": "Disciplina"
        }
    ],
    "CalendarioAcademico": [
        {
            "cuatrimestre_id": "3-2025",
            "evento": "Exámenes Finales",
            "fecha_inicio": "2025-12-01",
            "fecha_fin": "2025-12-10",
            "tipo": "Evaluación"
        }
    ],
    "ProcesosInscripcion": [
        {
            "articulo": "Retiro de Asignaturas",
            "contexto": "Retiro.EnLinea",
            "detalle": [
                "Ingresar al portal de estudiantes.",
                "Seleccionar la opción 'Retiro en Línea'.",
                "Confirmar la materia antes de la fecha límite."
            ],
            "tema": "Inscripción"
        }
    ]
}

# 3. Función para enviar los datos a la base de datos
def cargar_datos():
    for nombre_coleccion, datos in datasets.items():
        # Seleccionamos la colección (Módulo)
        coleccion = db[nombre_coleccion]
        
        # Insertamos los documentos
        coleccion.insert_many(datos)
        print(f"✅ Módulo '{nombre_coleccion}' cargado con éxito.")

if __name__ == "__main__":
    # Limpiar datos viejos antes de cargar (opcional)
    client.drop_database('UTESA_Chatbot')
    
    # Ejecutar la carga
    cargar_datos()
    print("\n🚀 Todos los datasets han sido enviados a MongoDB.")