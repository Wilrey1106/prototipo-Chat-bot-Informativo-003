from pymongo import MongoClient
import json

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "DBchatbot"

# Inicializa la conexión a MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

print(f"Iniciando proceso de carga ETL en {DB_NAME}...")

# --- FUNCIÓN DE CARGA ---

def cargar_documentos(coleccion_nombre, documentos):
    """Limpia la colección y carga los documentos proporcionados."""
    coleccion = db[coleccion_nombre]
    
    # 1. Limpiar la colección existente (para evitar duplicados)
    coleccion.delete_many({})
    
    # 2. Insertar los nuevos documentos
    resultado = coleccion.insert_many(documentos)
    
    print(f"✅ Colección '{coleccion_nombre}' cargada. Documentos insertados: {len(resultado.inserted_ids)}")

# =========================================================================
# I. CONTEXTO: CALENDARIO ACADÉMICO (Cuatrimestres 1, 2 y 3 de 2025)
# =========================================================================

calendario_total = []

# --- CALENDARIO CUATRIMESTRE 1-2025 (Enero - Abril) ---
calendario_1_2025 = [
    {"cuatrimestre_id": "1-2025", "fecha_inicio": "2025-01-16", "fecha_fin": "2025-01-16", "evento": "Inicio Docencia de Grado y Postgrado", "tipo": "Inicio"},
    {"cuatrimestre_id": "1-2025", "fecha_inicio": "2025-01-21", "fecha_fin": "2025-01-21", "evento": "Asueto Día de Nuestra Señora de la Altagracia", "tipo": "Asueto"},
    {"cuatrimestre_id": "1-2025", "fecha_inicio": "2025-03-03", "fecha_fin": "2025-03-08", "evento": "Primer Período Evaluativo (Parciales)", "tipo": "Evaluación"},
    {"cuatrimestre_id": "1-2025", "fecha_inicio": "2025-03-24", "fecha_fin": "2025-03-30", "evento": "Preselección de Asignaturas Cuatrimestre 2-2025", "tipo": "Inscripción"},
    {"cuatrimestre_id": "1-2025", "fecha_inicio": "2025-04-16", "fecha_fin": "2025-04-16", "evento": "Final de la Docencia", "tipo": "Académico"},
    {"cuatrimestre_id": "1-2025", "fecha_inicio": "2025-04-21", "fecha_fin": "2025-04-26", "evento": "Segundo Período Evaluativo (Exámenes Finales)", "tipo": "Evaluación"},
]
calendario_total.extend(calendario_1_2025)

# --- CALENDARIO CUATRIMESTRE 2-2025 (Mayo - Agosto) ---
calendario_2_2025 = [
    {"cuatrimestre_id": "2-2025", "fecha_inicio": "2025-05-19", "fecha_fin": "2025-05-19", "evento": "Inicio Docencia de Grado y Postgrado", "tipo": "Inicio"},
    {"cuatrimestre_id": "2-2025", "fecha_inicio": "2025-06-19", "fecha_fin": "2025-06-19", "evento": "Asueto Día de Corpus Christi", "tipo": "Asueto"},
    {"cuatrimestre_id": "2-2025", "fecha_inicio": "2025-06-30", "fecha_fin": "2025-07-05", "evento": "Primer Período Evaluativo (Parciales)", "tipo": "Evaluación"},
    {"cuatrimestre_id": "2-2025", "fecha_inicio": "2025-07-21", "fecha_fin": "2025-08-01", "evento": "Preselección de Asignaturas Cuatrimestre 3-2025", "tipo": "Inscripción"},
    {"cuatrimestre_id": "2-2025", "fecha_inicio": "2025-08-15", "fecha_fin": "2025-08-15", "evento": "Final de la Docencia", "tipo": "Académico"},
    {"cuatrimestre_id": "2-2025", "fecha_inicio": "2025-08-25", "fecha_fin": "2025-08-30", "evento": "Segundo Período Evaluativo (Exámenes Finales)", "tipo": "Evaluación"},
]
calendario_total.extend(calendario_2_2025)

