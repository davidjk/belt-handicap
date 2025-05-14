# JAR System Streamlit Implementation Guide

## Overview
This document outlines the implementation plan for a Streamlit application that will bring the Jiu-Jitsu Attribute Rating (JAR) system to life. The application will allow users to input practitioner data, visualize the various factors that contribute to a practitioner's Handicapped Score (HS), and compare two practitioners.

## Software Design Principles

### 1. Modularity
- **Domain-Driven Design**: Separate the core JAR system logic from the UI components
- **Interface-Based Programming**: Define clear interfaces for components to interact
- **Single Responsibility Principle**: Each module and class should have one responsibility
- **Dependency Injection**: Pass configurations and dependencies rather than hardcoding

### 2. Type Safety
- Use comprehensive type hints throughout the codebase
- Create custom data types/classes for domain entities
- Define clear interface contracts between components

### 3. Testability
- Design components to be easily unit-testable
- Use dependency injection to facilitate mocking in tests
- Keep pure calculation functions separate from UI logic

### 4. Code Organization
- Follow consistent naming conventions
- Organize code into logical packages/modules
- Use consistent import ordering and module structure

### 5. Documentation
- Include docstrings for all public functions and classes
- Provide usage examples in docstrings where appropriate
- Document design decisions and rationale

## Project Structure
```
belt-handicap/
├── app.py                  # Main Streamlit application entry point
├── jar/                    # JAR system core logic
│   ├── __init__.py
│   ├── types.py            # Type definitions and dataclasses
│   ├── calculator.py       # Core calculation functions
│   ├── config.py           # Configuration handling
│   ├── profiles.py         # Roll Dynamics Profile generation
│   └── utils.py            # Utility functions
├── ui/                     # UI components
│   ├── __init__.py
│   ├── input_forms.py      # Practitioner data input components
│   ├── visualizations.py   # Factor visualization components
│   ├── profile_display.py  # Roll Dynamics Profile display components
│   └── shared.py           # Shared UI utilities
├── data/                   # Default configuration and sample data
│   ├── default_config.json # Default JAR system configuration
│   └── sample_data.json    # Sample practitioner data
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── test_calculator.py  # Tests for calculation functions
│   ├── test_config.py      # Tests for configuration handling
│   └── test_profiles.py    # Tests for profile generation
└── docs/
    ├── initial_prd.md      # Original PRD
    └── streamlit_implementation.md  # This document
```

## Implementation Details

### 1. Core Types (`jar/types.py`)
```python
from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional, TypedDict, Union

# Belt rank type
BeltRank = Literal["White", "Blue", "Purple", "Brown", "Black"]

# Experience level types
GrapplingArtName = Literal["None", "Wrestling", "Judo", "Sambo", "Other"]
ExperienceLevel = Literal[
    "None",
    "Recreational/Limited (<1 year)",
    "Foundational (1-3 years)",
    "Accomplished (3-5+ years, regional level)",
    "High-Level Competitor (National level)",
    "Elite International (Olympic/World level)"
]
CompetitionLevel = Literal["None", "Limited Local", "Regular Regional", "National/International"]
ActivityLevel = Literal["Sedentary (Desk Job)", "Moderately Active", "Physically Demanding"]

# Type for other grappling experience
class GrapplingExperience(TypedDict):
    art_name: GrapplingArtName
    experience_level_descriptor: ExperienceLevel

# Practitioner data structure
@dataclass
class PractitionerData:
    name: str
    bjj_belt_rank: BeltRank
    age_years: int
    weight_lbs: float
    primary_occupation_activity_level: ActivityLevel
    standardized_fitness_test_percentile_estimate: int
    other_grappling_art_experience: List[GrapplingExperience]
    bjj_training_sessions_per_week: int
    bjj_competition_experience_level: CompetitionLevel
    practitioner_id: Optional[str] = None
    
    def __post_init__(self):
        # Validate ranges
        if not 16 <= self.age_years <= 90:
            raise ValueError("Age must be between 16 and 90")
        if not 80 <= self.weight_lbs <= 400:
            raise ValueError("Weight must be between 80 and 400 lbs")
        if not 0 <= self.standardized_fitness_test_percentile_estimate <= 100:
            raise ValueError("Fitness percentile must be between 0 and 100")
        if not 0 <= self.bjj_training_sessions_per_week <= 14:
            raise ValueError("Training sessions must be between 0 and 14 per week")

# Factor calculation results
@dataclass
class FactorResults:
    brs: float  # Belt Rank Score
    af: float   # Age Factor
    wf: float   # Weight/Size Factor 
    acf: float  # Athleticism & Conditioning Factor
    ref: float  # Relevant Grappling Experience Factor
    tff: float  # Training Intensity/Frequency Factor
    cef: float  # BJJ Competition Experience Factor
    
    def calculate_handicapped_score(self) -> float:
        """Calculate the final Handicapped Score from all factors."""
        return self.brs * self.af * self.wf * self.acf * self.ref * self.tff * self.cef

# Profile output structure
@dataclass
class RollDynamicsProfile:
    dominant_trait: str
    likely_approach: str
    key_strengths: List[str]
    key_challenges: List[str]
    control_potential: Literal["Low", "Medium", "High"]
    submission_offensive_threat: Literal["Low", "Medium", "High"]
    submission_defensive_resilience: Literal["Low", "Medium", "High"]
    
    # Additional metadata for UI display
    practitioner_name: str
    handicapped_score: float
```

