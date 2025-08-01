import { RollDynamicsProfile } from './types.js';

export class ProfileGenerator {
    constructor(config) {
        this.config = config;
    }
    
    /**
     * Identify which factors are significantly high or low
     */
    identifySignificantFactors(factors) {
        const dynamicsConfig = this.config.profile_dynamics_config;
        const highThreshold = dynamicsConfig.significant_multiplier_threshold_high;
        const lowThreshold = dynamicsConfig.significant_multiplier_threshold_low;
        
        const factorSignificance = {};
        
        // Check each factor
        const factorValues = {
            af: factors.af,
            wf: factors.wf,
            acf: factors.acf,
            ref: factors.ref,
            tff: factors.tff,
            cef: factors.cef
        };
        
        for (const [factorId, value] of Object.entries(factorValues)) {
            if (value >= highThreshold) {
                factorSignificance[factorId] = 'high';
            } else if (value <= lowThreshold) {
                factorSignificance[factorId] = 'low';
            } else {
                factorSignificance[factorId] = 'neutral';
            }
        }
        
        // Special handling for BRS (based on belt rank rather than multiplier)
        const beltScores = this.config.belt_rank_scores;
        const purpleThreshold = beltScores.Purple;
        
        if (factors.brs >= purpleThreshold) {
            factorSignificance.brs = 'high';
        } else {
            factorSignificance.brs = 'low';
        }
        
        return factorSignificance;
    }
    
    /**
     * Determine the practitioner's dominant trait based on significant factors
     */
    determineDominantTrait(factorSignificance) {
        // Technical BJJ Specialist
        if (factorSignificance.brs === 'high' && 
            !['wf', 'acf', 'ref'].some(f => factorSignificance[f] === 'high')) {
            return 'Technical BJJ Specialist';
        }
        
        // Physical Grappling Athlete
        if (factorSignificance.brs === 'low' && 
            ['wf', 'acf', 'ref'].some(f => factorSignificance[f] === 'high')) {
            return 'Physical Grappling Athlete';
        }
        
        // Dominant All-Rounder
        if (factorSignificance.brs === 'high' && 
            ['wf', 'acf', 'ref'].some(f => factorSignificance[f] === 'high')) {
            return 'Dominant All-Rounder';
        }
        
        return 'Balanced Practitioner';
    }
    
    /**
     * Determine the practitioner's likely roll approach based on significant factors
     */
    determineLikelyApproach(factorSignificance) {
        if (factorSignificance.brs === 'high' && factorSignificance.wf !== 'high') {
            return 'Technical & Opportunistic';
        }
        
        if (['wf', 'acf', 'ref'].some(f => factorSignificance[f] === 'high')) {
            return 'Pressure & Control-Oriented';
        }
        
        return 'Adaptable & Balanced';
    }
    
    /**
     * Generate key strengths based on significant factors
     */
    generateKeyStrengths(factorSignificance) {
        const dynamicsConfig = this.config.profile_dynamics_config;
        const implicationStatements = dynamicsConfig.implication_statements;
        const strengths = [];
        
        // Add statements for high factors
        if (factorSignificance.brs === 'high' && implicationStatements.BRS_high) {
            strengths.push(implicationStatements.BRS_high);
        }
        
        // Check for wrestling/judo experience
        if (factorSignificance.ref === 'high' && implicationStatements.REF_high_wrestling_judo) {
            strengths.push(implicationStatements.REF_high_wrestling_judo);
        }
        
        if (factorSignificance.acf === 'high' && implicationStatements.ACF_high) {
            strengths.push(implicationStatements.ACF_high);
        }
        
        if (factorSignificance.wf === 'high' && implicationStatements.WF_high) {
            strengths.push(implicationStatements.WF_high);
        }
        
        // Add default strength if none were found
        if (strengths.length === 0) {
            strengths.push('Well-rounded BJJ skills with balanced attributes');
        }
        
        return strengths;
    }
    
    /**
     * Generate key challenges based on significant factors
     */
    generateKeyChallenges(factorSignificance) {
        const dynamicsConfig = this.config.profile_dynamics_config;
        const implicationStatements = dynamicsConfig.implication_statements;
        const challenges = [];
        
        // Add statements for low factors
        if (factorSignificance.brs === 'low' && implicationStatements.BRS_low) {
            challenges.push(implicationStatements.BRS_low);
        }
        
        if (factorSignificance.af === 'low' && implicationStatements.AF_low) {
            challenges.push(implicationStatements.AF_low);
        }
        
        if (factorSignificance.wf === 'low' && implicationStatements.WF_low) {
            challenges.push(implicationStatements.WF_low);
        }
        
        // Add default challenge if none were found
        if (challenges.length === 0) {
            challenges.push('May need to adjust strategy against opponents with significant physical or technical advantages');
        }
        
        return challenges;
    }
    
    /**
     * Determine control potential based on significant factors
     */
    determineControlPotential(factorSignificance) {
        // Count how many control-related factors are high
        const controlFactors = ['ref', 'wf', 'acf'];
        const highCount = controlFactors.filter(f => factorSignificance[f] === 'high').length;
        
        if (highCount >= 2) {
            return 'High';
        } else if (highCount === 1) {
            return 'Medium';
        } else {
            return 'Low';
        }
    }
    
    /**
     * Determine submission offensive threat based on significant factors
     */
    determineSubmissionThreat(factorSignificance) {
        // Primarily based on BJJ belt rank
        if (factorSignificance.brs === 'high') {
            // Enhance with competition experience
            if (factorSignificance.cef === 'high') {
                return 'High';
            }
            return 'Medium';
        }
        return 'Low';
    }
    
    /**
     * Determine submission defensive resilience based on significant factors
     */
    determineSubmissionDefense(factorSignificance) {
        // Primarily based on BJJ belt rank
        if (factorSignificance.brs === 'high') {
            return 'High';
        }
        
        // Some enhancement from other grappling experience
        if (factorSignificance.ref === 'high') {
            return 'Medium';
        }
        
        return 'Low';
    }
    
    /**
     * Generate complete Roll Dynamics Profile
     */
    generateProfile(practitioner, factors, handicappedScore) {
        const factorSignificance = this.identifySignificantFactors(factors);
        
        return new RollDynamicsProfile({
            dominantTrait: this.determineDominantTrait(factorSignificance),
            likelyApproach: this.determineLikelyApproach(factorSignificance),
            keyStrengths: this.generateKeyStrengths(factorSignificance),
            keyChallenges: this.generateKeyChallenges(factorSignificance),
            controlPotential: this.determineControlPotential(factorSignificance),
            submissionOffensiveThreat: this.determineSubmissionThreat(factorSignificance),
            submissionDefensiveResilience: this.determineSubmissionDefense(factorSignificance),
            practitionerName: practitioner.name,
            handicappedScore: handicappedScore
        });
    }
}