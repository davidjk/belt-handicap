# JAR System - Jiu-Jitsu Attribute Rating

A modern web application implementing the Jiu-Jitsu Attribute Rating (JAR) system, which provides a multi-factor approach to assessing and comparing Brazilian Jiu-Jitsu practitioners beyond belt rank alone.

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
- **Animated Radar Charts**: Dynamic visualizations with smooth transitions using Chart.js
- **Modern UI**: Clean, professional interface with smooth animations and micro-interactions
- **Practitioner Comparison**: Side-by-side comparison with intuitive visualization of differences
- **Roll Dynamics Profiles**: Qualitative assessments of strengths, challenges, and likely roll approaches
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Performance Optimized**: Fast, client-side calculations with no server dependency

## Installation & Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/belt-handicap.git
cd belt-handicap
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Build for production:
```bash
npm run build
```

## Project Structure

- `index.html`: Main application entry point
- `src/`: Source code
  - `main.js`: Application initialization and coordination
  - `js/`: Core JavaScript modules
    - `calculator.js`: Factor calculation functions
    - `types.js`: Data types and models
    - `config.js`: Configuration handling
    - `profiles.js`: Roll Dynamics Profile generation
    - `forms.js`: Form handling and input management
    - `chart.js`: Radar chart visualization
    - `storage.js`: Local storage utilities
  - `css/`: Styling
    - `main.css`: Main stylesheet with modern design system
- `data/`: Configuration files
- `docs/`: Documentation
  - `initial_prd.md`: Original product requirements
  - `streamlit_implementation.md`: Implementation guide
- `archive/`: Archived Streamlit prototype

## Usage

1. Open the application in your web browser
2. Input details for two practitioners using the form fields
3. Watch scores update in real-time as you adjust values
4. View the dynamic radar chart comparing both practitioners
5. Read the Roll Dynamics Profiles for qualitative analysis
6. All calculations happen instantly in your browser - no server required

## Technology Stack

- **Frontend**: Vanilla JavaScript (ES6+), HTML5, CSS3
- **Build Tool**: Vite for fast development and optimized builds
- **Visualization**: Chart.js for animated radar charts
- **Styling**: Modern CSS with custom properties and animations
- **Deployment**: Static hosting (GitHub Pages compatible)

## Archive Note

The original Python/Streamlit prototype has been archived in the `archive/streamlit-prototype/` directory. The current implementation uses vanilla JavaScript for better performance and user experience.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.