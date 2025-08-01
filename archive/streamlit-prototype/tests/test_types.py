import unittest
from jar.types import PractitionerData, FactorResults, RollDynamicsProfile, BeltRank, ActivityLevel

class TestTypes(unittest.TestCase):
    def test_practitioner_data_validation(self):
        """Test PractitionerData validation."""
        # Valid practitioner
        valid_practitioner = PractitionerData(
            name="Test Practitioner",
            bjj_belt_rank="Blue",
            age_years=30,
            weight_lbs=170.0,
            primary_occupation_activity_level="Moderately Active",
            standardized_fitness_test_percentile_estimate=50,
            other_grappling_art_experience=[],
            bjj_training_sessions_per_week=3,
            bjj_competition_experience_level="None"
        )
        
        # Age validation
        with self.assertRaises(ValueError):
            PractitionerData(
                name="Invalid Age",
                bjj_belt_rank="White",
                age_years=10,  # Too young
                weight_lbs=170.0,
                primary_occupation_activity_level="Moderately Active",
                standardized_fitness_test_percentile_estimate=50,
                other_grappling_art_experience=[],
                bjj_training_sessions_per_week=3,
                bjj_competition_experience_level="None"
            )
        
        with self.assertRaises(ValueError):
            PractitionerData(
                name="Invalid Age",
                bjj_belt_rank="White",
                age_years=95,  # Too old
                weight_lbs=170.0,
                primary_occupation_activity_level="Moderately Active",
                standardized_fitness_test_percentile_estimate=50,
                other_grappling_art_experience=[],
                bjj_training_sessions_per_week=3,
                bjj_competition_experience_level="None"
            )
        
        # Weight validation
        with self.assertRaises(ValueError):
            PractitionerData(
                name="Invalid Weight",
                bjj_belt_rank="White",
                age_years=30,
                weight_lbs=70.0,  # Too light
                primary_occupation_activity_level="Moderately Active",
                standardized_fitness_test_percentile_estimate=50,
                other_grappling_art_experience=[],
                bjj_training_sessions_per_week=3,
                bjj_competition_experience_level="None"
            )
        
        # Fitness percentile validation
        with self.assertRaises(ValueError):
            PractitionerData(
                name="Invalid Fitness",
                bjj_belt_rank="White",
                age_years=30,
                weight_lbs=170.0,
                primary_occupation_activity_level="Moderately Active",
                standardized_fitness_test_percentile_estimate=110,  # Over 100
                other_grappling_art_experience=[],
                bjj_training_sessions_per_week=3,
                bjj_competition_experience_level="None"
            )
        
        # Training sessions validation
        with self.assertRaises(ValueError):
            PractitionerData(
                name="Invalid Training",
                bjj_belt_rank="White",
                age_years=30,
                weight_lbs=170.0,
                primary_occupation_activity_level="Moderately Active",
                standardized_fitness_test_percentile_estimate=50,
                other_grappling_art_experience=[],
                bjj_training_sessions_per_week=15,  # Too many
                bjj_competition_experience_level="None"
            )
    
    def test_factor_results_calculate_handicapped_score(self):
        """Test FactorResults handicapped score calculation."""
        # Create factor results with known values
        factors = FactorResults(
            brs=100.0,
            af=1.03,
            wf=0.94,
            acf=1.07,
            ref=1.0,
            tff=1.05,
            cef=1.03
        )
        
        # Calculate expected handicapped score
        expected_hs = 100.0 * 1.03 * 0.94 * 1.07 * 1.0 * 1.05 * 1.03
        
        # Check that the calculated score matches
        self.assertAlmostEqual(factors.calculate_handicapped_score(), expected_hs, places=10)
    
    def test_roll_dynamics_profile(self):
        """Test RollDynamicsProfile creation."""
        # Create a valid profile
        profile = RollDynamicsProfile(
            dominant_trait="Technical BJJ Specialist",
            likely_approach="Technical & Opportunistic",
            key_strengths=["Deep BJJ knowledge", "Technical submissions"],
            key_challenges=["Weight disadvantage", "Age limitations"],
            control_potential="Medium",
            submission_offensive_threat="High",
            submission_defensive_resilience="High",
            practitioner_name="Test Practitioner",
            handicapped_score=350.0
        )
        
        # Check that fields are accessible
        self.assertEqual(profile.dominant_trait, "Technical BJJ Specialist")
        self.assertEqual(profile.likely_approach, "Technical & Opportunistic")
        self.assertEqual(len(profile.key_strengths), 2)
        self.assertEqual(profile.control_potential, "Medium")
        self.assertEqual(profile.handicapped_score, 350.0)


if __name__ == "__main__":
    unittest.main()