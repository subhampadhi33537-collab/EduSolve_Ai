/**
 * EduSolve AI - Frontend JavaScript
 * Handles API communication, UI interactions, and data display
 */

// Configuration - Dynamically detect API URL based on environment
const API_BASE_URL = window.location.origin + '/api';

// DOM Elements
const questionInput = document.getElementById('questionInput');
const submitBtn = document.getElementById('submitBtn');
const responseSection = document.getElementById('responseSection');

const displayedQuestion = document.getElementById('displayedQuestion');
const subjectResult = document.getElementById('subjectResult');
const subjectConfidence = document.getElementById('subjectConfidence');
const difficultyResult = document.getElementById('difficultyResult');
const difficultyConfidence = document.getElementById('difficultyConfidence');
const explanationContent = document.getElementById('explanationContent');
const timingInfo = document.getElementById('timingInfo');

const askAgainBtn = document.getElementById('askAgainBtn');
const downloadBtn = document.getElementById('downloadBtn');

// State
let lastResponse = null;
let isSubmitting = false;

/**
 * Initialize event listeners
 */
function initializeEventListeners() {
    // Submit button listener
    if (submitBtn) {
        submitBtn.addEventListener('click', handleAskQuestion);
    }
    
    // Keyboard shortcut (Ctrl+Enter)
    if (questionInput) {
        questionInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                handleAskQuestion();
            }
        });
    }
    
    // Ask Again button
    if (askAgainBtn) {
        askAgainBtn.addEventListener('click', resetForm);
    }
    
    // Download button
    if (downloadBtn) {
        downloadBtn.addEventListener('click', downloadExplanation);
    }
    
    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    if (mobileMenuToggle && navMenu) {
        mobileMenuToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }
    
    // Load statistics on page load
    loadStatistics();
    
    // Initialize character counter
    if (questionInput) {
        questionInput.addEventListener('input', function() {
            const charCount = document.getElementById('charCount');
            if (charCount) {
                charCount.textContent = this.value.length;
            }
        });
    }
}

/**
 * Voice Input Function
 */
function startVoiceInput() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        
        recognition.onstart = function() {
            showToast('🎤 Listening... Speak now!', 'info');
        };
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            if (questionInput) {
                questionInput.value = transcript;
                const charCount = document.getElementById('charCount');
                if (charCount) {
                    charCount.textContent = transcript.length;
                }
            }
            showToast('✅ Voice input captured!', 'success');
        };
        
        recognition.onerror = function(event) {
            showToast('❌ Voice input error: ' + event.error, 'error');
        };
        
        recognition.start();
    } else {
        showToast('❌ Voice recognition not supported. Use Chrome or Edge.', 'error');
    }
}

/**
 * Copy Explanation Function
 */
function copyExplanation() {
    if (lastResponse && lastResponse.explanation) {
        const text = `Question: ${lastResponse.question}\n\nSubject: ${lastResponse.subject}\nDifficulty: ${lastResponse.difficulty}\n\nExplanation:\n${lastResponse.explanation}`;
        
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).then(() => {
                showToast('📋 Copied to clipboard!', 'success');
            }).catch(err => {
                showToast('❌ Failed to copy', 'error');
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
                showToast('📋 Copied to clipboard!', 'success');
            } catch (err) {
                showToast('❌ Failed to copy', 'error');
            }
            document.body.removeChild(textarea);
        }
    }
}

/**
 * Share Explanation Function
 */
async function shareExplanation() {
    if (lastResponse) {
        const shareData = {
            title: 'EduSolve AI - Question & Answer',
            text: `Question: ${lastResponse.question}\n\nSubject: ${lastResponse.subject} | Difficulty: ${lastResponse.difficulty}\n\nExplanation: ${lastResponse.explanation.substring(0, 200)}...`,
            url: window.location.href
        };
        
        if (navigator.share) {
            try {
                await navigator.share(shareData);
                showToast('📤 Shared successfully!', 'success');
            } catch (err) {
                if (err.name !== 'AbortError') {
                    copyExplanation();
                }
            }
        } else {
            copyExplanation();
        }
    }
}

/**
 * Submit question wrapper function
 */
function submitQuestion() {
    handleAskQuestion();
}

/**
 * Handle question submission
 */
