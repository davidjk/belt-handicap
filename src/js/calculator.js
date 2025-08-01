import { FactorResults } from './types.js';
import { ConfigManager } from './config.js';

export class JARCalculator {
    constructor() {
        this.configManager = new ConfigManager();
        this.config = this.configManager.getConfig();
    }
    
    /**
     * Calculate Belt Rank Score (BRS)
     */
    calculateBRS(practitioner) {
        return this.config.belt_rank_scores[practitioner.bjjBeltRank];
    }
    
    /**
     * Calculate Age Factor (AF) using age brackets
     */
    calculateAF(practitioner) {
        const ageConfig = this.config.age_factor_config;
        const age = practitioner.ageYears;
        
        // Find appropriate age bracket
        for (const bracket of ageConfig.age_brackets) {
            if (age >= bracket.age_min && age <= bracket.age_max) {
                return bracket.multiplier;
            }
        }
        
        // Default to neutral if age is outside all brackets
        return 1.0;
    }
    
    /**
     * Calculate Weight/Size Factor (WF) using exponential scaling
     */
    calculateWF(practitioner, comparisonPractitioner) {
        if (!comparisonPractitioner) {
            return 1.0; // Neutral if no comparison
        }
        
        const weightConfig = this.config.weight_factor_config;
        const weightDifference = Math.abs(practitioner.weightLbs - comparisonPractitioner.weightLbs);
        
        if (weightDifference <= 0) {
            return 1.0; // No difference
        }
        
        // Determine if this practitioner is heavier or lighter
        const isHeavier = practitioner.weightLbs > comparisonPractitioner.weightLbs;
        
        // Calculate exponential adjustment: (weight_diff / base_increment)^scaling_factor * base_rate
        const baseIncrement = weightConfig.base_increment_lbs;
        const scalingFactor = weightConfig.exponential_scaling_factor;
        const baseRate = weightConfig.base_adjustment_rate;
        
        const weightRatio = weightDifference / baseIncrement;
        const exponentialAdjustment = Math.pow(weightRatio, scalingFactor) * baseRate;
        
        // Apply adjustment based on whether practitioner is heavier or lighter
        return isHeavier ? 1.0 + exponentialAdjustment : 1.0 - exponentialAdjustment;
    }
    
    /**
     * Calculate Athleticism & Conditioning Factor (ACF)
     */
    calculateACF(practitioner) {
        const acfConfig = this.config.acf_config;
        const fitnessPercentile = practitioner.standardizedFitnessTestPercentileEstimate;
        
        // Find appropriate level based on fitness percentile
        for (const level of acfConfig.levels) {
            const levelId = level.level_id;
            
            // Define percentile ranges for each level
            if ((levelId === 1 && fitnessPercentile < 30) ||
                (levelId === 2 && fitnessPercentile >= 30 && fitnessPercentile < 60) ||
                (levelId === 3 && fitnessPercentile >= 60 && fitnessPercentile < 80) ||
                (levelId === 4 && fitnessPercentile >= 80 && fitnessPercentile < 95) ||
                (levelId === 5 && fitnessPercentile >= 95)) {
                return level.multiplier;
            }
        }
        
        // Default to middle level if no match found
        return 1.0;
    }
    
    /**
     * Calculate Relevant Grappling Experience Factor (REF)
     */
    calculateREF(practitioner) {
        const refConfig = this.config.ref_config;
        
        // If no other grappling experience
        if (!practitioner.otherGrapplingArtExperience || practitioner.otherGrapplingArtExperience.length === 0) {
            return refConfig.levels[0].multiplier; // Level 0 - None
        }
        
        // Get the most significant experience (for now, just use the first one)
        const experience = practitioner.otherGrapplingArtExperience[0];
        
        // Try to map using the configuration
        const mappingKey = `${experience.artName}_${experience.experienceLevel}`;
        if (mappingKey in refConfig.art_experience_level_mapping) {
            const levelId = refConfig.art_experience_level_mapping[mappingKey];
            
            // Find the corresponding multiplier
            for (const level of refConfig.levels) {
                if (level.level_id === levelId) {
                    return level.multiplier;
                }
            }
        }
        
        // Default to level 0 if no mapping found
        return refConfig.levels[0].multiplier;
    }
    
    /**
     * Calculate Training Intensity/Frequency Factor (TFF)
     */
    calculateTFF(practitioner) {
        const tffConfig = this.config.tff_config;
        const sessions = practitioner.bjjTrainingSessionsPerWeek;
        
        for (const level of tffConfig.levels) {
            if (sessions >= level.sessions_min && sessions <= level.sessions_max) {
                return level.multiplier;
            }
        }
        
        // Default to middle level if no match found
        return 1.0;
    }
    
    /**
     * Calculate BJJ Competition Experience Factor (CEF)
     */
    calculateCEF(practitioner) {
        const cefConfig = this.config.cef_config;
        const compLevel = practitioner.bjjCompetitionExperienceLevel;
        
        // Get level_id from mapping
        if (compLevel in cefConfig.competition_level_mapping) {
            const levelId = cefConfig.competition_level_mapping[compLevel];
            
            // Find the corresponding multiplier
            for (const level of cefConfig.levels) {
                if (level.level_id === levelId) {
                    return level.multiplier;
                }
            }
        }
        
        // Default to level 0 if no mapping found
        return cefConfig.levels[0].multiplier;
    }
    
    /**
     * Calculate all factors for a practitioner
     */
    calculateAllFactors(practitioner, comparisonPractitioner = null) {
        return new FactorResults(
            this.calculateBRS(practitioner),
            this.calculateAF(practitioner),
            this.calculateWF(practitioner, comparisonPractitioner),
            this.calculateACF(practitioner),
            this.calculateREF(practitioner),
            this.calculateTFF(practitioner),
            this.calculateCEF(practitioner)
        );
    }
}