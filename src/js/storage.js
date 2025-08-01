export class StorageManager {
    constructor() {
        this.storageKey = 'jar-practitioners';
        this.configKey = 'jar-config';
    }
    
    /**
     * Save practitioners to localStorage
     */
    savePractitioners(practitioners) {
        try {
            const serializable = {};
            for (const [key, practitioner] of Object.entries(practitioners)) {
                if (practitioner) {
                    serializable[key] = {
                        name: practitioner.name,
                        bjjBeltRank: practitioner.bjjBeltRank,
                        ageYears: practitioner.ageYears,
                        weightLbs: practitioner.weightLbs,
                        primaryOccupationActivityLevel: practitioner.primaryOccupationActivityLevel,
                        standardizedFitnessTestPercentileEstimate: practitioner.standardizedFitnessTestPercentileEstimate,
                        otherGrapplingArtExperience: practitioner.otherGrapplingArtExperience,
                        bjjTrainingSessionsPerWeek: practitioner.bjjTrainingSessionsPerWeek,
                        bjjCompetitionExperienceLevel: practitioner.bjjCompetitionExperienceLevel,
                        practitionerId: practitioner.practitionerId,
                        savedAt: new Date().toISOString()
                    };
                }
            }
            
            localStorage.setItem(this.storageKey, JSON.stringify(serializable));
            console.log('Practitioners saved to localStorage');
            return true;
        } catch (error) {
            console.error('Error saving practitioners:', error);
            return false;
        }
    }
    
    /**
     * Load practitioners from localStorage
     */
    loadPractitioners() {
        try {
            const stored = localStorage.getItem(this.storageKey);
            if (!stored) {
                return {};
            }
            
            const parsed = JSON.parse(stored);
            console.log('Practitioners loaded from localStorage:', Object.keys(parsed));
            return parsed;
        } catch (error) {
            console.error('Error loading practitioners:', error);
            return {};
        }
    }
    
    /**
     * Save a single practitioner with a custom name
     */
    savePractitioner(name, practitionerData) {
        try {
            const savedPractitioners = this.loadSavedPractitioners();
            
            const practitionerToSave = {
                name: practitionerData.name || name,
                bjjBeltRank: practitionerData.bjjBeltRank,
                ageYears: practitionerData.ageYears,
                weightLbs: practitionerData.weightLbs,
                primaryOccupationActivityLevel: practitionerData.primaryOccupationActivityLevel,
                standardizedFitnessTestPercentileEstimate: practitionerData.standardizedFitnessTestPercentileEstimate,
                otherGrapplingArtExperience: practitionerData.otherGrapplingArtExperience,
                bjjTrainingSessionsPerWeek: practitionerData.bjjTrainingSessionsPerWeek,
                bjjCompetitionExperienceLevel: practitionerData.bjjCompetitionExperienceLevel,
                practitionerId: practitionerData.practitionerId,
                savedAt: new Date().toISOString()
            };
            
            savedPractitioners[name] = practitionerToSave;
            localStorage.setItem('jar-saved-practitioners', JSON.stringify(savedPractitioners));
            
            console.log(`Practitioner '${name}' saved`);
            return true;
        } catch (error) {
            console.error('Error saving practitioner:', error);
            return false;
        }
    }
    
    /**
     * Load all saved practitioners (named saves)
     */
    loadSavedPractitioners() {
        try {
            const stored = localStorage.getItem('jar-saved-practitioners');
            if (!stored) {
                return {};
            }
            
            return JSON.parse(stored);
        } catch (error) {
            console.error('Error loading saved practitioners:', error);
            return {};
        }
    }
    
    /**
     * Delete a saved practitioner
     */
    deletePractitioner(name) {
        try {
            const savedPractitioners = this.loadSavedPractitioners();
            delete savedPractitioners[name];
            localStorage.setItem('jar-saved-practitioners', JSON.stringify(savedPractitioners));
            
            console.log(`Practitioner '${name}' deleted`);
            return true;
        } catch (error) {
            console.error('Error deleting practitioner:', error);
            return false;
        }
    }
    
    /**
     * Get a list of saved practitioner names
     */
    getSavedPractitionerNames() {
        const saved = this.loadSavedPractitioners();
        return Object.keys(saved).sort();
    }
    
    /**
     * Export practitioners as JSON
     */
    exportPractitioners(practitioners) {
        try {
            const exportData = {
                exportedAt: new Date().toISOString(),
                version: '1.0',
                practitioners: practitioners
            };
            
            const blob = new Blob([JSON.stringify(exportData, null, 2)], {
                type: 'application/json'
            });
            
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `jar-practitioners-${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            return true;
        } catch (error) {
            console.error('Error exporting practitioners:', error);
            return false;
        }
    }
    
    /**
     * Import practitioners from JSON file
     */
    importPractitioners(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            
            reader.onload = (e) => {
                try {
                    const data = JSON.parse(e.target.result);
                    
                    // Validate the import data structure
                    if (!data.practitioners) {
                        reject(new Error('Invalid file format: missing practitioners data'));
                        return;
                    }
                    
                    // Save imported practitioners
                    const savedPractitioners = this.loadSavedPractitioners();
                    let importCount = 0;
                    
                    for (const [key, practitioner] of Object.entries(data.practitioners)) {
                        if (practitioner && practitioner.name) {
                            savedPractitioners[practitioner.name] = {
                                ...practitioner,
                                importedAt: new Date().toISOString()
                            };
                            importCount++;
                        }
                    }
                    
                    localStorage.setItem('jar-saved-practitioners', JSON.stringify(savedPractitioners));
                    
                    resolve({
                        success: true,
                        importCount: importCount,
                        practitioners: data.practitioners
                    });
                    
                } catch (error) {
                    reject(new Error(`Error parsing file: ${error.message}`));
                }
            };
            
            reader.onerror = () => {
                reject(new Error('Error reading file'));
            };
            
            reader.readAsText(file);
        });
    }
    
    /**
     * Clear all stored data
     */
    clearAllData() {
        try {
            localStorage.removeItem(this.storageKey);
            localStorage.removeItem('jar-saved-practitioners');
            localStorage.removeItem(this.configKey);
            
            console.log('All JAR data cleared from localStorage');
            return true;
        } catch (error) {
            console.error('Error clearing data:', error);
            return false;
        }
    }
    
    /**
     * Get storage usage statistics
     */
    getStorageStats() {
        try {
            const practitioners = localStorage.getItem(this.storageKey) || '{}';
            const savedPractitioners = localStorage.getItem('jar-saved-practitioners') || '{}';
            const config = localStorage.getItem(this.configKey) || '{}';
            
            return {
                practitionersSize: new Blob([practitioners]).size,
                savedPractitionersSize: new Blob([savedPractitioners]).size,
                configSize: new Blob([config]).size,
                totalSize: new Blob([practitioners + savedPractitioners + config]).size,
                practitionersCount: Object.keys(JSON.parse(practitioners)).length,
                savedPractitionersCount: Object.keys(JSON.parse(savedPractitioners)).length
            };
        } catch (error) {
            console.error('Error getting storage stats:', error);
            return null;
        }
    }
}