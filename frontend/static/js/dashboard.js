/**
 * Navigation & Multi-page Support
 */

class Navigation {
    constructor() {
        this.currentPage = window.location.pathname.split('/').pop() || 'index.html';
        this.initMobileMenu();
        this.setActiveLink();
    }
    
    initMobileMenu() {
        const toggle = document.querySelector('.mobile-menu-toggle');
        const menu = document.querySelector('.nav-menu');
        
        if (toggle && menu) {
            toggle.addEventListener('click', () => {
                menu.classList.toggle('active');
            });
        }
    }
    
    setActiveLink() {
        const links = document.querySelectorAll('.nav-link');
        links.forEach(link => {
            if (link.getAttribute('href') === this.currentPage || 
                (this.currentPage === '' && link.getAttribute('href') === '/')) {
                link.classList.add('active');
            }
        });
    }
}

/**
 * Dashboard & Analytics
 */

class Dashboard {
    constructor() {
        this.loadDashboardData();
    }
    
    async loadDashboardData() {
        try {
            const [stats, history] = await Promise.all([
                fetch(`${API_BASE_URL}/stats`).then(r => r.json()),
                fetch(`${API_BASE_URL}/history`).then(r => r.json())
            ]);
            
            if (stats.status === 'success') {
                this.updateDashboardStats(stats);
            }
            
            if (history.status === 'success') {
                this.displayHistory(history.data);
            }
        } catch (error) {
            console.error('Failed to load dashboard data:', error);
        }
    }
    
    updateDashboardStats(stats) {
        // Extract nested data
        const statsData = stats.data || stats;
        
        // Animate counter values
        if (document.getElementById('dashTotalQuestions')) {
            animateCounter('dashTotalQuestions', 0, statsData.total_questions || 0, 1000);
        }
        
        // Update subject distribution
        if (document.getElementById('dashTotalSubjects')) {
            document.getElementById('dashTotalSubjects').textContent = Object.keys(statsData.subjects || {}).length;
        }
        
        // Calculate accuracy (placeholder)
        if (document.getElementById('dashAccuracy')) {
            document.getElementById('dashAccuracy').textContent = '94%';
        }
        
        // Show most popular subject
        if (document.getElementById('dashPopularSubject')) {
            const popular = Object.entries(statsData.subjects || {}).sort((a, b) => b[1] - a[1])[0];
            document.getElementById('dashPopularSubject').textContent = popular ? popular[0] : 'N/A';
        }
        
        // Display subject badges
        this.displaySubjectBadges(statsData.subjects || {});
        
        // Display difficulty distribution
        this.displayDifficultyProgress(statsData.difficulties || {});
    }
    
    displaySubjectBadges(subjects) {
        const container = document.getElementById('subjectBadges');
        if (!container) return;
        
        const icons = {
            'Mathematics': '🔢',
            'Physics': '⚛️',
            'Chemistry': '🧪',
            'Biology': '🧬',
            'English': '📖',
            'History': '🏛️',
            'Geography': '🌍'
        };
        
        container.innerHTML = '';
        Object.entries(subjects).forEach(([subject, count]) => {
            const badge = document.createElement('div');
            badge.className = 'subject-badge';
            badge.innerHTML = `
                <span class="badge-icon">${icons[subject] || '📚'}</span>
                <div class="badge-info">
                    <span class="badge-name">${subject}</span>
                    <span class="badge-count">${count} questions</span>
                </div>
            `;
            container.appendChild(badge);
        });
    }
    
    displayDifficultyProgress(difficulties) {
        const container = document.getElementById('difficultyProgress');
        if (!container) return;
        
        const total = Object.values(difficulties).reduce((a, b) => a + b, 0);
        const colors = {
            'Easy': '#10b981',
            'Medium': '#f59e0b',
            'Hard': '#ef4444'
        };
        
        container.innerHTML = '';
        Object.entries(difficulties).forEach(([level, count]) => {
            const percentage = total > 0 ? (count / total * 100).toFixed(1) : 0;
            const item = document.createElement('div');
            item.className = 'progress-item';
            item.innerHTML = `
                <div class="progress-header">
                    <span class="progress-label">${level}</span>
                    <span class="progress-value">${count} (${percentage}%)</span>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-bar" style="width: ${percentage}%; background: ${colors[level]}"></div>
                </div>
            `;
            container.appendChild(item);
        });
    }
    
