#!/usr/bin/env python3

"""
Test the profile generation system to see what output it creates.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from jar.types import PractitionerData, GrapplingExperience
from jar.calculator import Calculator
from jar.profiles import ProfileGenerator
from jar.config import load_config

def main():
    # Load config
    config_path = os.path.join(os.path.dirname(__file__), "data", "default_config.json")
    config = load_config(config_path)
    calculator = Calculator(config)
    profile_generator = ProfileGenerator(config)
    
    print("=== PROFILE GENERATION TEST ===\n")
    
    # Olympic wrestler
    olympic_wrestler = PractitionerData(
        name="Olympic Wrestler",
        bjj_belt_rank="White",
        age_years=28,
        weight_lbs=200.0,
        primary_occupation_activity_level="Physically Demanding",
        standardized_fitness_test_percentile_estimate=99,
        other_grappling_art_experience=[GrapplingExperience(
            art_name="Wrestling",
            experience_level_descriptor="Elite International (Olympic/World level)"
        )],
        bjj_training_sessions_per_week=6,
        bjj_competition_experience_level="None"
    )
    
    # 45-year-old purple belt
    purple_belt = PractitionerData(
        name="45yr Purple Belt",
        bjj_belt_rank="Purple",
        age_years=45,
        weight_lbs=180.0,
        primary_occupation_activity_level="Moderately Active",
        standardized_fitness_test_percentile_estimate=60,
        other_grappling_art_experience=[],
        bjj_training_sessions_per_week=3,
        bjj_competition_experience_level="Limited Local"
    )
    
    # Generate factors and profiles
    wrestler_factors = calculator.calculate_all_factors(olympic_wrestler, purple_belt)
    wrestler_score = wrestler_factors.calculate_handicapped_score()
    wrestler_profile = profile_generator.generate_profile(olympic_wrestler, wrestler_factors, wrestler_score)
    
    purple_factors = calculator.calculate_all_factors(purple_belt, olympic_wrestler)
    purple_score = purple_factors.calculate_handicapped_score()
    purple_profile = profile_generator.generate_profile(purple_belt, purple_factors, purple_score)
    
    # Display profiles
    print("=== OLYMPIC WRESTLER PROFILE ===")
    print(f"Name: {wrestler_profile.practitioner_name}")
    print(f"Score: {wrestler_profile.handicapped_score:.1f}")
    print(f"Dominant Trait: {wrestler_profile.dominant_trait}")
    print(f"Likely Approach: {wrestler_profile.likely_approach}")
    print(f"Control Potential: {wrestler_profile.control_potential}")
    print(f"Submission Offense: {wrestler_profile.submission_offensive_threat}")
    print(f"Submission Defense: {wrestler_profile.submission_defensive_resilience}")
    print("Key Strengths:")
    for strength in wrestler_profile.key_strengths:
        print(f"  - {strength}")
    print("Key Challenges:")
    for challenge in wrestler_profile.key_challenges:
        print(f"  - {challenge}")
    
    print("\n" + "="*60 + "\n")
    
    print("=== PURPLE BELT PROFILE ===")
    print(f"Name: {purple_profile.practitioner_name}")
    print(f"Score: {purple_profile.handicapped_score:.1f}")
    print(f"Dominant Trait: {purple_profile.dominant_trait}")
    print(f"Likely Approach: {purple_profile.likely_approach}")
    print(f"Control Potential: {purple_profile.control_potential}")
    print(f"Submission Offense: {purple_profile.submission_offensive_threat}")
    print(f"Submission Defense: {purple_profile.submission_defensive_resilience}")
    print("Key Strengths:")
    for strength in purple_profile.key_strengths:
        print(f"  - {strength}")
    print("Key Challenges:")
    for challenge in purple_profile.key_challenges:
        print(f"  - {challenge}")

if __name__ == "__main__":
    main()