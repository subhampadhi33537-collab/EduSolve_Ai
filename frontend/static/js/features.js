/**
 * Advanced Features & Utilities
 */

// Voice Input Support
class VoiceInput {
    constructor(textareaId) {
        this.textarea = document.getElementById(textareaId);
        this.recognition = null;
        this.initVoiceRecognition();
    }
    
    initVoiceRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';
            
            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                if (this.textarea) {
                    this.textarea.value = transcript;
                }
                showToast('Voice input captured! 🎤', 'success');
            };
            
            this.recognition.onerror = (event) => {
                showToast('Voice input error: ' + event.error, 'error');
            };
        }
    }
    
    start() {
        if (this.recognition) {
            this.recognition.start();
            showToast('Listening... 🎤', 'info');
        } else {
            showToast('Voice recognition not supported', 'error');
        }
    }
    
    stop() {
        if (this.recognition) {
            this.recognition.stop();
        }
    }
}

// Dark Mode Toggle
class DarkModeToggle {
    constructor() {
        this.isDark = localStorage.getItem('darkMode') === 'true';
        this.init();
    }
    
    init() {
        if (this.isDark) {
            document.body.classList.add('dark-mode');
        }
        this.createToggleButton();
    }
    
    createToggleButton() {
        const button = document.createElement('button');
        button.className = 'dark-mode-toggle';
        button.innerHTML = this.isDark ? '☀️' : '🌙';
        button.style.cssText = `
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: var(--purple-gradient);
            color: white;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            box-shadow: var(--shadow-xl);
            z-index: 1000;
            transition: var(--transition-bounce);
        `;
        
        button.addEventListener('click', () => this.toggle());
        document.body.appendChild(button);
        this.button = button;
    }
    
    toggle() {
        this.isDark = !this.isDark;
        document.body.classList.toggle('dark-mode');
        this.button.innerHTML = this.isDark ? '☀️' : '🌙';
        localStorage.setItem('darkMode', this.isDark);
        showToast(this.isDark ? 'Dark mode enabled 🌙' : 'Light mode enabled ☀️', 'success');
    }
}

// Local Storage Manager
class StorageManager {
    static save(key, data) {
        try {
            localStorage.setItem(key, JSON.stringify(data));
            return true;
        } catch (error) {
            console.error('Storage save error:', error);
            return false;
        }
    }
    
    static load(key) {
        try {
            const data = localStorage.getItem(key);
            return data ? JSON.parse(data) : null;
        } catch (error) {
            console.error('Storage load error:', error);
            return null;
        }
    }
    
    static remove(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (error) {
            console.error('Storage remove error:', error);
            return false;
        }
    }
    
    static clear() {
        try {
            localStorage.clear();
            return true;
        } catch (error) {
            console.error('Storage clear error:', error);
            return false;
        }
    }
}

// Bookmark System
class BookmarkManager {
    constructor() {
        this.bookmarks = StorageManager.load('bookmarks') || [];
    }
    
    add(question, explanation, subject, difficulty) {
        const bookmark = {
            id: Date.now(),
            question,
            explanation,
            subject,
            difficulty,
            timestamp: new Date().toISOString()
        };
        
        this.bookmarks.push(bookmark);
        StorageManager.save('bookmarks', this.bookmarks);
        showToast('Bookmark added! 📑', 'success');
        return bookmark;
    }
    
    remove(id) {
        this.bookmarks = this.bookmarks.filter(b => b.id !== id);
        StorageManager.save('bookmarks', this.bookmarks);
        showToast('Bookmark removed', 'info');
    }
    
    getAll() {
        return this.bookmarks;
    }
    
    search(query) {
        const lowerQuery = query.toLowerCase();
        return this.bookmarks.filter(b => 
            b.question.toLowerCase().includes(lowerQuery) ||
            b.explanation.toLowerCase().includes(lowerQuery)
        );
    }
}

