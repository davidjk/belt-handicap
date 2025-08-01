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
            raise ValueError(f"Age must be between 16 and 90 (got {self.age_years})")
        if not 80 <= self.weight_lbs <= 400:
            raise ValueError(f"Weight must be between 80 and 400 lbs (got {self.weight_lbs})")
        if not 0 <= self.standardized_fitness_test_percentile_estimate <= 100:
            raise ValueError(f"Fitness percentile must be between 0 and 100 (got {self.standardized_fitness_test_percentile_estimate})")
        if not 0 <= self.bjj_training_sessions_per_week <= 14:
            raise ValueError(f"Training sessions must be between 0 and 14 per week (got {self.bjj_training_sessions_per_week})")

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