# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The JAR (Jiu-Jitsu Attribute Rating) System is a modern vanilla JavaScript web application that calculates handicapped scores for Brazilian Jiu-Jitsu practitioners using seven factors beyond belt rank. It provides both quantitative scoring and qualitative "Roll Dynamics Profiles" for practitioner comparison.

**Current Implementation**: Vanilla JavaScript + Vite + Chart.js  
**Archived Implementation**: Python/Streamlit prototype (see `archive/streamlit-prototype/`)

## Development Commands

### Running the Application
```bash
npm run dev
```

### Building for Production
```bash
npm run build
```

### Testing
```bash
npm test
```

### Dependencies
```bash
npm install
```

## Architecture Overview

### Core Calculation Flow
1. Seven factors calculated: BRS × AF × WF × ACF × REF × TFF × CEF = Handicapped Score
2. Real-time updates on any input change via JavaScript event listeners
3. Qualitative profile generation based on factor significance thresholds
4. Dynamic radar chart visualization with Chart.js animations

### Module Structure
- **src/js/**: Core business logic with JavaScript modules:
  - `types.js`: Data models and type definitions
  - `calculator.js`: Seven-factor calculation engine with configuration-driven parameters
  - `config.js`: JSON-based configuration management
  - `profiles.js`: Qualitative analysis engine that converts scores to descriptive profiles
  - `forms.js`: Form handling and input management
  - `chart.js`: Radar chart visualization with Chart.js
  - `storage.js`: Local storage utilities
- **src/css/**: Modern styling with CSS custom properties and animations
- **data/**: Configuration files (JSON)
- **archive/streamlit-prototype/**: Archived Python/Streamlit implementation

### Key Design Patterns
- **Configuration-Driven**: All parameters externalized to `data/default_config.json`
- **Modern JavaScript**: ES6+ modules with clean separation of concerns
- **Real-time Reactivity**: Instant score updates using JavaScript event listeners and DOM manipulation
- **Immutable Calculations**: Pure functions for factor calculations
- **Client-side Only**: No server dependency, all calculations run in browser
- **Performance Optimized**: Minimal bundle size with Vite build optimization

## Data Models & Types

### Core Factor Calculation
Seven factors with specific purposes:
- **BRS**: Belt Rank Score (100-800 base points)
- **AF**: Age Factor (peak age modeling with decline curves)
- **WF**: Weight Factor (threshold-based weight difference)
- **ACF**: Athleticism Factor (fitness percentile mapping)
- **REF**: Relevant Experience Factor (other grappling arts)
- **TFF**: Training Frequency Factor (sessions per week)
- **CEF**: Competition Experience Factor (BJJ competition history)

### State Management
Client-side state management using JavaScript objects and local storage. Clean separation between practitioners A and B data prevents cross-contamination.

## Configuration System

The application is fully configurable via `data/default_config.json`. Key configuration areas:
- Belt rank base scores
- Factor calculation parameters (thresholds, multipliers)
- Profile generation text templates
- Significance thresholds for qualitative analysis

## Adding New Features

### New Calculation Factors
1. Update data models in `src/js/types.js`
2. Add calculation method in `src/js/calculator.js`
3. Update configuration schema and add parameters to `data/default_config.json`
4. Add UI inputs in `src/js/forms.js`
5. Update radar chart configuration in `src/js/chart.js`
6. Add corresponding tests

### UI Components
- Follow modern CSS patterns with custom properties
- Use JavaScript event listeners for reactive updates
- Maintain consistent design system with animations
- Add smooth transitions for new visual elements

## Testing Strategy

Unit tests focus on calculation logic correctness using Vitest. Key test patterns:
- Configuration loading and validation
- Factor calculation accuracy
- Edge case handling (invalid inputs, missing data)
- Profile generation logic
- DOM manipulation and event handling

## Data Persistence

The current implementation is focused on real-time calculation without persistence. Local storage utilities are available in `src/js/storage.js` for future features:
- Configuration preferences
- Recent calculations
- Custom factor weights

## Archive Note

The original Python/Streamlit implementation has been moved to `archive/streamlit-prototype/`. That implementation included:
- Practitioner data persistence to JSON files
- Complex session state management
- Python-based calculation engine
- Streamlit UI components

Refer to the archived implementation for:
- Alternative calculation approaches
- Data persistence patterns
- Testing strategies for Python code