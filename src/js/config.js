// Configuration manager for JAR system
export class ConfigManager {
    constructor() {
        this.config = null;
        this.defaultConfig = {
            "belt_rank_scores": {
                "White": 100,
                "Blue": 200,
                "Purple": 350,
                "Brown": 550,
                "Black": 800
            },
            "age_factor_config": {
                "peak_age_years": 25,
                "youthful_factor_multiplier": 1.03,
                "power_decline_rate_per_decade": 0.12
            },
            "weight_factor_config": {
                "increment_lbs": 15.0,
                "thresholds_bonuses_penalties": [
                    { "diff_max_lbs": 15.0, "adjustment": 0.06 },
                    { "diff_max_lbs": 30.0, "adjustment": 0.08 },
                    { "diff_max_lbs": 45.0, "adjustment": 0.10 }
                ]
            },
            "acf_config": {
                "levels": [
                    { "level_id": 1, "description": "Below Average (<30th percentile)", "multiplier": 0.90 },
                    { "level_id": 2, "description": "Average Hobbyist (30th-60th percentile)", "multiplier": 1.00 },
                    { "level_id": 3, "description": "Above Average (61st-80th percentile)", "multiplier": 1.07 },
                    { "level_id": 4, "description": "Notably Athletic (81st-95th percentile)", "multiplier": 1.15 },
                    { "level_id": 5, "description": "Exceptional Athlete (>95th percentile)", "multiplier": 1.25 }
                ]
            },
            "ref_config": {
                "levels": [
                    { "level_id": 0, "description": "None", "multiplier": 1.0 },
                    { "level_id": 1, "description": "Limited/Recreational (e.g., <1 yr casual in other art)", "multiplier": 1.03 },
                    { "level_id": 2, "description": "Foundational Skill (e.g., Avg HS Wrestler/Judoka, 1-3 yrs consistent)", "multiplier": 1.07 },
                    { "level_id": 3, "description": "Accomplished (e.g., Good HS Wrestler/Judoka, Judo Shodan, 3-5+ yrs, regional comps)", "multiplier": 1.12 },
                    { "level_id": 4, "description": "High-Level Competitor (e.g., NCAA D1 Wrestler, National Judoka)", "multiplier": 1.22 },
                    { "level_id": 5, "description": "Elite International (e.g., Olympic/World Medalist in Wrestling/Judo)", "multiplier": 1.38 }
                ],
                "art_experience_level_mapping": {
                    "Wrestling_Recreational/Limited (<1 year)": 1,
                    "Wrestling_Foundational (1-3 years)": 2,
                    "Wrestling_Accomplished (3-5+ years, regional level)": 3,
                    "Wrestling_High-Level Competitor (National level)": 4,
                    "Wrestling_Elite International (Olympic/World level)": 5,
                    
                    "Judo_Recreational/Limited (<1 year)": 1,
                    "Judo_Foundational (1-3 years)": 2, 
                    "Judo_Accomplished (3-5+ years, regional level)": 3,
                    "Judo_High-Level Competitor (National level)": 4,
                    "Judo_Elite International (Olympic/World level)": 5,
                    
                    "Sambo_Recreational/Limited (<1 year)": 1,
                    "Sambo_Foundational (1-3 years)": 2,
                    "Sambo_Accomplished (3-5+ years, regional level)": 3,
                    "Sambo_High-Level Competitor (National level)": 4,
                    "Sambo_Elite International (Olympic/World level)": 5,
                    
                    "Other_Recreational/Limited (<1 year)": 1,
                    "Other_Foundational (1-3 years)": 2,
                    "Other_Accomplished (3-5+ years, regional level)": 3,
                    "Other_High-Level Competitor (National level)": 4,
                    "Other_Elite International (Olympic/World level)": 5,
                    
                    "None_None": 0
                }
            },
            "tff_config": {
                "levels": [
                    { "sessions_min": 0, "sessions_max": 1, "multiplier": 0.95 },
                    { "sessions_min": 2, "sessions_max": 3, "multiplier": 1.00 },
                    { "sessions_min": 4, "sessions_max": 5, "multiplier": 1.05 },
                    { "sessions_min": 6, "sessions_max": 100, "multiplier": 1.10 }
                ]
            },
            "cef_config": {
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
                },
                "control_implication_factors": ["REF_high_wrestling_judo", "ACF_high", "WF_high"],
                "submission_implication_factors_offense": ["BRS_high"],
                "submission_implication_factors_defense": ["BRS_high"]
            }
        };
        
        this.loadConfig();
    }
    
    loadConfig() {
        // For now, use the default config
        // In the future, this could load from localStorage or a remote source
        this.config = { ...this.defaultConfig };
    }
    
    getConfig() {
        return this.config;
    }
    
    saveConfig(newConfig) {
        this.config = { ...newConfig };
        // Save to localStorage for persistence
        localStorage.setItem('jar-config', JSON.stringify(this.config));
    }
}