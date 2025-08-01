# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The JAR (Jiu-Jitsu Attribute Rating) System is a Streamlit web application that calculates handicapped scores for Brazilian Jiu-Jitsu practitioners using seven factors beyond belt rank. It provides both quantitative scoring and qualitative "Roll Dynamics Profiles" for practitioner comparison.

## Development Commands

### Running the Application
```bash
streamlit run app.py
```

### Testing
```bash
python -m pytest tests/
python -m pytest tests/test_calculator.py::TestCalculator::test_specific_method  # Single test
python -m pytest -v  # Verbose output
```

### Dependencies
```bash
pip install -r requirements.txt
```

## Architecture Overview

### Core Calculation Flow
1. Seven factors calculated: BRS × AF × WF × ACF × REF × TFF × CEF = Handicapped Score
2. Real-time updates on any input change via Streamlit callbacks
3. Qualitative profile generation based on factor significance thresholds

### Module Structure
- **jar/**: Core business logic with four key modules:
  - `types.py`: Strongly-typed data models (`PractitionerData`, `FactorResults`, `RollDynamicsProfile`)
  - `calculator.py`: Seven-factor calculation engine with configuration-driven parameters
  - `config.py`: JSON-based configuration management with TypedDict validation
  - `profiles.py`: Qualitative analysis engine that converts scores to descriptive profiles
- **ui/**: Streamlit interface components with real-time reactivity
- **data/**: Configuration and practitioner storage (JSON persistence)

### Key Design Patterns
- **Configuration-Driven**: All parameters externalized to `data/default_config.json`
- **Type Safety**: Extensive use of dataclasses, TypedDict, and Literal types
- **Real-time Reactivity**: Instant score updates using Streamlit session state and callbacks
- **Immutable Calculations**: Pure functions for factor calculations

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
Complex session state handling prevents cross-contamination between practitioners A and B. Special `_loaded` keys preserve original data when practitioners are loaded from saved data.

## Configuration System

The application is fully configurable via `data/default_config.json`. Key configuration areas:
- Belt rank base scores
- Factor calculation parameters (thresholds, multipliers)
- Profile generation text templates
- Significance thresholds for qualitative analysis

## Adding New Features

### New Calculation Factors
1. Update `FactorResults` dataclass in `jar/types.py`
2. Add calculation method in `jar/calculator.py`
3. Update configuration schema and add parameters to `default_config.json`
4. Add UI inputs in `ui/input_forms.py`
5. Update tests in `tests/test_calculator.py`

### UI Components
- Follow existing patterns in `ui/` modules
- Use session state for reactive updates
- Maintain dark theme consistency
- Add impact indicators for new factors

## Testing Strategy

Unit tests focus on calculation logic correctness. Key test patterns:
- Configuration loading and validation
- Factor calculation accuracy
- Edge case handling (invalid inputs, missing data)
- Profile generation logic

## Data Persistence

Practitioners are saved to `data/saved_practitioners.json`. The system handles:
- Loading practitioners into forms
- Preventing data loss during edits
- Maintaining comparison state between practitioners A and B