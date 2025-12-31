document.addEventListener('DOMContentLoaded', () => {
    const chatHistory = document.getElementById('chat-history');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const systemLog = document.getElementById('system-log');
    
    // Memory Viz Elements
    const bufferUsageBar = document.getElementById('buffer-usage-bar');
    const bufferUsageText = document.getElementById('buffer-usage-text');
    const bufferMap = document.getElementById('buffer-map');
    const totalAllocated = document.getElementById('total-allocated');
    const activeSegment = document.getElementById('active-segment');
    const briefStatus = document.getElementById('brief-status');
    const briefText = document.getElementById('brief-text');

    // Initialize Memory Map Grid
    for (let i = 0; i < 64; i++) {
        const block = document.createElement('div');
        block.className = 'memory-block';
        bufferMap.appendChild(block);
    }

    function addLog(message) {
        const time = new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
        const entry = document.createElement('div');
        entry.className = 'log-entry';
        entry.innerHTML = `<span class="time">[${time}]</span> ${message}`;
        systemLog.appendChild(entry);
        systemLog.scrollTop = systemLog.scrollHeight;
    }

    function appendMessage(sender, text, isUser = false) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${isUser ? 'user' : ''}`;
        
        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.textContent = isUser ? 'You' : sender.substring(0, 3).toLowerCase();
        
        const content = document.createElement('div');
        content.className = 'content';
        content.textContent = text;
        
        msgDiv.appendChild(avatar);
        msgDiv.appendChild(content);
        chatHistory.appendChild(msgDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        appendMessage('User', text, true);
        userInput.value = '';
        addLog(`Input received: "${text.substring(0, 15)}..."`);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await response.json();
            appendMessage('Agent', data.response);
            addLog(`Response generated`);
        } catch (error) {
            console.error('Error:', error);
            addLog(`Error: ${error.message}`);
        }
    }

    async function updateMemoryStats() {
        try {
            const response = await fetch('/api/memory-status');
            const stats = await response.json();

            // Update Buffer Usage
            bufferUsageBar.style.width = `${stats.buffer_usage}%`;
            bufferUsageText.textContent = `${stats.buffer_usage}%`;

            // Update Stats Text
            totalAllocated.textContent = `${(stats.total_allocated / 1024).toFixed(1)} KB`;
            activeSegment.textContent = stats.active_segment;

            // Randomly animate memory blocks to simulate activity
            const blocks = bufferMap.children;
            for (let i = 0; i < blocks.length; i++) {
                if (Math.random() > 0.9) {
                    blocks[i].classList.toggle('active');
                }
            }

            // Update Brief Status
            if (stats.brief_locked) {
                briefStatus.innerHTML = '<div class="icon-lock locked"></div><span>Locked (Debating)</span>';
                briefStatus.style.borderColor = 'var(--danger-color)';
            }

        } catch (error) {
            console.error('Stats Error:', error);
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    // Poll for stats every 1 second
    setInterval(updateMemoryStats, 1000);
});
