import unittest
from jar.types import PractitionerData, FactorResults, RollDynamicsProfile
from jar.config import JARConfig
from jar.profiles import ProfileGenerator

class TestProfileGenerator(unittest.TestCase):
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
                "implication_statements": {
                    "BRS_high": "Deep BJJ-specific technical knowledge, extensive submission arsenal.",
                    "BRS_low": "Limited BJJ-specific submission knowledge and positional play.",
                    "REF_high_wrestling_judo": "Strong foundational grappling from another discipline.",
                    "ACF_high": "Significant athletic advantage.",
                    "WF_high": "Substantial size/weight advantage.",
                    "AF_low": "Age-related physical limitations.",
                    "WF_low": "Size/weight disadvantage."
                },
                "control_implication_factors": ["REF_high_wrestling_judo", "ACF_high", "WF_high"],
                "submission_implication_factors_offense": ["BRS_high"],
                "submission_implication_factors_defense": ["BRS_high"]
            }
        }
        
        self.profile_generator = ProfileGenerator(self.config)
        
        # Define test practitioners
        self.white_belt_practitioner = PractitionerData(
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
        
        self.black_belt_athletic_practitioner = PractitionerData(
            name="Test Black Belt",
            bjj_belt_rank="Black",
            age_years=32,
            weight_lbs=200,
            primary_occupation_activity_level="Physically Demanding",
            standardized_fitness_test_percentile_estimate=90,
            other_grappling_art_experience=[
                {
                    "art_name": "Wrestling",
                    "experience_level_descriptor": "High-Level Competitor (National level)"
                }
            ],
            bjj_training_sessions_per_week=6,
            bjj_competition_experience_level="National/International"
        )
        
        self.older_purple_belt_practitioner = PractitionerData(
            name="Test Older Purple Belt",
            bjj_belt_rank="Purple",
            age_years=45,
            weight_lbs=160,
            primary_occupation_activity_level="Moderately Active",
            standardized_fitness_test_percentile_estimate=60,
            other_grappling_art_experience=[],
            bjj_training_sessions_per_week=3,
            bjj_competition_experience_level="Regular Regional"
        )
        
        # Create mock factor results
        self.white_belt_factors = FactorResults(
            brs=100,
            af=1.0,
            wf=0.85,
            acf=1.0,
            ref=1.0,
            tff=1.0,
            cef=1.0
        )
        
        self.dominant_black_belt_factors = FactorResults(
            brs=800,
            af=0.95,
            wf=1.15,
            acf=1.15,
            ref=1.22,
            tff=1.10,
            cef=1.12
        )
        
        self.older_purple_belt_factors = FactorResults(
            brs=350,
            af=0.78,
            wf=0.90,
            acf=1.07,
            ref=1.0,
            tff=1.0,
            cef=1.08
        )
    
    def test_identify_significant_factors(self):
        """Test identification of significant factors."""
        # Test white belt with weight disadvantage
        white_belt_significance = self.profile_generator.identify_significant_factors(self.white_belt_factors)
        
        self.assertEqual(white_belt_significance["brs"], "low")  # Low belt rank
        self.assertEqual(white_belt_significance["af"], "neutral")  # Neutral age
        self.assertEqual(white_belt_significance["wf"], "low")  # Weight disadvantage
        
        # Test dominant black belt
        black_belt_significance = self.profile_generator.identify_significant_factors(self.dominant_black_belt_factors)
        
        self.assertEqual(black_belt_significance["brs"], "high")  # High belt rank
        self.assertEqual(black_belt_significance["wf"], "high")  # Weight advantage
        self.assertEqual(black_belt_significance["acf"], "high")  # Athletic advantage
        self.assertEqual(black_belt_significance["ref"], "high")  # Wrestling background
        
        # Test older purple belt
        purple_belt_significance = self.profile_generator.identify_significant_factors(self.older_purple_belt_factors)
        
        self.assertEqual(purple_belt_significance["brs"], "high")  # High belt rank
        self.assertEqual(purple_belt_significance["af"], "low")  # Age disadvantage
        self.assertEqual(purple_belt_significance["wf"], "low")  # Weight disadvantage
    
    def test_determine_dominant_trait(self):
        """Test determination of dominant trait."""
        # White belt with no significant advantages
        white_belt_significance = self.profile_generator.identify_significant_factors(self.white_belt_factors)
        white_belt_trait = self.profile_generator.determine_dominant_trait(white_belt_significance)
        
        # Black belt with multiple advantages
        black_belt_significance = self.profile_generator.identify_significant_factors(self.dominant_black_belt_factors)
        black_belt_trait = self.profile_generator.determine_dominant_trait(black_belt_significance)
        
        # Purple belt with technical skill but physical disadvantages
        purple_belt_significance = self.profile_generator.identify_significant_factors(self.older_purple_belt_factors)
        purple_belt_trait = self.profile_generator.determine_dominant_trait(purple_belt_significance)
        
        # Check expected traits
        self.assertEqual(black_belt_trait, "Dominant All-Rounder")
        self.assertTrue("Technical" in purple_belt_trait or "Balanced" in purple_belt_trait)
    
    def test_determine_control_potential(self):
        """Test determination of control potential rating."""
        # White belt should have low control potential
        white_belt_significance = self.profile_generator.identify_significant_factors(self.white_belt_factors)
        self.assertEqual(
            self.profile_generator.determine_control_potential(white_belt_significance),
            "Low"
        )
        
        # Black belt with multiple physical advantages should have high control
        black_belt_significance = self.profile_generator.identify_significant_factors(self.dominant_black_belt_factors)
        self.assertEqual(
            self.profile_generator.determine_control_potential(black_belt_significance),
            "High"
        )
    
    def test_determine_submission_threat(self):
        """Test determination of submission threat rating."""
        # White belt should have low submission threat
        white_belt_significance = self.profile_generator.identify_significant_factors(self.white_belt_factors)
        self.assertEqual(
            self.profile_generator.determine_submission_threat(white_belt_significance),
            "Low"
        )
        
        # Black belt should have high submission threat
        black_belt_significance = self.profile_generator.identify_significant_factors(self.dominant_black_belt_factors)
        self.assertEqual(
            self.profile_generator.determine_submission_threat(black_belt_significance),
            "High"
        )
        
        # Purple belt should have medium or high submission threat
        purple_belt_significance = self.profile_generator.identify_significant_factors(self.older_purple_belt_factors)
        submission_threat = self.profile_generator.determine_submission_threat(purple_belt_significance)
        self.assertIn(submission_threat, ["Medium", "High"])
    
    def test_generate_key_strengths(self):
        """Test generation of key strengths."""
        # Black belt with multiple advantages
        black_belt_significance = self.profile_generator.identify_significant_factors(self.dominant_black_belt_factors)
        strengths = self.profile_generator.generate_key_strengths(black_belt_significance)
        
        # Should include multiple strengths
        self.assertGreater(len(strengths), 2)
        
        # Should include specific statements for high factors
        brs_statement = self.config["profile_dynamics_config"]["implication_statements"]["BRS_high"]
        self.assertIn(brs_statement, strengths)
        
        wrestling_statement = self.config["profile_dynamics_config"]["implication_statements"]["REF_high_wrestling_judo"]
        self.assertIn(wrestling_statement, strengths)
    
    def test_generate_key_challenges(self):
        """Test generation of key challenges."""
        # Older purple belt with weight and age disadvantages
        purple_belt_significance = self.profile_generator.identify_significant_factors(self.older_purple_belt_factors)
        challenges = self.profile_generator.generate_key_challenges(purple_belt_significance)
        
        # Should include specific statements for low factors
        age_statement = self.config["profile_dynamics_config"]["implication_statements"]["AF_low"]
        self.assertIn(age_statement, challenges)
        
        weight_statement = self.config["profile_dynamics_config"]["implication_statements"]["WF_low"]
        self.assertIn(weight_statement, challenges)
    
    def test_generate_profile(self):
        """Test generation of complete profile."""
        # Generate profile for black belt
        profile = self.profile_generator.generate_profile(
            self.black_belt_athletic_practitioner,
            self.dominant_black_belt_factors,
            1500.0  # Arbitrary HS for testing
        )
        
        # Validate profile structure
        self.assertIsInstance(profile, RollDynamicsProfile)
        self.assertEqual(profile.handicapped_score, 1500.0)
        self.assertEqual(profile.practitioner_name, "Test Black Belt")
        
        # Profile should have dominant trait, approach, etc.
        self.assertGreater(len(profile.dominant_trait), 0)
        self.assertGreater(len(profile.likely_approach), 0)
        self.assertGreater(len(profile.key_strengths), 0)
        
        # High-level black belt should have high ratings
        self.assertEqual(profile.submission_offensive_threat, "High")
        self.assertEqual(profile.submission_defensive_resilience, "High")
        
        # Generate profile for white belt
        white_profile = self.profile_generator.generate_profile(
            self.white_belt_practitioner,
            self.white_belt_factors,
            85.0  # Arbitrary HS for testing
        )
        
        # Beginner should have low ratings
        self.assertEqual(white_profile.submission_offensive_threat, "Low")


if __name__ == "__main__":
    unittest.main()