# --- CALENDARIO CUATRIMESTRE 3-2025 (Septiembre - Diciembre) ---
calendario_3_2025 = [
    {"cuatrimestre_id": "3-2025", "fecha_inicio": "2025-09-05", "fecha_fin": "2025-09-11", "evento": "Inscripciones Regulares", "tipo": "Inscripción"},
    {"cuatrimestre_id": "3-2025", "fecha_inicio": "2025-09-16", "fecha_fin": "2025-09-16", "evento": "Inicio Docencia de Grado y Postgrado", "tipo": "Inicio"},
    {"cuatrimestre_id": "3-2025", "fecha_inicio": "2025-10-20", "fecha_fin": "2025-10-25", "evento": "Primer Período Evaluativo (Parciales)", "tipo": "Evaluación"},
    {"cuatrimestre_id": "3-2025", "fecha_inicio": "2025-12-01", "fecha_fin": "2025-12-07", "evento": "Preselección de Asignaturas Cuatrimestre 1-2026", "tipo": "Inscripción"},
    {"cuatrimestre_id": "3-2025", "fecha_inicio": "2025-12-13", "fecha_fin": "2025-12-13", "evento": "Final de la Docencia", "tipo": "Académico"},
    {"cuatrimestre_id": "3-2025", "fecha_inicio": "2025-12-15", "fecha_fin": "2025-12-20", "evento": "Segundo Período Evaluativo (Exámenes Finales)", "tipo": "Evaluación"},
]
calendario_total.extend(calendario_3_2025)

# =========================================================================
# II. CONTEXTO: REGLAMENTOS INSTITUCIONALES (Disciplina y Derechos)
# =========================================================================

reglamentos_disciplina = [
    {
        "tema": "Normas Disciplinarias (Abstenciones)",
        "contexto_ia": "disciplina_prohibiciones",
        "detalle": [
            "Hacer comentarios negativos en redes sociales o medios sobre la Universidad o autoridades académicas.",
            "Utilizar el nombre o insignias de la Institución sin autorización.",
            "Publicar fotos o videos tomados en áreas de la Institución sin autorización.",
            "Fumar, comer o beber dentro del salón de clases.",
            "Participar en juegos de azar o realizar recolecta de dinero sin autorización."
        ],
        "sancion_asociada": "Falta leve, grave o gravísima."
    },
    {
        "tema": "Faltas Gravísimas",
        "contexto_ia": "disciplina_gravísimas",
        "detalle": [
            "Sustraer dinero, equipos, artículos, vehículos o documentos oficiales.",
            "Falsificar documentos oficiales o presentar documentos adulterados.",
            "Realizar actos que puedan viciar pruebas evaluativas (fotocopiar exámenes, examinarse por otro).",
            "Plagiar cualquier trabajo de la Universidad, incluido el Anteproyecto o Proyecto de Grado."
        ],
        "sancion_asociada": "Suspensión de tres cuatrimestres en adelante, suspensión de la carrera o cancelación de la matrícula (retiro definitivo)."
    }
]

derechos_estudiantiles = [
    {
        "tema": "Derechos del Estudiante",
        "contexto_ia": "derechos_generales",
        "articulo": "Artículo 12",
        "detalle": [
            "Una educación que desarrolle la creatividad, la participación y el respeto a sus ideas.",
            "Ser tratado con respeto a su dignidad y creencias.",
            "Presentar quejas o sugerencias ante el organismo competente y obtener respuestas.",
            "Solicitar intertransferencia de un Recinto a otro.",
            "Tener privacidad de su Récord de Calificaciones."
        ]
    },
    {
        "tema": "Deberes del Estudiante",
        "contexto_ia": "deberes_generales",
        "articulo": "Artículo 13",
        "detalle": [
            "Respetar y preservar la institucionalidad (asistencia, exámenes, pagos oportunos).",
            "Proponer soluciones factibles a situaciones universitarias usando canales establecidos.",
            "Preservar y respetar la imagen institucional, portando el carnet visible y cuidando la infraestructura."
        ]
    }
]

# =========================================================================
# III. CONTEXTO: PROCESOS DE TESIS Y HONORES
# =========================================================================

requisitos_titulacion = [
    {
        "tema": "Requisitos para Obtención del Título",
        "contexto_ia": "obtencion_titulo",
        "articulo": "Artículo 92",
        "detalle": [
            "Tener un Índice Acumulado igual o mayor a 2.0.",
            "Aprobar todas las asignaturas del pénsum respectivo.",
            "Participar en tres seminarios relacionados con su área profesional.",
            "Participar en el acto de investidura."
        ]
    },
    {
        "tema": "Modalidades de Titulación",
        "contexto_ia": "modalidad_titulacion",
        "articulo": "Artículo 94",
        "detalle": [
            "Curso Monográfico o Proyecto de Grado o su equivalente es uno de los requisitos.",
            "El Curso Monográfico y el Proyecto de Grado solo podrán cursarse cuando el estudiante haya aprobado todas las asignaturas del pénsum."
        ]
    }
]

