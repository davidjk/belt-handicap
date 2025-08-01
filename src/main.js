import './css/main.css';
import { JARCalculator } from './js/calculator.js';
import { PractitionerForm } from './js/forms.js';
import { RadarChart } from './js/chart.js';
import { StorageManager } from './js/storage.js';
import { ProfileGenerator } from './js/profiles.js';

class JARApp {
    constructor() {
        this.calculator = new JARCalculator();
        this.storage = new StorageManager();
        this.profileGenerator = new ProfileGenerator(this.calculator.config);
        this.practitioners = { a: null, b: null };
        this.forms = {};
        this.chart = null;
        
        this.init();
    }
    
    init() {
        this.setupForms();
        this.setupChart();
        this.bindEvents();
        console.log('JAR System initialized');
    }
    
    setupForms() {
        this.forms.a = new PractitionerForm('practitioner-a-form', 'a');
        this.forms.b = new PractitionerForm('practitioner-b-form', 'b');
        
        // Listen for form updates
        this.forms.a.onUpdate = (data) => this.handlePractitionerUpdate('a', data);
        this.forms.b.onUpdate = (data) => this.handlePractitionerUpdate('b', data);
    }
    
    setupChart() {
        const canvas = document.getElementById('radar-chart');
        this.chart = new RadarChart(canvas);
    }
    
    handlePractitionerUpdate(id, data) {
        console.log(`Updating practitioner ${id}:`, data);
        this.practitioners[id] = data;
        this.updateResults();
        this.updateComparison();
    }
    
    updateResults() {
        ['a', 'b'].forEach(id => {
            const practitioner = this.practitioners[id];
            if (!practitioner) {
                console.log(`No practitioner data for ${id}`);
                // Clear the results container if no practitioner data
                const container = document.getElementById(`practitioner-${id}-results`);
                container.innerHTML = '';
                return;
            }
            
            const other = this.practitioners[id === 'a' ? 'b' : 'a'];
            console.log(`Calculating factors for ${id}:`, practitioner);
            const results = this.calculator.calculateAllFactors(practitioner, other);
            console.log(`Results for ${id}:`, results);
            
            // Only show full results (including profile) if both practitioners exist
            const showProfile = this.practitioners.a && this.practitioners.b;
            this.displayResults(id, results, showProfile);
        });
    }
    
    displayResults(id, results, showProfile = false) {
        const container = document.getElementById(`practitioner-${id}-results`);
        const practitioner = this.practitioners[id];
        const handicappedScore = results.calculateHandicappedScore();
        
        // Always show the score
        let html = `
            <div class="results-display">
                <div class="handicapped-score">
                    <span class="score-label">Handicapped Score</span>
                    <span class="score-value">${handicappedScore.toFixed(1)}</span>
                </div>`;
        
        // Only show profile if both practitioners exist
        if (showProfile) {
            const profile = this.profileGenerator.generateProfile(practitioner, results, handicappedScore);
            
            html += `
                <div class="roll-dynamics-profile">
                    <h3 class="profile-title">Roll Dynamics Profile</h3>
                    
                    <div class="profile-summary">
                        <div class="profile-trait">
                            <span class="trait-label">Dominant Trait:</span>
                            <span class="trait-value">${profile.dominantTrait}</span>
                        </div>
                        <div class="profile-trait">
                            <span class="trait-label">Likely Approach:</span>
                            <span class="trait-value">${profile.likelyApproach}</span>
                        </div>
                    </div>
                    
                    <div class="profile-ratings">
                        <div class="rating-item">
                            <span class="rating-label">Control Potential</span>
                            <span class="rating-badge rating-${profile.controlPotential.toLowerCase()}">${profile.controlPotential}</span>
                        </div>
                        <div class="rating-item">
                            <span class="rating-label">Submission Offense</span>
                            <span class="rating-badge rating-${profile.submissionOffensiveThreat.toLowerCase()}">${profile.submissionOffensiveThreat}</span>
                        </div>
                        <div class="rating-item">
                            <span class="rating-label">Submission Defense</span>
                            <span class="rating-badge rating-${profile.submissionDefensiveResilience.toLowerCase()}">${profile.submissionDefensiveResilience}</span>
                        </div>
                    </div>
                    
                    <div class="profile-details">
                        <div class="strengths-section">
                            <h4 class="section-title">Key Strengths</h4>
                            <ul class="strengths-list">
                                ${profile.keyStrengths.map(strength => `<li>${strength}</li>`).join('')}
                            </ul>
                        </div>
                        
                        <div class="challenges-section">
                            <h4 class="section-title">Key Challenges</h4>
                            <ul class="challenges-list">
                                ${profile.keyChallenges.map(challenge => `<li>${challenge}</li>`).join('')}
                            </ul>
                        </div>
                    </div>
                </div>`;
        } else {
            // Show message when only one practitioner is filled out
            html += `
                <div class="incomplete-comparison">
                    <p class="comparison-message">
                        <span class="message-icon">⚠️</span>
                        Fill out both practitioners to see Roll Dynamics Profile and comparison analysis
                    </p>
                </div>`;
        }
        
        // Always show factors section
        html += `
                <div class="factors-section">
                    <button class="factors-toggle" onclick="this.parentElement.classList.toggle('expanded')">
                        <span class="toggle-text">Show Factor Breakdown</span>
                        <span class="toggle-icon">▼</span>
                    </button>
                    <div class="factors-breakdown">
                        <div class="factor">
                            <span class="factor-name">Belt Rank Score</span>
                            <span class="factor-value">${results.brs}</span>
                        </div>
                        <div class="factor">
                            <span class="factor-name">Age Factor</span>
                            <span class="factor-value">${results.af.toFixed(3)}</span>
                        </div>
                        <div class="factor">
                            <span class="factor-name">Weight Factor</span>
                            <span class="factor-value">${results.wf.toFixed(3)}</span>
                        </div>
                        <div class="factor">
                            <span class="factor-name">Athleticism Factor</span>
                            <span class="factor-value">${results.acf.toFixed(3)}</span>
                        </div>
                        <div class="factor">
                            <span class="factor-name">Experience Factor</span>
                            <span class="factor-value">${results.ref.toFixed(3)}</span>
                        </div>
                        <div class="factor">
                            <span class="factor-name">Training Factor</span>
                            <span class="factor-value">${results.tff.toFixed(3)}</span>
                        </div>
                        <div class="factor">
                            <span class="factor-name">Competition Factor</span>
                            <span class="factor-value">${results.cef.toFixed(3)}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }
    
    updateComparison() {
        if (!this.practitioners.a || !this.practitioners.b) {
            return;
        }
        
        const resultsA = this.calculator.calculateAllFactors(this.practitioners.a, this.practitioners.b);
        const resultsB = this.calculator.calculateAllFactors(this.practitioners.b, this.practitioners.a);
        
        this.chart.updateData([resultsA, resultsB], [
            this.practitioners.a.name || 'Practitioner A',
            this.practitioners.b.name || 'Practitioner B'
        ]);
    }
    
    bindEvents() {
        // Add any global event listeners here
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.jarApp = new JARApp();
});