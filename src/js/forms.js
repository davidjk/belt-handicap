import { PractitionerData, BeltRanks, GrapplingArts, WrestlingLevels, JudoLevels, OtherGrapplingLevels, CompetitionLevels } from './types.js';

export class PractitionerForm {
    constructor(containerId, practitionerId) {
        this.container = document.getElementById(containerId);
        this.practitionerId = practitionerId;
        this.onUpdate = null; // Callback for when data updates
        this.currentData = null;
        
        this.render();
        this.bindEvents();
    }
    
    render() {
        this.container.innerHTML = `
            <form class="practitioner-form-element">
                <div class="form-group">
                    <label class="form-label" for="${this.practitionerId}-name">Name</label>
                    <input 
                        type="text" 
                        id="${this.practitionerId}-name" 
                        class="form-input" 
                        placeholder="Enter practitioner name"
                        data-field="name">
                </div>
                
                <div class="form-group">
                    <label class="form-label">BJJ Belt Rank</label>
                    <div class="belt-selection" id="${this.practitionerId}-belt-selection" data-field="bjjBeltRank">
                        ${Object.values(BeltRanks).map(belt => 
                            `<div class="belt-block belt-${belt.toLowerCase()}" 
                                 data-belt="${belt}" 
                                 title="${belt} Belt">
                                <span class="belt-label">${belt}</span>
                            </div>`
                        ).join('')}
                    </div>
                    <input type="hidden" id="${this.practitionerId}-belt" data-field="bjjBeltRank" value="${BeltRanks.WHITE}">
                </div>
                
                <div class="form-group">
                    <label class="form-label" for="${this.practitionerId}-age">Age (years)</label>
                    <input 
                        type="number" 
                        id="${this.practitionerId}-age" 
                        class="form-input" 
                        min="16" 
                        max="90" 
                        value="25"
                        data-field="ageYears">
                </div>
                
                <div class="form-group">
                    <label class="form-label" for="${this.practitionerId}-weight">Weight (lbs)</label>
                    <input 
                        type="number" 
                        id="${this.practitionerId}-weight" 
                        class="form-input" 
                        min="80" 
                        max="400" 
                        value="170"
                        data-field="weightLbs">
                </div>
                
                
                <div class="form-group">
                    <label class="form-label" for="${this.practitionerId}-fitness">Fitness Test Percentile</label>
                    <div class="fitness-description">
                        <small>Rate your overall fitness compared to others your age/gender:</small>
                    </div>
                    <input 
                        type="range" 
                        id="${this.practitionerId}-fitness" 
                        class="form-range" 
                        min="0" 
                        max="100" 
                        value="50"
                        data-field="standardizedFitnessTestPercentileEstimate">
                    <div class="range-value">
                        <div class="percentile-display">
                            <span id="${this.practitionerId}-fitness-value">50</span><span class="percentile-suffix">th percentile</span>
                        </div>
                        <div class="fitness-guide" id="${this.practitionerId}-fitness-guide">
                            Average fitness level
                        </div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Other Grappling Experience</label>
                    <div class="grappling-experience-section">
                        <select id="${this.practitionerId}-grappling-art" class="form-select">
                            ${Object.values(GrapplingArts).map(art => 
                                `<option value="${art}">${art}</option>`
                            ).join('')}
                        </select>
                        <select id="${this.practitionerId}-grappling-level" class="form-select mt-sm">
                            <!-- Dynamically populated based on art selection -->
                        </select>
                    </div>
                </div>
                
                <div class="form-group">
                    <label class="form-label" for="${this.practitionerId}-training">BJJ Training Sessions per Week</label>
                    <input 
                        type="number" 
                        id="${this.practitionerId}-training" 
                        class="form-input" 
                        min="0" 
                        max="14" 
                        value="3"
                        data-field="bjjTrainingSessionsPerWeek">
                </div>
                
                <div class="form-group">
                    <label class="form-label" for="${this.practitionerId}-competition">BJJ Competition Experience</label>
                    <select id="${this.practitionerId}-competition" class="form-select" data-field="bjjCompetitionExperienceLevel">
                        ${Object.values(CompetitionLevels).map(level => 
                            `<option value="${level}">${level}</option>`
                        ).join('')}
                    </select>
                </div>
            </form>
        `;
        
        this.addRangeValueDisplay();
        this.addBeltIndicators();
        this.setupGrapplingExperienceDropdowns();
    }
    
