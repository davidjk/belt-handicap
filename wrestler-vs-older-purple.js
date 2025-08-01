// Test: Young wrestler vs older purple belt
import { JARCalculator } from './src/js/calculator.js';

const calculator = new JARCalculator();

// 25-year-old college wrestler (White belt)
const youngWrestler = {
    name: "Young College Wrestler",
    bjjBeltRank: "White",
    ageYears: 25,
    weightLbs: 190,
    standardizedFitnessTestPercentileEstimate: 80, // Good fitness for age
    otherGrapplingArtExperience: [
        {
            artName: "Wrestling",
            experienceLevel: "College D1"
        }
    ],
    bjjTrainingSessionsPerWeek: 3,
    bjjCompetitionExperienceLevel: "None"
};

// 46-year-old Purple belt (no other experience)
const olderPurple = {
    name: "Older Purple Belt",
    bjjBeltRank: "Purple", 
    ageYears: 46,
    weightLbs: 180,
    standardizedFitnessTestPercentileEstimate: 75, // Good fitness for his age
    otherGrapplingArtExperience: [],
    bjjTrainingSessionsPerWeek: 4,
    bjjCompetitionExperienceLevel: "Limited Local"
};

console.log("=== WRESTLER VS OLDER PURPLE COMPARISON ===");

// Calculate factors for each
const wrestlerFactors = calculator.calculateAllFactors(youngWrestler, olderPurple);
const purpleFactors = calculator.calculateAllFactors(olderPurple, youngWrestler);

console.log("\n25-year-old College Wrestler (White Belt, 190lbs):");
console.log(`  BRS: ${wrestlerFactors.brs}`);
console.log(`  AF (Age 25): ${wrestlerFactors.af.toFixed(3)}`);
console.log(`  WF (10lbs heavier): ${wrestlerFactors.wf.toFixed(3)}`);
console.log(`  ACF (80th percentile): ${wrestlerFactors.acf.toFixed(3)}`);
console.log(`  REF (College D1 Wrestling): ${wrestlerFactors.ref.toFixed(3)}`);
console.log(`  TFF (3 sessions/week): ${wrestlerFactors.tff.toFixed(3)}`);
console.log(`  CEF (No competition): ${wrestlerFactors.cef.toFixed(3)}`);
console.log(`  HANDICAPPED SCORE: ${wrestlerFactors.calculateHandicappedScore().toFixed(1)}`);

console.log("\n46-year-old Purple Belt (180lbs, no other experience):");
console.log(`  BRS: ${purpleFactors.brs}`);
console.log(`  AF (Age 46): ${purpleFactors.af.toFixed(3)}`);
console.log(`  WF (10lbs lighter): ${purpleFactors.wf.toFixed(3)}`);
console.log(`  ACF (75th percentile): ${purpleFactors.acf.toFixed(3)}`);
console.log(`  REF (No other experience): ${purpleFactors.ref.toFixed(3)}`);
console.log(`  TFF (4 sessions/week): ${purpleFactors.tff.toFixed(3)}`);
console.log(`  CEF (Limited Local): ${purpleFactors.cef.toFixed(3)}`);
console.log(`  HANDICAPPED SCORE: ${purpleFactors.calculateHandicappedScore().toFixed(1)}`);

console.log(`\n=== SCORE DIFFERENCE ===`);
const scoreDiff = wrestlerFactors.calculateHandicappedScore() - purpleFactors.calculateHandicappedScore();
console.log(`Wrestler score - Purple score: ${scoreDiff.toFixed(1)}`);

if (scoreDiff > 0) {
    console.log("The young wrestler scores HIGHER despite being a white belt");
} else if (scoreDiff < 0) {
    console.log("The older purple belt scores HIGHER despite age disadvantage");
} else {
    console.log("The scores are essentially equal");
}