async function handleAskQuestion() {
    // Prevent double submissions
    if (isSubmitting) {
        return;
    }
    
    const question = questionInput.value.trim();
    
    // Validation
    if (!question) {
        showError('Please enter a question');
        return;
    }
    
    if (question.length < 5) {
        showError('Question is too short. Please provide more details.');
        return;
    }
    
    // Clear previous errors
    clearError();
    
    // Set submitting flag and disable button
    isSubmitting = true;
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.style.opacity = '0.6';
        submitBtn.style.cursor = 'not-allowed';
    }
    
    // Show loading state
    showLoading();
    
    // Animate loading steps
    animateLoadingSteps();
    
    try {
        // Make API request
        const response = await fetch(`${API_BASE_URL}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: question })
        });
        
        const data = await response.json();
        
        if (response.ok && data.status === 'success') {
            // Display response (lastResponse is set inside displayResponse)
            displayResponse(data);
            
            // Update statistics
            loadStatistics();
        } else {
            const errorMsg = data.message || data.error_detail || 'Failed to get explanation';
            console.error('API Error:', data);
            showError(errorMsg);
            hideLoading();
        }
    } catch (error) {
        console.error('API Error:', error);
        showError('Failed to connect to the server. Make sure the backend is running on http://localhost:5000');
        hideLoading();
    } finally {
        // Re-enable button after request completes
        isSubmitting = false;
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.style.opacity = '1';
            submitBtn.style.cursor = 'pointer';
        }
    }
}

/**
 * Display the API response
 */
function displayResponse(response) {
    // Hide loading, show response
    hideLoading();
    
    if (!responseSection) {
        showError('Response section not found in the page');
        return;
    }
    
    // Extract data from nested structure
    const data = response.data || response;
    
    // Store for later use in download/copy functions
    lastResponse = {
        question: data.question || questionInput.value,
        subject: data.subject,
        subject_confidence: data.subject_confidence,
        difficulty: data.difficulty,
        difficulty_confidence: data.difficulty_confidence,
        explanation: data.explanation
    };
    
    responseSection.classList.remove('hidden-section');
    responseSection.style.display = 'block';
    
    // Show success notification
    showToast('🎉 Explanation generated successfully!', 'success');
    
    // Safely populate response fields with fallbacks
    if (displayedQuestion) {
        displayedQuestion.textContent = data.question || questionInput.value || 'Your question';
    }
    
    if (subjectResult) {
        subjectResult.textContent = data.subject || 'Unknown';
    }
    
    if (subjectConfidence) {
        const confidence = data.subject_confidence ? (data.subject_confidence * 100).toFixed(1) : '0';
        subjectConfidence.textContent = `Confidence: ${confidence}%`;
    }
    
    if (difficultyResult) {
        difficultyResult.textContent = data.difficulty || 'Unknown';
    }
    
    if (difficultyConfidence) {
        const confidence = data.difficulty_confidence ? (data.difficulty_confidence * 100).toFixed(1) : '0';
        difficultyConfidence.textContent = `Confidence: ${confidence}%`;
    }
    
    // Format explanation (break into sections)
    if (explanationContent) {
        const formattedExplanation = formatExplanation(data.explanation || 'No explanation available');
        explanationContent.innerHTML = formattedExplanation;
    }
    
    // Display timing info
    if (timingInfo) {
        const timestamp = data.timestamp ? new Date(data.timestamp).toLocaleString() : new Date().toLocaleString();
        timingInfo.textContent = `Generated on: ${timestamp}`;
    }
    
    // Make response cards visible
    document.querySelectorAll('.response-card-enhanced').forEach(card => {
        card.classList.add('visible');
    });
    
    // Scroll to response
    setTimeout(() => {
        responseSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

/**
 * Animate loading steps
 */
function animateLoadingSteps() {
    const steps = document.querySelectorAll('.loading-step');
    steps.forEach(step => step.classList.remove('active'));
    
    if (steps[0]) {
        steps[0].classList.add('active');
        setTimeout(() => {
            if (steps[1]) steps[1].classList.add('active');
        }, 800);
        setTimeout(() => {
            if (steps[2]) steps[2].classList.add('active');
        }, 1600);
    }
}

/**
 * Format explanation text for better readability - Book style
 */
function formatExplanation(text) {
    // Strip all markdown formatting
    text = text.replace(/\*\*/g, '').replace(/#{1,6}\s/g, '');
    
    // Parse into book-like format
    let formatted = text
        .split('\n')
        .map(line => line.trim())
        .filter(line => line.length > 0)
        .map(line => {
            // Questions and main headings (ending with ? or :)
            if (line.match(/\?$/) || line.match(/^[A-Z][^:]*:$/)) {
                return `<h3 class="book-heading">${line}</h3>`;
            }
            // Numbered points (1. 2. 3.)
            else if (line.match(/^\d+\./)) {
                return `<div class="book-point"><strong>${line}</strong></div>`;
            }
            // Regular content
            else {
                return `<p class="book-text">${line}</p>`;
            }
        })
        .join('');
    
    return formatted;
}

/**
 * Load and display statistics with animated counters
 */
async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`);
        const data = await response.json();
        
        if (data.status === 'success') {
            // Extract nested data
            const statsData = data.data || data;
            
            // Animate number counters
            animateCounter('totalQuestions', 0, statsData.total_questions || 0, 1000);
            animateCounter('totalSubjects', 0, Object.keys(statsData.subjects || {}).length, 1000);
            
            // Find most common difficulty
            const difficulties = statsData.difficulties || {};
            const mostCommon = Object.entries(difficulties).sort((a, b) => b[1] - a[1])[0];
            document.getElementById('avgDifficulty').textContent = mostCommon ? mostCommon[0] : '-';
        }
    } catch (error) {
        console.error('Failed to load statistics:', error);
    }
}

