import './css/main.css';
import { JARCalculator } from './js/calculator.js';
import { PractitionerForm } from './js/forms.js';
import { RadarChart } from './js/chart.js';
import { StorageManager } from './js/storage.js';

class JARApp {
    constructor() {
        this.calculator = new JARCalculator();
        this.storage = new StorageManager();
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
        this.practitioners[id] = data;
        this.updateResults();
        this.updateComparison();
    }
    
    updateResults() {
        ['a', 'b'].forEach(id => {
            const practitioner = this.practitioners[id];
            if (!practitioner) return;
            
            const other = this.practitioners[id === 'a' ? 'b' : 'a'];
            const results = this.calculator.calculateAllFactors(practitioner, other);
            
            this.displayResults(id, results);
        });
    }
    
    displayResults(id, results) {
        const container = document.getElementById(`practitioner-${id}-results`);
        const handicappedScore = results.calculateHandicappedScore();
        
        container.innerHTML = `
            <div class="results-display">
                <div class="handicapped-score">
                    <span class="score-label">Handicapped Score</span>
                    <span class="score-value">${handicappedScore.toFixed(1)}</span>
                </div>
                
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
        `;
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