### 2. Configuration Interface (`jar/config.py`)
```python
from typing import Dict, List, Any, Optional, TypedDict, cast
import json
import os
from dataclasses import dataclass

class AgeFactorConfig(TypedDict):
    peak_age_years: int
    youthful_factor_multiplier: float
    power_decline_rate_per_decade: float

class WeightThreshold(TypedDict):
    diff_max_lbs: float
    adjustment: float

class WeightFactorConfig(TypedDict):
    increment_lbs: float
    thresholds_bonuses_penalties: List[WeightThreshold]

class FactorLevel(TypedDict):
    level_id: int
    description: str
    multiplier: float

class FactorConfig(TypedDict):
    levels: List[FactorLevel]
    
class REFConfig(FactorConfig):
    art_experience_level_mapping: Dict[str, int]

class CEFConfig(FactorConfig):
    competition_level_mapping: Dict[str, int]

class TFFLevel(TypedDict):
    sessions_min: int
    sessions_max: int
    multiplier: float

class TFFConfig(TypedDict):
    levels: List[TFFLevel]

class ProfileDynamicsConfig(TypedDict):
    significant_multiplier_threshold_high: float
    significant_multiplier_threshold_low: float
    implication_statements: Dict[str, str]
    control_implication_factors: List[str]
    submission_implication_factors_offense: List[str]
    submission_implication_factors_defense: List[str]

class JARConfig(TypedDict):
    belt_rank_scores: Dict[str, int]
    age_factor_config: AgeFactorConfig
    weight_factor_config: WeightFactorConfig
    acf_config: FactorConfig
    ref_config: REFConfig
    tff_config: TFFConfig
    cef_config: CEFConfig
    profile_dynamics_config: ProfileDynamicsConfig

def load_config(config_path: str) -> JARConfig:
    """
    Load JAR system configuration from JSON file.
    
    Args:
        config_path: Path to the configuration JSON file
        
    Returns:
        Parsed configuration as JARConfig
        
    Raises:
        FileNotFoundError: If the configuration file doesn't exist
        ValueError: If the configuration is invalid
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
    with open(config_path, 'r') as f:
        config_data = json.load(f)
    
    # Validate basic structure
    validate_config(config_data)
    
    return cast(JARConfig, config_data)

def validate_config(config: Any) -> None:
    """
    Validate the JAR configuration structure.
    
    Args:
        config: Configuration data to validate
        
    Raises:
        ValueError: If the configuration is invalid
    """
    required_sections = [
        "belt_rank_scores", "age_factor_config", "weight_factor_config",
        "acf_config", "ref_config", "tff_config", "cef_config",
        "profile_dynamics_config"
    ]
    
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Missing required configuration section: {section}")
    
    # Validate belt ranks
    required_belts = ["White", "Blue", "Purple", "Brown", "Black"]
    for belt in required_belts:
        if belt not in config["belt_rank_scores"]:
            raise ValueError(f"Missing required belt rank: {belt}")

def save_config(config: JARConfig, config_path: str) -> None:
    """
    Save JAR system configuration to JSON file.
    
    Args:
        config: The configuration to save
        config_path: Path to save the configuration JSON file
    """
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
```

