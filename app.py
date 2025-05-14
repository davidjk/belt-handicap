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

# Setup for persistent storage of saved practitioners
practitioners_path = os.path.join(os.path.dirname(__file__), "data", "saved_practitioners.json")

# Function to save practitioners to disk
def save_practitioners_to_disk():
    try:
        # Ensure data directory exists
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        # Convert dict keys to strings to ensure JSON serialization works
        serializable_practitioners = {}
        for key, value in st.session_state.saved_practitioners.items():
            serializable_practitioners[str(key)] = value
            
        with open(practitioners_path, 'w') as f:
            json.dump(serializable_practitioners, f, indent=2)
    except Exception as e:
        st.error(f"Error saving practitioners: {e}")

# Function to load practitioners from disk
def load_practitioners_from_disk():
    try:
        if os.path.exists(practitioners_path):
            with open(practitioners_path, 'r') as f:
                loaded_practitioners = json.load(f)
                # Log successful load
                print(f"Successfully loaded {len(loaded_practitioners)} saved practitioners")
                return loaded_practitioners
        else:
            print("No saved practitioners file found, starting with empty practitioners")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding saved practitioners JSON: {e}")
        # If the file is corrupted, create a backup
        if os.path.exists(practitioners_path):
            backup_path = practitioners_path + ".backup"
            try:
                import shutil
                shutil.copy2(practitioners_path, backup_path)
                print(f"Created backup of corrupted practitioners file at {backup_path}")
            except Exception as backup_error:
                print(f"Failed to create backup: {backup_error}")
        return {}
    except Exception as e:
        print(f"Error loading saved practitioners: {e}")
        return {}

def load_practitioner_a(practitioner_name):
    """Load a saved practitioner into the A slot."""
    print(f"\n----- LOADING PRACTITIONER A: {practitioner_name} -----")
    
    # Log keys that start with practitioner_a_ before loading
    print("BEFORE LOADING - Practitioner A session state keys:")
    for key in st.session_state:
        if key.startswith("practitioner_a_"):
            print(f"  {key}: {st.session_state[key]}")
    
    if practitioner_name in st.session_state.saved_practitioners:
        data = st.session_state.saved_practitioners[practitioner_name]
        print(f"Loading data from saved_practitioners: {data}")
        
        # First, clear any existing practitioner A data to prevent contamination
        # This ensures we don't have lingering values from a previous practitioner
        to_remove = []
        for key in st.session_state:
            if key.startswith("practitioner_a_"):
                to_remove.append(key)
        
        for key in to_remove:
            del st.session_state[key]
        
        # Save the original loaded practitioner state in a special key
        # This will be used to restore values if they get overwritten
        st.session_state.loaded_practitioner_a = {}
            
        # Store all loaded values in this special key
        st.session_state.loaded_practitioner_a["name"] = data["name"]
        st.session_state.loaded_practitioner_a["belt"] = data["belt"]
        st.session_state.loaded_practitioner_a["age"] = data["age"]
        st.session_state.loaded_practitioner_a["weight"] = int(data["weight"])
        
        # Save the raw fitness value from the data
        st.session_state.loaded_practitioner_a["fitness"] = data["fitness"]
        print(f"Saved raw fitness value for A: {data['fitness']}")
        
        # Convert fitness score to readable format
        fitness_level = {
            25: "Below Average (<30th percentile)",
            50: "Average (30th-60th percentile)",
            70: "Above Average (61st-80th percentile)", 
            88: "Notably Athletic (81st-95th percentile)",
            97: "Exceptional Athlete (>95th percentile)"
        }.get(data["fitness"], "Average (30th-60th percentile)")
        
        st.session_state.loaded_practitioner_a["fitness_level"] = fitness_level
        st.session_state.loaded_practitioner_a["sessions"] = data["sessions"]
        st.session_state.loaded_practitioner_a["comp"] = data["competition"]
        
        # Set the numeric value for fitness slider
        fitness_options = [
            "Below Average (<30th percentile)",
            "Average (30th-60th percentile)",
            "Above Average (61st-80th percentile)",
            "Notably Athletic (81st-95th percentile)",
            "Exceptional Athlete (>95th percentile)"
        ]
        try:
            fitness_index = fitness_options.index(fitness_level)
            st.session_state.loaded_practitioner_a["fitness_numeric"] = fitness_index + 1
        except ValueError:
            st.session_state.loaded_practitioner_a["fitness_numeric"] = 2  # Default to average
        
        # Handle grappling art experience
        if "art" in data:
            st.session_state.loaded_practitioner_a["art"] = data["art"]
            if data["art"] != "None" and "exp_level" in data:
                st.session_state.loaded_practitioner_a["exp_level"] = data["exp_level"]
                
        # Now, also set the actual form fields
        st.session_state.practitioner_a_name = data["name"]
        st.session_state.practitioner_a_belt = data["belt"]
        st.session_state.practitioner_a_age = data["age"]
        st.session_state.practitioner_a_weight = int(data["weight"])
        st.session_state.practitioner_a_fitness_level = fitness_level
        st.session_state.practitioner_a_sessions = data["sessions"]
        st.session_state.practitioner_a_comp = data["competition"]
        
        try:
            st.session_state.practitioner_a_fitness_numeric = fitness_index + 1
        except:
            st.session_state.practitioner_a_fitness_numeric = 2
            
        if "art" in data:
            st.session_state.practitioner_a_art = data["art"]
            if data["art"] != "None" and "exp_level" in data:
                st.session_state.practitioner_a_exp_level = data["exp_level"]
        
        # Log keys that start with practitioner_a_ after loading
        print("AFTER LOADING - Practitioner A session state keys:")
        for key in st.session_state:
            if key.startswith("practitioner_a_"):
                print(f"  {key}: {st.session_state[key]}")
        
        print("----- FINISHED LOADING PRACTITIONER A -----\n")
        return True
    return False

