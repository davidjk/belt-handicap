import streamlit as st
from typing import Dict, Any, List, Optional, cast
import uuid
from jar.types import PractitionerData, BeltRank, ActivityLevel, CompetitionLevel
from jar.config import JARConfig

def render_practitioner_form(key_prefix: str, config: JARConfig) -> PractitionerData:
    """
    Render form for practitioner data input with appropriate controls.
    
    Args:
        key_prefix: Prefix for unique Streamlit widget keys
        config: JAR system configuration
        
    Returns:
        Populated PractitionerData object
    """
    # Initialize session state for form fields if they don't exist
    if f"{key_prefix}_name" not in st.session_state:
        st.session_state[f"{key_prefix}_name"] = ""
    if f"{key_prefix}_belt" not in st.session_state:
        st.session_state[f"{key_prefix}_belt"] = "White"
    if f"{key_prefix}_age" not in st.session_state:
        st.session_state[f"{key_prefix}_age"] = 30
    if f"{key_prefix}_weight" not in st.session_state:
        st.session_state[f"{key_prefix}_weight"] = 170
    if f"{key_prefix}_fitness_level" not in st.session_state:
        st.session_state[f"{key_prefix}_fitness_level"] = "Average (30th-60th percentile)"
    if f"{key_prefix}_sessions" not in st.session_state:
        st.session_state[f"{key_prefix}_sessions"] = 3
    if f"{key_prefix}_comp" not in st.session_state:
        st.session_state[f"{key_prefix}_comp"] = "None"
    if f"{key_prefix}_art" not in st.session_state:
        st.session_state[f"{key_prefix}_art"] = "None"
        
    # Basic info
    name = st.text_input(
        "Name", 
        value=st.session_state[f"{key_prefix}_name"],
        key=f"{key_prefix}_name"
    )
    
    # Belt rank selection
    belt_options = list(config["belt_rank_scores"].keys())
    bjj_belt_rank = st.selectbox(
        "BJJ Belt Rank", 
        options=belt_options,
        index=belt_options.index(st.session_state[f"{key_prefix}_belt"]) if st.session_state[f"{key_prefix}_belt"] in belt_options else 0,
        key=f"{key_prefix}_belt"
    )
    
    # Create uniform slider layout section
    st.markdown("""<div class="form-row">""", unsafe_allow_html=True)
    
    # Age and Weight sliders in the first row with consistent heights
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""<div class="slider-container">""", unsafe_allow_html=True)
        age_years = st.slider(
            "Age (years)", 
            min_value=16, 
            max_value=70, 
            value=st.session_state[f"{key_prefix}_age"],
            key=f"{key_prefix}_age"
        )
        st.markdown("""</div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""<div class="slider-container">""", unsafe_allow_html=True)
        weight_lbs = st.slider(
            "Weight (lbs)", 
            min_value=100, 
            max_value=350, 
            value=st.session_state[f"{key_prefix}_weight"],
            step=5,
            key=f"{key_prefix}_weight"
        )
        st.markdown("""</div>""", unsafe_allow_html=True)
    
    # Fitness level and training frequency in the second row with consistent heights
    col1, col2 = st.columns(2)
    
    with col1:
        # Fitness assessment with qualitative slider
        fitness_options = [
            "Below Average (<30th percentile)",
            "Average (30th-60th percentile)",
            "Above Average (61st-80th percentile)",
            "Notably Athletic (81st-95th percentile)",
            "Exceptional Athlete (>95th percentile)"
        ]
        
        fitness_level_index = fitness_options.index(st.session_state[f"{key_prefix}_fitness_level"]) if st.session_state[f"{key_prefix}_fitness_level"] in fitness_options else 1
        
        st.markdown("""<div class="slider-container">""", unsafe_allow_html=True)
        fitness_level_numeric = st.slider(
            "Fitness Level",
            min_value=1,
            max_value=5,
            value=fitness_level_index + 1,
            key=f"{key_prefix}_fitness_numeric"
        )
        
        # Convert numeric value to the text option
        fitness_level = fitness_options[fitness_level_numeric - 1]
        st.session_state[f"{key_prefix}_fitness_level"] = fitness_level
        
        # Small label to show the selected fitness level
        st.caption(fitness_level)
        st.markdown("""</div>""", unsafe_allow_html=True)
    
    with col2:
        # Training frequency with slider
        st.markdown("""<div class="slider-container">""", unsafe_allow_html=True)
        bjj_training_sessions_per_week = st.slider(
            "BJJ Training Sessions per Week",
            min_value=0,
            max_value=10,
            value=st.session_state[f"{key_prefix}_sessions"],
            key=f"{key_prefix}_sessions"
        )
        st.markdown("""</div>""", unsafe_allow_html=True)
    
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    # Map qualitative fitness levels to percentile ranges for internal calculations
    fitness_level_mapping = {
        "Below Average (<30th percentile)": 25,
        "Average (30th-60th percentile)": 50,
        "Above Average (61st-80th percentile)": 70,
        "Notably Athletic (81st-95th percentile)": 88,
        "Exceptional Athlete (>95th percentile)": 97
    }
    
    # Set fitness percentile based on selection
    fitness_percentile = fitness_level_mapping[fitness_level]
    
    # Keep the activity level for backward compatibility, but mark as deprecated
    primary_occupation_activity_level = "Moderately Active"  # Default value
    
    # Competition experience
    competition_options = list(config["cef_config"]["competition_level_mapping"].keys())
    bjj_competition_experience_level = st.selectbox(
        "BJJ Competition Experience",
        options=competition_options,
        index=competition_options.index(st.session_state[f"{key_prefix}_comp"]) if st.session_state[f"{key_prefix}_comp"] in competition_options else 0,
        key=f"{key_prefix}_comp"
    )
    
    # Grappling experience with consistent dark theme styling
    st.markdown(f"""
    <div style="margin-top: 20px; margin-bottom: 15px;">
        <div style="background-color: #2a2a2a; border: 1px solid #495057; color: #adb5bd; padding: 12px; border-radius: 6px; margin: 10px 0;">
            Select your experience in other grappling arts. This significantly impacts your JAR score.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Grappling Art selection
    art_options = ["None", "Wrestling", "Judo", "Sambo", "Other"]
    selected_art = st.selectbox(
        "Grappling Art",
        options=art_options,
        index=art_options.index(st.session_state[f"{key_prefix}_art"]) if st.session_state[f"{key_prefix}_art"] in art_options else 0,
        key=f"{key_prefix}_art"
    )
    
    # Process grappling experience
    grappling_experience = []
    
    if selected_art != "None":
        # Define experience options
        experience_options = [
            "Recreational/Limited (<1 year)",
            "Foundational (1-3 years)",
            "Accomplished (3-5+ years, regional level)",
            "High-Level Competitor (National level)",
            "Elite International (Olympic/World level)"
        ]
        
        # Impact mapping
        level_to_effect = {
            "Recreational/Limited (<1 year)": "+3%",
            "Foundational (1-3 years)": "+7%",
            "Accomplished (3-5+ years, regional level)": "+12%",
            "High-Level Competitor (National level)": "+22%",
            "Elite International (Olympic/World level)": "+38%"
        }
        
        # Display the experience level and corresponding multiplier effects side by side
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Experience level selection
            if f"{key_prefix}_exp_level" not in st.session_state:
                st.session_state[f"{key_prefix}_exp_level"] = experience_options[0]
                
            experience_level = st.selectbox(
                "Experience Level",
                options=experience_options,
                index=experience_options.index(st.session_state[f"{key_prefix}_exp_level"]) if st.session_state[f"{key_prefix}_exp_level"] in experience_options else 0,
                key=f"{key_prefix}_exp_level"
            )
        
        with col2:
            # Show the impact of the selected experience level
            if experience_level in level_to_effect:
                st.markdown(f"""
                <div style="background-color: rgba(79, 146, 211, 0.15); padding: 12px; border-radius: 6px; margin-top: 24px; border: 1px solid #495057;">
                    <p style="margin: 0; text-align: center; font-weight: bold; font-size: 1.1em; color: #4f92d3;">
                        Score Impact: {level_to_effect[experience_level]}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        # Add the experience to the list
        grappling_experience = [{
            "art_name": selected_art,
            "experience_level_descriptor": experience_level
        }]
    
    # Create PractitionerData object
    practitioner_id = str(uuid.uuid4())
    
    try:
        # Cast string types to their proper Literal types
        belt_rank = cast(BeltRank, bjj_belt_rank)
        activity_level = cast(ActivityLevel, primary_occupation_activity_level)
        competition_level = cast(CompetitionLevel, bjj_competition_experience_level)
        
        practitioner_data = PractitionerData(
            name=name,
            bjj_belt_rank=belt_rank,
            age_years=age_years,
            weight_lbs=float(weight_lbs),
            primary_occupation_activity_level=activity_level,
            standardized_fitness_test_percentile_estimate=fitness_percentile,
            other_grappling_art_experience=grappling_experience,
            bjj_training_sessions_per_week=bjj_training_sessions_per_week,
            bjj_competition_experience_level=competition_level,
            practitioner_id=practitioner_id
        )
        
        return practitioner_data
        
    except ValueError as e:
        st.error(f"Invalid input: {e}")
        # Return a default practitioner data to avoid errors
        return create_default_practitioner(practitioner_id)


def create_default_practitioner(practitioner_id: str) -> PractitionerData:
    """
    Create a default practitioner with valid values.
    
    Args:
        practitioner_id: Unique identifier for the practitioner
        
    Returns:
        Default PractitionerData object
    """
    return PractitionerData(
        name="Default Practitioner",
        bjj_belt_rank="White",
        age_years=30,
        weight_lbs=170.0,
        primary_occupation_activity_level="Moderately Active",
        standardized_fitness_test_percentile_estimate=50,
        other_grappling_art_experience=[],
        bjj_training_sessions_per_week=3,
        bjj_competition_experience_level="None",
        practitioner_id=practitioner_id
    )