/**
 * Animate counter from start to end
 */
function animateCounter(elementId, start, end, duration) {
    const element = document.getElementById(elementId);
    const range = end - start;
    const increment = range / (duration / 16); // 60fps
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current);
    }, 16);
}

/**
 * Download explanation as PDF file
 */
function downloadExplanation() {
    if (!lastResponse) {
        showError('No explanation to download');
        return;
    }
    
    // Get jsPDF from window object
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    // Set colors and fonts
    const primaryColor = [102, 126, 234];
    const secondaryColor = [118, 75, 162];
    const textColor = [30, 41, 59];
    
    let yPos = 20;
    const margin = 20;
    const pageWidth = doc.internal.pageSize.getWidth();
    const maxWidth = pageWidth - 2 * margin;
    
    // Title with gradient effect (using colored rectangles)
    doc.setFillColor(primaryColor[0], primaryColor[1], primaryColor[2]);
    doc.rect(0, 0, pageWidth, 40, 'F');
    
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(24);
    doc.setFont(undefined, 'bold');
    doc.text('🎓 EduSolve AI', pageWidth / 2, 15, { align: 'center' });
    
    doc.setFontSize(12);
    doc.setFont(undefined, 'normal');
    doc.text('Question & Explanation Report', pageWidth / 2, 28, { align: 'center' });
    
    yPos = 50;
    
    // Question Section
    doc.setTextColor(textColor[0], textColor[1], textColor[2]);
    doc.setFontSize(14);
    doc.setFont(undefined, 'bold');
    doc.text('📌 Your Question:', margin, yPos);
    yPos += 8;
    
    doc.setFontSize(11);
    doc.setFont(undefined, 'normal');
    const questionLines = doc.splitTextToSize(lastResponse.question, maxWidth);
    doc.text(questionLines, margin, yPos);
    yPos += questionLines.length * 6 + 10;
    
    // Classification Section
    doc.setFillColor(245, 158, 11, 50);
    doc.rect(margin - 5, yPos - 8, maxWidth + 10, 30, 'F');
    
    doc.setFontSize(14);
    doc.setFont(undefined, 'bold');
    doc.setTextColor(primaryColor[0], primaryColor[1], primaryColor[2]);
    doc.text('🏷️ Classification:', margin, yPos);
    yPos += 8;
    
    doc.setFontSize(11);
    doc.setFont(undefined, 'normal');
    doc.setTextColor(textColor[0], textColor[1], textColor[2]);
    doc.text(`Subject: ${lastResponse.subject}`, margin, yPos);
    doc.text(`(Confidence: ${(lastResponse.subject_confidence * 100).toFixed(1)}%)`, margin + 60, yPos);
    yPos += 6;
    
    doc.text(`Difficulty: ${lastResponse.difficulty}`, margin, yPos);
    doc.text(`(Confidence: ${(lastResponse.difficulty_confidence * 100).toFixed(1)}%)`, margin + 60, yPos);
    yPos += 15;
    
    // Explanation Section
    doc.setFontSize(14);
    doc.setFont(undefined, 'bold');
    doc.setTextColor(16, 185, 129);
    doc.text('💡 AI-Generated Explanation:', margin, yPos);
    yPos += 8;
    
    doc.setFontSize(10);
    doc.setFont(undefined, 'normal');
    doc.setTextColor(textColor[0], textColor[1], textColor[2]);
    
    // Split explanation into lines and handle page breaks
    const explanationLines = doc.splitTextToSize(lastResponse.explanation, maxWidth);
    for (let i = 0; i < explanationLines.length; i++) {
        if (yPos > 270) {
            doc.addPage();
            yPos = 20;
        }
        doc.text(explanationLines[i], margin, yPos);
        yPos += 5;
    }
    
    // Footer
    yPos += 10;
    if (yPos > 260) {
        doc.addPage();
        yPos = 20;
    }
    
    doc.setFillColor(secondaryColor[0], secondaryColor[1], secondaryColor[2]);
    doc.rect(0, yPos, pageWidth, 20, 'F');
    
    doc.setFontSize(9);
    doc.setTextColor(255, 255, 255);
    doc.setFont(undefined, 'italic');
    const timestamp = new Date(lastResponse.data_id).toLocaleString();
    doc.text(`Generated: ${timestamp}`, pageWidth / 2, yPos + 8, { align: 'center' });
    doc.text('Powered by EduSolve AI | Groq API & Scikit-learn ML', pageWidth / 2, yPos + 14, { align: 'center' });
    
    // Save PDF
    const filename = `EduSolve_${lastResponse.subject}_${new Date().toISOString().slice(0, 10)}.pdf`;
    doc.save(filename);
    
    // Show success notification
    showToast('✅ PDF downloaded successfully!', 'success');
}

