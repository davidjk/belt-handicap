#!/usr/bin/env python3

"""
Python comparison test to verify JavaScript implementation matches Python exactly.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from jar.types import PractitionerData, GrapplingExperience
from jar.calculator import Calculator
from jar.config import load_config

def main():
    # Load config
    config_path = os.path.join(os.path.dirname(__file__), "data", "default_config.json")
    config = load_config(config_path)
    calculator = Calculator(config)
    
    print("=== PYTHON CALIBRATION TEST ===\n")
    
    # Olympic wrestler (should score very high)
    olympic_wrestler = PractitionerData(
        name="Olympic Wrestler",
        bjj_belt_rank="White",  # New to BJJ
        age_years=28,
        weight_lbs=200.0,
        primary_occupation_activity_level="Physically Demanding",
        standardized_fitness_test_percentile_estimate=99,  # Elite athlete
        other_grappling_art_experience=[GrapplingExperience(
            art_name="Wrestling",
            experience_level_descriptor="Elite International (Olympic/World level)"
        )],
        bjj_training_sessions_per_week=6,
        bjj_competition_experience_level="None"  # New to BJJ
    )
    
    # 45-year-old purple belt (experienced BJJ)
    purple_belt = PractitionerData(
        name="45yr Purple Belt",
        bjj_belt_rank="Purple",
        age_years=45,
        weight_lbs=180.0,
        primary_occupation_activity_level="Moderately Active",
        standardized_fitness_test_percentile_estimate=60,  # Above average
        other_grappling_art_experience=[],  # No other experience
        bjj_training_sessions_per_week=3,
        bjj_competition_experience_level="Limited Local"
    )
    
    # Calculate factors for Olympic wrestler
    wrestler_factors = calculator.calculate_all_factors(olympic_wrestler, purple_belt)
    wrestler_score = wrestler_factors.calculate_handicapped_score()
    
    print("Olympic Wrestler (Python):")
    print(f"  BRS: {wrestler_factors.brs} (White belt = 100)")
    print(f"  AF: {wrestler_factors.af:.6f} (Age 28)")
    print(f"  WF: {wrestler_factors.wf:.6f} (200 vs 180 lbs)")
    print(f"  ACF: {wrestler_factors.acf:.6f} (99th percentile fitness)")
    print(f"  REF: {wrestler_factors.ref:.6f} (Olympic wrestling)")
    print(f"  TFF: {wrestler_factors.tff:.6f} (6 sessions/week)")
    print(f"  CEF: {wrestler_factors.cef:.6f} (No BJJ comps)")
    print(f"  TOTAL SCORE: {wrestler_score:.1f}\n")
    
    # Calculate factors for purple belt
    purple_factors = calculator.calculate_all_factors(purple_belt, olympic_wrestler)
    purple_score = purple_factors.calculate_handicapped_score()
    
    print("45yr Purple Belt (Python):")
    print(f"  BRS: {purple_factors.brs} (Purple belt = 350)")
    print(f"  AF: {purple_factors.af:.6f} (Age 45)")
    print(f"  WF: {purple_factors.wf:.6f} (180 vs 200 lbs)")
    print(f"  ACF: {purple_factors.acf:.6f} (60th percentile fitness)")
    print(f"  REF: {purple_factors.ref:.6f} (No other experience)")
    print(f"  TFF: {purple_factors.tff:.6f} (3 sessions/week)")
    print(f"  CEF: {purple_factors.cef:.6f} (Limited local comps)")
    print(f"  TOTAL SCORE: {purple_score:.1f}\n")
    
    print("=== PYTHON ANALYSIS ===")
    print(f"Wrestling advantage: {(wrestler_score / purple_score):.2f}x")
    
    # Check REF calculation specifically
    print(f"\n=== REF DEBUG (Python) ===")
    print(f"Wrestler experience: {olympic_wrestler.other_grappling_art_experience}")
    ref_manual = calculator.calculate_ref(olympic_wrestler)
    print(f"Manual REF calculation: {ref_manual:.6f}")
    
    # Check config
    print(f"\n=== CONFIG CHECK (Python) ===")
    wrestling_elite_key = "Wrestling_Elite International (Olympic/World level)"
    if wrestling_elite_key in config["ref_config"]["art_experience_level_mapping"]:
        level_id = config["ref_config"]["art_experience_level_mapping"][wrestling_elite_key]
        print(f"Wrestling Elite maps to level_id: {level_id}")
        
        # Find multiplier for this level
        for level in config["ref_config"]["levels"]:
            if level["level_id"] == level_id:
                print(f"Level {level_id} multiplier: {level['multiplier']}")
                break
    
if __name__ == "__main__":
    main()