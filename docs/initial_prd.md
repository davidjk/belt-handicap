# Jiu-Jitsu Attribute Rating (JAR) System
## Software Specification Document
**Version:** 1.0  
**Date:** May 13, 2025  
**Author:** Gemini AI (based on collaborative development)

## Table of Contents:
1. [Introduction & Purpose](#1-introduction--purpose)
2. [System Architecture Overview](#2-system-architecture-overview)
3. [Data Structures](#3-data-structures)
   - [3.1. Practitioner Input Data](#31-practitioner-input-data)
   - [3.2. JAR System Configuration Data](#32-jar-system-configuration-data)
4. [Core Calculation Logic](#4-core-calculation-logic)
   - [4.1. Belt Rank Score (BRS)](#41-belt-rank-score-brs)
   - [4.2. Age Factor (AF)](#42-age-factor-af)
   - [4.3. Weight/Size Factor (WF)](#43-weightsize-factor-wf)
   - [4.4. Athleticism & Conditioning Factor (ACF)](#44-athleticism--conditioning-factor-acf)
   - [4.5. Relevant Grappling Experience Factor (REF)](#45-relevant-grappling-experience-factor-ref)
   - [4.6. Training Intensity/Frequency Factor (TFF)](#46-training-intensityfrequency-factor-tff)
   - [4.7. BJJ Competition Experience Factor (CEF)](#47-bjj-competition-experience-factor-cef)
   - [4.8. Handicapped Score (HS) Calculation](#48-handicapped-score-hs-calculation)
5. [Roll Dynamics Profile Generation](#5-roll-dynamics-profile-generation)
   - [5.1. Inputs for Profile Generation](#51-inputs-for-profile-generation)
   - [5.2. Logic for Profile Generation](#52-logic-for-profile-generation)
   - [5.3. Profile Output Structure](#53-profile-output-structure)
   - [5.4. Rationale for Profile Components](#54-rationale-for-profile-components)
6. [System Configuration and Calibration](#6-system-configuration-and-calibration)
7. [Example Usage Flow (Conceptual)](#7-example-usage-flow-conceptual)
8. [Desired Code Characteristics](#8-desired-code-characteristics)

## 1. Introduction & Purpose
The Jiu-Jitsu Attribute Rating (JAR) system is a conceptual framework designed to provide a more nuanced understanding of practitioner matchups in Brazilian Jiu-Jitsu (BJJ), moving beyond sole reliance on belt rank.

**Purpose:**
- To calculate a relative Handicapped Score (HS) for individual BJJ practitioners based on a range of attributes.
- To generate a Roll Dynamics Profile that offers qualitative insights into potential matchup dynamics, including control versus submission likelihoods.
- To serve as a tool for practitioners, instructors, and analysts to facilitate more informed discussions about training, individual strengths/weaknesses, and development.
- To help in setting appropriate training challenges and managing expectations for sparring sessions.

Crucially, the JAR system is NOT designed to definitively predict winners or losers but rather to contextualize potential performance based on a broader set of factors.

**Why this system?** BJJ performance is influenced by more than just belt rank. Factors like age, physical attributes, experience in other grappling arts, and competitive history play significant roles. This system attempts to quantify these influences in a structured, transparent, and calibrate-able manner.

## 2. System Architecture Overview
The JAR system will function based on the following flow:

**Inputs:**
- Data for two (or more) BJJ practitioners.
- A set of configurable JAR system parameters (BRS values, factor rules, multiplier scales, etc.).

**Processing:**
- For each practitioner, calculate individual Attribute Adjuster (AA) multipliers (AF, WF, ACF, REF, TFF, CEF) based on their input data and the system's configuration rules.
- Calculate the final Handicapped Score (HS) for each practitioner by applying these multipliers to their Belt Rank Score (BRS).
- Generate a qualitative "Roll Dynamics Profile" for each practitioner based on their HS and the key contributing factors.

**Outputs:**
- The calculated Handicapped Score (HS) for each practitioner.
- The generated Roll Dynamics Profile for each practitioner.

**Key Design Principle: Calibrate-ability**
The entire system is designed to be highly calibrate-able. All base scores, thresholds, rates of change, and even the descriptive text for profiles should be configurable by the end-users (e.g., a gym or a group of analysts) to best reflect their specific observations and environment. This specification will provide a "reference implementation" for these values, but the software should allow them to be overridden.

## 3. Data Structures
### 3.1. Practitioner Input Data
For each practitioner, the following data points are required:
```json
{
  "practitioner_id": "string", // Unique identifier
  "name": "string", // Optional, for display
  "bjj_belt_rank": "string", // e.g., "White", "Blue", "Purple", "Brown", "Black"
  "age_years": "integer",
  "weight_lbs": "float",
  "primary_occupation_activity_level": "string", // e.g., "Sedentary (Desk Job)", "Moderately Active", "Physically Demanding" - used to help inform ACF
  "standardized_fitness_test_percentile_estimate": "integer", // Optional: 0-100, if available, to inform ACF. If not, ACF relies on qualitative assessment based on occupation/observation.
  "other_grappling_art_experience": [ // Array of objects for multiple arts if necessary
    {
      "art_name": "string", // e.g., "Wrestling", "Judo", "Sambo"
      "experience_level_descriptor": "string" // e.g., "Recreational High School", "NCAA D1 Starter", "Judo Shodan", "Olympic Medalist" - used to map to REF Level
    }
  ],
  "bjj_training_sessions_per_week": "integer",
  "bjj_competition_experience_level": "string" // e.g., "None", "Limited Local", "Regular Regional", "National/International" - used to map to CEF Level
}
```

### 3.2. JAR System Configuration Data
This data structure will hold all the calibrate-able parameters of the JAR system.
```json
{
  "belt_rank_scores": {
    "White": 100,
    "Blue": 200,
    "Purple": 350,
    "Brown": 550,
    "Black": 800
    // Potentially more for degrees/coral belts
  },
  "age_factor_config": {
    "peak_age_years": 25,
    "youthful_factor_multiplier": 1.03, // For ages < peak_age
    "power_decline_rate_per_decade": 0.12 // e.g., 12% from previous value
  },
  "weight_factor_config": {
    "increment_lbs": 15.0,
    "thresholds_bonuses_penalties": [ // Non-linear: [max_lbs_in_threshold, marginal_multiplier_adjustment]
      { "diff_max_lbs": 15.0, "adjustment": 0.06 },
      { "diff_max_lbs": 30.0, "adjustment": 0.08 }, // This is the *additional* adjustment for this tier
      { "diff_max_lbs": 45.0, "adjustment": 0.10 }  // Additional for this tier
      // Add more tiers if needed
    ]
  },
  "acf_config": { // Athleticism & Conditioning Factor
    "levels": [ // Based on qualitative assessment or fitness percentile estimates
      { "level_id": 1, "description": "Below Average (<30th percentile)", "multiplier": 0.90 },
      { "level_id": 2, "description": "Average Hobbyist (30th-60th percentile)", "multiplier": 1.00 },
      { "level_id": 3, "description": "Above Average (61st-80th percentile)", "multiplier": 1.07 },
      { "level_id": 4, "description": "Notably Athletic (81st-95th percentile)", "multiplier": 1.15 },
      { "level_id": 5, "description": "Exceptional Athlete (>95th percentile)", "multiplier": 1.25 }
    ]
  },
  "ref_config": { // Relevant Grappling Experience Factor (Non-Linear Direct Assignment)
    "levels": [
      { "level_id": 0, "description": "None", "multiplier": 1.0 },
      { "level_id": 1, "description": "Limited/Recreational (e.g., <1 yr casual in other art)", "multiplier": 1.03 },
      { "level_id": 2, "description": "Foundational Skill (e.g., Avg HS Wrestler/Judoka, 1-3 yrs consistent)", "multiplier": 1.07 },
      { "level_id": 3, "description": "Accomplished (e.g., Good HS Wrestler/Judoka, Judo Shodan, 3-5+ yrs, regional comps)", "multiplier": 1.12 },
      { "level_id": 4, "description": "High-Level Competitor (e.g., NCAA D1 Wrestler, National Judoka)", "multiplier": 1.22 },
      { "level_id": 5, "description": "Elite International (e.g., Olympic/World Medalist in Wrestling/Judo)", "multiplier": 1.38 }
    ],
    "art_experience_level_mapping": { // Helper to map practitioner input to REF level_id
      // Examples:
      "Wrestling_NCAA D1 Starter": 4,
      "Judo_Shodan": 3,
      "Wrestling_Olympic Medalist": 5,
      "None_None": 0 // Default if no experience
    }
  },
  "tff_config": { // Training Intensity/Frequency Factor
    "levels": [
      { "sessions_min": 0, "sessions_max": 1, "multiplier": 0.95 },
      { "sessions_min": 2, "sessions_max": 3, "multiplier": 1.00 },
      { "sessions_min": 4, "sessions_max": 5, "multiplier": 1.05 },
      { "sessions_min": 6, "sessions_max": 100, "multiplier": 1.10 } // 100 as a practical upper bound
    ]
  },
  "cef_config": { // BJJ Competition Experience Factor
    "levels": [
      { "level_id": 0, "description": "None", "multiplier": 1.0 },
      { "level_id": 1, "description": "Limited Local (1-2 local comps)", "multiplier": 1.03 },
      { "level_id": 2, "description": "Regular Regional (multiple regional/state comps per year)", "multiplier": 1.08 },
      { "level_id": 3, "description": "National/International (Pans, Euros, Worlds, ADCC Trials)", "multiplier": 1.12 }
    ],
    "competition_level_mapping": {
      "None": 0,
      "Limited Local": 1,
      "Regular Regional": 2,
      "National/International": 3
    }
  },
  "profile_dynamics_config": {
    "significant_multiplier_threshold_high": 1.10,
    "significant_multiplier_threshold_low": 0.90,
    "implication_statements": {
      "BRS_high": "Deep BJJ-specific technical knowledge, extensive submission arsenal, advanced defensive/offensive positional understanding.",
      "BRS_low": "Limited BJJ-specific submission knowledge (offense and defense) and nuanced BJJ positional play.",
      "REF_high_wrestling_judo": "Strong foundational grappling from another discipline (e.g., powerful takedowns, dominant top control, excellent scrambles, high grappling intensity).",
      "ACF_high": "Significant athletic advantage (e.g., superior strength, speed, explosiveness, or endurance).",
      "WF_high": "Substantial size/weight advantage; can apply significant pressure, more difficult to move or sweep.",
      "AF_low": "Age-related physical limitations; may face challenges with opponent's pace, explosiveness, recovery, and prolonged high-intensity exchanges.",
      "WF_low": "Size/weight disadvantage; may be vulnerable to being overpowered, struggle to escape bottom positions under pressure."
      // Add more for other factors and nuances
    },
    "control_implication_factors": ["REF_high_wrestling_judo", "ACF_high", "WF_high"],
    "submission_implication_factors_offense": ["BRS_high"],
    "submission_implication_factors_defense": ["BRS_high"]
  }
}
```

## 4. Core Calculation Logic
### 4.1. Belt Rank Score (BRS)
- **Input:** practitioner_data.bjj_belt_rank
- **Logic:** Direct lookup from jar_config.belt_rank_scores.
  ```
  BRS = jar_config.belt_rank_scores[practitioner_data.bjj_belt_rank]
  ```
- **Output:** BRS (integer).
- **Rationale:** BRS is the foundational score representing accumulated BJJ-specific skill, knowledge, and mat time. Values are scaled to provide significant differentiation between ranks.

### 4.2. Age Factor (AF)
- **Input:** practitioner_data.age_years, jar_config.age_factor_config
- **Logic (Reference: Power Decline Model):**
  - If age_years < peak_age_years, AF = youthful_factor_multiplier.
  - Else, calculate decades past peak: decades_past_peak = (age_years - peak_age_years) / 10.0.
  - AF = (1.0 - power_decline_rate_per_decade) ^ decades_past_peak.
- **Output:** AF (float multiplier).
- **Rationale:** Models age-related physiological decline, particularly in power output, which is critical for grappling. The power decline model is chosen over simpler VO2 max models as it may better reflect explosive capabilities. The youthful factor acknowledges benefits like rapid recovery for younger practitioners.

### 4.3. Weight/Size Factor (WF)
- **Inputs:** practitioner1_data.weight_lbs, practitioner2_data.weight_lbs, jar_config.weight_factor_config
- **Logic (Reference: Non-Linear Scaling, Threshold-Based - Calculated relative to opponent):**
  - Determine weight_difference = abs(practitioner1_data.weight_lbs - practitioner2_data.weight_lbs).
  - Identify heavier and lighter practitioner.
  - Initialize adjustment = 0.0.
  - Iterate through jar_config.weight_factor_config.thresholds_bonuses_penalties in order:
    - If weight_difference > 0:
      - weight_in_this_tier = min(weight_difference, current_threshold.diff_max_lbs - previous_threshold_diff_max_lbs_or_0)
      - adjustment += (weight_in_this_tier / jar_config.weight_factor_config.increment_lbs) * current_threshold.adjustment

  A more direct interpretation of the threshold logic:
  - Initialize total_adjustment = 0.0, remaining_diff = weight_difference, last_tier_max_lbs = 0.
  - For each tier in thresholds_bonuses_penalties:
    - lbs_covered_by_this_tier_max = tier.diff_max_lbs - last_tier_max_lbs
    - lbs_to_consider_in_this_tier = min(remaining_diff, lbs_covered_by_this_tier_max)
    - total_adjustment += (lbs_to_consider_in_this_tier / jar_config.weight_factor_config.increment_lbs_for_tier_rate_application) * tier.adjustment
    - remaining_diff -= lbs_to_consider_in_this_tier
    - last_tier_max_lbs = tier.diff_max_lbs
    - If remaining_diff <= 0, break.
  - For the heavier practitioner, WF = 1.0 + total_adjustment.
  - For the lighter practitioner, WF = 1.0 - total_adjustment.
- **Output:** WF (float multiplier) for each practitioner.
- **Rationale:** Acknowledges the significant physical impact of mass. The non-linear, threshold-based approach reflects the idea that the marginal impact of weight differences can increase as the disparity grows, rather than being strictly linear.

### 4.4. Athleticism & Conditioning Factor (ACF)
- **Inputs:** practitioner_data.primary_occupation_activity_level, practitioner_data.standardized_fitness_test_percentile_estimate (optional), jar_config.acf_config.
- **Logic:**
  - Determine ACF Level (1-5). This can be:
    - Directly from standardized_fitness_test_percentile_estimate mapped to acf_config.levels percentile bands.
    - Qualitatively assessed by users based on primary_occupation_activity_level, observation of the practitioner, and mapped to an acf_config.levels.level_id. The system should provide guidance for this qualitative mapping.
  - ACF_multiplier = jar_config.acf_config.levels[determined_level_id-1].multiplier.
- **Output:** ACF (float multiplier).
- **Rationale:** Quantifies general physical prowess beyond specific BJJ skill or weight. Linking to fitness percentiles (even if estimated) provides a more objective grounding than pure observation alone.

### 4.5. Relevant Grappling Experience Factor (REF)
- **Inputs:** practitioner_data.other_grappling_art_experience, jar_config.ref_config.
- **Logic (Reference: Non-Linear Direct Assignment):**
  - If practitioner_data.other_grappling_art_experience is empty or indicates no significant experience, REF_level_id = 0.
  - Else, for the most significant prior art:
    - Use jar_config.ref_config.art_experience_level_mapping to determine the REF_level_id based on art_name and experience_level_descriptor.
    - If no direct map, users may need to qualitatively assign to the closest REF_level_id based on jar_config.ref_config.levels.description.
  - REF_multiplier = jar_config.ref_config.levels[REF_level_id].multiplier.
- **Output:** REF (float multiplier).
- **Rationale:** Credits transferable skills, competitive hardening, and grappling acumen from other significant disciplines. The non-linear scale acknowledges that the jump in ability between experience levels (e.g., accomplished high school vs. Olympic medalist) is not uniform.

### 4.6. Training Intensity/Frequency Factor (TFF)
- **Inputs:** practitioner_data.bjj_training_sessions_per_week, jar_config.tff_config.
- **Logic:**
  - Iterate through jar_config.tff_config.levels.
  - Find the level where sessions_per_week falls between sessions_min and sessions_max.
  - TFF_multiplier = matched_level.multiplier.
- **Output:** TFF (float multiplier).
- **Rationale:** Reflects current BJJ training volume and preparedness. More frequent training typically leads to better skill retention, conditioning, and timing.

### 4.7. BJJ Competition Experience Factor (CEF)
- **Inputs:** practitioner_data.bjj_competition_experience_level, jar_config.cef_config.
- **Logic:**
  - Use jar_config.cef_config.competition_level_mapping to get the CEF_level_id from practitioner_data.bjj_competition_experience_level.
  - CEF_multiplier = jar_config.cef_config.levels[CEF_level_id].multiplier.
- **Output:** CEF (float multiplier).
- **Rationale:** Accounts for skills and mental adaptations developed specifically through BJJ competition (performing under pressure, strategy against resisting BJJ opponents, rule set familiarity).

### 4.8. Handicapped Score (HS) Calculation
- **Inputs:** BRS, AF, WF, ACF, REF, TFF, CEF for a practitioner.
- **Logic:**
  ```
  HS = BRS * AF * WF * ACF * REF * TFF * CEF
  ```
- **Output:** HS (float).
- **Rationale:** The HS is a composite score representing the overall "effective grappling potential" after all attribute adjustments are applied to the base BJJ skill score.

## 5. Roll Dynamics Profile Generation
### 5.1. Inputs for Profile Generation:
- Practitioner's calculated HS.
- Practitioner's BRS value.
- Practitioner's individual Attribute Adjuster multipliers (AF, WF, ACF, REF, TFF, CEF).
- jar_config.profile_dynamics_config.

### 5.2. Logic for Profile Generation:
**Identify Significant Factors:**
- For each AA multiplier, compare it to significant_multiplier_threshold_high and significant_multiplier_threshold_low.
- Store factors that are "significantly high" or "significantly low."

**Determine "Dominant Trait(s)" and "Likely Roll Approach":**
- This involves a heuristic. Example logic:
  - If BRS is high and most AAs are neutral or negative: "Technical BJJ Specialist," "Defensive & Opportunistic."
  - If BRS is low but REF, ACF, WF are high: "Physical Grappling Athlete," "Control-Oriented."
  - If BRS is high and many AAs are also high: "Dominant All-Rounder."
- This part might require more complex rule-based logic or pattern matching based on the profile of multipliers.

**Populate Key Strengths:**
- Include BRS if it's a defining feature (e.g., Purple belt and above). Use implication_statements.BRS_high.
- For each "significantly high" AA multiplier, retrieve the corresponding general implication statement (e.g., implication_statements.REF_high_wrestling_judo).
- Add specific "Control Implication" or "Submission Implication" if the factor is listed in control_implication_factors or submission_implication_factors_offense.

**Populate Key Challenges/Disadvantages:**
- Include BRS if low. Use implication_statements.BRS_low.
- For each "significantly low" AA multiplier, retrieve the corresponding implication statement.

**Determine Specific Outlook (Control/Submission Threat/Defense):**
- Control Potential: Heuristic based on the net positive impact of REF, WF (if heavier), ACF. (e.g., High if REF > 1.15 and WF > 1.10).
- BJJ Submission Offensive Threat: Primarily based on BRS tier (e.g., High for Purple+, Medium for Blue, Low for White), potentially modified slightly by CEF.
- BJJ Submission Defensive Resilience: Primarily based on BRS tier, potentially modified by negative physicals (low AF/WF might reduce it slightly).

### 5.3. Profile Output Structure (Text-based):
Follow the template provided in the previous discussion (response #15), populating sections with the derived statements.

### 5.4. Rationale for Profile Components:
The profile aims to translate the quantitative HS and its constituent factors into qualitative, actionable insights about how a roll might unfold, specifically addressing the control vs. submission dynamic. It acknowledges that a single score doesn't tell the whole story.

## 6. System Configuration and Calibration
**Mechanism:** The software should load its operational parameters (all values within the jar_config structure) from an external configuration source (e.g., a JSON file, a database, environment variables).

**User Interface (Ideal):** For advanced use, a UI could allow users to view and modify these configuration parameters.

**Default Configuration:** The software should ship with the "reference implementation" values as detailed in this specification as its default configuration.

**Rationale:** This ensures the system is adaptable to different user groups, observations, and evolving understandings of grappling dynamics. Calibration is key to the JAR system's long-term utility and acceptance.

## 7. Example Usage Flow (Conceptual)
1. System loads jar_config.
2. User inputs data for Practitioner A and Practitioner B.
3. For Practitioner A:
   - BRS is determined.
   - AF, WF (relative to B), ACF, REF, TFF, CEF multipliers are calculated.
   - HS_A is calculated.
   - Roll Dynamics Profile_A is generated.
4. For Practitioner B:
   - BRS is determined.
   - AF, WF (relative to A), ACF, REF, TFF, CEF multipliers are calculated.
   - HS_B is calculated.
   - Roll Dynamics Profile_B is generated.
5. System outputs HS_A, Profile_A, HS_B, Profile_B.

## 8. Desired Code Characteristics (for the LLM generating the code)
- **Modularity:** Each factor calculation should ideally be a separate function or method. Profile generation should also be modular.
- **Clarity & Readability:** Code should be well-commented, with clear variable names and logical structure.
- **Configuration Driven:** All calibrate-able values (BRS, thresholds, rates, multipliers, text snippets for profiles) must be sourced from the configuration data structure, not hardcoded.
- **Testability:** Design components in a way that allows for unit testing (though the LLM won't write the tests unless asked).
- **Error Handling (Basic):** Handle potential issues like missing configuration values or invalid practitioner input gracefully (e.g., default values, clear error messages).
- **Language Agnostic (Conceptual):** While this specification is language-agnostic, if a specific language is chosen for implementation (e.g., Python for its data handling and readability), the code should follow best practices for that language.
- **Completeness:** The generated code should be a complete, runnable representation of the logic described.

This specification document provides a detailed blueprint for an LLM to create the JAR system. The emphasis on referencing the configuration for all parameters is critical for achieving the desired calibrate-ability.