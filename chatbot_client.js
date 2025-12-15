// =========================================================================
// SCRIPT DEL CLIENTE CHATBOT (SIMULACIÓN DEL WIDGET)
// Este código se ejecuta en el navegador (index.html)
// =========================================================================

// Configuración del Endpoint (usar la URL de Ngrok o la de prueba local)
// IMPORTANTE: Sustituye la URL de abajo por la URL pública de tu Webhook (la de Ngrok)
const FLASK_WEBHOOK_URL = 'http://127.0.0.1:5000/webhook'; 

// --- 1. CONSTRUCCIÓN DE LA INTERFAZ ---

function renderChatWidget() {
    const container = document.getElementById('chatbot-widget-container');
    
    // Crear el botón flotante
    const floatingButton = document.createElement('button');
    floatingButton.id = 'chat-button';
    floatingButton.innerHTML = '<i class="fas fa-comment"></i>';
    
    // Crear la ventana de chat
    const chatWindow = document.createElement('div');
    chatWindow.id = 'chat-window';
    chatWindow.classList.add('hidden'); // Inicialmente oculta
    chatWindow.innerHTML = `
        <div class="chat-header">
            <span>UTESA InfoBot</span>
            <button id="close-chat">X</button>
        </div>
        <div class="chat-body" id="chat-messages">
            <div class="message bot-message">¡Hola! Soy tu asistente de UTESA. Pregúntame sobre reglamentos, inscripciones o fechas académicas.</div>
        </div>
        <div class="chat-footer">
            <input type="text" id="user-input" placeholder="Escribe tu consulta...">
            <button id="send-button"><i class="fas fa-paper-plane"></i></button>
        </div>
    `;

    container.appendChild(floatingButton);
    container.appendChild(chatWindow);

    // Añadir eventos
    floatingButton.onclick = () => chatWindow.classList.toggle('hidden');
    document.getElementById('close-chat').onclick = () => chatWindow.classList.add('hidden');
    document.getElementById('send-button').onclick = sendMessage;
    document.getElementById('user-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
}


// --- 2. COMUNICACIÓN CON FLASK/WEBHOOK (LA CONEXIÓN) ---

async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const messageText = userInput.value.trim();
    
    if (messageText === "") return;

    // Mostrar mensaje del usuario inmediatamente
    appendMessage(messageText, 'user-message');
    userInput.value = '';
    
    // Simulación de Dialogflow (asumimos que Dialogflow reenvía la consulta sin cambios)
    appendMessage("Pensando...", 'bot-message loading');

    try {
        // Petición POST simulada al Webhook de Flask
        const response = await fetch(FLASK_WEBHOOK_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Simulamos la estructura mínima que Dialogflow enviaría
            },
            body: JSON.stringify({ 
                queryResult: { 
                    queryText: messageText,
                    // Normalmente Dialogflow detecta y envía la Intención, 
                    // pero aquí enviamos solo el texto para que Flask simule la detección.
                } 
            })
        });

        const data = await response.json();
        
        // Remover el mensaje de "Pensando..."
        const loadingMessage = document.querySelector('.loading');
        if (loadingMessage) loadingMessage.remove();

        // Mostrar la respuesta de Flask (fulfillmentText)
        if (data.fulfillmentText) {
            appendMessage(data.fulfillmentText, 'bot-message');
        } else {
            appendMessage("Error: La respuesta del servidor está vacía.", 'bot-message');
        }

    } catch (error) {
        console.error('Error al conectar con el Webhook:', error);
        const loadingMessage = document.querySelector('.loading');
        if (loadingMessage) loadingMessage.remove();
        appendMessage("Error: No se pudo conectar con el servidor (Webhook). ¿Está corriendo Ngrok?", 'bot-message error');
    }
}


// --- 3. FUNCIONES DE UTILIDAD ---

function appendMessage(text, className) {
    const chatBody = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', className);
    
    // Reemplazar saltos de línea (\n) con <br> para formatear la respuesta del backend
    messageDiv.innerHTML = text.replace(/\n/g, '<br>'); 
    
    chatBody.appendChild(messageDiv);
    chatBody.scrollTop = chatBody.scrollHeight; // Scroll al final
}

// Inicializar el widget cuando el documento esté listo
document.addEventListener('DOMContentLoaded', () => {
    renderChatWidget();
});