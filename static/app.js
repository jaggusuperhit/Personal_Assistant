// DOM Elements
const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const loadingIndicator = document.getElementById('loading');

// Configuration
const config = {
  apiEndpoint: 'http://localhost:5000/ask',
  assistantName: 'AI Assistant',
  userAvatar: '👤',
  assistantAvatar: '🤖',
  thinkingMessages: [
    "Let me think about that...",
    "Consulting my knowledge base...",
    "Processing your question...",
    "Generating a response..."
  ]
};

// Initialize chat
function initChat() {
  addSystemMessage(`Hello! I'm your personal assistant. How can I help you today?`);
  userInput.focus();
  
  // Load chat history from localStorage if available
  const chatHistory = localStorage.getItem('chatHistory');
  if (chatHistory) {
    chatContainer.innerHTML = chatHistory;
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }
}

// Add message to chat
function addMessage(content, sender, avatar = null) {
  const messageDiv = document.createElement('div');
  messageDiv.classList.add('message');
  messageDiv.classList.add(`${sender}-message`);
  
  const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  
  messageDiv.innerHTML = `
    ${avatar ? `<span class="avatar">${avatar}</span>` : ''}
    <div class="message-content">${content}</div>
    <div class="timestamp">${timestamp}</div>
  `;
  
  chatContainer.appendChild(messageDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
  
  // Save to localStorage
  localStorage.setItem('chatHistory', chatContainer.innerHTML);
  
  return messageDiv;
}

// Add system message (no avatar, centered)
function addSystemMessage(content) {
  const messageDiv = document.createElement('div');
  messageDiv.classList.add('message');
  messageDiv.classList.add('system-message');
  messageDiv.textContent = content;
  chatContainer.appendChild(messageDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Show loading state
function showLoading() {
  loadingIndicator.style.display = 'block';
  
  // Random thinking message
  const thinkingMessage = config.thinkingMessages[
    Math.floor(Math.random() * config.thinkingMessages.length)
  ];
  
  const thinkingElement = addMessage(thinkingMessage, 'assistant', config.assistantAvatar);
  thinkingElement.classList.add('thinking');
  
  return thinkingElement;
}

// Hide loading state
function hideLoading(thinkingElement) {
  loadingIndicator.style.display = 'none';
  if (thinkingElement) {
    thinkingElement.remove();
  }
}

// Process user input
async function processInput() {
  const message = userInput.value.trim();
  if (!message) return;
  
  // Add user message
  addMessage(message, 'user', config.userAvatar);
  userInput.value = '';
  
  // Show loading
  const thinkingElement = showLoading();
  
  try {
    // Call backend API
    const response = await fetch(config.apiEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: message })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    // Remove thinking message and show actual response
    hideLoading(thinkingElement);
    addMessage(data.response, 'assistant', config.assistantAvatar);
    
    // Add source documents if available
    if (data.source_documents && data.source_documents.length > 0) {
      const sources = data.source_documents
        .map(doc => doc.metadata.source || 'Document')
        .filter((value, index, self) => self.indexOf(value) === index)
        .join(', ');
      
      const sourceDiv = document.createElement('div');
      sourceDiv.classList.add('source-docs');
      sourceDiv.textContent = `Sources: ${sources}`;
      chatContainer.appendChild(sourceDiv);
    }
    
  } catch (error) {
    hideLoading(thinkingElement);
    addMessage(`Sorry, I encountered an error: ${error.message}`, 'assistant', config.assistantAvatar);
    console.error('Error:', error);
  }
}

// Event Listeners
sendButton.addEventListener('click', processInput);

userInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    processInput();
  }
});

// Clear chat history (optional - add a button in HTML to trigger this)
function clearChat() {
  if (confirm('Are you sure you want to clear the chat history?')) {
    localStorage.removeItem('chatHistory');
    chatContainer.innerHTML = '';
    addSystemMessage(`Chat history cleared. How can I help you now?`);
  }
}

// Initialize chat when DOM is loaded
document.addEventListener('DOMContentLoaded', initChat);