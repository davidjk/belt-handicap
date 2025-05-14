import streamlit as st
import os
import json
from jar.types import PractitionerData, FactorResults, RollDynamicsProfile
from jar.config import JARConfig, load_config, save_config
from jar.calculator import Calculator
from jar.profiles import ProfileGenerator
from ui.input_forms import render_practitioner_form
from ui.visualizations import render_factor_visualization, render_comparison_visualization
from ui.profile_display import render_profile, render_profile_comparison

def main():
    """
    Main Streamlit application entry point.
    """
    # Configure the page with built-in dark theme
    st.set_page_config(
        page_title="JAR System",
        page_icon="🥋",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "# JAR System\nJiu-Jitsu Attribute Rating for comparing practitioners"
        }
    )
    
    # Use Streamlit's built-in theming with minimal customizations
    st.markdown("""
    <style>
    /* Custom styles that preserve the built-in dark theme while adding our specific UI needs */
    .section-title {
        font-size: 1.8em;
        font-weight: 500;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(250, 250, 250, 0.2);
    }
    
    .practitioner-heading {
        font-size: 1.2rem;
        font-weight: 400;
        color: rgba(250, 250, 250, 0.6);
        letter-spacing: 0.5px;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* Create wrapper for same-height sliders */
    .slider-container {
        display: flex;
        flex-direction: column;
        height: 80px;
    }
    
    /* Styles for profile assessment items */
    .assessment-item {
        transition: transform 0.2s;
    }
    
    .assessment-item:hover {
        transform: translateY(-2px);
    }
    
    /* Make expanders and info boxes consistent with theme */
    .streamlit-expanderContent {
        border-top: 1px solid rgba(250, 250, 250, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Activate dark mode
    st.markdown("""
        <script>
            var elements = window.parent.document.querySelectorAll('.sidebar-content');
            var theme = elements[elements.length - 1];
            theme.click();
            theme.children[0].click();
        </script>
    """, unsafe_allow_html=True)
    
    st.title("Jiu-Jitsu Attribute Rating (JAR) System")
    
    # Initialize session state for storing data between interactions
    if "config" not in st.session_state:
        config_path = os.path.join(os.path.dirname(__file__), "data", "default_config.json")
        try:
            st.session_state.config = load_config(config_path)
        except (FileNotFoundError, ValueError) as e:
            st.error(f"Error loading configuration: {e}")
            return
    
    # Create core system components
    calculator = Calculator(st.session_state.config)
    profile_generator = ProfileGenerator(st.session_state.config)
    
    # Just show the comparison view by default
    compare_practitioners_view(calculator, profile_generator)
    
    # Add About and Configuration in tabs below the main content
    st.markdown('<div class="section-title" style="margin-top: 40px;">Additional Information</div>', unsafe_allow_html=True)
    about_tab, config_tab = st.tabs(["About JAR System", "Configuration"])
    
    with about_tab:
        about_view()
        
    with config_tab:
        configuration_view()


def compare_practitioners_view(calculator: Calculator, profile_generator: ProfileGenerator):
    """
    View for comparing two practitioners.
    
    Args:
        calculator: JAR system calculator
        profile_generator: Profile generator
    """
    st.markdown('<div class="section-title">JAR System Analysis</div>', unsafe_allow_html=True)
    
    # Initialize session state for saved practitioners if not exists
    if "saved_pairs" not in st.session_state:
        st.session_state.saved_pairs = {}
    
    # Add pair management UI
    with st.expander("Saved Practitioner Pairs", expanded=False):
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            pair_name = st.text_input("Pair Name", key="new_pair_name")
        
        with col2:
            save_pair = st.button("Save Current")
        
        with col3:
            clear_pairs = st.button("Clear All")
            
        # Display saved pairs for selection
        if st.session_state.saved_pairs:
            selected_pair = st.selectbox(
                "Select a saved pair",
                options=[""] + list(st.session_state.saved_pairs.keys()),
                index=0
            )
            
            if selected_pair and st.button("Load Selected Pair"):
                # Load the selected pair into the form
                st.session_state.practitioner_a_name = st.session_state.saved_pairs[selected_pair]["a"]["name"]
                st.session_state.practitioner_a_belt = st.session_state.saved_pairs[selected_pair]["a"]["belt"]
                st.session_state.practitioner_a_age = st.session_state.saved_pairs[selected_pair]["a"]["age"]
                st.session_state.practitioner_a_weight = st.session_state.saved_pairs[selected_pair]["a"]["weight"]
                st.session_state.practitioner_a_fitness = st.session_state.saved_pairs[selected_pair]["a"]["fitness"]
                st.session_state.practitioner_a_sessions = st.session_state.saved_pairs[selected_pair]["a"]["sessions"]
                st.session_state.practitioner_a_competition = st.session_state.saved_pairs[selected_pair]["a"]["competition"]
                
                st.session_state.practitioner_b_name = st.session_state.saved_pairs[selected_pair]["b"]["name"]
                st.session_state.practitioner_b_belt = st.session_state.saved_pairs[selected_pair]["b"]["belt"]
                st.session_state.practitioner_b_age = st.session_state.saved_pairs[selected_pair]["b"]["age"]
                st.session_state.practitioner_b_weight = st.session_state.saved_pairs[selected_pair]["b"]["weight"]
                st.session_state.practitioner_b_fitness = st.session_state.saved_pairs[selected_pair]["b"]["fitness"]
                st.session_state.practitioner_b_sessions = st.session_state.saved_pairs[selected_pair]["b"]["sessions"]
                st.session_state.practitioner_b_competition = st.session_state.saved_pairs[selected_pair]["b"]["competition"]
                
                st.rerun()
        
        if not st.session_state.saved_pairs:
            st.info("No saved pairs yet. Fill out both forms and save them.")
            
        if clear_pairs:
            st.session_state.saved_pairs = {}
            st.rerun()
    
    # Create two columns for practitioner inputs
    col1, col2 = st.columns(2)
    
    # Initialize placeholder scores in session state
    if "score_a" not in st.session_state:
        st.session_state.score_a = 0
    if "score_b" not in st.session_state:
        st.session_state.score_b = 0
    if "factors_a" not in st.session_state:
        st.session_state.factors_a = None
    if "factors_b" not in st.session_state:
        st.session_state.factors_b = None
        
    # Define the fitness level mapping for score calculation
    fitness_level_mapping = {
        "Below Average (<30th percentile)": 25,
        "Average (30th-60th percentile)": 50,
        "Above Average (61st-80th percentile)": 70,
        "Notably Athletic (81st-95th percentile)": 88,
        "Exceptional Athlete (>95th percentile)": 97
    }
    
    # Function to calculate and display scores reactively
    def update_scores():
        try:
            # Create a new calculator
            calculator = Calculator(st.session_state.config)
            
            # Create practitioner objects based on current session state
            practitioner_a = PractitionerData(
                name=st.session_state.practitioner_a_name if "practitioner_a_name" in st.session_state else "",
                bjj_belt_rank=st.session_state.practitioner_a_belt if "practitioner_a_belt" in st.session_state else "White",
                age_years=st.session_state.practitioner_a_age if "practitioner_a_age" in st.session_state else 30,
                weight_lbs=float(st.session_state.practitioner_a_weight) if "practitioner_a_weight" in st.session_state else 170.0,
                primary_occupation_activity_level="Moderately Active",
                standardized_fitness_test_percentile_estimate=(
                    fitness_level_mapping[st.session_state.practitioner_a_fitness_level] 
                    if "practitioner_a_fitness_level" in st.session_state else 50
                ),
                other_grappling_art_experience=(
                    [{"art_name": st.session_state.practitioner_a_art, 
                      "experience_level_descriptor": st.session_state.practitioner_a_exp_level}] 
                    if "practitioner_a_art" in st.session_state and st.session_state.practitioner_a_art != "None" 
                    else []
                ),
                bjj_training_sessions_per_week=st.session_state.practitioner_a_sessions if "practitioner_a_sessions" in st.session_state else 3,
                bjj_competition_experience_level=st.session_state.practitioner_a_comp if "practitioner_a_comp" in st.session_state else "None",
                practitioner_id="a"
            )
            
            practitioner_b = PractitionerData(
                name=st.session_state.practitioner_b_name if "practitioner_b_name" in st.session_state else "",
                bjj_belt_rank=st.session_state.practitioner_b_belt if "practitioner_b_belt" in st.session_state else "White",
                age_years=st.session_state.practitioner_b_age if "practitioner_b_age" in st.session_state else 30,
                weight_lbs=float(st.session_state.practitioner_b_weight) if "practitioner_b_weight" in st.session_state else 170.0,
                primary_occupation_activity_level="Moderately Active",
                standardized_fitness_test_percentile_estimate=(
                    fitness_level_mapping[st.session_state.practitioner_b_fitness_level] 
                    if "practitioner_b_fitness_level" in st.session_state else 50
                ),
                other_grappling_art_experience=(
                    [{"art_name": st.session_state.practitioner_b_art, 
                      "experience_level_descriptor": st.session_state.practitioner_b_exp_level}] 
                    if "practitioner_b_art" in st.session_state and st.session_state.practitioner_b_art != "None" 
                    else []
                ),
                bjj_training_sessions_per_week=st.session_state.practitioner_b_sessions if "practitioner_b_sessions" in st.session_state else 3,
                bjj_competition_experience_level=st.session_state.practitioner_b_comp if "practitioner_b_comp" in st.session_state else "None",
                practitioner_id="b"
            )
            
            # Calculate factors and scores
            factors_a = calculator.calculate_all_factors(practitioner_a, practitioner_b)
            hs_a = factors_a.calculate_handicapped_score()
            
            factors_b = calculator.calculate_all_factors(practitioner_b, practitioner_a)
            hs_b = factors_b.calculate_handicapped_score()
            
            # Store in session state
            st.session_state.score_a = hs_a
            st.session_state.score_b = hs_b
            st.session_state.factors_a = factors_a
            st.session_state.factors_b = factors_b
            
            st.experimental_rerun()
        except Exception as e:
            print(f"Error updating scores: {e}")
            pass
    
    # Calculate initial scores if they haven't been calculated yet
    if st.session_state.score_a == 0 and st.session_state.score_b == 0:
        update_scores()
    
    with col1:
        # Display score centered above the practitioner container
        st.markdown(
            f'<div style="text-align: center; margin-bottom: 20px;">'
            f'<h2 style="font-size: 3.5rem; margin: 0; color: #4f92d3;">Score: {st.session_state.score_a:.1f}</h2>'
            f'</div>',
            unsafe_allow_html=True
        )
        st.markdown('<div class="practitioner-heading">Practitioner A</div>', unsafe_allow_html=True)
        practitioner_a = render_practitioner_form("practitioner_a", st.session_state.config, 
                                                 score_factors=st.session_state.factors_a,
                                                 on_change=update_scores)
    
    with col2:
        # Display score centered above the practitioner container
        st.markdown(
            f'<div style="text-align: center; margin-bottom: 20px;">'
            f'<h2 style="font-size: 3.5rem; margin: 0; color: #4f92d3;">Score: {st.session_state.score_b:.1f}</h2>'
            f'</div>',
            unsafe_allow_html=True
        )
        st.markdown('<div class="practitioner-heading">Practitioner B</div>', unsafe_allow_html=True)
        practitioner_b = render_practitioner_form("practitioner_b", st.session_state.config, 
                                                 score_factors=st.session_state.factors_b,
                                                 on_change=update_scores)
    
    compare_button = st.button("Compare Practitioners")
    
    # Save the current pair if requested
    if save_pair and pair_name:
        st.session_state.saved_pairs[pair_name] = {
            "a": {
                "name": practitioner_a.name,
                "belt": practitioner_a.bjj_belt_rank,
                "age": practitioner_a.age_years,
                "weight": practitioner_a.weight_lbs,
                "fitness": practitioner_a.standardized_fitness_test_percentile_estimate,
                "sessions": practitioner_a.bjj_training_sessions_per_week,
                "competition": practitioner_a.bjj_competition_experience_level
            },
            "b": {
                "name": practitioner_b.name,
                "belt": practitioner_b.bjj_belt_rank,
                "age": practitioner_b.age_years,
                "weight": practitioner_b.weight_lbs,
                "fitness": practitioner_b.standardized_fitness_test_percentile_estimate,
                "sessions": practitioner_b.bjj_training_sessions_per_week,
                "competition": practitioner_b.bjj_competition_experience_level
            }
        }
        st.success(f"Pair '{pair_name}' saved!")
    
    if compare_button:
        # Calculate factors and HS for both
        factors_a = calculator.calculate_all_factors(practitioner_a, practitioner_b)
        hs_a = factors_a.calculate_handicapped_score()
        
        factors_b = calculator.calculate_all_factors(practitioner_b, practitioner_a)
        hs_b = factors_b.calculate_handicapped_score()
        
        # Generate profiles
        profile_a = profile_generator.generate_profile(practitioner_a, factors_a, hs_a)
        profile_b = profile_generator.generate_profile(practitioner_b, factors_b, hs_b)
        
        # Display visualization comparison
        render_comparison_visualization(factors_a, factors_b, hs_a, hs_b, st.session_state.config)
        
        # Display profile comparison
        render_profile_comparison(profile_a, profile_b)

def about_view():
    """View for displaying information about the JAR system."""
    
    st.markdown("""
    ## Jiu-Jitsu Attribute Rating (JAR) System

    The JAR system is a conceptual framework designed to provide a more nuanced understanding of 
    practitioner matchups in Brazilian Jiu-Jitsu (BJJ), moving beyond sole reliance on belt rank.
    
    ### Purpose:
    - To calculate a relative Handicapped Score (HS) for individual BJJ practitioners based on a range of attributes.
    - To generate a Roll Dynamics Profile that offers qualitative insights into potential matchup dynamics.
    - To serve as a tool for practitioners, instructors, and analysts to facilitate more informed discussions.
    - To help in setting appropriate training challenges and managing expectations for sparring sessions.
    
    ### System Components:
    - **Belt Rank Score (BRS)**: Foundational score representing accumulated BJJ-specific skill
    - **Age Factor (AF)**: Accounts for age-related physiological factors
    - **Weight/Size Factor (WF)**: Reflects the impact of weight differences
    - **Athleticism & Conditioning Factor (ACF)**: Quantifies general physical prowess
    - **Relevant Grappling Experience Factor (REF)**: Credits transferable skills from other disciplines
    - **Training Intensity/Frequency Factor (TFF)**: Reflects current BJJ training volume
    - **BJJ Competition Experience Factor (CEF)**: Accounts for competition-specific skills
    
    The JAR system is NOT designed to definitively predict winners or losers but rather to contextualize 
    potential performance based on a broader set of factors.
    """)
    
    
    st.markdown("""
    ### How to Use This App:
    
    #### Single Practitioner Analysis
    1. Enter the practitioner's details
    2. Click "Calculate Score" to see their Handicapped Score and profile
    3. Review the factor breakdown to understand which attributes are contributing most
    
    #### Compare Practitioners
    1. Enter details for both practitioners
    2. Click "Compare" to see a side-by-side analysis
    3. Review the matchup assessment for insights on how the roll might unfold
    
    #### Configuration
    The system is fully configurable. Advanced users can modify parameters like:
    - Belt rank scores
    - Age factor calculations
    - Weight difference impact
    - Other factor multipliers
    
    ### Disclaimer
    This is a conceptual tool meant to enhance understanding and discussion, not to replace 
    actual mat experience or coach assessment. Many intangible factors affect BJJ performance 
    that cannot be fully quantified.
    """)

def configuration_view():
    """View for editing system configuration."""
    
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
    
    with st.expander("Weight Factor Configuration"):
        config["weight_factor_config"]["increment_lbs"] = st.number_input(
            "Weight Increment (lbs)",
            min_value=1.0,
            max_value=50.0,
            value=float(config["weight_factor_config"]["increment_lbs"]),
            step=1.0
        )
        
        st.subheader("Weight Difference Thresholds")
        for i, tier in enumerate(config["weight_factor_config"]["thresholds_bonuses_penalties"]):
            col1, col2 = st.columns(2)
            with col1:
                tier["diff_max_lbs"] = st.number_input(
                    f"Tier {i+1} Max Difference (lbs)",
                    min_value=float(0 if i == 0 else config["weight_factor_config"]["thresholds_bonuses_penalties"][i-1]["diff_max_lbs"]),
                    value=float(tier["diff_max_lbs"]),
                    step=5.0
                )
            with col2:
                tier["adjustment"] = st.number_input(
                    f"Tier {i+1} Adjustment Factor",
                    min_value=0.01,
                    max_value=0.5,
                    value=float(tier["adjustment"]),
                    step=0.01
                )
    
    # Add more configuration sections as needed
    
    if st.button("Save Configuration"):
        try:
            if not os.path.exists("data"):
                os.makedirs("data")
                
            config_path = os.path.join(os.path.dirname(__file__), "data", "user_config.json")
            save_config(config, config_path)
                
            st.success("Configuration saved!")
        except Exception as e:
            st.error(f"Error saving configuration: {e}")

if __name__ == "__main__":
    main()