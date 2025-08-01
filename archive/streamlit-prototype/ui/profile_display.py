import streamlit as st
from typing import Dict, List, Any
from jar.types import RollDynamicsProfile

def render_profile(profile: RollDynamicsProfile) -> None:
    """
    Render the Roll Dynamics Profile in a structured format.
    
    Args:
        profile: Generated Roll Dynamics Profile
    """
    st.markdown("""
    <style>
    /* Profile container styling for dark theme */
    .profile-container {
        border: 1px solid #495057;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 30px;
        background-color: #222222;
        color: #e9ecef;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    
    .profile-header {
        font-size: 1.8em;
        font-weight: 600;
        margin-bottom: 18px;
        color: #4f92d3;
        padding-bottom: 10px;
        border-bottom: 1px solid #495057;
    }
    
    .profile-data {
        font-size: 1.2em;
        margin-bottom: 12px;
        color: #adb5bd;
        display: flex;
        align-items: center;
    }
    
    .profile-data strong {
        min-width: 180px;
        display: inline-block;
        color: #e9ecef;
    }
    
    .profile-section-header {
        font-size: 1.5em;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 12px;
        color: #4f92d3;
        background: transparent;
        padding-top: 10px;
        border-top: 1px solid #495057;
    }
    
    .strength-item {
        font-size: 1.15em;
        margin-bottom: 10px;
        font-weight: 400;
        color: #e9ecef;
        background-color: rgba(77, 179, 128, 0.15);
        padding: 10px 15px;
        border-radius: 6px;
        border-left: 4px solid #4db380;
    }
    
    .challenge-item {
        font-size: 1.15em;
        margin-bottom: 10px;
        font-weight: 400;
        color: #e9ecef;
        background-color: rgba(224, 90, 69, 0.15);
        padding: 10px 15px;
        border-radius: 6px;
        border-left: 4px solid #e05a45;
    }
    
    .assessment-container {
        display: flex;
        justify-content: space-between;
        margin-top: 25px;
        gap: 15px;
    }
    
    .assessment-item {
        flex: 1;
        text-align: center;
        padding: 18px 15px;
        border-radius: 10px;
        font-size: 1.15em;
        background-color: #2a2a2a;
        color: #e9ecef;
        border: 1px solid #495057;
        transition: transform 0.2s;
    }
    
    .assessment-item:hover {
        transform: translateY(-2px);
    }
    
    .level-high {
        border-left: 4px solid #4db380;
        font-weight: 600;
    }
    
    .level-medium {
        border-left: 4px solid #d8b24b;
    }
    
    .level-low {
        border-left: 4px solid #e05a45;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render the profile container with basic info
    st.markdown(f"""
    <div class="profile-container">
        <div class="profile-header">Roll Dynamics Profile: {profile.practitioner_name}</div>
        <p class="profile-data"><strong>Handicapped Score:</strong> {profile.handicapped_score:.2f}</p>
        <p class="profile-data"><strong>Dominant Trait:</strong> {profile.dominant_trait}</p>
        <p class="profile-data"><strong>Likely Roll Approach:</strong> {profile.likely_approach}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Use separate Streamlit components for the sections
    st.markdown("<h3>Key Strengths</h3>", unsafe_allow_html=True)
    
    # Check if key_strengths exists and has content
    if profile.key_strengths and len(profile.key_strengths) > 0:
        for strength in profile.key_strengths:
            st.markdown(f"""
            <div class="strength-item">• {strength}</div>
            """, unsafe_allow_html=True)
    else:
        # Display a placeholder when no strengths are available
        st.markdown("""
        <div class="strength-item">No specific strengths identified</div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h3>Key Challenges</h3>", unsafe_allow_html=True)
    
    # Check if key_challenges exists and has content
    if profile.key_challenges and len(profile.key_challenges) > 0:
        for challenge in profile.key_challenges:
            st.markdown(f"""
            <div class="challenge-item">• {challenge}</div>
            """, unsafe_allow_html=True)
    else:
        # Display a placeholder when no challenges are available
        st.markdown("""
        <div class="challenge-item">No specific challenges identified</div>
        """, unsafe_allow_html=True)
    
    # Create level classes
    level_classes = {
        "High": "level-high",
        "Medium": "level-medium",
        "Low": "level-low"
    }
    
    st.markdown("<h3>Technical Assessment</h3>", unsafe_allow_html=True)
    st.markdown("""<div class="assessment-container">""", unsafe_allow_html=True)
    
    # Display Control Potential
    st.markdown(f"""
    <div class="assessment-item {level_classes[profile.control_potential]}">
        <div style="font-weight: bold; font-size: 1.2em; margin-bottom: 8px;">Control Potential</div>
        <div style="font-size: 1.3em;">{profile.control_potential}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display Submission Threat
    st.markdown(f"""
    <div class="assessment-item {level_classes[profile.submission_offensive_threat]}">
        <div style="font-weight: bold; font-size: 1.2em; margin-bottom: 8px;">Submission Threat</div>
        <div style="font-size: 1.3em;">{profile.submission_offensive_threat}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display Submission Defense
    st.markdown(f"""
    <div class="assessment-item {level_classes[profile.submission_defensive_resilience]}">
        <div style="font-weight: bold; font-size: 1.2em; margin-bottom: 8px;">Submission Defense</div>
        <div style="font-size: 1.3em;">{profile.submission_defensive_resilience}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Close the assessment container
    st.markdown("</div>", unsafe_allow_html=True)

def render_profile_comparison(
    profile_a: RollDynamicsProfile, 
    profile_b: RollDynamicsProfile
) -> None:
    """
    Render a side-by-side comparison of two profiles.
    
    Args:
        profile_a: Roll Dynamics Profile for practitioner A
        profile_b: Roll Dynamics Profile for practitioner B
    """
    # Using the built-in column layout with custom styling for better control
    st.markdown(
        """
        <style>
        .profile-columns {
            display: flex;
            gap: 20px;
        }
        .profile-column {
            flex: 1;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Create two columns for the comparison
    col1, col2 = st.columns(2)
    
    with col1:
        # Use markdown with HTML to ensure proper rendering
        st.markdown(f"## Profile: {profile_a.practitioner_name}", unsafe_allow_html=True)
        render_profile(profile_a)
    
    with col2:
        # Use markdown with HTML to ensure proper rendering
        st.markdown(f"## Profile: {profile_b.practitioner_name}", unsafe_allow_html=True)
        render_profile(profile_b)
    
    # Display a comparison analysis
    st.markdown("## Matchup Analysis", unsafe_allow_html=True)
    
    # Calculate score differential
    score_diff = abs(profile_a.handicapped_score - profile_b.handicapped_score)
    score_ratio = max(profile_a.handicapped_score, profile_b.handicapped_score) / min(profile_a.handicapped_score, profile_b.handicapped_score)
    
    if score_ratio < 1.2:
        evenness = "Very Even"
        diff_color = "green"
    elif score_ratio < 1.5:
        evenness = "Moderately Even"
        diff_color = "orange"
    else:
        evenness = "Significant Difference"
        diff_color = "red"
    
    # Determine higher-scored practitioner
    higher_profile = profile_a if profile_a.handicapped_score > profile_b.handicapped_score else profile_b
    
    # Use container and columns for the matchup analysis
    with st.container():
        st.markdown(f"""
        <div class="profile-container" style="margin-top: 30px;">
            <div class="profile-header">Matchup Analysis</div>
            <div class="profile-data"><strong>Score Differential:</strong> {score_diff:.2f} points ({evenness})</div>
            <div class="profile-data"><strong>Matchup Type:</strong> {determine_matchup_type(profile_a, profile_b)}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Separate analysis into its own component
        st.markdown("<h3>Analysis</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size: 1.2em; line-height: 1.5; padding: 15px; background-color: rgba(79, 146, 211, 0.15); border-radius: 8px; border: 1px solid #495057;">
            {generate_matchup_analysis(profile_a, profile_b)}
        </div>
        """, unsafe_allow_html=True)

def determine_matchup_type(
    profile_a: RollDynamicsProfile, 
    profile_b: RollDynamicsProfile
) -> str:
    """
    Determine the type of matchup based on the profiles.
    
    Args:
        profile_a: Roll Dynamics Profile for practitioner A
        profile_b: Roll Dynamics Profile for practitioner B
        
    Returns:
        Description of the matchup type
    """
    # Technical vs Physical matchup
    if profile_a.dominant_trait == "Technical BJJ Specialist" and profile_b.dominant_trait == "Physical Grappling Athlete":
        return "Technical vs Physical"
    elif profile_a.dominant_trait == "Physical Grappling Athlete" and profile_b.dominant_trait == "Technical BJJ Specialist":
        return "Physical vs Technical"
    
    # All-rounder matchups
    if "All-Rounder" in profile_a.dominant_trait or "All-Rounder" in profile_b.dominant_trait:
        return "All-Rounder Present"
    
    # Similar styles
    if profile_a.dominant_trait == profile_b.dominant_trait:
        return f"Similar Styles ({profile_a.dominant_trait})"
    
    # Default case
    return "Mixed Styles"

def generate_matchup_analysis(
    profile_a: RollDynamicsProfile, 
    profile_b: RollDynamicsProfile
) -> str:
    """
    Generate a narrative analysis of the matchup.
    
    Args:
        profile_a: Roll Dynamics Profile for practitioner A
        profile_b: Roll Dynamics Profile for practitioner B
        
    Returns:
        Analysis of the matchup dynamics
    """
    analysis = []
    
    # Control dynamics
    if profile_a.control_potential == "High" and profile_b.control_potential != "High":
        analysis.append(f"{profile_a.practitioner_name} likely has a control advantage.")
    elif profile_b.control_potential == "High" and profile_a.control_potential != "High":
        analysis.append(f"{profile_b.practitioner_name} likely has a control advantage.")
    elif profile_a.control_potential == "High" and profile_b.control_potential == "High":
        analysis.append("Both practitioners have strong control games; expect a battle for dominant position.")
    
    # Submission dynamics
    if profile_a.submission_offensive_threat == "High" and profile_b.submission_defensive_resilience != "High":
        analysis.append(f"{profile_a.practitioner_name} may find submission opportunities against {profile_b.practitioner_name}.")
    if profile_b.submission_offensive_threat == "High" and profile_a.submission_defensive_resilience != "High":
        analysis.append(f"{profile_b.practitioner_name} may find submission opportunities against {profile_a.practitioner_name}.")
    
    # Overall approaches that may clash or complement
    if profile_a.likely_approach == "Pressure & Control-Oriented" and profile_b.likely_approach == "Technical & Opportunistic":
        analysis.append(f"Expect {profile_a.practitioner_name} to seek dominant position while {profile_b.practitioner_name} looks for technical escapes and counters.")
    
    # If we couldn't generate specific insights
    if not analysis:
        return "This matchup appears balanced across multiple dimensions. The outcome may depend on specific techniques, timing, and mental aspects not captured in the profile."
    
    return " ".join(analysis)