honores_academicos = [
    {
        "tema": "Escala de Honores",
        "contexto_ia": "escala_honores",
        "detalle": [
            "CUM LAUDE: Índice Académico de 3.2 - 3.4.",
            "MAGNA CUM LAUDE: Índice Académico de 3.5 - 3.7.",
            "SUMMA CUM LAUDE: Índice Académico de 3.8 - 4.0."
        ]
    },
    {
        "tema": "Exclusiones de Honores",
        "contexto_ia": "exclusiones_honores",
        "detalle": [
            "Reprueban alguna asignatura, módulo en el Curso Monográfico o Proyecto de Grado.",
            "Han sido sancionados por el Consejo Disciplinario.",
            "Retiran más de cinco asignaturas en el curso de su carrera."
        ]
    }
]

# =========================================================================
# IV. CONTEXTO: INSCRIPCIONES Y CONVALIDACIONES
# =========================================================================

procesos_inscripcion = [
    {
        "tema": "Preselección de Asignaturas",
        "contexto_ia": "Inscripcion.Preseleccion",
        "articulo": "Artículo 49",
        "detalle": [
            "Es el proceso para seleccionar las asignaturas que se desean cursar en el cuatrimestre siguiente.",
            "Se realiza en la fecha establecida en el Calendario Académico de la Universidad.",
            "Las modificaciones pueden realizarse en línea o de manera presencial."
        ]
    },
    {
        "tema": "Retiro de Asignaturas Presencial",
        "contexto_ia": "Retiro.Presencial",
        "articulo": "Artículo 51.1",
        "detalle": [
            "Se realiza hasta la primera semana después de iniciada la docencia.",
            "La asignatura retirada no aparecerá en el Récord de Calificaciones."
        ]
    },
    {
        "tema": "Retiro de Asignaturas en Línea",
        "contexto_ia": "Retiro.EnLinea",
        "articulo": "Artículo 51.2",
        "detalle": [
            "Se realiza a partir de la tercera semana, hasta una semana antes de la segunda prueba parcial.",
            "La asignatura retirada aparecerá con la letra 'R' en el reporte de calificaciones.",
            "El retiro de más de cinco asignaturas durante la carrera es motivo de exclusión de honores académicos."
        ]
    }
]

procesos_convalidacion = [
    {
        "tema": "Definición de Convalidación",
        "contexto_ia": "Convalidacion.Definicion",
        "articulo": "Artículo 56",
        "detalle": ["Es una validación de asignaturas aprobadas en otra Institución de Educación Superior, reconocida por el MESCyT."]
    },
    {
        "tema": "Requisitos de Convalidación",
        "contexto_ia": "Convalidacion.Requisitos",
        "articulo": "Artículo 56",
        "requisitos": [
            "Los programas deben coincidir en su contenido en un 80%.",
            "El número de créditos debe ser igual o superior.",
            "La calificación obtenida debe ser igual o mayor a 70 puntos (o su equivalente).",
            "El mínimo de créditos convalidables es de nueve (9).",
            "Debe realizarse previamente a la inscripción del estudiante."
        ]
    },
]

# =========================================================================
# V. PROCESOS DE CARGA PRINCIPALES
# =========================================================================

# Carga de Datos
cargar_documentos("CalendarioAcademico", calendario_total)
cargar_documentos("ReglamentosDisciplinarios", reglamentos_disciplina)
cargar_documentos("DerechosYDeberes", derechos_estudiantiles)
cargar_documentos("RequisitosTitulacion", requisitos_titulacion)
cargar_documentos("HonoresAcademicos", honores_academicos)
cargar_documentos("ProcesosInscripcion", procesos_inscripcion)
cargar_documentos("ProcesosConvalidacion", procesos_convalidacion)

# --- FINALIZACIÓN ---
print(" Proceso de carga de la Base de Conocimiento completo.")
print("Las colecciones están listas en la base de datos 'DBchatbot'.")

client.close()