    addRangeValueDisplay() {
        const rangeInput = this.container.querySelector(`#${this.practitionerId}-fitness`);
        const valueDisplay = this.container.querySelector(`#${this.practitionerId}-fitness-value`);
        const guideDisplay = this.container.querySelector(`#${this.practitionerId}-fitness-guide`);
        
        const updateFitnessGuide = (value) => {
            let guide = '';
            if (value <= 5) guide = 'Basement dwelling snack monster 🍕';
            else if (value <= 15) guide = 'Couch potato - stairs are the enemy 🛋️';
            else if (value <= 25) guide = 'Getting winded tying shoes 👟';
            else if (value <= 35) guide = 'Weekend warrior wannabe 🏃‍♂️';
            else if (value <= 45) guide = 'Casual gym visitor - sometimes 💪';
            else if (value <= 55) guide = 'Average fitness - can handle stairs 🚶';
            else if (value <= 65) guide = 'Above average - regular gym goer 💪';
            else if (value <= 75) guide = 'Pretty fit - enjoys working out 🏋️';
            else if (value <= 85) guide = 'Very fit - fitness is a lifestyle 🔥';
            else if (value <= 90) guide = 'Athlete level - others are jealous 🏆';
            else if (value <= 95) guide = 'Elite fitness - gym inspiration 💎';
            else if (value <= 99) guide = 'Adonis level - Greek god physique ⚡';
            else guide = 'Superhuman - probably not natural 🦸‍♂️';
            
            guideDisplay.textContent = guide;
        };
        
        rangeInput.addEventListener('input', (e) => {
            valueDisplay.textContent = e.target.value;
            updateFitnessGuide(parseInt(e.target.value));
        });
        
        // Initialize guide
        updateFitnessGuide(50);
    }
    
    addBeltIndicators() {
        const beltSelection = this.container.querySelector(`#${this.practitionerId}-belt-selection`);
        const hiddenInput = this.container.querySelector(`#${this.practitionerId}-belt`);
        
        // Add click handlers to belt blocks
        beltSelection.addEventListener('click', (e) => {
            const beltBlock = e.target.closest('.belt-block');
            if (!beltBlock) return;
            
            // Remove active class from all blocks
            beltSelection.querySelectorAll('.belt-block').forEach(block => {
                block.classList.remove('active');
            });
            
            // Add active class to clicked block
            beltBlock.classList.add('active');
            
            // Update hidden input value
            const selectedBelt = beltBlock.getAttribute('data-belt');
            hiddenInput.value = selectedBelt;
            
            // Trigger form update
            this.handleFormUpdate();
        });
        
        // Set initial selection to white belt
        const whiteBelt = beltSelection.querySelector('.belt-block[data-belt="White"]');
        if (whiteBelt) {
            whiteBelt.classList.add('active');
        }
    }
    
    setupGrapplingExperienceDropdowns() {
        const artSelect = this.container.querySelector(`#${this.practitionerId}-grappling-art`);
        const levelSelect = this.container.querySelector(`#${this.practitionerId}-grappling-level`);
        
        const updateLevelOptions = (selectedArt) => {
            let levels = {};
            
            switch (selectedArt) {
                case 'Wrestling':
                    levels = WrestlingLevels;
                    break;
                case 'Judo':
                    levels = JudoLevels;
                    break;
                case 'Sambo':
                case 'Other':
                    levels = OtherGrapplingLevels;
                    break;
                default:
                    levels = { NONE: 'None' };
            }
            
            levelSelect.innerHTML = Object.values(levels).map(level => 
                `<option value="${level}">${level}</option>`
            ).join('');
        };
        
        // Set up event listener for art changes
        artSelect.addEventListener('change', (e) => {
            updateLevelOptions(e.target.value);
            this.handleFormUpdate();
        });
        
        // Initialize with default selection
        updateLevelOptions(artSelect.value);
    }
    
    bindEvents() {
        const form = this.container.querySelector('.practitioner-form-element');
        
        // Add debounced input handling for real-time updates
        let updateTimeout;
        
        form.addEventListener('input', (e) => {
            clearTimeout(updateTimeout);
            updateTimeout = setTimeout(() => {
                this.handleFormUpdate();
            }, 300); // 300ms debounce
        });
        
        form.addEventListener('change', () => {
            this.handleFormUpdate();
        });
        
        // Special handling for grappling experience
        const grapplingArt = this.container.querySelector(`#${this.practitionerId}-grappling-art`);
        const grapplingLevel = this.container.querySelector(`#${this.practitionerId}-grappling-level`);
        
        [grapplingArt, grapplingLevel].forEach(element => {
            element.addEventListener('change', () => {
                this.handleFormUpdate();
            });
        });
    }
    
