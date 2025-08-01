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