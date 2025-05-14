import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from typing import Dict, List, Tuple, Optional
from jar.types import FactorResults
from jar.config import JARConfig

# Configure visualization style
plt.style.use('default')  # Use a cleaner, more readable style
plt.rcParams['font.size'] = 14  # Increase default font size
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 12

# Simpler color palette with better contrast
FACTOR_COLORS = {
    'brs': '#336699',  # Darker Blue
    'af': '#993333',   # Darker Red
    'wf': '#339966',   # Darker Green
    'acf': '#996633',  # Darker Orange
    'ref': '#663399',  # Darker Purple
    'tff': '#339999',  # Darker Teal
    'cef': '#996600',  # Darker Gold
    'total': '#333333'  # Dark Gray
}

FACTOR_FULL_NAMES = {
    'brs': 'Belt Rank Score',
    'af': 'Age Factor',
    'wf': 'Weight Factor',
    'acf': 'Athleticism Factor',
    'ref': 'Grappling Experience',
    'tff': 'Training Frequency',
    'cef': 'Competition Experience'
}

def render_factor_visualization(factors: FactorResults, config: JARConfig) -> None:
    """
    Render visualization for factors and their contribution.
    
    Args:
        factors: Calculated factor results
        config: JAR system configuration
    """
    # Calculate the final handicapped score
    hs = factors.calculate_handicapped_score()
    
    # Create a prominent score display
    st.markdown("""
    <style>
    .primary-score-container {
        text-align: center;
        padding: 30px 20px;
        margin: 20px 0;
        border-radius: 12px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 2px solid #dee2e6;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .score-value {
        font-size: 5rem;
        font-weight: 700;
        color: #336699;
        margin: 0;
        line-height: 1.2;
    }
    .score-label {
        font-size: 1.5rem;
        color: #495057;
        margin-top: 5px;
    }
    .multiplier-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        margin-top: 25px;
        gap: 15px;
    }
    .multiplier-item {
        padding: 12px 15px;
        border-radius: 8px;
        text-align: center;
        min-width: 130px;
        background-color: #ffffff;
        border: 1px solid #dee2e6;
    }
    .multiplier-value {
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
    }
    .multiplier-label {
        font-size: 0.9rem;
        color: #6c757d;
        margin: 5px 0 0 0;
    }
    .positive-multiplier {
        color: #2d8659;
        border-left: 4px solid #2d8659;
    }
    .negative-multiplier {
        color: #994436;
        border-left: 4px solid #994436;
    }
    .neutral-multiplier {
        color: #6c757d;
        border-left: 4px solid #6c757d;
    }
    .base-score {
        color: #336699;
        border-left: 4px solid #336699;
        font-weight: bold;
    }
    
    /* Updated tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        border-bottom: 1px solid #dee2e6;
        padding-bottom: 10px;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 18px;
        font-weight: 500;
        color: #495057;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #f8f9fa;
        border-radius: 4px 4px 0 0;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] [data-testid="stMarkdownContainer"] p {
        color: #336699;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render the large score with multipliers
    st.markdown(f"""
    <div class="primary-score-container">
        <div class="score-value">{hs:.1f}</div>
        <div class="score-label">Handicapped Score</div>
        
        <div class="multiplier-container">
            <div class="multiplier-item base-score">
                <div class="multiplier-value">{factors.brs:.0f}</div>
                <div class="multiplier-label">Belt Rank Score</div>
            </div>
            
            <div class="multiplier-item {'positive-multiplier' if factors.af > 1.0 else 'negative-multiplier' if factors.af < 1.0 else 'neutral-multiplier'}">
                <div class="multiplier-value">{factors.af:.2f}x</div>
                <div class="multiplier-label">Age</div>
            </div>
            
            <div class="multiplier-item {'positive-multiplier' if factors.wf > 1.0 else 'negative-multiplier' if factors.wf < 1.0 else 'neutral-multiplier'}">
                <div class="multiplier-value">{factors.wf:.2f}x</div>
                <div class="multiplier-label">Weight</div>
            </div>
            
            <div class="multiplier-item {'positive-multiplier' if factors.acf > 1.0 else 'negative-multiplier' if factors.acf < 1.0 else 'neutral-multiplier'}">
                <div class="multiplier-value">{factors.acf:.2f}x</div>
                <div class="multiplier-label">Athleticism</div>
            </div>
            
            <div class="multiplier-item {'positive-multiplier' if factors.ref > 1.0 else 'negative-multiplier' if factors.ref < 1.0 else 'neutral-multiplier'}">
                <div class="multiplier-value">{factors.ref:.2f}x</div>
                <div class="multiplier-label">Grappling Exp.</div>
            </div>
            
            <div class="multiplier-item {'positive-multiplier' if factors.tff > 1.0 else 'negative-multiplier' if factors.tff < 1.0 else 'neutral-multiplier'}">
                <div class="multiplier-value">{factors.tff:.2f}x</div>
                <div class="multiplier-label">Training Freq.</div>
            </div>
            
            <div class="multiplier-item {'positive-multiplier' if factors.cef > 1.0 else 'negative-multiplier' if factors.cef < 1.0 else 'neutral-multiplier'}">
                <div class="multiplier-value">{factors.cef:.2f}x</div>
                <div class="multiplier-label">Competition</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Provide detailed views as tabs
    tab1, tab2 = st.tabs([
        "Details", 
        "Radar Chart"
    ])
    
    with tab1:
        st.markdown("<h3 style='font-size: 24px; margin: 20px 0;'>Factor Breakdown</h3>", unsafe_allow_html=True)
        render_factor_breakdown_table(factors, hs)
    
    with tab2:
        st.markdown("<h3 style='font-size: 24px; margin: 20px 0;'>Attribute Radar</h3>", unsafe_allow_html=True)
        render_practitioner_radar(factors)

def render_practitioner_radar(factors: FactorResults) -> None:
    """
    Render a radar chart for a single practitioner's attributes.
    
    Args:
        factors: Calculated factor results
    """
    # Define categories for radar chart
    categories = ['Belt Rank', 'Age', 'Weight', 'Athleticism', 
                 'Grappling Exp', 'Training Freq', 'Competition']
    
    # Normalize values for radar chart
    # For BRS, we need to normalize it to a 0-1 scale
    # We'll use a 800 (Black belt) as the max
    brs_max = 800
    
    # Create normalized values array
    values = [
        factors.brs / brs_max,  # Normalize BRS
        factors.af,
        factors.wf,
        factors.acf,
        factors.ref,
        factors.tff,
        factors.cef
    ]
    
    # Compute angles for each category
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Close the loop
    
    # Extend values arrays to close the loop
    values += values[:1]
    
    # Create the figure with larger size and dark theme style
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    
    # Set background color to match the dark theme
    fig.patch.set_facecolor('#1e1e1e')
    ax.set_facecolor('#2a2a2a')
    
    # Set text colors for better visibility in dark mode
    for label in ax.get_xticklabels():
        label.set_color('#e9ecef')
    for label in ax.get_yticklabels():
        label.set_color('#e9ecef')
    ax.title.set_color('#e9ecef')
    
    # Draw the radar chart with thicker lines and clearer markers
    ax.plot(angles, values, 'o-', linewidth=3, markersize=10, 
            label='Attributes', color='#336699')
    ax.fill(angles, values, alpha=0.2, color='#336699')
    
    # Add categories labels with larger, more readable font
    ax.set_thetagrids(np.degrees(angles[:-1]), categories, fontsize=16)
    
    # Add reference line at 1.0
    ax.plot(angles, [1.0] * len(angles), '--', color='#6c757d', 
            alpha=0.7, linewidth=1.5)
    
    # Draw reference circles at different levels
    for level in [0.25, 0.5, 0.75]:
        ax.plot(angles, [level] * len(angles), '--', color='#dee2e6', 
                alpha=0.5, linewidth=1)
    
    # Customize grid and axes for dark theme
    ax.grid(color='#495057', alpha=0.7)
    ax.spines['polar'].set_color('#495057')
    
    # Add factor descriptions at each point
    for i, (angle, value, category) in enumerate(zip(angles[:-1], values[:-1], categories)):
        ha = 'left' if 0 <= angle < np.pi else 'right'
        va = 'bottom' if angle < 0.5*np.pi or angle > 1.5*np.pi else 'top'
        
        # Add value labels near the points
        ax.text(angle, value + 0.1, f"{value:.2f}", 
                ha=ha, va=va, color='#495057', fontweight='bold')
    
    plt.title('Practitioner Attribute Profile', size=20, pad=20, color='#e9ecef')
    
    # Show the plot
    st.pyplot(fig)

def render_factor_multipliers_chart(factors: FactorResults) -> None:
    """
    Render a horizontal bar chart of factor multipliers.
    
    Args:
        factors: Calculated factor results
    """
    # Create dataframe for factor multipliers
    df = pd.DataFrame({
        'Factor': [FACTOR_FULL_NAMES[k] for k in ['af', 'wf', 'acf', 'ref', 'tff', 'cef']],
        'Multiplier': [getattr(factors, k) for k in ['af', 'wf', 'acf', 'ref', 'tff', 'cef']],
        'Code': ['af', 'wf', 'acf', 'ref', 'tff', 'cef']
    })
    
    # Sort by absolute deviation from 1.0 to highlight most significant factors
    df['Deviation'] = abs(df['Multiplier'] - 1.0)
    df = df.sort_values('Deviation', ascending=False)
    
    # Create the figure with larger size
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Generate colors based on whether multiplier is > or < 1.0
    colors = [FACTOR_COLORS[code] for code in df['Code']]
    
    # Add a vertical line at x=1.0 to show neutral
    ax.axvline(x=1.0, color='black', linestyle='--', alpha=0.8, linewidth=1.5)
    
    # Create horizontal bar chart with larger bars
    bars = ax.barh(df['Factor'], df['Multiplier'], color=colors, alpha=0.8, height=0.6)
    
    # Add labels to the bars with larger, more readable font
    for bar, multiplier in zip(bars, df['Multiplier']):
        width = bar.get_width()
        label_x_pos = width + 0.01 if width > 1.0 else width - 0.04
        direction = 'left' if width > 1.0 else 'right'
        color = '#006600' if width > 1.0 else '#990000'  # Darker colors for better contrast
        
        ax.text(label_x_pos, 
                bar.get_y() + bar.get_height()/2, 
                f'{width:.2f}×', 
                va='center', 
                ha=direction, 
                color=color,
                fontweight='bold',
                fontsize=14)
    
    # Set the title and labels
    ax.set_title('Factor Multipliers')
    ax.set_xlabel('Multiplier Value')
    
    # Set the x-axis to better show deviations
    min_mult = min(df['Multiplier']) * 0.9  # Add some padding
    max_mult = max(df['Multiplier']) * 1.1  # Add some padding
    
    # Ensure we include 1.0 in the visible range
    min_mult = min(min_mult, 0.9)
    max_mult = max(max_mult, 1.1)
    
    ax.set_xlim(min_mult, max_mult)
    
    # Show the plot
    st.pyplot(fig)

def render_waterfall_chart(factors: FactorResults, final_score: float) -> None:
    """
    Create a waterfall chart showing how each factor contributes to the final score.
    
    Args:
        factors: Calculated factor results
        final_score: Final handicapped score
    """
    # Base value (BRS)
    base_value = factors.brs
    
    # Calculate the contribution of each factor
    current_value = base_value
    contributions = {}
    for k in ["af", "wf", "acf", "ref", "tff", "cef"]:
        factor_value = getattr(factors, k)
        new_value = current_value * factor_value
        contributions[k] = new_value - current_value
        current_value = new_value
    
    # Create the figure with larger size and dark background
    fig, ax = plt.subplots(figsize=(14, 9))
    fig.patch.set_facecolor('#1e1e1e')
    ax.set_facecolor('#2a2a2a')
    
    # Update text color for better visibility in dark mode
    ax.xaxis.label.set_color('#e9ecef')
    ax.yaxis.label.set_color('#e9ecef')
    ax.tick_params(axis='x', colors='#e9ecef')
    ax.tick_params(axis='y', colors='#e9ecef')
    ax.title.set_color('#e9ecef')
    
    # Start with BRS
    values = [base_value] + list(contributions.values()) + [final_score]
    labels = ["Base BRS"] + [FACTOR_FULL_NAMES[k] for k in contributions.keys()] + ["Final HS"]
    
    # Colors for each bar with higher opacity
    colors = [FACTOR_COLORS['brs']] + [FACTOR_COLORS[k] for k in contributions.keys()] + [FACTOR_COLORS['total']]
    
    # Create a blank baseline
    blank = np.zeros(len(values))
    
    # The cumulative sum is the positions of the left side of each bar
    cumsum = np.zeros(len(values))
    cumsum[0] = 0  # Start at 0
    for i in range(1, len(values)-1):
        cumsum[i] = cumsum[i-1] + values[i-1]
    
    # Create the waterfall chart
    for i, (label, val, cs, col) in enumerate(zip(labels, values, cumsum, colors)):
        if i == 0:  # First bar (BRS)
            ax.bar(i, val, bottom=0, color=col, alpha=0.8, edgecolor='black')
        elif i == len(values) - 1:  # Last bar (Final HS)
            # This is a special case to make the final bar start at 0
            ax.bar(i, final_score, bottom=0, color=col, alpha=0.8, edgecolor='black')
        else:  # Middle bars (contributions)
            ax.bar(i, val, bottom=cs, color=col, alpha=0.8, edgecolor='black')
    
    # Add connector lines between bars
    for i in range(len(values) - 2):
        current_total = cumsum[i] + values[i]
        next_bottom = cumsum[i+1]
        ax.plot([i+0.5, i+1.5], [current_total, next_bottom], 'k-', alpha=0.3)
    
    # Connect last regular bar to final
    ax.plot([len(values)-2.5, len(values)-1.5], [final_score, 0], 'k-', alpha=0.3)
    
    # Add value labels to each bar with larger, more readable font
    for i, val in enumerate(values):
        if i == 0:  # First bar
            ax.text(i, val/2, f"{val:.1f}", ha='center', va='center', 
                   fontweight='bold', fontsize=14, color='white')
        elif i == len(values) - 1:  # Last bar
            ax.text(i, final_score/2, f"{final_score:.1f}", ha='center', va='center', 
                   fontweight='bold', fontsize=14, color='white')
        else:  # Middle bars
            # Determine if contribution is positive or negative
            sign = '+' if val > 0 else ''
            
            # Position the label appropriately
            bottom = cumsum[i]
            height = val
            
            # Make contribution labels more visible
            text_color = 'white' if abs(height) > 15 else 'black'
            
            ax.text(i, bottom + height/2, f"{sign}{val:.1f}", ha='center', va='center',
                   fontweight='bold', fontsize=12, color=text_color)
    
    # Set the x-axis ticks and labels
    ax.set_xticks(range(len(values)))
    ax.set_xticklabels(labels, rotation=45, ha='right')
    
    # Set the title
    ax.set_title('Contribution to Final Score')
    ax.set_ylabel('Score')
    
    # Adjust the bottom margin to accommodate rotated labels
    plt.tight_layout()
    
    # Show the plot
    st.pyplot(fig)

def render_factor_breakdown_table(factors: FactorResults, final_score: float) -> None:
    """
    Render a detailed table breakdown of all factors.
    
    Args:
        factors: Calculated factor results
        final_score: Final handicapped score
    """
    # Create a DataFrame with factor details
    data = {
        'Factor': [FACTOR_FULL_NAMES[k] for k in ['brs', 'af', 'wf', 'acf', 'ref', 'tff', 'cef']],
        'Value': [
            factors.brs, 
            factors.af, 
            factors.wf, 
            factors.acf, 
            factors.ref, 
            factors.tff, 
            factors.cef
        ],
        'Category': [
            'Base Score', 
            'Physical', 
            'Physical', 
            'Physical', 
            'Experience', 
            'Training', 
            'Experience'
        ],
        'Impact': ['Base'] + [
            'Positive' if getattr(factors, k) > 1.0 else 
            'Negative' if getattr(factors, k) < 1.0 else 
            'Neutral' 
            for k in ['af', 'wf', 'acf', 'ref', 'tff', 'cef']
        ]
    }
    
    df = pd.DataFrame(data)
    
    # Add a row for the final score
    df = pd.concat([df, pd.DataFrame([{
        'Factor': 'Final Handicapped Score',
        'Value': final_score,
        'Category': 'Result',
        'Impact': 'N/A'
    }])], ignore_index=True)
    
    # Style the dataframe for display with better dark theme readability
    styled_df = df.style.format({
        'Value': lambda x: f"{x:.2f}" if isinstance(x, float) else x,
    }).set_table_styles([
        # Increase font size and padding for all cells
        {'selector': '*', 'props': [('font-size', '16px'), ('padding', '10px'), ('color', '#e9ecef')]},
        # Bold headers
        {'selector': 'th', 'props': [
            ('font-weight', 'bold'), 
            ('text-align', 'left'),
            ('background-color', '#333333'),
            ('font-size', '18px'),
            ('color', '#e9ecef')
        ]},
        # Style cells
        {'selector': 'td', 'props': [
            ('text-align', 'left'),
            ('font-size', '16px'),
            ('background-color', '#2a2a2a')
        ]},
        # Add borders
        {'selector': 'table', 'props': [
            ('border', '2px solid #495057'),
            ('border-collapse', 'collapse'),
            ('background-color', '#2a2a2a')
        ]},
        {'selector': 'th, td', 'props': [
            ('border', '1px solid #495057')
        ]}
    ]).apply(lambda x: [
        # Apply custom cell styling for values instead of background gradient
        'font-weight: bold; color: #4db380;' if x.name == 'Final Handicapped Score' else
        'font-weight: bold; color: #4db380;' if not isinstance(x['Value'], str) and x['Value'] > 1.0 else
        'font-weight: bold; color: #e05a45;' if not isinstance(x['Value'], str) and x['Value'] < 1.0 else
        'font-weight: normal; color: #e9ecef;',
        '' if isinstance(x['Value'], str) else
        'font-weight: bold;' if x.name == 7 else  # Final score row
        '',
        '',
        ''
    ], axis=1)
    
    # Display the table
    st.dataframe(styled_df, use_container_width=True)

def render_comparison_visualization(
    factors_a: FactorResults, 
    factors_b: FactorResults, 
    hs_a: float, 
    hs_b: float, 
    config: JARConfig
) -> None:
    """
    Render visualization comparing two practitioners.
    
    Args:
        factors_a: Calculated factors for practitioner A
        factors_b: Calculated factors for practitioner B
        hs_a: Handicapped score for practitioner A
        hs_b: Handicapped score for practitioner B
        config: JAR system configuration
    """
    st.write("### Practitioner Comparison")
    
    # Create tabs for different comparisons
    tab1, tab2 = st.tabs(["Factor Comparison", "Radar Chart"])
    
    with tab1:
        render_factor_comparison_chart(factors_a, factors_b, hs_a, hs_b)
    
    with tab2:
        render_radar_chart(factors_a, factors_b)

def render_factor_comparison_chart(
    factors_a: FactorResults, 
    factors_b: FactorResults, 
    hs_a: float, 
    hs_b: float
) -> None:
    """
    Render a bar chart comparing factors between two practitioners.
    
    Args:
        factors_a: Calculated factors for practitioner A
        factors_b: Calculated factors for practitioner B
        hs_a: Handicapped score for practitioner A
        hs_b: Handicapped score for practitioner B
    """
    # Create dataframe for comparison
    factors_list = ['brs', 'af', 'wf', 'acf', 'ref', 'tff', 'cef']
    data = []
    
    # Add factor data for both practitioners
    for factor in factors_list:
        data.append({
            'Factor': FACTOR_FULL_NAMES[factor],
            'Practitioner A': getattr(factors_a, factor),
            'Practitioner B': getattr(factors_b, factor),
            'Type': 'Base' if factor == 'brs' else 'Multiplier'
        })
    
    # Add final scores
    data.append({
        'Factor': 'Final Score',
        'Practitioner A': hs_a,
        'Practitioner B': hs_b,
        'Type': 'Result'
    })
    
    df = pd.DataFrame(data)
    
    # Create the comparison chart with larger size and dark background
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor('#1e1e1e')
    ax.set_facecolor('#2a2a2a')
    
    # Update text color for better visibility in dark mode
    ax.xaxis.label.set_color('#e9ecef')
    ax.yaxis.label.set_color('#e9ecef')
    ax.tick_params(axis='x', colors='#e9ecef')
    ax.tick_params(axis='y', colors='#e9ecef')
    ax.title.set_color('#e9ecef')
    
    # Get positions for bars
    x = np.arange(len(df))
    width = 0.4  # Wider bars
    
    # Create bars with stronger colors
    rects1 = ax.bar(x - width/2, df['Practitioner A'], width, label='Practitioner A', color='#3366cc', alpha=0.9)
    rects2 = ax.bar(x + width/2, df['Practitioner B'], width, label='Practitioner B', color='#cc3333', alpha=0.9)
    
    # Add labels and title with larger font
    ax.set_title('Factor Comparison Between Practitioners', fontsize=18, pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(df['Factor'], rotation=30, ha='right', fontsize=14)  # Less rotation, larger font
    
    # Add a horizontal line at y=1.0 for multiplier reference
    ax.axhline(y=1.0, color='black', linestyle='--', alpha=0.7, linewidth=1.5)
    
    # Add legend
    ax.legend()
    
    # Add value labels above bars
    def add_labels(rects):
        for rect in rects:
            height = rect.get_height()
            if height >= 10:  # For BRS and Final Score
                label_format = f"{height:.0f}"
            else:  # For multipliers
                label_format = f"{height:.2f}x"
            
            ax.annotate(label_format,
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=8)
    
    add_labels(rects1)
    add_labels(rects2)
    
    # Adjust layout
    plt.tight_layout()
    
    # Show the plot
    st.pyplot(fig)

def render_radar_chart(factors_a: FactorResults, factors_b: FactorResults) -> None:
    """
    Render a radar chart comparing practitioners' attributes.
    
    Args:
        factors_a: Calculated factors for practitioner A
        factors_b: Calculated factors for practitioner B
    """
    # Define categories for radar chart
    categories = ['Belt Rank', 'Age', 'Weight', 'Athleticism', 
                 'Grappling Exp', 'Training Freq', 'Competition']
    
    # Normalize values for radar chart
    # For BRS, we need to normalize it to a 0-1 scale
    # We'll use a 800 (Black belt) as the max
    brs_max = 800
    
    # Create normalized values array
    values_a = [
        factors_a.brs / brs_max,  # Normalize BRS
        factors_a.af,
        factors_a.wf,
        factors_a.acf,
        factors_a.ref,
        factors_a.tff,
        factors_a.cef
    ]
    
    values_b = [
        factors_b.brs / brs_max,  # Normalize BRS
        factors_b.af,
        factors_b.wf,
        factors_b.acf,
        factors_b.ref,
        factors_b.tff,
        factors_b.cef
    ]
    
    # Compute angles for each category
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Close the loop
    
    # Extend values arrays to close the loop
    values_a += values_a[:1]
    values_b += values_b[:1]
    
    # Create the figure with larger size and dark background
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#1e1e1e')
    ax.set_facecolor('#2a2a2a')
    
    # Set text color for better visibility in dark mode
    for label in ax.get_xticklabels():
        label.set_color('#e9ecef')
    for label in ax.get_yticklabels():
        label.set_color('#e9ecef')
    ax.title.set_color('#e9ecef')
    
    # Draw the radar chart with thicker lines and clearer markers
    ax.plot(angles, values_a, 'o-', linewidth=3, markersize=8, label='Practitioner A', color='#3366cc')
    ax.fill(angles, values_a, alpha=0.2, color='#3366cc')
    
    ax.plot(angles, values_b, 'o-', linewidth=3, markersize=8, label='Practitioner B', color='#cc3333')
    ax.fill(angles, values_b, alpha=0.2, color='#cc3333')
    
    # Add categories labels with larger, more readable font
    ax.set_thetagrids(np.degrees(angles[:-1]), categories, fontsize=16)
    
    # Add reference line at 1.0
    ax.plot(angles, [1.0] * len(angles), '--', color='black', alpha=0.7, linewidth=1.5)
    
    # Add labels for the values
    for i, (angle, value_a, value_b) in enumerate(zip(angles[:-1], values_a[:-1], values_b[:-1])):
        if categories[i] == 'Belt Rank':
            # For belt rank, show actual belt names
            if values_a[i] <= 0.125:  # White belt
                label_a = "White"
            elif values_a[i] <= 0.25:  # Blue belt
                label_a = "Blue"
            elif values_a[i] <= 0.4375:  # Purple belt
                label_a = "Purple"
            elif values_a[i] <= 0.6875:  # Brown belt
                label_a = "Brown"
            else:  # Black belt
                label_a = "Black"
                
            if values_b[i] <= 0.125:  # White belt
                label_b = "White"
            elif values_b[i] <= 0.25:  # Blue belt
                label_b = "Blue"
            elif values_b[i] <= 0.4375:  # Purple belt
                label_b = "Purple"
            elif values_b[i] <= 0.6875:  # Brown belt
                label_b = "Brown"
            else:  # Black belt
                label_b = "Black"
                
            ax.annotate(f"A: {label_a}", xy=(angle, value_a + 0.1), 
                       xytext=(angle, value_a + 0.2),
                       arrowprops=dict(arrowstyle='->', color='#3498db'),
                       ha='center', va='center', color='#3498db')
            
            ax.annotate(f"B: {label_b}", xy=(angle, value_b + 0.1), 
                       xytext=(angle, value_b + 0.2),
                       arrowprops=dict(arrowstyle='->', color='#e74c3c'),
                       ha='center', va='center', color='#e74c3c')
    
    # Add legend
    ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    # Add title
    plt.title('Practitioner Attributes Comparison', size=20, y=1.05, color='#e9ecef')
    
    # Show the plot
    st.pyplot(fig)