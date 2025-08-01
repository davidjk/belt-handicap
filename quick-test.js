// Quick test to verify JavaScript modules are working
import { JARCalculator } from './src/js/calculator.js';
import { PractitionerData, BeltRanks } from './src/js/types.js';
import { ProfileGenerator } from './src/js/profiles.js';

console.log('Testing JavaScript modules...');

try {
    const calculator = new JARCalculator();
    const profileGenerator = new ProfileGenerator(calculator.config);
    
    const testPractitioner = new PractitionerData({
        name: 'Test',
        bjjBeltRank: BeltRanks.WHITE,
        ageYears: 25,
        weightLbs: 170
    });
    
    console.log('✅ Modules loaded successfully');
    console.log('✅ Calculator created');
    console.log('✅ Profile generator created');
    console.log('✅ Test practitioner created:', testPractitioner.name);
    
} catch (error) {
    console.error('❌ Error loading modules:', error);
}