    displayHistory(history) {
        const container = document.getElementById('historyTimeline');
        if (!container) return;
        
        if (history.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">📭</div>
                    <h3 class="empty-title">No Questions Yet</h3>
                    <p class="empty-description">Start asking questions to see your history here!</p>
                    <a href="/" class="empty-action">Ask Your First Question</a>
                </div>
            `;
            return;
        }
        
        container.innerHTML = '';
        // Show most recent 10
        const recent = history.slice(-10).reverse();
        
        recent.forEach((item, index) => {
            const timelineItem = document.createElement('div');
            timelineItem.className = 'timeline-item';
            timelineItem.style.animationDelay = `${index * 0.1}s`;
            
            const date = new Date(item.timestamp).toLocaleString();
            const preview = item.question.substring(0, 100) + (item.question.length > 100 ? '...' : '');
            
            timelineItem.innerHTML = `
                <div class="timeline-marker"></div>
                <div class="timeline-content">
                    <div class="timeline-date">🕒 ${date}</div>
                    <div class="timeline-title">Subject: ${item.subject} | Difficulty: ${item.difficulty}</div>
                    <div class="timeline-description">${preview}</div>
                </div>
            `;
            container.appendChild(timelineItem);
        });
    }
}

/**
 * Search & Filter System
 */

class SearchFilter {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.allQuestions = [];
        this.filteredQuestions = [];
        this.init();
    }
    
    async init() {
        await this.loadQuestions();
        this.setupEventListeners();
    }
    
    async loadQuestions() {
        try {
            const response = await fetch(`${API_BASE_URL}/history`);
            const data = await response.json();
            if (data.status === 'success') {
                this.allQuestions = data.data;
                this.filteredQuestions = [...this.allQuestions];
                this.render();
            }
        } catch (error) {
            console.error('Failed to load questions:', error);
        }
    }
    
    setupEventListeners() {
        const searchInput = document.getElementById('searchInput');
        const subjectFilter = document.getElementById('subjectFilter');
        const difficultyFilter = document.getElementById('difficultyFilter');
        
        if (searchInput) {
            searchInput.addEventListener('input', (e) => this.applyFilters());
        }
        
        if (subjectFilter) {
            subjectFilter.addEventListener('change', (e) => this.applyFilters());
        }
        
        if (difficultyFilter) {
            difficultyFilter.addEventListener('change', (e) => this.applyFilters());
        }
    }
    
    applyFilters() {
        const searchTerm = document.getElementById('searchInput')?.value.toLowerCase() || '';
        const subjectFilter = document.getElementById('subjectFilter')?.value || 'all';
        const difficultyFilter = document.getElementById('difficultyFilter')?.value || 'all';
        
        this.filteredQuestions = this.allQuestions.filter(q => {
            const matchesSearch = q.question.toLowerCase().includes(searchTerm) || 
                                 q.explanation.toLowerCase().includes(searchTerm);
            const matchesSubject = subjectFilter === 'all' || q.subject === subjectFilter;
            const matchesDifficulty = difficultyFilter === 'all' || q.difficulty === difficultyFilter;
            
            return matchesSearch && matchesSubject && matchesDifficulty;
        });
        
        this.render();
    }
    
    render() {
        if (!this.container) return;
        
        if (this.filteredQuestions.length === 0) {
            this.container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">🔍</div>
                    <h3 class="empty-title">No Results Found</h3>
                    <p class="empty-description">Try adjusting your search or filters</p>
                </div>
            `;
            return;
        }
        
        this.container.innerHTML = this.filteredQuestions.map((q, index) => `
            <div class="timeline-item" style="animation-delay: ${index * 0.05}s">
                <div class="timeline-marker"></div>
                <div class="timeline-content">
                    <div class="timeline-date">🕒 ${new Date(q.timestamp).toLocaleString()}</div>
                    <div class="timeline-title">
                        <span class="badge badge-subject">${q.subject}</span>
                        <span class="badge badge-difficulty">${q.difficulty}</span>
                    </div>
                    <div class="timeline-description"><strong>Q:</strong> ${q.question}</div>
                    <details style="margin-top: 1rem;">
                        <summary style="cursor: pointer; font-weight: 600; color: var(--primary-color);">View Explanation</summary>
                        <div style="margin-top: 1rem; padding: 1rem; background: var(--background-color); border-radius: 8px;">
                            ${q.explanation}
                        </div>
                    </details>
                </div>
            </div>
        `).join('');
    }
}

// Initialize navigation on all pages
document.addEventListener('DOMContentLoaded', () => {
    new Navigation();
});
