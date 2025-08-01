// Test script to verify JavaScript calculations match Python implementation
import { JARCalculator } from './src/js/calculator.js';
import { PractitionerData, BeltRanks, ActivityLevels, CompetitionLevels } from './src/js/types.js';

// Create test calculator
const calculator = new JARCalculator();

// Test practitioner data - matches expected values from Python implementation
const testPractitioner = new PractitionerData({
    name: 'Test Practitioner',
    bjjBeltRank: BeltRanks.PURPLE,
    ageYears: 28,
    weightLbs: 180,
    primaryOccupationActivityLevel: ActivityLevels.MODERATELY_ACTIVE,
    standardizedFitnessTestPercentileEstimate: 75,
    otherGrapplingArtExperience: [],
    bjjTrainingSessionsPerWeek: 4,
    bjjCompetitionExperienceLevel: CompetitionLevels.LIMITED_LOCAL
});

console.log('Testing JAR Calculator Implementation...\n');

// Test individual factors
const factors = calculator.calculateAllFactors(testPractitioner);

console.log('Factor Results:');
console.log(`BRS (Belt Rank Score): ${factors.brs}`);
console.log(`AF (Age Factor): ${factors.af.toFixed(6)}`);
console.log(`WF (Weight Factor): ${factors.wf.toFixed(6)}`);
console.log(`ACF (Athleticism Factor): ${factors.acf.toFixed(6)}`);
console.log(`REF (Experience Factor): ${factors.ref.toFixed(6)}`);
console.log(`TFF (Training Factor): ${factors.tff.toFixed(6)}`);
console.log(`CEF (Competition Factor): ${factors.cef.toFixed(6)}`);

const handicappedScore = factors.calculateHandicappedScore();
console.log(`\nHandicapped Score: ${handicappedScore.toFixed(2)}`);

// Expected values based on the configuration:
// BRS: 350 (Purple belt)
// AF: 0.976704 (28 years old, past peak of 25)
// WF: 1.0 (no comparison practitioner)
// ACF: 1.07 (75th percentile)
// REF: 1.0 (no other experience)
// TFF: 1.05 (4 sessions per week)
// CEF: 1.03 (Limited Local competition)

const expectedBRS = 350;
const expectedAF = Math.pow(1.0 - 0.12, (28 - 25) / 10.0); // ~0.976704
const expectedWF = 1.0;
const expectedACF = 1.07;
const expectedREF = 1.0;
const expectedTFF = 1.05;
const expectedCEF = 1.03;

console.log('\n--- Verification ---');
console.log(`BRS matches expected (${expectedBRS}): ${factors.brs === expectedBRS}`);
console.log(`AF matches expected (${expectedAF.toFixed(6)}): ${Math.abs(factors.af - expectedAF) < 0.000001}`);
console.log(`WF matches expected (${expectedWF}): ${factors.wf === expectedWF}`);
console.log(`ACF matches expected (${expectedACF}): ${factors.acf === expectedACF}`);
console.log(`REF matches expected (${expectedREF}): ${factors.ref === expectedREF}`);
console.log(`TFF matches expected (${expectedTFF}): ${factors.tff === expectedTFF}`);
console.log(`CEF matches expected (${expectedCEF}): ${factors.cef === expectedCEF}`);

const expectedHS = expectedBRS * expectedAF * expectedWF * expectedACF * expectedREF * expectedTFF * expectedCEF;
console.log(`\nExpected Handicapped Score: ${expectedHS.toFixed(2)}`);
console.log(`Calculated Handicapped Score: ${handicappedScore.toFixed(2)}`);
console.log(`Handicapped Score matches: ${Math.abs(handicappedScore - expectedHS) < 0.01}`);

console.log('\n✅ JavaScript implementation verification complete!');