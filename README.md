# Belt Handicap (JAR System)

A Streamlit application implementing the Jiu-Jitsu Attribute Rating (JAR) system, which provides a multi-factor approach to assessing and comparing Brazilian Jiu-Jitsu practitioners beyond belt rank alone.

## Overview

The JAR system calculates a Handicapped Score (HS) for BJJ practitioners based on multiple attributes:

- Belt Rank Score (BRS): Foundational score representing accumulated BJJ-specific skill
- Age Factor (AF): Accounts for age-related physiological factors
- Weight/Size Factor (WF): Reflects the impact of weight differences
- Athleticism & Conditioning Factor (ACF): Quantifies general physical prowess
- Relevant Grappling Experience Factor (REF): Credits transferable skills from other disciplines
- Training Intensity/Frequency Factor (TFF): Reflects current BJJ training volume
- BJJ Competition Experience Factor (CEF): Accounts for competition-specific skills

The system also generates a Roll Dynamics Profile that provides qualitative insights into potential matchup dynamics.

## Features

- **Live Interactive Scoring**: Scores update in real-time as you adjust any attribute
- **Impact Visualization**: Clear display of how each factor affects the final score with percentage indicators
- **Practitioner Comparison**: Side-by-side comparison with intuitive visualization of differences
- **Roll Dynamics Profiles**: Qualitative assessments of strengths, challenges, and likely roll approaches
- **Save Practitioner Pairs**: Store frequently compared practitioners for quick access
- **Configurable System**: All parameters can be customized through the UI
- **Dark Theme**: Enhanced readability with a dark theme throughout the application

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/belt-handicap.git
cd belt-handicap
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run app.py
```

## Project Structure

- `app.py`: Main Streamlit application entry point
- `jar/`: Core JAR system logic
  - `types.py`: Data types and models
  - `calculator.py`: Factor calculation functions
  - `config.py`: Configuration handling
  - `profiles.py`: Roll Dynamics Profile generation
- `ui/`: UI components
  - `input_forms.py`: Practitioner data input forms
  - `visualizations.py`: Data visualization components
  - `profile_display.py`: Profile rendering
- `data/`: Configuration and example data
- `docs/`: Documentation
  - `initial_prd.md`: Original product requirements
  - `streamlit_implementation.md`: Implementation guide

## Usage

1. Input details for two practitioners in the comparison view
2. Watch scores update in real-time as you adjust values
3. See the percentage impact of each attribute next to the input
4. Click "Compare Practitioners" to view detailed radar charts and profiles
5. Save frequently used pairs with the "Save Current" button
6. Load saved pairs for quick comparison
7. Advanced users can modify system parameters in the "Configuration" tab

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.