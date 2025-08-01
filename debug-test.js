// Debug test for specific calibration issue
import { JARCalculator } from './src/js/calculator.js';
import { PractitionerData, BeltRanks, ActivityLevels, CompetitionLevels, GrapplingArts, ExperienceLevels } from './src/js/types.js';

const calculator = new JARCalculator();

// Olympic wrestler (should score very high)
const olympicWrestler = new PractitionerData({
    name: 'Olympic Wrestler',
    bjjBeltRank: BeltRanks.WHITE, // New to BJJ
    ageYears: 28,
    weightLbs: 200,
    primaryOccupationActivityLevel: ActivityLevels.PHYSICALLY_DEMANDING,
    standardizedFitnessTestPercentileEstimate: 99, // Elite athlete
    otherGrapplingArtExperience: [{
        artName: GrapplingArts.WRESTLING,
        experienceLevel: ExperienceLevels.ELITE // Olympic level
    }],
    bjjTrainingSessionsPerWeek: 6,
    bjjCompetitionExperienceLevel: CompetitionLevels.NONE // New to BJJ
});

// 45-year-old purple belt (experienced BJJ)
const purpleBelt = new PractitionerData({
    name: '45yr Purple Belt',
    bjjBeltRank: BeltRanks.PURPLE,
    ageYears: 45,
    weightLbs: 180,
    primaryOccupationActivityLevel: ActivityLevels.MODERATELY_ACTIVE,
    standardizedFitnessTestPercentileEstimate: 60, // Above average
    otherGrapplingArtExperience: [{
        artName: GrapplingArts.NONE,
        experienceLevel: ExperienceLevels.NONE
    }],
    bjjTrainingSessionsPerWeek: 3,
    bjjCompetitionExperienceLevel: CompetitionLevels.LIMITED_LOCAL
});

console.log('=== CALIBRATION DEBUG TEST ===\n');

// Calculate factors for Olympic wrestler
const wrestlerFactors = calculator.calculateAllFactors(olympicWrestler, purpleBelt);
const wrestlerScore = wrestlerFactors.calculateHandicappedScore();

console.log('Olympic Wrestler:');
console.log(`  BRS: ${wrestlerFactors.brs} (White belt = 100)`);
console.log(`  AF: ${wrestlerFactors.af.toFixed(3)} (Age 28)`);
console.log(`  WF: ${wrestlerFactors.wf.toFixed(3)} (200 vs 180 lbs)`);
console.log(`  ACF: ${wrestlerFactors.acf.toFixed(3)} (99th percentile fitness)`);
console.log(`  REF: ${wrestlerFactors.ref.toFixed(3)} (Olympic wrestling)`);
console.log(`  TFF: ${wrestlerFactors.tff.toFixed(3)} (6 sessions/week)`);
console.log(`  CEF: ${wrestlerFactors.cef.toFixed(3)} (No BJJ comps)`);
console.log(`  TOTAL SCORE: ${wrestlerScore.toFixed(1)}\n`);

// Calculate factors for purple belt
const purpleFactors = calculator.calculateAllFactors(purpleBelt, olympicWrestler);
const purpleScore = purpleFactors.calculateHandicappedScore();

console.log('45yr Purple Belt:');
console.log(`  BRS: ${purpleFactors.brs} (Purple belt = 350)`);
console.log(`  AF: ${purpleFactors.af.toFixed(3)} (Age 45)`);
console.log(`  WF: ${purpleFactors.wf.toFixed(3)} (180 vs 200 lbs)`);
console.log(`  ACF: ${purpleFactors.acf.toFixed(3)} (60th percentile fitness)`);
console.log(`  REF: ${purpleFactors.ref.toFixed(3)} (No other experience)`);
console.log(`  TFF: ${purpleFactors.tff.toFixed(3)} (3 sessions/week)`);
console.log(`  CEF: ${purpleFactors.cef.toFixed(3)} (Limited local comps)`);
console.log(`  TOTAL SCORE: ${purpleScore.toFixed(1)}\n`);

console.log('=== ANALYSIS ===');
console.log(`Wrestling advantage: ${(wrestlerScore / purpleScore).toFixed(2)}x`);

// Let's check the config values
console.log('\n=== CONFIG CHECK ===');
const config = calculator.config;
console.log('REF levels:', config.ref_config.levels);
console.log('Olympic wrestling mapping:', config.ref_config.art_experience_level_mapping['Wrestling_Elite International (Olympic/World level)']);

// Check what REF level the wrestler should get
const wrestlerExperience = olympicWrestler.otherGrapplingArtExperience[0];
const mappingKey = `${wrestlerExperience.artName}_${wrestlerExperience.experienceLevel}`;
console.log(`\nWrestler mapping key: "${mappingKey}"`);
console.log('Mapped level_id:', config.ref_config.art_experience_level_mapping[mappingKey]);

// Find the actual multiplier for level 5
const level5 = config.ref_config.levels.find(level => level.level_id === 5);
console.log('Level 5 details:', level5);

// Manual REF calculation check
console.log('\n=== MANUAL REF CALCULATION ===');
const refResult = calculator.calculateREF(olympicWrestler);
console.log('REF calculation result:', refResult);

// Check all available mapping keys
console.log('\n=== AVAILABLE MAPPING KEYS ===');
Object.keys(config.ref_config.art_experience_level_mapping).forEach(key => {
    if (key.includes('Wrestling')) {
        console.log(`"${key}" -> ${config.ref_config.art_experience_level_mapping[key]}`);
    }
});