/**
 * Reset form and clear response with animation
 */
function resetForm() {
    // Fade out animation
    responseSection.style.opacity = '0';
    responseSection.style.transform = 'scale(0.95)';
    
    setTimeout(() => {
        questionInput.value = '';
        questionInput.focus();
        responseSection.style.display = 'none';
        responseSection.style.opacity = '1';
        responseSection.style.transform = 'scale(1)';
        clearError();
        lastResponse = null;
        
        // Scroll to top smoothly
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }, 300);
}

/**
 * Show loading state
 */
function showLoading() {
    const submitButton = document.getElementById('submitBtn');
    const responseDiv = document.getElementById('responseSection');
    
    if (submitButton) {
        submitButton.disabled = true;
        submitButton.textContent = '⏳ Processing...';
    }
    
    if (responseDiv) {
        responseDiv.style.display = 'none';
    }
}

/**
 * Hide loading state
 */
function hideLoading() {
    const submitButton = document.getElementById('submitBtn');
    
    if (submitButton) {
        submitButton.disabled = false;
        submitButton.innerHTML = '<span class=\"btn-content\">🚀 Get Answer</span>';
    }
}

/**
 * Show error message with animation
 */
function showError(message) {
    showToast('❌ ' + message, 'error');
}

/**
 * Clear error message with fade out
 */
function clearError() {
    // Error messages auto-dismiss via toast
}

/**
 * Check if backend is running
 */
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        return response.ok;
    } catch (error) {
        console.error('Backend health check failed:', error);
        return false;
    }
}

/**
 * Show toast notification
 */
function showToast(message, type = 'success') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        background: ${type === 'success' ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)' : 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)'};
        color: white;
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
        z-index: 10000;
        font-weight: 600;
        font-size: 14px;
        animation: slideInRight 0.4s ease-out;
        display: flex;
        align-items: center;
        gap: 10px;
    `;
    
    const icon = type === 'success' ? '✅' : '❌';
    toast.innerHTML = `<span style="font-size: 20px;">${icon}</span> ${message}`;
    
    document.body.appendChild(toast);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.4s ease-out';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 400);
    }, 3000);
}

/**
 * Initialize on page load
 */
document.addEventListener('DOMContentLoaded', async () => {
    initializeEventListeners();
    
    // Add CSS for toast animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(100px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        @keyframes slideOutRight {
            from {
                opacity: 1;
                transform: translateX(0);
            }
            to {
                opacity: 0;
                transform: translateX(100px);
            }
        }
    `;
    document.head.appendChild(style);
    
    // Check backend health
    const isHealthy = await checkBackendHealth();
    if (!isHealthy) {
        showError('Backend server is not responding. Please make sure the Flask server is running on http://localhost:5000');
    } else {
        showToast('Welcome to EduSolve AI! 🎓', 'success');
    }
    
    // Load statistics with animation
    loadStatistics();
});

/**
 * Handle beforeunload to preserve state
 */
window.addEventListener('beforeunload', (e) => {
    if (questionInput.value.trim() && !responseSection.style.display !== 'none') {
        e.preventDefault();
        e.returnValue = '';
    }
});
