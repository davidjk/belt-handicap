from typing import Optional, Dict, Callable, Any, cast
import math
from .types import PractitionerData, FactorResults
from .config import JARConfig

class Calculator:
    """
    Main calculator class for JAR system factors and scores.
    
    This class contains methods to calculate all the factors that contribute
    to a practitioner's Handicapped Score (HS).
    """
    
    def __init__(self, config: JARConfig):
        """
        Initialize the calculator with configuration.
        
        Args:
            config: JAR system configuration
        """
        self.config = config
    
    def calculate_brs(self, practitioner: PractitionerData) -> float:
        """
        Calculate Belt Rank Score (BRS).
        
        Args:
            practitioner: Practitioner data
            
        Returns:
            Belt Rank Score
        """
        return float(self.config["belt_rank_scores"][practitioner.bjj_belt_rank])
    
    def calculate_af(self, practitioner: PractitionerData) -> float:
        """
        Calculate Age Factor (AF).
        
        Args:
            practitioner: Practitioner data
            
        Returns:
            Age Factor multiplier
        """
        age_config = self.config["age_factor_config"]
        peak_age = age_config["peak_age_years"]
        
        if practitioner.age_years < peak_age:
            return age_config["youthful_factor_multiplier"]
        
        decades_past_peak = (practitioner.age_years - peak_age) / 10.0
        return (1.0 - age_config["power_decline_rate_per_decade"]) ** decades_past_peak
    
    def calculate_wf(
        self, 
        practitioner: PractitionerData, 
        comparison_practitioner: Optional[PractitionerData]
    ) -> float:
        """
        Calculate Weight/Size Factor (WF).
        
        Args:
            practitioner: Practitioner data
            comparison_practitioner: Optional comparison practitioner for relative weight calculations
            
        Returns:
            Weight Factor multiplier
        """
        if not comparison_practitioner:
            return 1.0  # Neutral if no comparison
        
        weight_config = self.config["weight_factor_config"]
        weight_difference = abs(practitioner.weight_lbs - comparison_practitioner.weight_lbs)
        
        if weight_difference <= 0:
            return 1.0  # No difference
        
        # Determine if this practitioner is heavier or lighter
        is_heavier = practitioner.weight_lbs > comparison_practitioner.weight_lbs
        
        # Calculate adjustment using threshold tiers
        total_adjustment = 0.0
        remaining_diff = weight_difference
        last_tier_max_lbs = 0.0
        highest_tier_adjustment = 0.0
        
        for tier in weight_config["thresholds_bonuses_penalties"]:
            lbs_covered_by_this_tier = tier["diff_max_lbs"] - last_tier_max_lbs
            lbs_to_consider = min(remaining_diff, lbs_covered_by_this_tier)
            
            if lbs_to_consider <= 0:
                break
                
            tier_adjustment = (lbs_to_consider / weight_config["increment_lbs"]) * tier["adjustment"]
            total_adjustment += tier_adjustment
            highest_tier_adjustment = tier["adjustment"]  # Keep track of highest tier adjustment
            
            remaining_diff -= lbs_to_consider
            last_tier_max_lbs = tier["diff_max_lbs"]
            
            if remaining_diff <= 0:
                break
        
        # Handle any remaining weight difference using the highest tier adjustment
        if remaining_diff > 0 and highest_tier_adjustment > 0:
            tier_adjustment = (remaining_diff / weight_config["increment_lbs"]) * highest_tier_adjustment
            total_adjustment += tier_adjustment
        
        # Apply adjustment based on whether practitioner is heavier or lighter
        return 1.0 + total_adjustment if is_heavier else 1.0 - total_adjustment
    
    def calculate_acf(self, practitioner: PractitionerData) -> float:
        """
        Calculate Athleticism & Conditioning Factor (ACF).
        
        Args:
            practitioner: Practitioner data
            
        Returns:
            Athleticism Factor multiplier
        """
        acf_config = self.config["acf_config"]
        fitness_percentile = practitioner.standardized_fitness_test_percentile_estimate
        
        # Find appropriate level based on fitness percentile
        for level in acf_config["levels"]:
            level_id = level["level_id"]
            
            # Define percentile ranges for each level
            if (level_id == 1 and fitness_percentile < 30) or \
               (level_id == 2 and 30 <= fitness_percentile < 60) or \
               (level_id == 3 and 60 <= fitness_percentile < 80) or \
               (level_id == 4 and 80 <= fitness_percentile < 95) or \
               (level_id == 5 and fitness_percentile >= 95):
                return level["multiplier"]
        
        # Default to middle level if no match found
        return 1.0
    
    def calculate_ref(self, practitioner: PractitionerData) -> float:
        """
        Calculate Relevant Grappling Experience Factor (REF).
        
        Args:
            practitioner: Practitioner data
            
        Returns:
            Relevant Experience Factor multiplier
        """
        ref_config = self.config["ref_config"]
        
        # If no other grappling experience
        if not practitioner.other_grappling_art_experience:
            return ref_config["levels"][0]["multiplier"]  # Level 0 - None
        
        # Get the most significant experience (for now, just use the first one)
        experience = practitioner.other_grappling_art_experience[0]
        
        # Try to map using the configuration
        mapping_key = f"{experience['art_name']}_{experience['experience_level_descriptor']}"
        if mapping_key in ref_config["art_experience_level_mapping"]:
            level_id = ref_config["art_experience_level_mapping"][mapping_key]
            
            # Find the corresponding multiplier
            for level in ref_config["levels"]:
                if level["level_id"] == level_id:
                    return level["multiplier"]
        
        # Default to level 0 if no mapping found
        return ref_config["levels"][0]["multiplier"]
    
    def calculate_tff(self, practitioner: PractitionerData) -> float:
        """
        Calculate Training Intensity/Frequency Factor (TFF).
        
        Args:
            practitioner: Practitioner data
            
        Returns:
            Training Frequency Factor multiplier
        """
        tff_config = self.config["tff_config"]
        sessions = practitioner.bjj_training_sessions_per_week
        
        for level in tff_config["levels"]:
            if level["sessions_min"] <= sessions <= level["sessions_max"]:
                return level["multiplier"]
        
        # Default to middle level if no match found
        return 1.0
    
    def calculate_cef(self, practitioner: PractitionerData) -> float:
        """
        Calculate BJJ Competition Experience Factor (CEF).
        
        Args:
            practitioner: Practitioner data
            
        Returns:
            Competition Experience Factor multiplier
        """
        cef_config = self.config["cef_config"]
        comp_level = practitioner.bjj_competition_experience_level
        
        # Get level_id from mapping
        if comp_level in cef_config["competition_level_mapping"]:
            level_id = cef_config["competition_level_mapping"][comp_level]
            
            # Find the corresponding multiplier
            for level in cef_config["levels"]:
                if level["level_id"] == level_id:
                    return level["multiplier"]
        
        # Default to level 0 if no mapping found
        return cef_config["levels"][0]["multiplier"]
    
    def calculate_all_factors(
        self, 
        practitioner: PractitionerData, 
        comparison_practitioner: Optional[PractitionerData] = None
    ) -> FactorResults:
        """
        Calculate all factors for a practitioner.
        
        Args:
            practitioner: Practitioner data
            comparison_practitioner: Optional comparison practitioner for relative calculations
            
        Returns:
            All calculated factors
        """
        return FactorResults(
            brs=self.calculate_brs(practitioner),
            af=self.calculate_af(practitioner),
            wf=self.calculate_wf(practitioner, comparison_practitioner),
            acf=self.calculate_acf(practitioner),
            ref=self.calculate_ref(practitioner),
            tff=self.calculate_tff(practitioner),
            cef=self.calculate_cef(practitioner)
        )