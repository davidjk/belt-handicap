import unittest
from jar.types import PractitionerData, FactorResults
from jar.config import JARConfig
from jar.calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        # Create a minimal test configuration
        self.config: JARConfig = {
            "belt_rank_scores": {
                "White": 100,
                "Blue": 200,
                "Purple": 350,
                "Brown": 550,
                "Black": 800
            },
            "age_factor_config": {
                "peak_age_years": 25,
                "youthful_factor_multiplier": 1.03,
                "power_decline_rate_per_decade": 0.12
            },
            "weight_factor_config": {
                "increment_lbs": 15.0,
                "thresholds_bonuses_penalties": [
                    {"diff_max_lbs": 15.0, "adjustment": 0.06},
                    {"diff_max_lbs": 30.0, "adjustment": 0.08},
                    {"diff_max_lbs": 45.0, "adjustment": 0.10}
                ]
            },
            "acf_config": {
                "levels": [
                    {"level_id": 1, "description": "Below Average", "multiplier": 0.90},
                    {"level_id": 2, "description": "Average", "multiplier": 1.00},
                    {"level_id": 3, "description": "Above Average", "multiplier": 1.07},
                    {"level_id": 4, "description": "Notably Athletic", "multiplier": 1.15},
                    {"level_id": 5, "description": "Exceptional", "multiplier": 1.25}
                ]
            },
            "ref_config": {
                "levels": [
                    {"level_id": 0, "description": "None", "multiplier": 1.0},
                    {"level_id": 1, "description": "Limited", "multiplier": 1.03},
                    {"level_id": 2, "description": "Foundational", "multiplier": 1.07},
                    {"level_id": 3, "description": "Accomplished", "multiplier": 1.12},
                    {"level_id": 4, "description": "High-Level", "multiplier": 1.22},
                    {"level_id": 5, "description": "Elite", "multiplier": 1.38}
                ],
                "art_experience_level_mapping": {
                    "Wrestling_High-Level Competitor (National level)": 4,
                    "Judo_Accomplished (3-5+ years, regional level)": 3
                }
            },
            "tff_config": {
                "levels": [
                    {"sessions_min": 0, "sessions_max": 1, "multiplier": 0.95},
                    {"sessions_min": 2, "sessions_max": 3, "multiplier": 1.00},
                    {"sessions_min": 4, "sessions_max": 5, "multiplier": 1.05},
                    {"sessions_min": 6, "sessions_max": 100, "multiplier": 1.10}
                ]
            },
            "cef_config": {
                "levels": [
                    {"level_id": 0, "description": "None", "multiplier": 1.0},
                    {"level_id": 1, "description": "Limited Local", "multiplier": 1.03},
                    {"level_id": 2, "description": "Regular Regional", "multiplier": 1.08},
                    {"level_id": 3, "description": "National/International", "multiplier": 1.12}
                ],
                "competition_level_mapping": {
                    "None": 0,
                    "Limited Local": 1,
                    "Regular Regional": 2,
                    "National/International": 3
                }
            },
            "profile_dynamics_config": {
                "significant_multiplier_threshold_high": 1.10,
                "significant_multiplier_threshold_low": 0.90,
                "implication_statements": {},
                "control_implication_factors": [],
                "submission_implication_factors_offense": [],
                "submission_implication_factors_defense": []
            }
        }
        
        self.calculator = Calculator(self.config)
        
        # Create test practitioners
        self.white_belt = PractitionerData(
            name="Test White Belt",
            bjj_belt_rank="White",
            age_years=30,
            weight_lbs=170,
            primary_occupation_activity_level="Sedentary (Desk Job)",
            standardized_fitness_test_percentile_estimate=50,
            other_grappling_art_experience=[],
            bjj_training_sessions_per_week=2,
            bjj_competition_experience_level="None"
        )
        
        self.blue_belt = PractitionerData(
            name="Test Blue Belt",
            bjj_belt_rank="Blue",
            age_years=25,
            weight_lbs=170,
            primary_occupation_activity_level="Moderately Active",
            standardized_fitness_test_percentile_estimate=60,
            other_grappling_art_experience=[],
            bjj_training_sessions_per_week=3,
            bjj_competition_experience_level="Limited Local"
        )
        
        self.purple_belt = PractitionerData(
            name="Test Purple Belt",
            bjj_belt_rank="Purple",
            age_years=35,
            weight_lbs=185,
            primary_occupation_activity_level="Moderately Active",
            standardized_fitness_test_percentile_estimate=70,
            other_grappling_art_experience=[
                {
                    "art_name": "Wrestling",
                    "experience_level_descriptor": "High-Level Competitor (National level)"
                }
            ],
            bjj_training_sessions_per_week=4,
            bjj_competition_experience_level="Regular Regional"
        )
        
        self.black_belt = PractitionerData(
            name="Test Black Belt",
            bjj_belt_rank="Black",
            age_years=45,
            weight_lbs=170,
            primary_occupation_activity_level="Physically Demanding",
            standardized_fitness_test_percentile_estimate=85,
            other_grappling_art_experience=[
                {
                    "art_name": "Judo",
                    "experience_level_descriptor": "Accomplished (3-5+ years, regional level)"
                }
            ],
            bjj_training_sessions_per_week=6,
            bjj_competition_experience_level="National/International"
        )
    
    def test_calculate_brs(self):
        """Test Belt Rank Score calculation."""
        self.assertEqual(self.calculator.calculate_brs(self.white_belt), 100)
        self.assertEqual(self.calculator.calculate_brs(self.blue_belt), 200)
        self.assertEqual(self.calculator.calculate_brs(self.purple_belt), 350)
        self.assertEqual(self.calculator.calculate_brs(self.black_belt), 800)
    
    def test_calculate_af(self):
        """Test Age Factor calculation."""
        # Test at peak age
        self.assertEqual(self.calculator.calculate_af(self.blue_belt), 1.0)
        
        # Test below peak age
        young_practitioner = PractitionerData(
            name="Young Practitioner",
            bjj_belt_rank="White",
            age_years=20,
            weight_lbs=170,
            primary_occupation_activity_level="Moderately Active",
            standardized_fitness_test_percentile_estimate=50,
            other_grappling_art_experience=[],
            bjj_training_sessions_per_week=3,
            bjj_competition_experience_level="None"
        )
        self.assertEqual(self.calculator.calculate_af(young_practitioner), 1.03)
        
        # Test above peak age
        # For age 35, decades_past_peak = (35 - 25) / 10 = 1
        # AF = (1.0 - 0.12) ^ 1 = 0.88
        self.assertAlmostEqual(self.calculator.calculate_af(self.purple_belt), 0.88, places=2)
        
        # Test older age
        # For age 45, decades_past_peak = (45 - 25) / 10 = 2
        # AF = (1.0 - 0.12) ^ 2 = 0.7744
        self.assertAlmostEqual(self.calculator.calculate_af(self.black_belt), 0.7744, places=4)
    
    def test_calculate_wf(self):
        """Test Weight Factor calculation."""
        # Test case where both practitioners are the same weight
        self.assertEqual(self.calculator.calculate_wf(self.white_belt, self.blue_belt), 1.0)
        
        # Test case with a weight difference
        # Weight difference: 185 - 170 = 15 lbs
        # From tier 1: 15/15 * 0.06 = 0.06
        # Purple belt is heavier, so WF = 1.0 + 0.06 = 1.06
        # White belt is lighter, so WF = 1.0 - 0.06 = 0.94
        self.assertAlmostEqual(
            self.calculator.calculate_wf(self.purple_belt, self.white_belt), 
            1.06, 
            places=2
        )
        self.assertAlmostEqual(
            self.calculator.calculate_wf(self.white_belt, self.purple_belt), 
            0.94, 
            places=2
        )
        
        # Test case with a larger weight difference
        very_heavy_practitioner = PractitionerData(
            name="Heavy Practitioner",
            bjj_belt_rank="Blue",
            age_years=30,
            weight_lbs=230,  # 230 - 170 = 60 lbs difference
            primary_occupation_activity_level="Moderately Active",
            standardized_fitness_test_percentile_estimate=60,
            other_grappling_art_experience=[],
            bjj_training_sessions_per_week=3,
            bjj_competition_experience_level="None"
        )
        
        # 60 lbs difference would use multiple tiers:
        # Tier 1: 15 lbs -> 15/15 * 0.06 = 0.06
        # Tier 2: 15 lbs -> 15/15 * 0.08 = 0.08
        # Tier 3: 15 lbs -> 15/15 * 0.10 = 0.10
        # Remainder: 15 lbs -> 15/15 * 0.10 = 0.10 (using last tier for remainder)
        # Total: 0.06 + 0.08 + 0.10 + 0.10 = 0.34
        self.assertAlmostEqual(
            self.calculator.calculate_wf(very_heavy_practitioner, self.white_belt), 
            1.34, 
            places=2
        )
        self.assertAlmostEqual(
            self.calculator.calculate_wf(self.white_belt, very_heavy_practitioner), 
            0.66, 
            places=2
        )
        
        # Test with no comparison practitioner
        self.assertEqual(self.calculator.calculate_wf(self.white_belt, None), 1.0)
    
    def test_calculate_acf(self):
        """Test Athleticism & Conditioning Factor calculation."""
        # Test different fitness percentiles
        low_fitness = PractitionerData(
            name="Low Fitness",
            bjj_belt_rank="White",
            age_years=30,
            weight_lbs=170,
            primary_occupation_activity_level="Sedentary (Desk Job)",
            standardized_fitness_test_percentile_estimate=25,  # Below Average
            other_grappling_art_experience=[],
            bjj_training_sessions_per_week=2,
            bjj_competition_experience_level="None"
        )
        self.assertEqual(self.calculator.calculate_acf(low_fitness), 0.90)
        
        # Average fitness
        self.assertEqual(self.calculator.calculate_acf(self.white_belt), 1.00)
        
        # Above average fitness
        self.assertEqual(self.calculator.calculate_acf(self.purple_belt), 1.07)
        
        # High fitness
        self.assertEqual(self.calculator.calculate_acf(self.black_belt), 1.15)
        
        # Exceptional fitness
        exceptional_fitness = PractitionerData(
            name="Exceptional Fitness",
            bjj_belt_rank="Purple",
            age_years=28,
            weight_lbs=175,
            primary_occupation_activity_level="Physically Demanding",
            standardized_fitness_test_percentile_estimate=98,  # Exceptional
            other_grappling_art_experience=[],
            bjj_training_sessions_per_week=5,
            bjj_competition_experience_level="Regular Regional"
        )
        self.assertEqual(self.calculator.calculate_acf(exceptional_fitness), 1.25)
    
    def test_calculate_ref(self):
        """Test Relevant Grappling Experience Factor calculation."""
        # No other grappling experience
        self.assertEqual(self.calculator.calculate_ref(self.white_belt), 1.0)
        
        # High-level wrestling experience
        self.assertEqual(self.calculator.calculate_ref(self.purple_belt), 1.22)
        
        # Accomplished Judo experience
        self.assertEqual(self.calculator.calculate_ref(self.black_belt), 1.12)
        
        # Test with unmapped experience (should default to level 0)
        unmapped_experience = PractitionerData(
            name="Unmapped Experience",
            bjj_belt_rank="Blue",
            age_years=30,
            weight_lbs=170,
            primary_occupation_activity_level="Moderately Active",
            standardized_fitness_test_percentile_estimate=60,
            other_grappling_art_experience=[
                {
                    "art_name": "Sambo",  # Not in our mapping
                    "experience_level_descriptor": "Foundational (1-3 years)"
                }
            ],
            bjj_training_sessions_per_week=3,
            bjj_competition_experience_level="None"
        )
        self.assertEqual(self.calculator.calculate_ref(unmapped_experience), 1.0)
    
    def test_calculate_tff(self):
        """Test Training Intensity/Frequency Factor calculation."""
        # 0-1 sessions per week
        low_frequency = PractitionerData(
            name="Low Frequency",
            bjj_belt_rank="White",
            age_years=30,
            weight_lbs=170,
            primary_occupation_activity_level="Sedentary (Desk Job)",
            standardized_fitness_test_percentile_estimate=50,
            other_grappling_art_experience=[],
            bjj_training_sessions_per_week=1,
            bjj_competition_experience_level="None"
        )
        self.assertEqual(self.calculator.calculate_tff(low_frequency), 0.95)
        
        # 2-3 sessions per week
        self.assertEqual(self.calculator.calculate_tff(self.white_belt), 1.00)
        self.assertEqual(self.calculator.calculate_tff(self.blue_belt), 1.00)
        
        # 4-5 sessions per week
        self.assertEqual(self.calculator.calculate_tff(self.purple_belt), 1.05)
        
        # 6+ sessions per week
        self.assertEqual(self.calculator.calculate_tff(self.black_belt), 1.10)
    
    def test_calculate_cef(self):
        """Test BJJ Competition Experience Factor calculation."""
        # No competition experience
        self.assertEqual(self.calculator.calculate_cef(self.white_belt), 1.0)
        
        # Limited Local
        self.assertEqual(self.calculator.calculate_cef(self.blue_belt), 1.03)
        
        # Regular Regional
        self.assertEqual(self.calculator.calculate_cef(self.purple_belt), 1.08)
        
        # National/International
        self.assertEqual(self.calculator.calculate_cef(self.black_belt), 1.12)
    
    def test_calculate_all_factors(self):
        """Test calculation of all factors together."""
        factors = self.calculator.calculate_all_factors(self.purple_belt, self.white_belt)
        
        # Verify each factor
        self.assertEqual(factors.brs, 350)
        self.assertAlmostEqual(factors.af, 0.88, places=2)
        self.assertAlmostEqual(factors.wf, 1.06, places=2)
        self.assertEqual(factors.acf, 1.07)
        self.assertEqual(factors.ref, 1.22)
        self.assertEqual(factors.tff, 1.05)
        self.assertEqual(factors.cef, 1.08)
        
        # Verify Handicapped Score calculation
        expected_hs = 350 * 0.88 * 1.06 * 1.07 * 1.22 * 1.05 * 1.08
        self.assertAlmostEqual(factors.calculate_handicapped_score(), expected_hs, places=2)
        
        # Test with no comparison practitioner (WF should be 1.0)
        solo_factors = self.calculator.calculate_all_factors(self.purple_belt)
        self.assertEqual(solo_factors.wf, 1.0)


if __name__ == "__main__":
    unittest.main()