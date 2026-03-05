/**
 * FreshBot AI Shopping Assistant
 * Handles the floating chatbot UI and API communication
 */

(function () {
    'use strict';

    // ── Configuration ──────────────────────────────────────────────────────────
    const CONFIG = {
        apiEndpoint: '/api/chatbot',
        resetEndpoint: '/api/chatbot/reset',
        maxMessageLength: 500,
        animationDelay: 50,
        typingDelay: { min: 800, max: 1800 }, // ms
    };

    const SUGGESTIONS = [
        '🥦 What vegetables do you have?',
        '🍳 Suggest a recipe',
        '📦 Track my order',
        '💰 Budget tips',
        '⭐ Loyalty points',
    ];

    // ── State ──────────────────────────────────────────────────────────────────
    let isOpen = false;
    let isSending = false;
    let messageCount = 0;
    let hasShownWelcome = false;

    // ── DOM Elements ────────────────────────────────────────────────────────────
    let fab, window_, messages, input, sendBtn, suggestions;

    // ── Init ────────────────────────────────────────────────────────────────────
    function init() {
        injectHTML();
        cacheElements();
        bindEvents();
        renderSuggestions();

        // Show welcome notification after short delay
        setTimeout(() => {
            if (!isOpen) showFabBadge();
        }, 2500);
    }

    function injectHTML() {
        const wrapper = document.createElement('div');
        wrapper.innerHTML = `
        <button id="freshbot-fab" aria-label="Open FreshBot AI Assistant" title="Chat with FreshBot">
            <span class="material-icons fab-icon fab-icon-bot">smart_toy</span>
            <span class="material-icons fab-icon fab-icon-open">close</span>
        </button>
        <div id="freshbot-window" role="dialog" aria-label="FreshBot AI Shopping Assistant" aria-live="polite">
            <div id="freshbot-header">
                <div class="freshbot-avatar">🤖</div>
                <div class="freshbot-header-info">
                    <div class="freshbot-header-name">FreshBot AI</div>
                    <div class="freshbot-header-status">Online &bull; AI Shopping Assistant</div>
                </div>
                <button id="freshbot-reset-btn" title="New conversation" aria-label="Reset conversation">
                    <span class="material-icons" style="font-size:18px">restart_alt</span>
                </button>
                <button id="freshbot-close-btn" title="Close chat" aria-label="Close FreshBot">
                    <span class="material-icons" style="font-size:18px">expand_more</span>
                </button>
            </div>
            <div id="freshbot-suggestions" aria-label="Quick question suggestions"></div>
            <div id="freshbot-messages" role="log" aria-label="Chat messages"></div>
            <div id="freshbot-input-area">
                <textarea
                    id="freshbot-input"
                    placeholder="Ask FreshBot anything..."
                    rows="1"
                    maxlength="500"
                    aria-label="Message input"
                ></textarea>
                <button id="freshbot-send-btn" aria-label="Send message" disabled>
                    <span class="material-icons">send</span>
                </button>
            </div>
        </div>`;

        // Append children individually to avoid a wrapper div in DOM
        while (wrapper.firstElementChild) {
            document.body.appendChild(wrapper.firstElementChild);
        }
    }

    function cacheElements() {
        fab = document.getElementById('freshbot-fab');
        window_ = document.getElementById('freshbot-window');
        messages = document.getElementById('freshbot-messages');
        input = document.getElementById('freshbot-input');
        sendBtn = document.getElementById('freshbot-send-btn');
        suggestions = document.getElementById('freshbot-suggestions');
    }

    function bindEvents() {
        fab.addEventListener('click', toggleChat);

        const closeBtn = document.getElementById('freshbot-close-btn');
        if (closeBtn) closeBtn.addEventListener('click', closeChat);

        const resetBtn = document.getElementById('freshbot-reset-btn');
        if (resetBtn) resetBtn.addEventListener('click', resetConversation);

        input.addEventListener('input', onInputChange);
        input.addEventListener('keydown', onInputKeydown);
        sendBtn.addEventListener('click', sendMessage);

        // Close on click outside
        document.addEventListener('click', (e) => {
            if (isOpen && !window_.contains(e.target) && !fab.contains(e.target)) {
                closeChat();
            }
        });

        // Escape to close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && isOpen) closeChat();
        });
    }

    // ── Chat Toggle ─────────────────────────────────────────────────────────────
    function toggleChat() {
        isOpen ? closeChat() : openChat();
    }

    function openChat() {
        isOpen = true;
        window_.classList.add('is-open');
        fab.classList.add('is-open');
        hideFabBadge();

        // Show welcome message on first open
        if (!hasShownWelcome) {
            hasShownWelcome = true;
            showWelcome();
        }

        // Focus input after animation
        setTimeout(() => input.focus(), 350);
        scrollToBottom();
    }

    function closeChat() {
        isOpen = false;
        window_.classList.remove('is-open');
        fab.classList.remove('is-open');
    }

    // ── Welcome Message ─────────────────────────────────────────────────────────
    function showWelcome() {
        const welcomeDiv = document.createElement('div');
        welcomeDiv.className = 'freshbot-welcome';
        welcomeDiv.innerHTML = `
            <div class="freshbot-welcome-icon">👋</div>
            <h3 class="freshbot-welcome-title">Hey there! I'm FreshBot!</h3>
            <p class="freshbot-welcome-subtitle">Your AI shopping assistant for FreshMarket. I can help you find products, suggest recipes, track orders, and more!</p>
        `;
        messages.appendChild(welcomeDiv);

        // Welcome bot message after short delay
        setTimeout(() => {
            appendBotMessage("Hello! 👋 I'm **FreshBot**, your AI grocery assistant! I can help you with:\n\n• 🛒 Product recommendations\n• 🍳 Recipe suggestions\n• 📦 Order tracking\n• 💰 Budget-friendly shopping tips\n\nWhat can I help you with today?");
        }, 600);
    }

    // ── Quick Suggestions ────────────────────────────────────────────────────────
    function renderSuggestions() {
        if (!suggestions) return;
        SUGGESTIONS.forEach(text => {
            const chip = document.createElement('button');
            chip.className = 'freshbot-suggestion-chip';
            chip.textContent = text;
            chip.addEventListener('click', () => {
                input.value = text.replace(/^[\u{1F300}-\u{1F9FF}]\s*/u, '');
                sendMessage();
                suggestions.style.display = 'none';
            });
            suggestions.appendChild(chip);
        });
    }

    // ── Input Handling ───────────────────────────────────────────────────────────
    function onInputChange() {
        // Auto-resize textarea
        input.style.height = 'auto';
        input.style.height = Math.min(input.scrollHeight, 100) + 'px';

        const hasText = input.value.trim().length > 0;
        sendBtn.disabled = !hasText || isSending;

        if (hasText && suggestions) {
            suggestions.style.display = 'none';
        }
    }

    function onInputKeydown(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!sendBtn.disabled) sendMessage();
        }
    }

    // ── Send Message ─────────────────────────────────────────────────────────────
    async function sendMessage() {
        const text = input.value.trim();
        if (!text || isSending) return;
        if (text.length > CONFIG.maxMessageLength) {
            showError('Message too long. Please keep it under 500 characters.');
            return;
        }

        // Clear input
        input.value = '';
        input.style.height = 'auto';
        sendBtn.disabled = true;
        isSending = true;

        // Add user message
        appendUserMessage(text);

        // Show typing indicator
        const typingEl = showTypingIndicator();

        try {
            const response = await fetch(CONFIG.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ message: text })
            });

            const data = await response.json();

            // Remove typing indicator after simulated thinking time
            const minDelay = CONFIG.typingDelay.min;
            await sleep(Math.max(minDelay - 400, 200));
            removeTypingIndicator(typingEl);

            if (data.success) {
                appendBotMessage(data.message);
            } else {
                appendBotMessage("Sorry, I had trouble understanding that. Could you rephrase? 🤔");
            }
        } catch (err) {
            removeTypingIndicator(typingEl);
            appendBotMessage("I'm having connectivity issues. Please check your connection and try again! 🌐");
        }

        isSending = false;
        sendBtn.disabled = input.value.trim().length === 0;
        input.focus();
    }

    // ── Message Rendering ────────────────────────────────────────────────────────
    function appendUserMessage(text) {
        const time = formatTime(new Date());
        const div = document.createElement('div');
        div.className = 'freshbot-message user-msg';
        div.innerHTML = `
            <div class="freshbot-msg-avatar">👤</div>
            <div>
                <div class="freshbot-bubble">${escapeHTML(text)}</div>
                <div class="freshbot-timestamp">${time}</div>
            </div>`;
        messages.appendChild(div);
        scrollToBottom();
        messageCount++;
    }

    function appendBotMessage(text) {
        const time = formatTime(new Date());
        const div = document.createElement('div');
        div.className = 'freshbot-message bot-msg';
        div.innerHTML = `
            <div class="freshbot-msg-avatar">🤖</div>
            <div>
                <div class="freshbot-bubble">${formatBotText(text)}</div>
                <div class="freshbot-timestamp">${time}</div>
            </div>`;
        messages.appendChild(div);
        scrollToBottom();
        messageCount++;
    }

    function showTypingIndicator() {
        const wrapper = document.createElement('div');
        wrapper.className = 'freshbot-message bot-msg';
        wrapper.id = 'freshbot-typing';
        wrapper.innerHTML = `
            <div class="freshbot-msg-avatar">🤖</div>
            <div class="freshbot-typing">
                <span class="freshbot-typing-dot"></span>
                <span class="freshbot-typing-dot"></span>
                <span class="freshbot-typing-dot"></span>
            </div>`;
        messages.appendChild(wrapper);
        scrollToBottom();
        return wrapper;
    }

    function removeTypingIndicator(el) {
        if (el && el.parentNode) el.parentNode.removeChild(el);
    }

    // ── Helpers ──────────────────────────────────────────────────────────────────
    function scrollToBottom() {
        requestAnimationFrame(() => {
            messages.scrollTop = messages.scrollHeight;
        });
    }

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    function formatTime(date) {
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function escapeHTML(str) {
        const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
        return str.replace(/[&<>"']/g, m => map[m]);
    }

    /**
     * Markdown renderer for bot messages.
     * Handles: **bold**, *italic*, _italic_, numbered lists, bullet lists,
     * section headers (ending with :), divider lines, and line breaks.
     *
     * Works in multiple passes to avoid regex conflicts.
     */
    function formatBotText(raw) {
        // Split into lines for list-aware processing
        const lines = raw.split('\n');
        const out = [];
        let inUL = false;   // inside <ul>
        let inOL = false;   // inside <ol>

        for (let i = 0; i < lines.length; i++) {
            let line = lines[i];

            // ── Bullet point line  (•  -  *)
            const bulletMatch = line.match(/^([•\-\*])\s+(.+)$/);
            if (bulletMatch) {
                if (inOL) { out.push('</ol>'); inOL = false; }
                if (!inUL) { out.push('<ul class="fb-list">'); inUL = true; }
                out.push('<li>' + inlineFormat(bulletMatch[2]) + '</li>');
                continue;
            }

            // ── Numbered list line  (1. 2. 3.)
            const numMatch = line.match(/^(\d+)\.\s+(.+)$/);
            if (numMatch) {
                if (inUL) { out.push('</ul>'); inUL = false; }
                if (!inOL) { out.push('<ol class="fb-list">'); inOL = true; }
                out.push('<li>' + inlineFormat(numMatch[2]) + '</li>');
                continue;
            }

            // Close any open list before processing normal line
            if (inUL) { out.push('</ul>'); inUL = false; }
            if (inOL) { out.push('</ol>'); inOL = false; }

            // ── Empty line → paragraph break
            if (line.trim() === '') {
                out.push('<div class="fb-spacer"></div>');
                continue;
            }

            // ── Divider line (--- or ***)
            if (/^[-\*]{3,}$/.test(line.trim())) {
                out.push('<hr class="fb-hr">');
                continue;
            }

            // ── Section header: line ending with ":" and fairly short
            if (line.trim().endsWith(':') && line.trim().length < 60 && !line.startsWith('http')) {
                out.push('<div class="fb-section-header">' + inlineFormat(line.trim()) + '</div>');
                continue;
            }

            // ── Normal text line
            out.push('<div class="fb-line">' + inlineFormat(line) + '</div>');
        }

        // Close any lingering lists
        if (inUL) out.push('</ul>');
        if (inOL) out.push('</ol>');

        return out.join('');
    }

    /**
     * Apply inline formatting: **bold**, *italic*, _italic_, `code`, emojis pass-through.
     */
    function inlineFormat(text) {
        // Escape HTML first (except we'll re-insert our tags)
        let s = escapeHTML(text);

        // **bold**
        s = s.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

        // *italic* (not preceded or followed by another *)
        s = s.replace(/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/g, '<em>$1</em>');

        // _italic_
        s = s.replace(/(?<!_)_(?!_)(.+?)(?<!_)_(?!_)/g, '<em>$1</em>');

        // `code`
        s = s.replace(/`(.+?)`/g, '<code class="fb-code">$1</code>');

        return s;
    }

    function showFabBadge() {
        if (document.querySelector('#freshbot-fab .fab-badge')) return;
        const badge = document.createElement('span');
        badge.className = 'fab-badge';
        badge.textContent = '1';
        badge.title = 'FreshBot has a message for you!';
        fab.appendChild(badge);
    }

    function hideFabBadge() {
        const badge = document.querySelector('#freshbot-fab .fab-badge');
        if (badge) badge.remove();
    }

    function showError(msg) {
        appendBotMessage('⚠️ ' + msg);
    }

    // ── Reset Conversation ───────────────────────────────────────────────────────
    async function resetConversation() {
        try {
            await fetch(CONFIG.resetEndpoint, {
                method: 'POST',
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
        } catch (e) { /* ignore */ }

        // Clear UI
        messages.innerHTML = '';
        messageCount = 0;
        hasShownWelcome = false;
        showWelcome();

        // Show suggestions again
        if (suggestions) suggestions.style.display = 'flex';
    }

    // ── Bootstrap ────────────────────────────────────────────────────────────────
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
