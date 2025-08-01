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
     * Calculate Age Factor (AF)
     */
    calculateAF(practitioner) {
        const ageConfig = this.config.age_factor_config;
        const peakAge = ageConfig.peak_age_years;
        
        if (practitioner.ageYears < peakAge) {
            return ageConfig.youthful_factor_multiplier;
        }
        
        const decadesPastPeak = (practitioner.ageYears - peakAge) / 10.0;
        return Math.pow(1.0 - ageConfig.power_decline_rate_per_decade, decadesPastPeak);
    }
    
    /**
     * Calculate Weight/Size Factor (WF)
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
        
        // Calculate adjustment using threshold tiers
        let totalAdjustment = 0.0;
        let remainingDiff = weightDifference;
        let lastTierMaxLbs = 0.0;
        let highestTierAdjustment = 0.0;
        
        for (const tier of weightConfig.thresholds_bonuses_penalties) {
            const lbsCoveredByThisTier = tier.diff_max_lbs - lastTierMaxLbs;
            const lbsToConsider = Math.min(remainingDiff, lbsCoveredByThisTier);
            
            if (lbsToConsider <= 0) {
                break;
            }
            
            const tierAdjustment = (lbsToConsider / weightConfig.increment_lbs) * tier.adjustment;
            totalAdjustment += tierAdjustment;
            highestTierAdjustment = tier.adjustment; // Keep track of highest tier adjustment
            
            remainingDiff -= lbsToConsider;
            lastTierMaxLbs = tier.diff_max_lbs;
            
            if (remainingDiff <= 0) {
                break;
            }
        }
        
        // Handle any remaining weight difference using the highest tier adjustment
        if (remainingDiff > 0 && highestTierAdjustment > 0) {
            const tierAdjustment = (remainingDiff / weightConfig.increment_lbs) * highestTierAdjustment;
            totalAdjustment += tierAdjustment;
        }
        
        // Apply adjustment based on whether practitioner is heavier or lighter
        return isHeavier ? 1.0 + totalAdjustment : 1.0 - totalAdjustment;
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