### 3. Core Calculator Interface (`jar/calculator.py`)
```python
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
        
        for tier in weight_config["thresholds_bonuses_penalties"]:
            lbs_covered_by_this_tier = tier["diff_max_lbs"] - last_tier_max_lbs
            lbs_to_consider = min(remaining_diff, lbs_covered_by_this_tier)
            
            if lbs_to_consider <= 0:
                break
                
            tier_adjustment = (lbs_to_consider / weight_config["increment_lbs"]) * tier["adjustment"]
            total_adjustment += tier_adjustment
            
            remaining_diff -= lbs_to_consider
            last_tier_max_lbs = tier["diff_max_lbs"]
            
            if remaining_diff <= 0:
                break
        
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
            # Logic depends on the percentile ranges defined in config
            # This is a simplified example
            level_id = level["level_id"]
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
```

### 4. Profile Generator Interface (`jar/profiles.py`)
```python
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
        if factor_significance["brs"] == "high":
            strengths.append(implication_statements["BRS_high"])
        
        # Check for wrestling/judo experience
        if factor_significance["ref"] == "high":
            strengths.append(implication_statements["REF_high_wrestling_judo"])
        
        if factor_significance["acf"] == "high":
            strengths.append(implication_statements["ACF_high"])
        
        if factor_significance["wf"] == "high":
            strengths.append(implication_statements["WF_high"])
        
        # Additional logic for other factors would be added
        
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
        if factor_significance["brs"] == "low":
            challenges.append(implication_statements["BRS_low"])
        
        if factor_significance["af"] == "low":
            challenges.append(implication_statements["AF_low"])
        
        if factor_significance["wf"] == "low":
            challenges.append(implication_statements["WF_low"])
        
        # Additional logic for other factors would be added
        
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
```

