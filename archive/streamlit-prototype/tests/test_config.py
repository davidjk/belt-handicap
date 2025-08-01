import unittest
import os
import tempfile
import json
from jar.config import load_config, validate_config, save_config, JARConfig

class TestConfig(unittest.TestCase):
    def setUp(self):
        # Create a valid minimal configuration
        self.valid_config = {
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
                    {"diff_max_lbs": 15.0, "adjustment": 0.06}
                ]
            },
            "acf_config": {
                "levels": [
                    {"level_id": 1, "description": "Below Average", "multiplier": 0.90},
                    {"level_id": 2, "description": "Average", "multiplier": 1.00}
                ]
            },
            "ref_config": {
                "levels": [
                    {"level_id": 0, "description": "None", "multiplier": 1.0}
                ],
                "art_experience_level_mapping": {}
            },
            "tff_config": {
                "levels": [
                    {"sessions_min": 0, "sessions_max": 100, "multiplier": 1.0}
                ]
            },
            "cef_config": {
                "levels": [
                    {"level_id": 0, "description": "None", "multiplier": 1.0}
                ],
                "competition_level_mapping": {
                    "None": 0
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
        
        # Create a temporary file for config testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.temp_dir.name, "test_config.json")
        
        # Write the valid config to the temp file
        with open(self.config_path, 'w') as f:
            json.dump(self.valid_config, f)
    
    def tearDown(self):
        # Clean up temp directory
        self.temp_dir.cleanup()
    
    def test_validate_config_valid(self):
        """Test validation with valid configuration."""
        # Should not raise any exceptions
        validate_config(self.valid_config)
    
    def test_validate_config_missing_section(self):
        """Test validation with missing required section."""
        # Create invalid config with missing section
        invalid_config = self.valid_config.copy()
        del invalid_config["belt_rank_scores"]
        
        # Should raise ValueError
        with self.assertRaises(ValueError):
            validate_config(invalid_config)
    
    def test_validate_config_missing_belt(self):
        """Test validation with missing required belt rank."""
        # Create invalid config with missing belt
        invalid_config = self.valid_config.copy()
        invalid_config["belt_rank_scores"] = {
            "White": 100,
            "Blue": 200,
            # Purple is missing
            "Brown": 550,
            "Black": 800
        }
        
        # Should raise ValueError
        with self.assertRaises(ValueError):
            validate_config(invalid_config)
    
    def test_load_config(self):
        """Test loading configuration from file."""
        # Load the config from our temp file
        config = load_config(self.config_path)
        
        # Verify basic structure is intact
        self.assertIn("belt_rank_scores", config)
        self.assertIn("age_factor_config", config)
        self.assertIn("White", config["belt_rank_scores"])
        self.assertEqual(config["belt_rank_scores"]["White"], 100)
    
    def test_load_config_nonexistent(self):
        """Test loading from nonexistent file."""
        with self.assertRaises(FileNotFoundError):
            load_config("/path/does/not/exist.json")
    
    def test_save_config(self):
        """Test saving configuration to file."""
        # Modify the config
        modified_config = self.valid_config.copy()
        modified_config["belt_rank_scores"]["White"] = 110
        
        # Save to a new path
        new_path = os.path.join(self.temp_dir.name, "new_config.json")
        save_config(modified_config, new_path)
        
        # Load it back and verify changes
        loaded_config = load_config(new_path)
        self.assertEqual(loaded_config["belt_rank_scores"]["White"], 110)


if __name__ == "__main__":
    unittest.main()