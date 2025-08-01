// Belt rank constants
export const BeltRanks = {
    WHITE: 'White',
    BLUE: 'Blue',
    PURPLE: 'Purple',
    BROWN: 'Brown',
    BLACK: 'Black'
};

// Experience level constants
export const GrapplingArts = {
    NONE: 'None',
    WRESTLING: 'Wrestling',
    JUDO: 'Judo',
    SAMBO: 'Sambo',
    OTHER: 'Other'
};

export const WrestlingLevels = {
    NONE: 'None',
    HIGH_SCHOOL: 'High School',
    HIGH_SCHOOL_STATE: 'High School State Qualifier',
    COLLEGE: 'College',
    COLLEGE_D1: 'College D1',
    INTERNATIONAL_OLYMPIC: 'International/Olympic'
};

export const JudoLevels = {
    NONE: 'None',
    LOCAL: 'Local',
    REGIONAL: 'Regional', 
    NATIONAL: 'National',
    INTERNATIONAL: 'International',
    OLYMPIC: 'Olympic'
};

export const OtherGrapplingLevels = {
    NONE: 'None',
    RECREATIONAL: 'Recreational (<1 year)',
    CLUB_LEVEL: 'Club Level (1-3 years)',
    REGIONAL: 'Regional Competition',
    NATIONAL: 'National Competition',
    INTERNATIONAL: 'International Competition'
};

export const CompetitionLevels = {
    NONE: 'None',
    LIMITED_LOCAL: 'Limited Local',
    REGULAR_REGIONAL: 'Regular Regional',
    NATIONAL_INTERNATIONAL: 'National/International'
};


// Data classes
export class GrapplingExperience {
    constructor(artName, experienceLevel) {
        this.artName = artName;
        this.experienceLevel = experienceLevel;
    }
}

export class PractitionerData {
    constructor({
        name = '',
        bjjBeltRank = BeltRanks.WHITE,
        ageYears = 25,
        weightLbs = 170,
        standardizedFitnessTestPercentileEstimate = 50,
        otherGrapplingArtExperience = [],
        bjjTrainingSessionsPerWeek = 3,
        bjjCompetitionExperienceLevel = CompetitionLevels.NONE,
        practitionerId = null
    } = {}) {
        this.name = name;
        this.bjjBeltRank = bjjBeltRank;
        this.ageYears = ageYears;
        this.weightLbs = weightLbs;
        this.standardizedFitnessTestPercentileEstimate = standardizedFitnessTestPercentileEstimate;
        this.otherGrapplingArtExperience = otherGrapplingArtExperience;
        this.bjjTrainingSessionsPerWeek = bjjTrainingSessionsPerWeek;
        this.bjjCompetitionExperienceLevel = bjjCompetitionExperienceLevel;
        this.practitionerId = practitionerId;
        
        this.validate();
    }
    
    validate() {
        if (this.ageYears < 16 || this.ageYears > 90) {
            throw new Error(`Age must be between 16 and 90 (got ${this.ageYears})`);
        }
        if (this.weightLbs < 80 || this.weightLbs > 400) {
            throw new Error(`Weight must be between 80 and 400 lbs (got ${this.weightLbs})`);
        }
        if (this.standardizedFitnessTestPercentileEstimate < 0 || this.standardizedFitnessTestPercentileEstimate > 100) {
            throw new Error(`Fitness percentile must be between 0 and 100 (got ${this.standardizedFitnessTestPercentileEstimate})`);
        }
        if (this.bjjTrainingSessionsPerWeek < 0 || this.bjjTrainingSessionsPerWeek > 14) {
            throw new Error(`Training sessions must be between 0 and 14 per week (got ${this.bjjTrainingSessionsPerWeek})`);
        }
    }
}

export class FactorResults {
    constructor(brs, af, wf, acf, ref, tff, cef) {
        this.brs = brs;   // Belt Rank Score
        this.af = af;     // Age Factor
        this.wf = wf;     // Weight/Size Factor
        this.acf = acf;   // Athleticism & Conditioning Factor
        this.ref = ref;   // Relevant Grappling Experience Factor
        this.tff = tff;   // Training Intensity/Frequency Factor
        this.cef = cef;   // BJJ Competition Experience Factor
    }
    
    calculateHandicappedScore() {
        return this.brs * this.af * this.wf * this.acf * this.ref * this.tff * this.cef;
    }
}

export class RollDynamicsProfile {
    constructor({
        dominantTrait,
        likelyApproach,
        keyStrengths,
        keyChallenges,
        controlPotential,
        submissionOffensiveThreat,
        submissionDefensiveResilience,
        practitionerName,
        handicappedScore
    }) {
        this.dominantTrait = dominantTrait;
        this.likelyApproach = likelyApproach;
        this.keyStrengths = keyStrengths;
        this.keyChallenges = keyChallenges;
        this.controlPotential = controlPotential;
        this.submissionOffensiveThreat = submissionOffensiveThreat;
        this.submissionDefensiveResilience = submissionDefensiveResilience;
        this.practitionerName = practitionerName;
        this.handicappedScore = handicappedScore;
    }
}