    handleFormUpdate() {
        try {
            const formData = this.getFormData();
            console.log(`Form data for ${this.practitionerId}:`, formData);
            
            this.currentData = new PractitionerData(formData);
            console.log(`Practitioner data for ${this.practitionerId}:`, this.currentData);
            
            // Add visual feedback for successful validation
            this.showValidationSuccess();
            
            if (this.onUpdate) {
                console.log(`Calling onUpdate for ${this.practitionerId}`);
                this.onUpdate(this.currentData);
            }
        } catch (error) {
            console.error('Form validation error:', error);
            this.showValidationError(error.message);
        }
    }
    
    getFormData() {
        const form = this.container.querySelector('.practitioner-form-element');
        const formData = {};
        
        // Get basic form fields
        form.querySelectorAll('[data-field]').forEach(input => {
            const field = input.getAttribute('data-field');
            let value = input.value;
            
            // Convert numeric fields
            if (input.type === 'number' || input.type === 'range') {
                value = parseFloat(value);
            }
            
            formData[field] = value;
        });
        
        // Handle grappling experience separately - always include the selection
        const grapplingArt = this.container.querySelector(`#${this.practitionerId}-grappling-art`).value;
        const grapplingLevel = this.container.querySelector(`#${this.practitionerId}-grappling-level`).value;
        
        formData.otherGrapplingArtExperience = [{
            artName: grapplingArt,
            experienceLevel: grapplingLevel
        }];
        
        formData.practitionerId = this.practitionerId;
        
        return formData;
    }
    
    showValidationSuccess() {
        const form = this.container.querySelector('.practitioner-form-element');
        form.classList.remove('validation-error');
        form.classList.add('validation-success');
        
        setTimeout(() => {
            form.classList.remove('validation-success');
        }, 1000);
    }
    
    showValidationError(message) {
        const form = this.container.querySelector('.practitioner-form-element');
        form.classList.remove('validation-success');
        form.classList.add('validation-error');
        
        // Show error message
        let errorDiv = this.container.querySelector('.error-message');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            form.appendChild(errorDiv);
        }
        
        errorDiv.textContent = message;
        
        setTimeout(() => {
            form.classList.remove('validation-error');
            if (errorDiv) {
                errorDiv.remove();
            }
        }, 3000);
    }
    
    loadData(data) {
        try {
            const practitioner = new PractitionerData(data);
            
            // Populate form fields
            this.container.querySelector(`#${this.practitionerId}-name`).value = practitioner.name || '';
            
            // Handle belt selection
            this.container.querySelector(`#${this.practitionerId}-belt`).value = practitioner.bjjBeltRank;
            // Update belt block selection
            const beltSelection = this.container.querySelector(`#${this.practitionerId}-belt-selection`);
            beltSelection.querySelectorAll('.belt-block').forEach(block => {
                block.classList.remove('active');
                if (block.getAttribute('data-belt') === practitioner.bjjBeltRank) {
                    block.classList.add('active');
                }
            });
            this.container.querySelector(`#${this.practitionerId}-age`).value = practitioner.ageYears;
            this.container.querySelector(`#${this.practitionerId}-weight`).value = practitioner.weightLbs;
            this.container.querySelector(`#${this.practitionerId}-fitness`).value = practitioner.standardizedFitnessTestPercentileEstimate;
            this.container.querySelector(`#${this.practitionerId}-training`).value = practitioner.bjjTrainingSessionsPerWeek;
            this.container.querySelector(`#${this.practitionerId}-competition`).value = practitioner.bjjCompetitionExperienceLevel;
            
            // Handle grappling experience
            if (practitioner.otherGrapplingArtExperience && practitioner.otherGrapplingArtExperience.length > 0) {
                const experience = practitioner.otherGrapplingArtExperience[0];
                this.container.querySelector(`#${this.practitionerId}-grappling-art`).value = experience.artName;
                this.container.querySelector(`#${this.practitionerId}-grappling-level`).value = experience.experienceLevel;
            }
            
            // Update fitness display
            this.container.querySelector(`#${this.practitionerId}-fitness-value`).textContent = practitioner.standardizedFitnessTestPercentileEstimate;
            
            this.currentData = practitioner;
            
            if (this.onUpdate) {
                this.onUpdate(this.currentData);
            }
            
        } catch (error) {
            console.error('Error loading data:', error);
            this.showValidationError('Error loading practitioner data');
        }
    }
    
    getData() {
        return this.currentData;
    }
}