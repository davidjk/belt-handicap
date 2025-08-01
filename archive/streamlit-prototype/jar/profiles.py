from typing import Dict, List, Literal, Optional, cast
from .types import PractitionerData, FactorResults, RollDynamicsProfile
from .config import JARConfig

class ProfileGenerator:
    """
    Generator for Roll Dynamics Profiles based on practitioner data and calculated factors.
    """
    
    def __init__(self, config: JARConfig):
        """
        Initialize the profile generator with configuration.
        
        Args:
            config: JAR system configuration
        """
        self.config = config
    
    def identify_significant_factors(
        self, 
        factors: FactorResults
    ) -> Dict[str, Literal["high", "low", "neutral"]]:
        """
        Identify which factors are significantly high or low.
        
        Args:
            factors: Calculated factor results
            
        Returns:
            Dictionary mapping factor IDs to their significance level
        """
        dynamics_config = self.config["profile_dynamics_config"]
        high_threshold = dynamics_config["significant_multiplier_threshold_high"]
        low_threshold = dynamics_config["significant_multiplier_threshold_low"]
        
        factor_significance = {}
        
        # Check each factor
        for factor_id, value in {
            "af": factors.af,
            "wf": factors.wf,
            "acf": factors.acf,
            "ref": factors.ref,
            "tff": factors.tff,
            "cef": factors.cef
        }.items():
            if value >= high_threshold:
                factor_significance[factor_id] = "high"
            elif value <= low_threshold:
                factor_significance[factor_id] = "low"
            else:
                factor_significance[factor_id] = "neutral"
        
        # Special handling for BRS (based on belt rank rather than multiplier)
        belt_scores = self.config["belt_rank_scores"]
        purple_threshold = belt_scores["Purple"]
        
        if factors.brs >= purple_threshold:
            factor_significance["brs"] = "high"
        else:
            factor_significance["brs"] = "low"
            
        return cast(Dict[str, Literal["high", "low", "neutral"]], factor_significance)
    
    def determine_dominant_trait(
        self, 
        factor_significance: Dict[str, Literal["high", "low", "neutral"]]
    ) -> str:
        """
        Determine the practitioner's dominant trait based on significant factors.
        
        Args:
            factor_significance: Dictionary of significant factors
            
        Returns:
            Description of dominant trait
        """
        # Example logic - this would be expanded with more sophisticated rules
        if factor_significance["brs"] == "high" and all(
            factor_significance[f] != "high" for f in ["wf", "acf", "ref"]
        ):
            return "Technical BJJ Specialist"
        
        if factor_significance["brs"] == "low" and any(
            factor_significance[f] == "high" for f in ["wf", "acf", "ref"]
        ):
            return "Physical Grappling Athlete"
        
        if factor_significance["brs"] == "high" and any(
            factor_significance[f] == "high" for f in ["wf", "acf", "ref"]
        ):
            return "Dominant All-Rounder"
        
        # More rules would be added
        return "Balanced Practitioner"
    
    def determine_likely_approach(
        self, 
        factor_significance: Dict[str, Literal["high", "low", "neutral"]]
    ) -> str:
        """
        Determine the practitioner's likely roll approach based on significant factors.
        
        Args:
            factor_significance: Dictionary of significant factors
            
        Returns:
            Description of likely approach
        """
        # Example logic - this would be expanded with more sophisticated rules
        if factor_significance["brs"] == "high" and factor_significance["wf"] != "high":
            return "Technical & Opportunistic"
        
        if any(factor_significance[f] == "high" for f in ["wf", "acf", "ref"]):
            return "Pressure & Control-Oriented"
        
        # More rules would be added
        return "Adaptable & Balanced"
    
    def generate_key_strengths(
        self, 
        factor_significance: Dict[str, Literal["high", "low", "neutral"]]
    ) -> List[str]:
        """
        Generate key strengths based on significant factors.
        
        Args:
            factor_significance: Dictionary of significant factors
            
        Returns:
            List of key strength descriptions
        """
        dynamics_config = self.config["profile_dynamics_config"]
        implication_statements = dynamics_config["implication_statements"]
        strengths = []
        
        # Add statements for high factors
        if factor_significance["brs"] == "high" and "BRS_high" in implication_statements:
            strengths.append(implication_statements["BRS_high"])
        
        # Check for wrestling/judo experience
        if factor_significance["ref"] == "high" and "REF_high_wrestling_judo" in implication_statements:
            strengths.append(implication_statements["REF_high_wrestling_judo"])
        
        if factor_significance["acf"] == "high" and "ACF_high" in implication_statements:
            strengths.append(implication_statements["ACF_high"])
        
        if factor_significance["wf"] == "high" and "WF_high" in implication_statements:
            strengths.append(implication_statements["WF_high"])
        
        # Add default strength if none were found
        if not strengths:
            strengths.append("Well-rounded BJJ skills with balanced attributes")
        
        return strengths
    
    def generate_key_challenges(
        self, 
        factor_significance: Dict[str, Literal["high", "low", "neutral"]]
    ) -> List[str]:
        """
        Generate key challenges based on significant factors.
        
        Args:
            factor_significance: Dictionary of significant factors
            
        Returns:
            List of key challenge descriptions
        """
        dynamics_config = self.config["profile_dynamics_config"]
        implication_statements = dynamics_config["implication_statements"]
        challenges = []
        
        # Add statements for low factors
        if factor_significance["brs"] == "low" and "BRS_low" in implication_statements:
            challenges.append(implication_statements["BRS_low"])
        
        if factor_significance["af"] == "low" and "AF_low" in implication_statements:
            challenges.append(implication_statements["AF_low"])
        
        if factor_significance["wf"] == "low" and "WF_low" in implication_statements:
            challenges.append(implication_statements["WF_low"])
        
        # Add default challenge if none were found
        if not challenges:
            challenges.append("May need to adjust strategy against opponents with significant physical or technical advantages")
        
        return challenges
    
    def determine_control_potential(
        self, 
        factor_significance: Dict[str, Literal["high", "low", "neutral"]]
    ) -> Literal["Low", "Medium", "High"]:
        """
        Determine control potential based on significant factors.
        
        Args:
            factor_significance: Dictionary of significant factors
            
        Returns:
            Control potential rating
        """
        # Count how many control-related factors are high
        control_factors = ["ref", "wf", "acf"]
        high_count = sum(1 for f in control_factors if factor_significance[f] == "high")
        
        if high_count >= 2:
            return "High"
        elif high_count == 1:
            return "Medium"
        else:
            return "Low"
    
    def determine_submission_threat(
        self, 
        factor_significance: Dict[str, Literal["high", "low", "neutral"]]
    ) -> Literal["Low", "Medium", "High"]:
        """
        Determine submission offensive threat based on significant factors.
        
        Args:
            factor_significance: Dictionary of significant factors
            
        Returns:
            Submission threat rating
        """
        # Primarily based on BJJ belt rank
        if factor_significance["brs"] == "high":
            # Enhance with competition experience
            if factor_significance["cef"] == "high":
                return "High"
            return "Medium"
        return "Low"
    
    def determine_submission_defense(
        self, 
        factor_significance: Dict[str, Literal["high", "low", "neutral"]]
    ) -> Literal["Low", "Medium", "High"]:
        """
        Determine submission defensive resilience based on significant factors.
        
        Args:
            factor_significance: Dictionary of significant factors
            
        Returns:
            Submission defense rating
        """
        # Primarily based on BJJ belt rank
        if factor_significance["brs"] == "high":
            return "High"
        
        # Some enhancement from other grappling experience
        if factor_significance["ref"] == "high":
            return "Medium"
            
        return "Low"
    
    def generate_profile(
        self, 
        practitioner: PractitionerData, 
        factors: FactorResults, 
        hs: float
    ) -> RollDynamicsProfile:
        """
        Generate complete Roll Dynamics Profile.
        
        Args:
            practitioner: Practitioner data
            factors: Calculated factor results
            hs: Final Handicapped Score
            
        Returns:
            Complete Roll Dynamics Profile
        """
        factor_significance = self.identify_significant_factors(factors)
        
        return RollDynamicsProfile(
            dominant_trait=self.determine_dominant_trait(factor_significance),
            likely_approach=self.determine_likely_approach(factor_significance),
            key_strengths=self.generate_key_strengths(factor_significance),
            key_challenges=self.generate_key_challenges(factor_significance),
            control_potential=self.determine_control_potential(factor_significance),
            submission_offensive_threat=self.determine_submission_threat(factor_significance),
            submission_defensive_resilience=self.determine_submission_defense(factor_significance),
            practitioner_name=practitioner.name,
            handicapped_score=hs
        )