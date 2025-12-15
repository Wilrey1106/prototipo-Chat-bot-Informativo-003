# UTESA InfoBot 

Este proyecto es un chatbot inteligente diseñado para automatizar la asistencia estudiantil en la **Universidad Tecnológica de Santiago (UTESA)**.

## Información del Autor
* **Nombre:** Wilmer R. Ortega Reynoso 
* **Matrícula:** 2-23-3666 
* **Carrera:** Ingeniería en Sistemas Computacionales.
* **Docente:** Juan José Díaz Nerio 
## Tecnologías (Stack)
* **IA/PLN:** Google Dialogflow (para entender qué dice el estudiante).
* **Backend:** Flask (Python) para la lógica del Webhook.
* **Base de Datos:** MongoDB (NoSQL) para guardar reglamentos y fechas.
* **Interfaz:** Widget de JavaScript para la web.

## Organización del Proyecto
* `/backend`: Código en Python (`main.py`).
* `/data`: Esquemas de colecciones de MongoDB.
* `/frontend`: Archivos de la interfaz web.

## Cómo funciona
1. El estudiante hace una pregunta en el chat.
2. **Dialogflow** detecta la intención (ej. "Requisitos de Tesis").
3. El servidor **Flask** busca la respuesta exacta en **MongoDB**.
4. El bot responde de forma inmediata 24/7.

---
*Proyecto final para la asignatura Seminario de Informática / Inteligencia Artificial - 2025.*.