### 5. Streamlit UI Implementation (`app.py`)
```python
import streamlit as st
import os
import json
from jar.types import PractitionerData, FactorResults, RollDynamicsProfile
from jar.config import JARConfig, load_config
from jar.calculator import Calculator
from jar.profiles import ProfileGenerator
from ui.input_forms import render_practitioner_form
from ui.visualizations import render_factor_visualization
from ui.profile_display import render_profile

def main():
    """
    Main Streamlit application entry point.
    """
    st.set_page_config(
        page_title="JAR System",
        page_icon="🥋",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    st.title("Jiu-Jitsu Attribute Rating (JAR) System")
    
    # Initialize session state for storing data between interactions
    if "config" not in st.session_state:
        config_path = "data/default_config.json"
        try:
            st.session_state.config = load_config(config_path)
        except (FileNotFoundError, ValueError) as e:
            st.error(f"Error loading configuration: {e}")
            return
    
    # Create core system components
    calculator = Calculator(st.session_state.config)
    profile_generator = ProfileGenerator(st.session_state.config)
    
    # Sidebar for app navigation
    page = st.sidebar.radio(
        "Select Page", 
        ["Single Practitioner", "Compare Practitioners", "About", "Configuration"]
    )
    
    if page == "Single Practitioner":
        single_practitioner_view(calculator, profile_generator)
    elif page == "Compare Practitioners":
        compare_practitioners_view(calculator, profile_generator)
    elif page == "About":
        about_view()
    else:
        configuration_view()

def single_practitioner_view(calculator: Calculator, profile_generator: ProfileGenerator):
    """
    View for analyzing a single practitioner.
    
    Args:
        calculator: JAR system calculator
        profile_generator: Profile generator
    """
    st.header("Single Practitioner Analysis")
    
    # Get practitioner data from form
    practitioner_data = render_practitioner_form("practitioner1", st.session_state.config)
    
    if st.button("Calculate Score"):
        # Calculate factors and HS
        factors = calculator.calculate_all_factors(practitioner_data)
        hs = factors.calculate_handicapped_score()
        
        # Display results
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Factor Breakdown")
            render_factor_visualization(factors, st.session_state.config)
        
        with col2:
            st.subheader("Handicapped Score")
            st.metric("Total Score", f"{hs:.2f}")
        
        # Generate and display profile
        profile = profile_generator.generate_profile(practitioner_data, factors, hs)
        render_profile(profile)

def compare_practitioners_view(calculator: Calculator, profile_generator: ProfileGenerator):
    """
    View for comparing two practitioners.
    
    Args:
        calculator: JAR system calculator
        profile_generator: Profile generator
    """
    st.header("Compare Two Practitioners")
    
    # Create two columns for practitioner inputs
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Practitioner A")
        practitioner_a = render_practitioner_form("practitioner_a", st.session_state.config)
    
    with col2:
        st.subheader("Practitioner B")
        practitioner_b = render_practitioner_form("practitioner_b", st.session_state.config)
    
    if st.button("Compare"):
        # Calculate factors and HS for both
        factors_a = calculator.calculate_all_factors(practitioner_a, practitioner_b)
        hs_a = factors_a.calculate_handicapped_score()
        
        factors_b = calculator.calculate_all_factors(practitioner_b, practitioner_a)
        hs_b = factors_b.calculate_handicapped_score()
        
        # Display results side-by-side
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"Practitioner A: {practitioner_a.name}")
            st.metric("Handicapped Score", f"{hs_a:.2f}")
            render_factor_visualization(factors_a, st.session_state.config)
            
            # Generate and display profile
            profile_a = profile_generator.generate_profile(practitioner_a, factors_a, hs_a)
            render_profile(profile_a)
        
        with col2:
            st.subheader(f"Practitioner B: {practitioner_b.name}")
            st.metric("Handicapped Score", f"{hs_b:.2f}")
            render_factor_visualization(factors_b, st.session_state.config)
            
            # Generate and display profile
            profile_b = profile_generator.generate_profile(practitioner_b, factors_b, hs_b)
            render_profile(profile_b)

def about_view():
    """View for displaying information about the JAR system."""
    st.header("About the JAR System")
    
    st.markdown("""
    The Jiu-Jitsu Attribute Rating (JAR) system is a conceptual framework designed to provide a more 
    nuanced understanding of practitioner matchups in Brazilian Jiu-Jitsu (BJJ), moving beyond sole 
    reliance on belt rank.
    
    ### Purpose:
    - To calculate a relative Handicapped Score (HS) for individual BJJ practitioners based on a range of attributes.
    - To generate a Roll Dynamics Profile that offers qualitative insights into potential matchup dynamics.
    - To serve as a tool for practitioners, instructors, and analysts to facilitate more informed discussions.
    - To help in setting appropriate training challenges and managing expectations for sparring sessions.
    
    ### System Components:
    - Belt Rank Score (BRS): Foundational score representing accumulated BJJ-specific skill
    - Age Factor (AF): Accounts for age-related physiological factors
    - Weight/Size Factor (WF): Reflects the impact of weight differences
    - Athleticism & Conditioning Factor (ACF): Quantifies general physical prowess
    - Relevant Grappling Experience Factor (REF): Credits transferable skills from other disciplines
    - Training Intensity/Frequency Factor (TFF): Reflects current BJJ training volume
    - BJJ Competition Experience Factor (CEF): Accounts for competition-specific skills
    
    The JAR system is NOT designed to definitively predict winners or losers but rather to contextualize 
    potential performance based on a broader set of factors.
    """)

def configuration_view():
    """View for editing system configuration."""
    st.header("System Configuration")
    
    st.warning("This is an advanced feature. Changing these values will affect all calculations.")
    
    config = st.session_state.config
    
    # Display configuration in expandable sections
    with st.expander("Belt Rank Scores"):
        for belt, score in config["belt_rank_scores"].items():
            config["belt_rank_scores"][belt] = st.number_input(
                f"{belt} Belt", 
                min_value=1, 
                value=score
            )
    
    with st.expander("Age Factor Configuration"):
        config["age_factor_config"]["peak_age_years"] = st.number_input(
            "Peak Age (years)", 
            min_value=18, 
            max_value=40, 
            value=config["age_factor_config"]["peak_age_years"]
        )
        config["age_factor_config"]["youthful_factor_multiplier"] = st.slider(
            "Youthful Factor Multiplier", 
            min_value=1.0, 
            max_value=1.1, 
            value=config["age_factor_config"]["youthful_factor_multiplier"],
            step=0.01
        )
        config["age_factor_config"]["power_decline_rate_per_decade"] = st.slider(
            "Power Decline Rate (per decade)", 
            min_value=0.05, 
            max_value=0.2, 
            value=config["age_factor_config"]["power_decline_rate_per_decade"],
            step=0.01
        )
    
    # Add more configuration sections as needed
    
    if st.button("Save Configuration"):
        try:
            if not os.path.exists("data"):
                os.makedirs("data")
                
            with open("data/user_config.json", "w") as f:
                json.dump(config, f, indent=2)
                
            st.success("Configuration saved!")
        except Exception as e:
            st.error(f"Error saving configuration: {e}")

if __name__ == "__main__":
    main()
```

