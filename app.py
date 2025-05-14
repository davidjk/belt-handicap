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
    st.set_page_config(
        page_title="JAR System",
        page_icon="🥋",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Add the dark theme configuration to session state for persistence
    if "css_injected" not in st.session_state:
        st.session_state.css_injected = True
    
        # Set dark theme CSS
        st.markdown("""
        <style>
        /* Modern, harmonious color palette optimized for dark theme */
        html {
            --primary-color: #4f92d3;
            --primary-light: rgba(79, 146, 211, 0.15);
            --accent-positive: #4db380;
            --accent-positive-light: rgba(77, 179, 128, 0.15);
            --accent-negative: #e05a45;
            --accent-negative-light: rgba(224, 90, 69, 0.15);
            --accent-neutral: #d8b24b;
            --accent-neutral-light: rgba(216, 178, 75, 0.15);
            --text-bright: #e9ecef;
            --text-medium: #adb5bd;
            --text-dim: #6c757d;
            --border-color: #495057;
            --background-main: #1a1a1a;
            --background-card: #222222;
            --background-elevated: #2a2a2a;
            --background-highlight: #333333;
        }
        
        /* Force dark theme on all elements */
        body {
            background-color: #1a1a1a !important;
            color: #e9ecef !important;
        }
        
        /* Global styles for dark theme */
        .main, .stApp, .css-18e3th9, .css-1d391kg, [data-testid="stAppViewContainer"], 
        [data-testid="stAppViewContainer"] .main {
            background-color: #1a1a1a !important;
            color: #e9ecef !important;
        }
        
        /* Forcefully override light theme and make all content containers dark */
        div.stBlock, div.row-widget, div.block-container, div.element-container, div.stTabs,
        div[data-testid="stDecoration"], div[data-testid="stToolbar"], div[data-testid="baseButton-secondary"],
        div.stToolbar, div[data-testid="stHeader"], [data-testid="stHeader"],
        div[data-testid="stVerticalBlock"], div[data-testid="stHorizontalBlock"] {
            background-color: #1a1a1a !important;
            border-color: #495057 !important;
            color: #e9ecef !important;
        }
        
        /* All form inputs and containers match the dark theme */
        .stTextInput input, 
        .stNumberInput input, 
        .stSelectbox > div,
        .stSlider > div,
        .stTextArea textarea,
        div[data-baseweb="select"] > div,
        div[data-baseweb="base-input"],
        [data-baseweb="input"] input {
            background-color: #2a2a2a !important;
            border: 1px solid #495057 !important;
            border-radius: 6px !important;
            color: #e9ecef !important;
        }
        
        /* Make select dropdown styling nicer in dark theme */
        div[data-baseweb="select"] > div,
        div[role="listbox"],
        div[data-baseweb="menu"],
        div[data-baseweb="popover"],
        div[role="option"] {
            background-color: #2a2a2a !important;
            color: #e9ecef !important;
            border-color: #495057 !important;
        }
        
        div[data-baseweb="popover"] div {
            background-color: #2a2a2a !important;
            color: #e9ecef !important;
        }
        
        div[data-testid="stMarkdownContainer"] > div {
            background-color: transparent !important;
        }
        
        /* Consistent form heading styles */
        h1, h2, h3, .css-10trblm, .css-zt5igj {
            color: #4f92d3 !important;
            font-weight: 500 !important;
        }
        
        h4, h5, h6 {
            color: #e9ecef !important;
            font-weight: 500 !important;
        }
        
        /* Override the stSubheader styling for dark theme */
        div[data-testid="stSubheader"] {
            color: #adb5bd !important;
            font-weight: 500 !important;
            font-size: 1.1rem !important;
            padding-top: 0.5rem !important;
            margin-bottom: 1rem !important;
        }
        
        /* Better styled tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px !important;
            border-bottom: 1px solid #495057 !important;
            background-color: #1a1a1a !important;
        }
        
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            color: #adb5bd !important;
        }
        
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] [data-testid="stMarkdownContainer"] p {
            color: #4f92d3 !important;
        }
        
        /* Better buttons */
        .stButton > button {
            background-color: #4f92d3 !important;
            color: white !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 0.6rem 1.7rem !important;
            font-weight: 500 !important;
            transition: all 0.2s !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
        }
        
        .stButton > button:hover {
            background-color: #3d77b0 !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
        }
        
        /* Make slider thumbs visible in dark theme */
        .stSlider [data-baseweb="slider"] div[role="slider"] {
            background-color: #4f92d3 !important;
            border-color: #4f92d3 !important;
        }
        
        /* Make slider rails match theme */
        .stSlider [data-baseweb="slider"] div {
            background-color: #495057 !important;
        }
        
        .stSlider [data-baseweb="slider"] div[role="progressbar"] {
            background-color: #4f92d3 !important;
        }
        
        /* Add light separator borders around interface sections */
        .interface-section {
            border-bottom: 1px solid #495057 !important;
            padding-bottom: 1.5rem !important;
            margin-bottom: 1.5rem !important;
        }
        
        /* Custom header format for section titles in dark theme */
        .section-title {
            font-size: 1.8em !important;
            font-weight: 500 !important;
            margin: 1.5rem 0 1rem 0 !important;
            padding-bottom: 0.5rem !important;
            border-bottom: 1px solid #495057 !important;
            color: #4f92d3 !important;
            background-color: #1a1a1a !important;
        }
        
        /* Practitioner heading styles */
        .practitioner-heading {
            color: #adb5bd !important;
            font-size: 1.2rem !important;
            font-weight: 400 !important;
            letter-spacing: 0.5px !important;
            border-bottom: none !important;
            padding-bottom: 0.5rem !important;
            margin-bottom: 1rem !important;
            background-color: #1a1a1a !important;
        }
        
        /* Fix for information boxes */
        .info-box {
            background-color: #2a2a2a !important;
            border: 1px solid #495057 !important;
            color: #adb5bd !important;
            padding: 12px !important;
            border-radius: 6px !important;
            margin: 10px 0 !important;
        }
        
        /* Make expanders match theme */
        .streamlit-expanderHeader {
            background-color: #2a2a2a !important;
            color: #adb5bd !important;
        }
        
        .streamlit-expanderContent {
            background-color: #222222 !important;
            border-top: 1px solid #495057 !important;
            color: #e9ecef !important;
        }
        
        /* Add consistent form field height and spacing */
        .form-field-container {
            margin-bottom: 1.2rem !important;
        }
        
        /* Create wrapper for same-height sliders */
        .slider-container {
            display: flex;
            flex-direction: column;
            height: 80px;
        }
        
        /* Fix any white text on white background issues */
        div.stMarkdown, div.stText, p, span, div {
            color: #e9ecef !important;
            background-color: transparent !important;
        }
        
        /* Fix matplotlib outputs */
        .stMarkdown img, [data-testid="stImage"] img {
            background-color: #222222 !important;
        }
        
        /* Fix dataframes */
        .dataframe {
            color: #e9ecef !important;
        }
        
        .dataframe tbody tr {
            background-color: #222222 !important;
        }
        
        .dataframe tbody tr:nth-child(odd) {
            background-color: #2a2a2a !important;
        }
        
        .dataframe thead tr {
            background-color: #333333 !important;
        }
        
        /* Fix metric */
        [data-testid="stMetricValue"] {
            background-color: transparent !important;
            color: #4f92d3 !important;
            font-weight: bold !important;
        }
        
        /* Force our dark theme on all elements, including ones added later */
        *, *:before, *:after {
            color-scheme: dark !important;
        }
        </style>
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
    
    with col1:
        st.markdown('<div class="practitioner-heading">Practitioner A</div>', unsafe_allow_html=True)
        practitioner_a = render_practitioner_form("practitioner_a", st.session_state.config)
    
    with col2:
        st.markdown('<div class="practitioner-heading">Practitioner B</div>', unsafe_allow_html=True)
        practitioner_b = render_practitioner_form("practitioner_b", st.session_state.config)
    
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
    
    st.image("https://images.unsplash.com/photo-1609710228159-0fa9bd7c0827?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&h=600&q=80", 
             caption="Brazilian Jiu-Jitsu training", use_column_width=True)
    
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