def load_practitioner_b(practitioner_name):
    """Load a saved practitioner into the B slot."""
    print(f"\n----- LOADING PRACTITIONER B: {practitioner_name} -----")
    
    # Log keys that start with practitioner_b_ before loading
    print("BEFORE LOADING - Practitioner B session state keys:")
    for key in st.session_state:
        if key.startswith("practitioner_b_"):
            print(f"  {key}: {st.session_state[key]}")
    
    # Also log keys for practitioner A to see if they change
    print("BEFORE LOADING B - Practitioner A session state keys:")
    for key in st.session_state:
        if key.startswith("practitioner_a_"):
            print(f"  {key}: {st.session_state[key]}")
    
    if practitioner_name in st.session_state.saved_practitioners:
        data = st.session_state.saved_practitioners[practitioner_name]
        print(f"Loading data from saved_practitioners: {data}")
        
        # First, clear any existing practitioner B data to prevent contamination
        # This ensures we don't have lingering values from a previous practitioner
        to_remove = []
        for key in st.session_state:
            if key.startswith("practitioner_b_"):
                to_remove.append(key)
        
        for key in to_remove:
            del st.session_state[key]
        
        # Save the original loaded practitioner state in a special key
        # This will be used to restore values if they get overwritten
        st.session_state.loaded_practitioner_b = {}
            
        # Store all loaded values in this special key
        st.session_state.loaded_practitioner_b["name"] = data["name"]
        st.session_state.loaded_practitioner_b["belt"] = data["belt"]
        st.session_state.loaded_practitioner_b["age"] = data["age"]
        st.session_state.loaded_practitioner_b["weight"] = int(data["weight"])
        
        # Save the raw fitness value from the data
        st.session_state.loaded_practitioner_b["fitness"] = data["fitness"]
        print(f"Saved raw fitness value for B: {data['fitness']}")
        
        # Convert fitness score to readable format
        fitness_level = {
            25: "Below Average (<30th percentile)",
            50: "Average (30th-60th percentile)",
            70: "Above Average (61st-80th percentile)", 
            88: "Notably Athletic (81st-95th percentile)",
            97: "Exceptional Athlete (>95th percentile)"
        }.get(data["fitness"], "Average (30th-60th percentile)")
        
        st.session_state.loaded_practitioner_b["fitness_level"] = fitness_level
        st.session_state.loaded_practitioner_b["sessions"] = data["sessions"]
        st.session_state.loaded_practitioner_b["comp"] = data["competition"]
        
        # Set the numeric value for fitness slider
        fitness_options = [
            "Below Average (<30th percentile)",
            "Average (30th-60th percentile)",
            "Above Average (61st-80th percentile)",
            "Notably Athletic (81st-95th percentile)",
            "Exceptional Athlete (>95th percentile)"
        ]
        try:
            fitness_index = fitness_options.index(fitness_level)
            st.session_state.loaded_practitioner_b["fitness_numeric"] = fitness_index + 1
        except ValueError:
            st.session_state.loaded_practitioner_b["fitness_numeric"] = 2  # Default to average
        
        # Handle grappling art experience
        if "art" in data:
            st.session_state.loaded_practitioner_b["art"] = data["art"]
            if data["art"] != "None" and "exp_level" in data:
                st.session_state.loaded_practitioner_b["exp_level"] = data["exp_level"]
                
        # Now, also set the actual form fields
        st.session_state.practitioner_b_name = data["name"]
        st.session_state.practitioner_b_belt = data["belt"]
        st.session_state.practitioner_b_age = data["age"]
        st.session_state.practitioner_b_weight = int(data["weight"])
        st.session_state.practitioner_b_fitness_level = fitness_level
        st.session_state.practitioner_b_sessions = data["sessions"]
        st.session_state.practitioner_b_comp = data["competition"]
        
        try:
            st.session_state.practitioner_b_fitness_numeric = fitness_index + 1
        except:
            st.session_state.practitioner_b_fitness_numeric = 2
            
        if "art" in data:
            st.session_state.practitioner_b_art = data["art"]
            if data["art"] != "None" and "exp_level" in data:
                st.session_state.practitioner_b_exp_level = data["exp_level"]
        
        # Log keys that start with practitioner_b_ after loading
        print("AFTER LOADING - Practitioner B session state keys:")
        for key in st.session_state:
            if key.startswith("practitioner_b_"):
                print(f"  {key}: {st.session_state[key]}")
        
        # Also log keys for practitioner A to see if they changed
        print("AFTER LOADING B - Practitioner A session state keys:")
        for key in st.session_state:
            if key.startswith("practitioner_a_"):
                print(f"  {key}: {st.session_state[key]}")
        
        print("----- FINISHED LOADING PRACTITIONER B -----\n")
        return True
    return False

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
        print("\n----- UPDATING SCORES -----")
        
        # Ensure loaded values are restored if needed
        loaded_key_a = "loaded_practitioner_a"
        if loaded_key_a in st.session_state:
            for field, value in st.session_state[loaded_key_a].items():
                field_key = f"practitioner_a_{field}"
                if field_key not in st.session_state or not st.session_state[field_key]:
                    print(f"RESTORING from loaded_practitioner_a: {field_key} = {value}")
                    st.session_state[field_key] = value
                    
        loaded_key_b = "loaded_practitioner_b"
        if loaded_key_b in st.session_state:
            for field, value in st.session_state[loaded_key_b].items():
                field_key = f"practitioner_b_{field}"
                if field_key not in st.session_state or not st.session_state[field_key]:
                    print(f"RESTORING from loaded_practitioner_b: {field_key} = {value}")
                    st.session_state[field_key] = value
        
        # Log the state of session variables for both practitioners
        print("PRACTITIONER A SESSION STATE BEFORE UPDATE:")
        for key in st.session_state:
            if key.startswith("practitioner_a_"):
                print(f"  {key}: {st.session_state[key]}")
                
        print("\nPRACTITIONER B SESSION STATE BEFORE UPDATE:")
        for key in st.session_state:
            if key.startswith("practitioner_b_"):
                print(f"  {key}: {st.session_state[key]}")
        
        try:
            # Create a new calculator
            calculator = Calculator(st.session_state.config)
            
            # Check if we have loaded practitioner data and force those values
            # This ensures data consistency across all calculations
            loaded_practitioner_a = {}
            if "loaded_practitioner_a" in st.session_state:
                loaded_practitioner_a = st.session_state.loaded_practitioner_a
                print("Loaded practitioner A found in session state - using these values for calculation")
            
            # Make a deep copy of the session state values for each practitioner
            # This prevents cross-contamination between practitioners
            practitioner_a_data = {
                "name": loaded_practitioner_a.get("name") if "name" in loaded_practitioner_a else st.session_state.get("practitioner_a_name", ""),
                "belt": loaded_practitioner_a.get("belt") if "belt" in loaded_practitioner_a else st.session_state.get("practitioner_a_belt", "White"),
                "age": loaded_practitioner_a.get("age") if "age" in loaded_practitioner_a else st.session_state.get("practitioner_a_age", 30),
                "weight": float(loaded_practitioner_a.get("weight", 0)) if "weight" in loaded_practitioner_a else float(st.session_state.get("practitioner_a_weight", 170.0)),
                "fitness_level": loaded_practitioner_a.get("fitness_level") if "fitness_level" in loaded_practitioner_a else st.session_state.get("practitioner_a_fitness_level", "Average (30th-60th percentile)"),
                "art": loaded_practitioner_a.get("art") if "art" in loaded_practitioner_a else st.session_state.get("practitioner_a_art", "None"),
                "exp_level": loaded_practitioner_a.get("exp_level") if "exp_level" in loaded_practitioner_a else st.session_state.get("practitioner_a_exp_level", ""),
                "sessions": loaded_practitioner_a.get("sessions") if "sessions" in loaded_practitioner_a else st.session_state.get("practitioner_a_sessions", 3),
                "comp": loaded_practitioner_a.get("comp") if "comp" in loaded_practitioner_a else st.session_state.get("practitioner_a_comp", "None")
            }
            
            # Check if we have loaded practitioner data for B
            loaded_practitioner_b = {}
            if "loaded_practitioner_b" in st.session_state:
                loaded_practitioner_b = st.session_state.loaded_practitioner_b
                print("Loaded practitioner B found in session state - using these values for calculation")
            
            practitioner_b_data = {
                "name": loaded_practitioner_b.get("name") if "name" in loaded_practitioner_b else st.session_state.get("practitioner_b_name", ""),
                "belt": loaded_practitioner_b.get("belt") if "belt" in loaded_practitioner_b else st.session_state.get("practitioner_b_belt", "White"),
                "age": loaded_practitioner_b.get("age") if "age" in loaded_practitioner_b else st.session_state.get("practitioner_b_age", 30),
                "weight": float(loaded_practitioner_b.get("weight", 0)) if "weight" in loaded_practitioner_b else float(st.session_state.get("practitioner_b_weight", 170.0)),
                "fitness_level": loaded_practitioner_b.get("fitness_level") if "fitness_level" in loaded_practitioner_b else st.session_state.get("practitioner_b_fitness_level", "Average (30th-60th percentile)"),
                "art": loaded_practitioner_b.get("art") if "art" in loaded_practitioner_b else st.session_state.get("practitioner_b_art", "None"),
                "exp_level": loaded_practitioner_b.get("exp_level") if "exp_level" in loaded_practitioner_b else st.session_state.get("practitioner_b_exp_level", ""),
                "sessions": loaded_practitioner_b.get("sessions") if "sessions" in loaded_practitioner_b else st.session_state.get("practitioner_b_sessions", 3),
                "comp": loaded_practitioner_b.get("comp") if "comp" in loaded_practitioner_b else st.session_state.get("practitioner_b_comp", "None")
            }
            
            # Get the fitness mapping for each practitioner
            # This is a critical mapping - make sure it's correct and used consistently
            fitness_level_mapping_table = {
                "Below Average (<30th percentile)": 25,
                "Average (30th-60th percentile)": 50,
                "Above Average (61st-80th percentile)": 70,
                "Notably Athletic (81st-95th percentile)": 88,
                "Exceptional Athlete (>95th percentile)": 97
            }
            
            # Log the exact fitness level string to help debug any mismatches
            print(f"Practitioner A fitness level string: '{practitioner_a_data['fitness_level']}'")
            practitioner_a_fitness = fitness_level_mapping_table.get(
                practitioner_a_data["fitness_level"], 50  # Default to 50th percentile
            )
            print(f"Practitioner A fitness: {practitioner_a_fitness} from '{practitioner_a_data['fitness_level']}'")
            
            print(f"Practitioner B fitness level string: '{practitioner_b_data['fitness_level']}'")
            practitioner_b_fitness = fitness_level_mapping_table.get(
                practitioner_b_data["fitness_level"], 50  # Default to 50th percentile
            )
            print(f"Practitioner B fitness: {practitioner_b_fitness} from '{practitioner_b_data['fitness_level']}'")
            
            # If we have numeric values directly from loaded data, use those as a fallback
            if practitioner_a_fitness == 50 and "loaded_practitioner_a" in st.session_state and "fitness" in st.session_state.loaded_practitioner_a:
                direct_fitness = st.session_state.loaded_practitioner_a.get("fitness")
                if direct_fitness:
                    print(f"Using direct fitness value for A: {direct_fitness}")
                    practitioner_a_fitness = direct_fitness
                    
            if practitioner_b_fitness == 50 and "loaded_practitioner_b" in st.session_state and "fitness" in st.session_state.loaded_practitioner_b:
                direct_fitness = st.session_state.loaded_practitioner_b.get("fitness")
                if direct_fitness:
                    print(f"Using direct fitness value for B: {direct_fitness}")
                    practitioner_b_fitness = direct_fitness
            print(f"Practitioner B fitness: {practitioner_b_fitness} from {practitioner_b_data['fitness_level']}")
            
            # Create practitioner objects based on copied data
            practitioner_a = PractitionerData(
                name=practitioner_a_data["name"],
                bjj_belt_rank=practitioner_a_data["belt"],
                age_years=practitioner_a_data["age"],
                weight_lbs=practitioner_a_data["weight"],
                primary_occupation_activity_level="Moderately Active",
                standardized_fitness_test_percentile_estimate=practitioner_a_fitness,
                other_grappling_art_experience=(
                    [{"art_name": practitioner_a_data["art"], 
                      "experience_level_descriptor": practitioner_a_data["exp_level"]}] 
                    if practitioner_a_data["art"] != "None" and practitioner_a_data["exp_level"]
                    else []
                ),
                bjj_training_sessions_per_week=practitioner_a_data["sessions"],
                bjj_competition_experience_level=practitioner_a_data["comp"],
                practitioner_id="a"
            )
            
            print(f"Created practitioner_a object: {practitioner_a}")
            
            practitioner_b = PractitionerData(
                name=practitioner_b_data["name"],
                bjj_belt_rank=practitioner_b_data["belt"],
                age_years=practitioner_b_data["age"],
                weight_lbs=practitioner_b_data["weight"],
                primary_occupation_activity_level="Moderately Active",
                standardized_fitness_test_percentile_estimate=practitioner_b_fitness,
                other_grappling_art_experience=(
                    [{"art_name": practitioner_b_data["art"], 
                      "experience_level_descriptor": practitioner_b_data["exp_level"]}] 
                    if practitioner_b_data["art"] != "None" and practitioner_b_data["exp_level"]
                    else []
                ),
                bjj_training_sessions_per_week=practitioner_b_data["sessions"],
                bjj_competition_experience_level=practitioner_b_data["comp"],
                practitioner_id="b"
            )
            
            print(f"Created practitioner_b object: {practitioner_b}")
            
            # Calculate factors and scores - recreate calculator for each calculation to avoid contamination
            calculator_a = Calculator(st.session_state.config)
            factors_a = calculator_a.calculate_all_factors(practitioner_a, practitioner_b)
            hs_a = factors_a.calculate_handicapped_score()
            
            calculator_b = Calculator(st.session_state.config)  
            factors_b = calculator_b.calculate_all_factors(practitioner_b, practitioner_a)
            hs_b = factors_b.calculate_handicapped_score()
            
            print(f"Calculated scores - A: {hs_a}, B: {hs_b}")
            
            # Store in session state
            st.session_state.score_a = hs_a
            st.session_state.score_b = hs_b
            st.session_state.factors_a = factors_a
            st.session_state.factors_b = factors_b
            
            print("Scores updated in session state")
            
        except Exception as e:
            print(f"Error updating scores: {e}")
            import traceback
            traceback.print_exc()
            pass
            
        print("----- FINISHED UPDATING SCORES -----\n")
    
    # Initialize session state for saved practitioners if not exists
    if "saved_practitioners" not in st.session_state:
        st.session_state.saved_practitioners = load_practitioners_from_disk()

    # Track whether we need to update scores after loading
    load_triggered = False

    # Add practitioner management UI
    with st.expander("Saved Practitioners", expanded=False):
        # Save current practitioner A or B
        st.subheader("Save Current Practitioners")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Practitioner A")
            save_name_a = st.text_input("Name for Practitioner A", 
                                        value=st.session_state.practitioner_a_name if "practitioner_a_name" in st.session_state else "", 
                                        key="save_name_a")
            save_a = st.button("Save Practitioner A", key="save_a_btn")
        
        with col2:
            st.write("Practitioner B")
            save_name_b = st.text_input("Name for Practitioner B", 
                                       value=st.session_state.practitioner_b_name if "practitioner_b_name" in st.session_state else "", 
                                       key="save_name_b")
            save_b = st.button("Save Practitioner B", key="save_b_btn")
        
        # Horizontal separator
        st.markdown("---")
        
        # Load saved practitioners
        st.subheader("Load Saved Practitioners")
        
        saved_practitioners = list(st.session_state.saved_practitioners.keys())
        if saved_practitioners:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("Select for Position A")
                selected_a = st.selectbox(
                    "Load into position A",
                    options=[""] + saved_practitioners,
                    index=0,
                    key="selected_a"
                )
                load_a = st.button("Load as A", key="load_a_btn")
            
            with col2:
                st.write("Select for Position B")
                selected_b = st.selectbox(
                    "Load into position B",
                    options=[""] + saved_practitioners,
                    index=0,
                    key="selected_b"
                )
                load_b = st.button("Load as B", key="load_b_btn")
            
            # Delete practitioner
            st.markdown("---")
            col1, col2 = st.columns([3, 1])
            
            with col1:
                to_delete = st.selectbox(
                    "Select practitioner to delete",
                    options=[""] + saved_practitioners,
                    index=0,
                    key="to_delete"
                )
            
            with col2:
                delete_btn = st.button("Delete", key="delete_btn", type="primary", use_container_width=True)
                
            if delete_btn and to_delete:
                if to_delete in st.session_state.saved_practitioners:
                    del st.session_state.saved_practitioners[to_delete]
                    save_practitioners_to_disk()
                    st.success(f"Deleted practitioner: {to_delete}")
                    st.rerun()
        else:
            st.info("No saved practitioners yet. Fill out the forms and save them individually.")
            
        # Handle loading practitioners
        if load_a and selected_a:
            if load_practitioner_a(selected_a):
                st.success(f"Loaded {selected_a} as Practitioner A")
                load_triggered = True
            
        if load_b and selected_b:
            if load_practitioner_b(selected_b):
                st.success(f"Loaded {selected_b} as Practitioner B")
                load_triggered = True
    
    # Initialize placeholder scores and state variables in session state
    if "score_a" not in st.session_state:
        st.session_state.score_a = 0
    if "score_b" not in st.session_state:
        st.session_state.score_b = 0
    if "factors_a" not in st.session_state:
        st.session_state.factors_a = None
    if "factors_b" not in st.session_state:
        st.session_state.factors_b = None
    
    # Check if we're on a page that needs a rerun after loading
    if "need_rerun" in st.session_state and st.session_state.need_rerun:
        # Clear the flag and rerun
        st.session_state.need_rerun = False
        update_scores()
        st.rerun()
        
    # Update scores if a practitioner was loaded
    if load_triggered:
        # Make sure our loaded values are preserved before updating scores
        print("\n----- PRESERVING LOADED VALUES BEFORE UPDATE -----")
        
        # Always force values from loaded_practitioner_a and loaded_practitioner_b
        # to override any potentially conflicting values in session state
        if "loaded_practitioner_a" in st.session_state:
            for field, value in st.session_state.loaded_practitioner_a.items():
                field_key = f"practitioner_a_{field}"
                print(f"Force restore field {field_key} with value {value}")
                st.session_state[field_key] = value
                
        if "loaded_practitioner_b" in st.session_state:
            for field, value in st.session_state.loaded_practitioner_b.items():
                field_key = f"practitioner_b_{field}"
                print(f"Force restore field {field_key} with value {value}")
                st.session_state[field_key] = value
                
        print("----- FINISHED PRESERVING LOADED VALUES -----\n")
        
        # Now update scores with the preserved values
        update_scores()
        
        # Set flag to force a rerun on the next page load
        st.session_state.need_rerun = True
        # Force a rerun to update the UI with the new scores
        st.rerun()
    
    # Calculate initial scores if they haven't been calculated yet
    if st.session_state.score_a == 0 and st.session_state.score_b == 0:
        update_scores()
    
    # Create two columns for practitioner inputs
    col1, col2 = st.columns(2)
    
    with col1:
        # Display score centered above the practitioner container
        st.markdown(
            f'<div style="text-align: center; margin-bottom: 20px;">'
            f'<h2 style="font-size: 3.5rem; margin: 0; color: #4f92d3;">Score: {st.session_state.score_a:.1f}</h2>'
            f'</div>',
            unsafe_allow_html=True
        )
        
        # Debug info
        if st.checkbox("Show debug info A", key="debug_a", value=False):
            st.write("### Session state for practitioner A")
            a_state = {k: v for k, v in st.session_state.items() if k.startswith("practitioner_a_")}
            st.write(a_state)
            
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
        
        # Debug info
        if st.checkbox("Show debug info B", key="debug_b", value=False):
            st.write("### Session state for practitioner B")
            b_state = {k: v for k, v in st.session_state.items() if k.startswith("practitioner_b_")}
            st.write(b_state)
            
        st.markdown('<div class="practitioner-heading">Practitioner B</div>', unsafe_allow_html=True)
        practitioner_b = render_practitioner_form("practitioner_b", st.session_state.config, 
                                                 score_factors=st.session_state.factors_b,
                                                 on_change=update_scores)
    
    compare_button = st.button("Compare Practitioners")
    
    # Save practitioner A if requested
    if save_a and save_name_a:
        # Check if there's already a practitioner with this name
        if save_name_a in st.session_state.saved_practitioners:
            st.warning(f"A practitioner named '{save_name_a}' already exists. Overwriting...")
            
        # Create a practitioner record
        st.session_state.saved_practitioners[save_name_a] = {
            "name": practitioner_a.name,
            "belt": practitioner_a.bjj_belt_rank,
            "age": practitioner_a.age_years,
            "weight": practitioner_a.weight_lbs,
            "fitness": practitioner_a.standardized_fitness_test_percentile_estimate,
            "sessions": practitioner_a.bjj_training_sessions_per_week,
            "competition": practitioner_a.bjj_competition_experience_level
        }
        
        # Add grappling experience if present
        if practitioner_a.other_grappling_art_experience:
            art_experience = practitioner_a.other_grappling_art_experience[0]
            st.session_state.saved_practitioners[save_name_a]["art"] = art_experience["art_name"]
            st.session_state.saved_practitioners[save_name_a]["exp_level"] = art_experience["experience_level_descriptor"]
        else:
            st.session_state.saved_practitioners[save_name_a]["art"] = "None"
            
        # Save to disk for persistence across sessions
        save_practitioners_to_disk()
        
        st.success(f"Practitioner '{save_name_a}' saved!")
        
    # Save practitioner B if requested
    if save_b and save_name_b:
        # Check if there's already a practitioner with this name
        if save_name_b in st.session_state.saved_practitioners:
            st.warning(f"A practitioner named '{save_name_b}' already exists. Overwriting...")
            
        # Create a practitioner record
        st.session_state.saved_practitioners[save_name_b] = {
            "name": practitioner_b.name,
            "belt": practitioner_b.bjj_belt_rank,
            "age": practitioner_b.age_years,
            "weight": practitioner_b.weight_lbs,
            "fitness": practitioner_b.standardized_fitness_test_percentile_estimate,
            "sessions": practitioner_b.bjj_training_sessions_per_week,
            "competition": practitioner_b.bjj_competition_experience_level
        }
        
        # Add grappling experience if present
        if practitioner_b.other_grappling_art_experience:
            art_experience = practitioner_b.other_grappling_art_experience[0]
            st.session_state.saved_practitioners[save_name_b]["art"] = art_experience["art_name"]
            st.session_state.saved_practitioners[save_name_b]["exp_level"] = art_experience["experience_level_descriptor"]
        else:
            st.session_state.saved_practitioners[save_name_b]["art"] = "None"
            
        # Save to disk for persistence across sessions
        save_practitioners_to_disk()
        
        st.success(f"Practitioner '{save_name_b}' saved!")
    
    if compare_button:
        # First update scores to ensure we have the most accurate data
        update_scores()
        
        # Use the scores and factors from the update_scores function
        factors_a = st.session_state.factors_a
        hs_a = st.session_state.score_a
        
        factors_b = st.session_state.factors_b
        hs_b = st.session_state.score_b
        
        # Recreate practitioner objects to ensure they match the scores
        # Make a deep copy of the session state values for each practitioner
        practitioner_a_data = {
            "name": st.session_state.get("practitioner_a_name", ""),
            "belt": st.session_state.get("practitioner_a_belt", "White"),
            "age": st.session_state.get("practitioner_a_age", 30),
            "weight": float(st.session_state.get("practitioner_a_weight", 170.0)),
            "fitness_level": st.session_state.get("practitioner_a_fitness_level", "Average (30th-60th percentile)"),
            "art": st.session_state.get("practitioner_a_art", "None"),
            "exp_level": st.session_state.get("practitioner_a_exp_level", ""),
            "sessions": st.session_state.get("practitioner_a_sessions", 3),
            "comp": st.session_state.get("practitioner_a_comp", "None")
        }
        
        practitioner_b_data = {
            "name": st.session_state.get("practitioner_b_name", ""),
            "belt": st.session_state.get("practitioner_b_belt", "White"),
            "age": st.session_state.get("practitioner_b_age", 30),
            "weight": float(st.session_state.get("practitioner_b_weight", 170.0)),
            "fitness_level": st.session_state.get("practitioner_b_fitness_level", "Average (30th-60th percentile)"),
            "art": st.session_state.get("practitioner_b_art", "None"),
            "exp_level": st.session_state.get("practitioner_b_exp_level", ""),
            "sessions": st.session_state.get("practitioner_b_sessions", 3),
            "comp": st.session_state.get("practitioner_b_comp", "None")
        }
        
        # Get the fitness mapping 
        fitness_level_mapping_a = {
            "Below Average (<30th percentile)": 25,
            "Average (30th-60th percentile)": 50,
            "Above Average (61st-80th percentile)": 70,
            "Notably Athletic (81st-95th percentile)": 88,
            "Exceptional Athlete (>95th percentile)": 97
        }
        
        practitioner_a_fitness = fitness_level_mapping_a.get(
            practitioner_a_data["fitness_level"], 50  # Default to 50th percentile
        )
        
        practitioner_b_fitness = fitness_level_mapping_a.get(
            practitioner_b_data["fitness_level"], 50  # Default to 50th percentile
        )
        
        # Create practitioner objects based on copied data
        practitioner_a = PractitionerData(
            name=practitioner_a_data["name"],
            bjj_belt_rank=practitioner_a_data["belt"],
            age_years=practitioner_a_data["age"],
            weight_lbs=practitioner_a_data["weight"],
            primary_occupation_activity_level="Moderately Active",
            standardized_fitness_test_percentile_estimate=practitioner_a_fitness,
            other_grappling_art_experience=(
                [{"art_name": practitioner_a_data["art"], 
                  "experience_level_descriptor": practitioner_a_data["exp_level"]}] 
                if practitioner_a_data["art"] != "None" and practitioner_a_data["exp_level"]
                else []
            ),
            bjj_training_sessions_per_week=practitioner_a_data["sessions"],
            bjj_competition_experience_level=practitioner_a_data["comp"],
            practitioner_id="a"
        )
        
        practitioner_b = PractitionerData(
            name=practitioner_b_data["name"],
            bjj_belt_rank=practitioner_b_data["belt"],
            age_years=practitioner_b_data["age"],
            weight_lbs=practitioner_b_data["weight"],
            primary_occupation_activity_level="Moderately Active",
            standardized_fitness_test_percentile_estimate=practitioner_b_fitness,
            other_grappling_art_experience=(
                [{"art_name": practitioner_b_data["art"], 
                  "experience_level_descriptor": practitioner_b_data["exp_level"]}] 
                if practitioner_b_data["art"] != "None" and practitioner_b_data["exp_level"]
                else []
            ),
            bjj_training_sessions_per_week=practitioner_b_data["sessions"],
            bjj_competition_experience_level=practitioner_b_data["comp"],
            practitioner_id="b"
        )
        
        # Generate profiles
        profile_a = profile_generator.generate_profile(practitioner_a, factors_a, hs_a)
        profile_b = profile_generator.generate_profile(practitioner_b, factors_b, hs_b)
        
        # Display visualization comparison with actual practitioner names
        render_comparison_visualization(
            factors_a, 
            factors_b, 
            hs_a, 
            hs_b, 
            st.session_state.config,
            name_a=practitioner_a.name if practitioner_a.name else "Practitioner A",
            name_b=practitioner_b.name if practitioner_b.name else "Practitioner B"
        )
        
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
    
    #### Interactive Practitioner Comparison
    1. Fill in details for both practitioners - notice how scores update instantly
    2. See the impact percentage next to each attribute to understand its contribution
    3. The large score display at the top of each practitioner updates in real-time
    4. Click "Compare Practitioners" for detailed radar charts and matchup profiles
    
    #### Managing Practitioners
    1. Save practitioners individually with custom names
    2. Load any saved practitioner into either position A or B
    3. Mix and match different saved practitioners for comparison
    4. Delete practitioners you no longer need
    
    #### Understanding the Factors
    - **Belt Rank Score (BRS)**: Your base score determined by belt rank
    - **Age Factor (AF)**: Adjustment based on age relative to peak performance age
    - **Weight Factor (WF)**: Adjustment based on weight difference between practitioners
    - **Athleticism Factor (ACF)**: Modification based on general physical capabilities
    - **Grappling Experience (REF)**: Bonus for relevant experience in other grappling arts
    - **Training Frequency (TFF)**: Impact of regular BJJ training sessions per week
    - **Competition Experience (CEF)**: Bonus for BJJ competition experience
    
    #### Configuration (Advanced)
    The system is fully customizable in the Configuration tab below:
    - Change belt rank base scores
    - Adjust age-related calculations
    - Modify weight difference impacts
    - Fine-tune all other multipliers
    
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