### 6. Unit Tests Example (`tests/test_calculator.py`)
```python
import unittest
from jar.types import PractitionerData, GrapplingExperience
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
    
    def test_calculate_brs(self):
        """Test Belt Rank Score calculation."""
        self.assertEqual(self.calculator.calculate_brs(self.white_belt), 100)
        self.assertEqual(self.calculator.calculate_brs(self.purple_belt), 350)
    
    def test_calculate_af(self):
        """Test Age Factor calculation."""
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
    
    def test_calculate_wf(self):
        """Test Weight Factor calculation."""
        # Test case where both practitioners are the same weight
        self.assertEqual(self.calculator.calculate_wf(self.white_belt, self.white_belt), 1.0)
        
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
    
    def test_calculate_all_factors(self):
        """Test calculation of all factors together."""
        factors = self.calculator.calculate_all_factors(self.purple_belt, self.white_belt)
        
        # Verify BRS
        self.assertEqual(factors.brs, 350)
        
        # Verify AF (age 35)
        self.assertAlmostEqual(factors.af, 0.88, places=2)
        
        # Verify WF (weight 185 vs 170)
        self.assertAlmostEqual(factors.wf, 1.06, places=2)
        
        # Verify ACF (70th percentile)
        self.assertEqual(factors.acf, 1.07)
        
        # Verify REF (Wrestling high-level)
        self.assertEqual(factors.ref, 1.22)
        
        # Verify TFF (4 sessions per week)
        self.assertEqual(factors.tff, 1.05)
        
        # Verify CEF (Regular Regional)
        self.assertEqual(factors.cef, 1.08)
        
        # Verify Handicapped Score calculation
        expected_hs = 350 * 0.88 * 1.06 * 1.07 * 1.22 * 1.05 * 1.08
        self.assertAlmostEqual(factors.calculate_handicapped_score(), expected_hs, places=2)

if __name__ == "__main__":
    unittest.main()
```

## Visualization Components (`ui/visualizations.py`)

For the visualization components, we'll use a combination of built-in Streamlit charts and custom Matplotlib visualizations to create:

1. Factor bar chart showing the impact of each factor
2. Waterfall chart showing the step-by-step contribution to the final score
3. Radar chart for comparing practitioners

The visualizations will be designed to:
- Be modular and reusable
- Include clear legends and labels
- Use consistent color schemes
- Highlight significant factors
- Show comparisons effectively when needed

## Recommended Implementation Steps

1. **Setup Project Structure**
   - Create directory structure
   - Initialize Python package structure
   - Create placeholder files

2. **Implement Core Types and Configuration**
   - Define data types and interfaces
   - Implement configuration loading/validation

3. **Implement Calculator**
   - Start with unit tests for each calculation function
   - Implement each factor calculation
   - Integrate calculations in the main calculator class

4. **Implement Profile Generator**
   - Create functions for each profile component
   - Build the comprehensive profile generator

5. **Develop Unit Tests**
   - Test core calculations
   - Test profile generation
   - Test configuration handling

6. **Create Streamlit UI Components**
   - Implement input forms
   - Create visualization components
   - Develop profile display

7. **Integration and Testing**
   - Integrate all components
   - Test with various scenarios
   - Fix edge cases and bugs

8. **Code Quality and Cleanup**
   - Review type hints
   - Enhance documentation
   - Refactor and optimize

## Additional Quality Considerations

1. **Error Handling**
   - Provide meaningful error messages
   - Validate input data
   - Gracefully handle edge cases

2. **Documentation**
   - Add docstrings to all public functions and classes
   - Include usage examples
   - Document design decisions

3. **Performance**
   - Use Streamlit caching where appropriate
   - Optimize heavy calculations

4. **Code Style**
   - Follow PEP 8 guidelines
   - Use consistent naming conventions
   - Organize imports logically

5. **Testing**
   - Achieve high test coverage for core components
   - Include edge cases in tests
   - Test UI interactions

By following these guidelines and structure, the JAR system implementation will be modular, maintainable, and deliver a high-quality user experience.