// Quick test of new scoring system
import { JARCalculator } from './src/js/calculator.js';

const calculator = new JARCalculator();

// Test practitioners
const whiteBelt = {
    name: "White Belt Test",
    bjjBeltRank: "White",
    ageYears: 30,
    weightLbs: 170,
    standardizedFitnessTestPercentileEstimate: 50,
    otherGrapplingArtExperience: [],
    bjjTrainingSessionsPerWeek: 3,
    bjjCompetitionExperienceLevel: "None"
};

const purpleBelt = {
    name: "Purple Belt Test", 
    bjjBeltRank: "Purple",
    ageYears: 35,
    weightLbs: 185,
    standardizedFitnessTestPercentileEstimate: 70,
    otherGrapplingArtExperience: [],
    bjjTrainingSessionsPerWeek: 4,
    bjjCompetitionExperienceLevel: "Regular Regional"
};

const blackBelt = {
    name: "Black Belt Test",
    bjjBeltRank: "Black", 
    ageYears: 45,
    weightLbs: 170,
    standardizedFitnessTestPercentileEstimate: 85,
    otherGrapplingArtExperience: [],
    bjjTrainingSessionsPerWeek: 6,
    bjjCompetitionExperienceLevel: "National/International"
};

const youngAthlete = {
    name: "Young Athlete",
    bjjBeltRank: "Blue",
    ageYears: 20,
    weightLbs: 160,
    standardizedFitnessTestPercentileEstimate: 90,
    otherGrapplingArtExperience: [],
    bjjTrainingSessionsPerWeek: 5,
    bjjCompetitionExperienceLevel: "Limited Local"
};

console.log("=== NEW SCORING SYSTEM TEST ===");

console.log("\nBelt Rank Scores:");
console.log(`White: ${calculator.calculateBRS(whiteBelt)}`);
console.log(`Purple: ${calculator.calculateBRS(purpleBelt)}`);
console.log(`Black: ${calculator.calculateBRS(blackBelt)}`);

console.log("\nAge Factors:");
console.log(`Age 20: ${calculator.calculateAF(youngAthlete).toFixed(3)}`);
console.log(`Age 30: ${calculator.calculateAF(whiteBelt).toFixed(3)}`);
console.log(`Age 35: ${calculator.calculateAF(purpleBelt).toFixed(3)}`);
console.log(`Age 45: ${calculator.calculateAF(blackBelt).toFixed(3)}`);

console.log("\nWeight Factors (15lb difference):");
console.log(`Purple vs White: ${calculator.calculateWF(purpleBelt, whiteBelt).toFixed(3)}`);
console.log(`White vs Purple: ${calculator.calculateWF(whiteBelt, purpleBelt).toFixed(3)}`);

// Test with larger weight difference
const heavyPractitioner = { ...whiteBelt, weightLbs: 230 }; // 60lb difference

console.log("\nWeight Factors (60lb difference):");
console.log(`Heavy vs White: ${calculator.calculateWF(heavyPractitioner, whiteBelt).toFixed(3)}`);
console.log(`White vs Heavy: ${calculator.calculateWF(whiteBelt, heavyPractitioner).toFixed(3)}`);

console.log("\n=== FULL FACTOR COMPARISON ===");
const whiteFactors = calculator.calculateAllFactors(whiteBelt, purpleBelt);
const purpleFactors = calculator.calculateAllFactors(purpleBelt, whiteBelt);
const blackFactors = calculator.calculateAllFactors(blackBelt, whiteBelt);
const youngFactors = calculator.calculateAllFactors(youngAthlete, whiteBelt);

console.log(`\nWhite Belt (Age 30):`);
console.log(`  BRS: ${whiteFactors.brs}, AF: ${whiteFactors.af.toFixed(3)}, WF: ${whiteFactors.wf.toFixed(3)}`);
console.log(`  Handicapped Score: ${whiteFactors.calculateHandicappedScore().toFixed(1)}`);

console.log(`\nPurple Belt (Age 35, +15lbs):`);
console.log(`  BRS: ${purpleFactors.brs}, AF: ${purpleFactors.af.toFixed(3)}, WF: ${purpleFactors.wf.toFixed(3)}`);
console.log(`  Handicapped Score: ${purpleFactors.calculateHandicappedScore().toFixed(1)}`);

console.log(`\nBlack Belt (Age 45):`);
console.log(`  BRS: ${blackFactors.brs}, AF: ${blackFactors.af.toFixed(3)}, WF: ${blackFactors.wf.toFixed(3)}`);
console.log(`  Handicapped Score: ${blackFactors.calculateHandicappedScore().toFixed(1)}`);

console.log(`\nYoung Blue Belt (Age 20, -10lbs, High Fitness):`);
console.log(`  BRS: ${youngFactors.brs}, AF: ${youngFactors.af.toFixed(3)}, WF: ${youngFactors.wf.toFixed(3)}`);
console.log(`  Handicapped Score: ${youngFactors.calculateHandicappedScore().toFixed(1)}`);