// Export System (Multiple Formats)
class ExportManager {
    static async exportToPDF(data, filename = 'edusolve-export.pdf') {
        if (typeof window.jspdf === 'undefined') {
            showToast('PDF library not loaded', 'error');
            return;
        }
        
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
        
        // Header
        doc.setFontSize(20);
        doc.setTextColor(102, 126, 234);
        doc.text('EduSolve AI', 20, 20);
        
        // Content
        doc.setFontSize(12);
        doc.setTextColor(0, 0, 0);
        let yPos = 40;
        
        if (Array.isArray(data)) {
            data.forEach((item, index) => {
                if (yPos > 270) {
                    doc.addPage();
                    yPos = 20;
                }
                
                doc.setFont(undefined, 'bold');
                doc.text(`${index + 1}. Question:`, 20, yPos);
                yPos += 7;
                
                doc.setFont(undefined, 'normal');
                const questionLines = doc.splitTextToSize(item.question, 170);
                doc.text(questionLines, 20, yPos);
                yPos += questionLines.length * 7 + 5;
                
                doc.setFont(undefined, 'bold');
                doc.text('Subject: ' + item.subject + ' | Difficulty: ' + item.difficulty, 20, yPos);
                yPos += 10;
                
                doc.setFont(undefined, 'bold');
                doc.text('Explanation:', 20, yPos);
                yPos += 7;
                
                doc.setFont(undefined, 'normal');
                const explanationLines = doc.splitTextToSize(item.explanation, 170);
                doc.text(explanationLines, 20, yPos);
                yPos += explanationLines.length * 7 + 15;
            });
        } else {
            doc.text('Question: ' + data.question, 20, yPos);
            yPos += 20;
            doc.text('Subject: ' + data.subject, 20, yPos);
            yPos += 10;
            doc.text('Difficulty: ' + data.difficulty, 20, yPos);
            yPos += 20;
            doc.text('Explanation:', 20, yPos);
            yPos += 10;
            const lines = doc.splitTextToSize(data.explanation, 170);
            doc.text(lines, 20, yPos);
        }
        
        doc.save(filename);
        showToast('PDF exported successfully! 📄', 'success');
    }
    
    static exportToJSON(data, filename = 'edusolve-export.json') {
        const jsonString = JSON.stringify(data, null, 2);
        const blob = new Blob([jsonString], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        
        URL.revokeObjectURL(url);
        showToast('JSON exported successfully! 📦', 'success');
    }
    
    static exportToCSV(data, filename = 'edusolve-export.csv') {
        if (!Array.isArray(data)) {
            data = [data];
        }
        
        const headers = ['Timestamp', 'Question', 'Subject', 'Difficulty', 'Explanation'];
        const csvRows = [headers.join(',')];
        
        data.forEach(item => {
            const row = [
                item.timestamp || new Date().toISOString(),
                `"${item.question.replace(/"/g, '""')}"`,
                item.subject,
                item.difficulty,
                `"${item.explanation.replace(/"/g, '""')}"`
            ];
            csvRows.push(row.join(','));
        });
        
        const csvString = csvRows.join('\n');
        const blob = new Blob([csvString], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        
        URL.revokeObjectURL(url);
        showToast('CSV exported successfully! 📊', 'success');
    }
}

// Copy to Clipboard
function copyToClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('Copied to clipboard! 📋', 'success');
        }).catch(err => {
            showToast('Failed to copy', 'error');
        });
    } else {
        // Fallback
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        try {
            document.execCommand('copy');
            showToast('Copied to clipboard! 📋', 'success');
        } catch (err) {
            showToast('Failed to copy', 'error');
        }
        document.body.removeChild(textarea);
    }
}

// Share System
async function shareContent(title, text, url) {
    if (navigator.share) {
        try {
            await navigator.share({ title, text, url });
            showToast('Shared successfully! 📤', 'success');
        } catch (err) {
            if (err.name !== 'AbortError') {
                showToast('Share failed', 'error');
            }
        }
    } else {
        // Fallback: copy to clipboard
        copyToClipboard(`${title}\n\n${text}\n\n${url}`);
    }
}

// Keyboard Shortcuts
class KeyboardShortcuts {
    constructor() {
        this.shortcuts = {
            'ctrl+enter': () => document.getElementById('submitBtn')?.click(),
            'ctrl+k': () => document.getElementById('questionInput')?.focus(),
            'ctrl+d': () => window.location.href = '/dashboard',
            'ctrl+h': () => window.location.href = '/',
            'escape': () => document.getElementById('questionInput')?.blur()
        };
        
        this.init();
    }
    
    init() {
        document.addEventListener('keydown', (e) => {
            const key = this.getKeyCombo(e);
            if (this.shortcuts[key]) {
                e.preventDefault();
                this.shortcuts[key]();
            }
        });
    }
    
    getKeyCombo(e) {
        const parts = [];
        if (e.ctrlKey) parts.push('ctrl');
        if (e.altKey) parts.push('alt');
        if (e.shiftKey) parts.push('shift');
        parts.push(e.key.toLowerCase());
        return parts.join('+');
    }
}

// Analytics Tracker
class Analytics {
    static track(event, data = {}) {
        const analyticsData = StorageManager.load('analytics') || [];
        analyticsData.push({
            event,
            data,
            timestamp: new Date().toISOString()
        });
        StorageManager.save('analytics', analyticsData);
    }
    
    static getEvents(eventType = null) {
        const data = StorageManager.load('analytics') || [];
        return eventType ? data.filter(d => d.event === eventType) : data;
    }
    
    static clear() {
        StorageManager.remove('analytics');
    }
}

// Initialize advanced features on page load
document.addEventListener('DOMContentLoaded', () => {
    // Dark mode toggle
    new DarkModeToggle();
    
    // Keyboard shortcuts
    new KeyboardShortcuts();
    
    // Track page view
    Analytics.track('page_view', { page: window.location.pathname });
});
