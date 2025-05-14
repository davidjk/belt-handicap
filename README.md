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

- **Single Practitioner Analysis**: Calculate and visualize a practitioner's Handicapped Score and profile
- **Practitioner Comparison**: Compare two practitioners side-by-side with visualization of differences
- **Factor Visualization**: Interactive charts showing the contribution of each factor to the final score
- **Roll Dynamics Profiles**: Qualitative assessments of practitioner strengths, challenges, and likely roll approaches
- **Configurable System**: All parameters can be customized through the UI

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

1. Navigate to the "Single Practitioner" page to analyze an individual
2. Input practitioner details and click "Calculate Score"
3. Review the factor breakdown and Roll Dynamics Profile
4. Use the "Compare Practitioners" page to assess two practitioners against each other
5. Advanced users can modify system parameters in the "Configuration" page

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.