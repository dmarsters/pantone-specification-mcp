#!/usr/bin/env python3
"""
Pantone Specification MCP Server

Bridge layer for production-ready color specification.
Translates abstract color concepts from upstream domains into
reproducible Pantone Graphics (PMS) specifications.

Architecture:
- Layer 1: Pure taxonomy (COTY, classic references, era palettes)
- Layer 2: Deterministic bridge morphisms (domain → Pantone)
- Layer 3: Claude synthesis of intentionality reasoning

Author: Dal Marsters / Lushy Project
"""

from fastmcp import FastMCP
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import math
import numpy as np

# ==============================================================================
# INITIALIZE SERVER
# ==============================================================================

mcp = FastMCP("pantone-specification")

# ==============================================================================
# DATA STRUCTURES
# ==============================================================================

@dataclass
class PantoneReference:
    """A specific Pantone color reference."""
    code: str
    name: str
    hex: str
    year: Optional[int] = None  # COTY year if applicable
    era_mood: Optional[str] = None
    associations: Optional[List[str]] = None
    production_notes: Optional[List[str]] = None


class ProductionContext(Enum):
    PRINT_COATED = "print_coated"
    PRINT_UNCOATED = "print_uncoated"


class SourceDomain(Enum):
    HERALDIC = "heraldic"
    COCKTAIL = "cocktail"
    WINE = "wine"
    ERA = "era"
    HSV = "hsv"
    HEX = "hex"
    MOOD = "mood"


# ==============================================================================
# COLOR OF THE YEAR DATABASE
# ==============================================================================

COLOR_OF_THE_YEAR: Dict[int, Dict[str, Any]] = {
    2000: {
        "name": "Cerulean",
        "code": "15-4020",
        "hex": "#9BB7D4",
        "era_mood": "millennium_optimism",
        "associations": ["sky", "clarity", "fresh_start", "digital_age_dawn"],
        "pairs_with": {"game_show": "early_2000s_clean", "cocktail": "light_refreshing"}
    },
    2001: {
        "name": "Fuchsia Rose",
        "code": "17-2031",
        "hex": "#C74375",
        "era_mood": "bold_confidence",
        "associations": ["energy", "passion", "attention_demanding"],
        "pairs_with": {}
    },
    2002: {
        "name": "True Red",
        "code": "19-1664",
        "hex": "#BF1932",
        "era_mood": "post_911_resolve",
        "associations": ["strength", "solidarity", "american_spirit"],
        "pairs_with": {"heraldic": "gules_modern"}
    },
    2003: {
        "name": "Aqua Sky",
        "code": "14-4811",
        "hex": "#7BC4C4",
        "era_mood": "escape_seeking",
        "associations": ["tranquility", "retreat", "spa_culture"],
        "pairs_with": {}
    },
    2004: {
        "name": "Tigerlily",
        "code": "17-1456",
        "hex": "#E2583E",
        "era_mood": "exotic_warmth",
        "associations": ["spice", "adventure", "global_influence"],
        "pairs_with": {"cocktail": "tiki_revival"}
    },
    2005: {
        "name": "Blue Turquoise",
        "code": "15-5217",
        "hex": "#53B0AE",
        "era_mood": "calming_escapism",
        "associations": ["tropical", "healing", "retreat"],
        "pairs_with": {}
    },
    2006: {
        "name": "Sand Dollar",
        "code": "13-1106",
        "hex": "#DECDBE",
        "era_mood": "natural_grounding",
        "associations": ["organic", "neutral", "earth_tones"],
        "pairs_with": {"japanese_garden": "wabi_sabi_neutral"}
    },
    2007: {
        "name": "Chili Pepper",
        "code": "19-1557",
        "hex": "#9B1B30",
        "era_mood": "spicy_confidence",
        "associations": ["heat", "passion", "culinary_culture"],
        "pairs_with": {"wine": "deep_garnet"}
    },
    2008: {
        "name": "Blue Iris",
        "code": "18-3943",
        "hex": "#5A5B9F",
        "era_mood": "creative_twilight",
        "associations": ["imagination", "mysticism", "transition"],
        "pairs_with": {}
    },
    2009: {
        "name": "Mimosa",
        "code": "14-0848",
        "hex": "#F0C05A",
        "era_mood": "recession_optimism",
        "associations": ["hope", "sunshine", "resilience", "brunch_culture"],
        "pairs_with": {"cocktail": "champagne_brightness", "heraldic": "or_warm"}
    },
    2010: {
        "name": "Turquoise",
        "code": "15-5519",
        "hex": "#45B5AA",
        "era_mood": "healing_escape",
        "associations": ["protection", "tropical", "bohemian"],
        "pairs_with": {}
    },
    2011: {
        "name": "Honeysuckle",
        "code": "18-2120",
        "hex": "#D65076",
        "era_mood": "courageous_warmth",
        "associations": ["encouraging", "uplifting", "energetic"],
        "pairs_with": {}
    },
    2012: {
        "name": "Tangerine Tango",
        "code": "17-1463",
        "hex": "#DD4124",
        "era_mood": "spirited_energy",
        "associations": ["vivacious", "dramatic", "attention"],
        "pairs_with": {}
    },
    2013: {
        "name": "Emerald",
        "code": "17-5641",
        "hex": "#009473",
        "era_mood": "elegant_growth",
        "associations": ["luxury", "renewal", "sophistication"],
        "pairs_with": {"heraldic": "vert_jewel"}
    },
    2014: {
        "name": "Radiant Orchid",
        "code": "18-3224",
        "hex": "#B163A3",
        "era_mood": "creative_confidence",
        "associations": ["innovation", "artistry", "originality"],
        "pairs_with": {}
    },
    2015: {
        "name": "Marsala",
        "code": "18-1438",
        "hex": "#955251",
        "era_mood": "grounded_richness",
        "associations": ["wine", "earthiness", "sophistication", "robust"],
        "pairs_with": {"wine": "aged_nebbiolo", "cocktail": "digestif_warmth"}
    },
    2016: {
        "name": "Rose Quartz",
        "code": "13-1520",
        "hex": "#F7CAC9",
        "era_mood": "gender_fluidity",
        "co_color": "Serenity",
        "associations": ["softness", "compassion", "wellness"],
        "pairs_with": {}
    },
    "2016_secondary": {
        "name": "Serenity",
        "code": "15-3919",
        "hex": "#92A8D1",
        "era_mood": "gender_fluidity",
        "co_color": "Rose Quartz",
        "associations": ["calm", "relaxation", "mindfulness"],
        "pairs_with": {}
    },
    2017: {
        "name": "Greenery",
        "code": "15-0343",
        "hex": "#88B04B",
        "era_mood": "nature_reconnection",
        "associations": ["fresh", "zesty", "revitalizing", "environmental"],
        "pairs_with": {"japanese_garden": "spring_vitality"}
    },
    2018: {
        "name": "Ultra Violet",
        "code": "18-3838",
        "hex": "#5F4B8B",
        "era_mood": "cosmic_spirituality",
        "associations": ["inventive", "visionary", "counterculture"],
        "pairs_with": {}
    },
    2019: {
        "name": "Living Coral",
        "code": "16-1546",
        "hex": "#FF6F61",
        "era_mood": "optimistic_warmth",
        "associations": ["life_affirming", "nurturing", "sociable"],
        "pairs_with": {"cocktail": "aperol_spritz_culture"}
    },
    2020: {
        "name": "Classic Blue",
        "code": "19-4052",
        "hex": "#0F4C81",
        "era_mood": "stability_seeking",
        "associations": ["dependable", "calming", "confident", "timeless"],
        "pairs_with": {"heraldic": "azure_depth"}
    },
    2021: {
        "name": "Ultimate Gray",
        "code": "17-5104",
        "hex": "#939597",
        "era_mood": "pandemic_resilience",
        "co_color": "Illuminating",
        "associations": ["solid", "dependable", "rock", "resilience"],
        "pairs_with": {}
    },
    "2021_secondary": {
        "name": "Illuminating",
        "code": "13-0647",
        "hex": "#F5DF4D",
        "era_mood": "pandemic_hope",
        "co_color": "Ultimate Gray",
        "associations": ["optimism", "sunshine", "positivity", "warmth"],
        "pairs_with": {"heraldic": "or_bright"}
    },
    2022: {
        "name": "Very Peri",
        "code": "17-3938",
        "hex": "#6667AB",
        "era_mood": "digital_native",
        "associations": ["metaverse", "creativity", "transition", "novel"],
        "pairs_with": {}
    },
    2023: {
        "name": "Viva Magenta",
        "code": "18-1750",
        "hex": "#BB2649",
        "era_mood": "unconventional_power",
        "associations": ["bold", "fearless", "pulsating", "joyous"],
        "pairs_with": {}
    },
    2024: {
        "name": "Peach Fuzz",
        "code": "13-1023",
        "hex": "#FFBE98",
        "era_mood": "gentle_comfort",
        "associations": ["nurturing", "soft", "cozy", "tactile", "community"],
        "pairs_with": {"cocktail": "approachable_warmth"}
    }
}

# ==============================================================================
# CLASSIC REFERENCES DATABASE
# ==============================================================================

CLASSIC_REFERENCES: Dict[str, Dict[str, Any]] = {
    # Process Colors
    "reflex_blue": {
        "code": "Reflex Blue C",
        "hex": "#001489",
        "category": "process",
        "use_case": "corporate_primary",
        "note": "Standard 'blue' in corporate contexts"
    },
    "process_blue": {
        "code": "Process Blue C",
        "hex": "#0085CA",
        "category": "process",
        "use_case": "cyan_component"
    },
    "rubine_red": {
        "code": "Rubine Red C",
        "hex": "#CE0058",
        "category": "process",
        "use_case": "magenta_component"
    },
    "warm_red": {
        "code": "Warm Red C",
        "hex": "#F9423A",
        "category": "process",
        "use_case": "accessible_red",
        "note": "Friendlier than pure red, common in retail"
    },
    "yellow": {
        "code": "Yellow C",
        "hex": "#FEDD00",
        "category": "process",
        "use_case": "yellow_component"
    },
    "green": {
        "code": "Green C",
        "hex": "#00AB84",
        "category": "process",
        "use_case": "environmental_default"
    },
    "purple": {
        "code": "Purple C",
        "hex": "#BB29BB",
        "category": "process",
        "use_case": "creative_accent"
    },
    "orange_021": {
        "code": "Orange 021 C",
        "hex": "#FE5000",
        "category": "process",
        "use_case": "high_visibility",
        "note": "Safety, warnings, attention"
    },
    
    # Metallics
    "gold": {
        "code": "871 C",
        "hex": "#85714D",
        "category": "metallic",
        "use_case": "luxury_accent",
        "production_notes": ["Requires metallic ink or foil", "Cannot reproduce in CMYK"],
        "heraldic_mapping": "or"
    },
    "silver": {
        "code": "877 C",
        "hex": "#8A8D8F",
        "category": "metallic",
        "use_case": "modern_luxury",
        "production_notes": ["Requires metallic ink or foil", "Cannot reproduce in CMYK"],
        "heraldic_mapping": "argent"
    },
    "copper": {
        "code": "876 C",
        "hex": "#8B634B",
        "category": "metallic",
        "use_case": "craft_warmth",
        "production_notes": ["Requires metallic ink or foil"]
    },
    
    # Neutrals
    "black": {
        "code": "Black C",
        "hex": "#2D2926",
        "category": "neutral",
        "use_case": "text_default",
        "note": "Richer than process black",
        "heraldic_mapping": "sable"
    },
    "cool_gray_11": {
        "code": "Cool Gray 11 C",
        "hex": "#53565A",
        "category": "neutral",
        "use_case": "sophisticated_dark_gray"
    },
    "cool_gray_7": {
        "code": "Cool Gray 7 C",
        "hex": "#97999B",
        "category": "neutral",
        "use_case": "mid_gray_cool"
    },
    "cool_gray_3": {
        "code": "Cool Gray 3 C",
        "hex": "#C8C9C7",
        "category": "neutral",
        "use_case": "light_gray_cool"
    },
    "cool_gray_1": {
        "code": "Cool Gray 1 C",
        "hex": "#D9D9D6",
        "category": "neutral",
        "use_case": "near_white_cool"
    },
    "warm_gray_11": {
        "code": "Warm Gray 11 C",
        "hex": "#6E6259",
        "category": "neutral",
        "use_case": "sophisticated_warm_dark"
    },
    "warm_gray_7": {
        "code": "Warm Gray 7 C",
        "hex": "#968C83",
        "category": "neutral",
        "use_case": "mid_gray_warm"
    },
    "warm_gray_3": {
        "code": "Warm Gray 3 C",
        "hex": "#CEC4B9",
        "category": "neutral",
        "use_case": "light_gray_warm"
    },
    
    # Heritage Colors
    "navy": {
        "code": "289 C",
        "hex": "#0C2340",
        "category": "heritage",
        "use_case": "traditional_authority",
        "era_associations": ["1950s_corporate", "nautical", "ivy_league"],
        "heraldic_mapping": "azure_deep"
    },
    "burgundy": {
        "code": "188 C",
        "hex": "#7C2529",
        "category": "heritage",
        "use_case": "traditional_luxury",
        "era_associations": ["victorian", "academic", "wine"],
        "wine_mapping": "aged_bordeaux"
    },
    "forest_green": {
        "code": "350 C",
        "hex": "#2C5234",
        "category": "heritage",
        "use_case": "traditional_nature",
        "era_associations": ["british_racing", "country_club", "heritage"],
        "heraldic_mapping": "vert_deep"
    },
    "ivory": {
        "code": "7527 C",
        "hex": "#D6D2C4",
        "category": "heritage",
        "use_case": "premium_paper_stock",
        "era_associations": ["classical", "academic", "archival"]
    },
    
    # Standard Blues
    "286_blue": {
        "code": "286 C",
        "hex": "#0032A0",
        "category": "standard",
        "use_case": "classic_blue",
        "heraldic_mapping": "azure"
    },
    
    # Standard Reds
    "186_red": {
        "code": "186 C",
        "hex": "#C8102E",
        "category": "standard",
        "use_case": "true_red",
        "heraldic_mapping": "gules"
    },
    "187_red": {
        "code": "187 C",
        "hex": "#A6192E",
        "category": "standard",
        "use_case": "deep_red"
    },
    
    # Standard Greens
    "348_green": {
        "code": "348 C",
        "hex": "#00843D",
        "category": "standard",
        "use_case": "clear_green",
        "heraldic_mapping": "vert"
    },
    "361_green": {
        "code": "361 C",
        "hex": "#43B02A",
        "category": "standard",
        "use_case": "bright_green"
    },
    
    # Purples
    "2685_purple": {
        "code": "2685 C",
        "hex": "#56147D",
        "category": "standard",
        "use_case": "royal_purple",
        "heraldic_mapping": "purpure"
    },
    
    # Oranges/Browns
    "1525_orange": {
        "code": "1525 C",
        "hex": "#B86125",
        "category": "standard",
        "use_case": "burnt_orange",
        "heraldic_mapping": "tenne"
    }
}

# ==============================================================================
# ERA PALETTES DATABASE
# ==============================================================================

ERA_PALETTES: Dict[str, Dict[str, Any]] = {
    "1950s": {
        "mood": "postwar_optimism",
        "palette": [
            {"name": "Aqua", "code": "3242 C", "hex": "#6BCABA", "role": "appliance_signature"},
            {"name": "Pink", "code": "182 C", "hex": "#F5A3C7", "role": "feminine_accent"},
            {"name": "Charcoal", "code": "425 C", "hex": "#54585A", "role": "masculine_ground"},
            {"name": "Chrome Yellow", "code": "116 C", "hex": "#FFCD00", "role": "energy_accent"}
        ],
        "game_show_match": "1950s_game_show"
    },
    "1960s": {
        "mood": "space_age_pop",
        "palette": [
            {"name": "Orange", "code": "1585 C", "hex": "#FF8200", "role": "mod_primary"},
            {"name": "Avocado", "code": "5763 C", "hex": "#737B4C", "role": "earth_tone"},
            {"name": "Harvest Gold", "code": "7555 C", "hex": "#D29F13", "role": "appliance_warm"},
            {"name": "Turquoise", "code": "320 C", "hex": "#009CA6", "role": "space_age_accent"}
        ],
        "game_show_match": "1960s_game_show"
    },
    "1970s": {
        "mood": "earth_tone_warmth",
        "palette": [
            {"name": "Burnt Orange", "code": "1525 C", "hex": "#B86125", "role": "dominant_warm"},
            {"name": "Avocado", "code": "5757 C", "hex": "#6B7752", "role": "organic_accent"},
            {"name": "Harvest Gold", "code": "7555 C", "hex": "#D29F13", "role": "appliance_standard"},
            {"name": "Brown", "code": "4625 C", "hex": "#4F2C1D", "role": "earth_ground"}
        ],
        "game_show_match": "1970s_game_show"
    },
    "1980s": {
        "mood": "neon_excess",
        "palette": [
            {"name": "Hot Pink", "code": "Rhodamine Red C", "hex": "#E10098", "role": "attention"},
            {"name": "Electric Blue", "code": "2995 C", "hex": "#00A3E0", "role": "new_wave"},
            {"name": "Teal", "code": "321 C", "hex": "#008E97", "role": "miami_vice"},
            {"name": "Black", "code": "Black C", "hex": "#2D2926", "role": "dramatic_ground"}
        ],
        "game_show_match": "1980s_game_show"
    },
    "1990s": {
        "mood": "minimalist_earth",
        "palette": [
            {"name": "Taupe", "code": "7530 C", "hex": "#B3A394", "role": "neutral_sophistication"},
            {"name": "Forest", "code": "3435 C", "hex": "#154734", "role": "nature_return"},
            {"name": "Burgundy", "code": "188 C", "hex": "#7C2529", "role": "mature_accent"},
            {"name": "Slate", "code": "431 C", "hex": "#5B6770", "role": "tech_neutral"}
        ],
        "game_show_match": "1990s_game_show"
    },
    "2000s": {
        "mood": "digital_clean",
        "palette": [
            {"name": "iPod White", "code": "7527 C", "hex": "#D6D2C4", "role": "tech_clean"},
            {"name": "Chrome Silver", "code": "877 C", "hex": "#8A8D8F", "role": "digital_accent"},
            {"name": "Aqua", "code": "3252 C", "hex": "#64CCC9", "role": "web_2_0"},
            {"name": "Lime", "code": "375 C", "hex": "#97D700", "role": "energy_accent"}
        ],
        "game_show_match": "2000s_game_show"
    },
    "2010s": {
        "mood": "instagram_warmth",
        "palette": [
            {"name": "Millennial Pink", "code": "2036 C", "hex": "#E8B4B8", "role": "cultural_marker"},
            {"name": "Rose Gold", "code": "7605 C", "hex": "#B76E79", "role": "luxury_approachable"},
            {"name": "Sage", "code": "5645 C", "hex": "#8A9A82", "role": "wellness_calm"},
            {"name": "Terracotta", "code": "7522 C", "hex": "#B55A30", "role": "artisanal_warmth"}
        ],
        "game_show_match": "2010s_game_show"
    }
}

# ==============================================================================
# HERALDIC TINCTURE MAPPINGS
# ==============================================================================

HERALDIC_TO_PANTONE: Dict[str, Dict[str, Any]] = {
    "or": {
        "primary": {"code": "871 C", "name": "Metallic Gold", "hex": "#85714D"},
        "alternate": {"code": "7555 C", "name": "Harvest Gold", "hex": "#D29F13"},
        "intentionality": "Heraldic gold requires metallic treatment for nobility; alternate for non-metallic production",
        "production_notes": ["Primary requires metallic ink or foil stamping"]
    },
    "argent": {
        "primary": {"code": "877 C", "name": "Metallic Silver", "hex": "#8A8D8F"},
        "alternate": {"code": "Cool Gray 1 C", "name": "Near White", "hex": "#D9D9D6"},
        "intentionality": "Heraldic silver implies reflective purity; alternate for standard printing",
        "production_notes": ["Primary requires metallic ink or foil stamping"]
    },
    "azure": {
        "primary": {"code": "286 C", "name": "Classic Blue", "hex": "#0032A0"},
        "deep_variant": {"code": "289 C", "name": "Navy", "hex": "#0C2340"},
        "bright_variant": {"code": "Process Blue C", "name": "Process Blue", "hex": "#0085CA"},
        "intentionality": "Azure spans sky to sea; context determines depth selection"
    },
    "gules": {
        "primary": {"code": "186 C", "name": "True Red", "hex": "#C8102E"},
        "warm_variant": {"code": "Warm Red C", "name": "Warm Red", "hex": "#F9423A"},
        "deep_variant": {"code": "187 C", "name": "Deep Red", "hex": "#A6192E"},
        "intentionality": "Gules carries martial energy; saturation conveys intensity"
    },
    "vert": {
        "primary": {"code": "348 C", "name": "Clear Green", "hex": "#00843D"},
        "forest_variant": {"code": "350 C", "name": "Forest Green", "hex": "#2C5234"},
        "bright_variant": {"code": "361 C", "name": "Bright Green", "hex": "#43B02A"},
        "intentionality": "Vert suggests growth; darkness implies age and tradition"
    },
    "purpure": {
        "primary": {"code": "2685 C", "name": "Royal Purple", "hex": "#56147D"},
        "red_variant": {"code": "2415 C", "name": "Red Purple", "hex": "#8E258D"},
        "blue_variant": {"code": "2735 C", "name": "Blue Purple", "hex": "#2E1A6E"},
        "intentionality": "Purpure is rare in heraldry; maintain regal saturation"
    },
    "sable": {
        "primary": {"code": "Black C", "name": "Black", "hex": "#2D2926"},
        "warm_variant": {"code": "Black 7 C", "name": "Warm Black", "hex": "#3D3935"},
        "intentionality": "Sable is absence, not merely dark gray; rich black required"
    },
    "tenne": {
        "primary": {"code": "1525 C", "name": "Burnt Orange", "hex": "#B86125"},
        "intentionality": "Tenne is a stain, not standard tincture; use sparingly for special purposes"
    },
    "sanguine": {
        "primary": {"code": "188 C", "name": "Burgundy", "hex": "#7C2529"},
        "intentionality": "Sanguine is a stain; darker than gules with blood association"
    }
}

# ==============================================================================
# COCKTAIL ATMOSPHERE MAPPINGS
# ==============================================================================

COCKTAIL_TO_PANTONE: Dict[str, Dict[str, Any]] = {
    "warm_amber": {
        "primary": {"code": "7510 C", "name": "Amber", "hex": "#C6893F"},
        "lighting_association": "tungsten_40w",
        "intentionality": "Whiskey bar glow, intimate warmth"
    },
    "cool_clarity": {
        "primary": {"code": "7457 C", "name": "Ice Blue", "hex": "#B0D0E8"},
        "lighting_association": "daylight_north",
        "intentionality": "Gin clarity, crisp precision"
    },
    "tropical_vibrance": {
        "primary": {"code": "1585 C", "name": "Tropical Orange", "hex": "#FF8200"},
        "lighting_association": "sunset_golden_hour",
        "intentionality": "Tiki energy, vacation escape"
    },
    "speakeasy_shadow": {
        "primary": {"code": "7540 C", "name": "Shadow Gray", "hex": "#4B4F54"},
        "lighting_association": "dim_incandescent",
        "intentionality": "Prohibition romance, hidden depth"
    },
    "aperitivo_glow": {
        "primary": {"code": "171 C", "name": "Aperol Orange", "hex": "#FF6A39"},
        "lighting_association": "mediterranean_evening",
        "intentionality": "Italian sunset, social warmth",
        "era_match": 2019  # Living Coral
    },
    "digestif_warmth": {
        "primary": {"code": "18-1438", "name": "Marsala", "hex": "#955251"},
        "lighting_association": "fireplace_glow",
        "intentionality": "After-dinner contemplation, aged spirits",
        "era_match": 2015
    },
    "champagne_brightness": {
        "primary": {"code": "14-0848", "name": "Mimosa", "hex": "#F0C05A"},
        "lighting_association": "morning_celebration",
        "intentionality": "Celebratory effervescence, brunch culture",
        "era_match": 2009
    }
}

# ==============================================================================
# WINE HUE MAPPINGS
# ==============================================================================

WINE_TO_PANTONE: Dict[str, Dict[str, Any]] = {
    "ruby": {
        "primary": {"code": "201 C", "name": "Ruby", "hex": "#9D2235"},
        "age_indication": "young",
        "grape_associations": ["pinot_noir_young", "grenache"]
    },
    "garnet": {
        "primary": {"code": "188 C", "name": "Garnet", "hex": "#7C2529"},
        "age_indication": "developing",
        "grape_associations": ["nebbiolo", "sangiovese_aged"]
    },
    "brick": {
        "primary": {"code": "7622 C", "name": "Brick", "hex": "#8B3F3F"},
        "age_indication": "mature",
        "grape_associations": ["aged_burgundy", "barolo"]
    },
    "tawny": {
        "primary": {"code": "7517 C", "name": "Tawny", "hex": "#9E6B4A"},
        "age_indication": "oxidized",
        "grape_associations": ["tawny_port", "aged_rioja"]
    },
    "straw": {
        "primary": {"code": "7499 C", "name": "Straw", "hex": "#E8D8B8"},
        "age_indication": "young_white",
        "grape_associations": ["sauvignon_blanc", "pinot_grigio"]
    },
    "gold": {
        "primary": {"code": "7555 C", "name": "Wine Gold", "hex": "#D29F13"},
        "age_indication": "rich_or_aged_white",
        "grape_associations": ["oaked_chardonnay", "sauternes"]
    },
    "amber": {
        "primary": {"code": "7510 C", "name": "Wine Amber", "hex": "#C6893F"},
        "age_indication": "oxidized_white",
        "grape_associations": ["orange_wine", "vin_jaune"]
    }
}

# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB to hex color."""
    return f"#{r:02X}{g:02X}{b:02X}"


def color_distance(hex1: str, hex2: str) -> float:
    """Calculate simple Euclidean distance between two hex colors."""
    r1, g1, b1 = hex_to_rgb(hex1)
    r2, g2, b2 = hex_to_rgb(hex2)
    return math.sqrt((r2-r1)**2 + (g2-g1)**2 + (b2-b1)**2)


def find_nearest_pantone(hex_color: str) -> Dict[str, Any]:
    """Find nearest Pantone reference to a hex color."""
    min_distance = float('inf')
    nearest = None
    nearest_key = None
    
    # Search classic references
    for key, ref in CLASSIC_REFERENCES.items():
        dist = color_distance(hex_color, ref["hex"])
        if dist < min_distance:
            min_distance = dist
            nearest = ref
            nearest_key = key
    
    # Search COTY
    for year, coty in COLOR_OF_THE_YEAR.items():
        if isinstance(year, int) or year.endswith("_secondary"):
            dist = color_distance(hex_color, coty["hex"])
            if dist < min_distance:
                min_distance = dist
                nearest = coty
                nearest_key = f"COTY_{year}"
    
    return {
        "key": nearest_key,
        "reference": nearest,
        "distance": min_distance,
        "match_quality": "exact" if min_distance < 10 else "close" if min_distance < 50 else "approximate"
    }


def get_production_suffix(context: str) -> str:
    """Get the appropriate Pantone suffix for production context."""
    if context == "print_coated":
        return " C"
    elif context == "print_uncoated":
        return " U"
    return " C"  # Default to coated


# ==============================================================================
# LAYER 1 TOOLS - PURE TAXONOMY
# ==============================================================================

@mcp.tool()
def list_colors_of_the_year(
    start_year: int = 2000,
    end_year: int = 2024
) -> Dict[str, Any]:
    """
    List all Pantone Colors of the Year within a date range.
    
    Layer 1: Pure taxonomy retrieval (zero LLM cost).
    
    Args:
        start_year: Beginning of range (default 2000)
        end_year: End of range (default 2024)
    
    Returns:
        Dictionary of COTY entries with codes, names, moods, and domain pairings
    """
    result = {}
    
    for year, data in COLOR_OF_THE_YEAR.items():
        # Handle both integer years and string keys like "2016_secondary"
        if isinstance(year, int):
            if start_year <= year <= end_year:
                result[str(year)] = data
        elif isinstance(year, str) and "_secondary" in year:
            base_year = int(year.split("_")[0])
            if start_year <= base_year <= end_year:
                result[year] = data
    
    return {
        "colors_of_the_year": result,
        "count": len(result),
        "range": f"{start_year}-{end_year}"
    }


@mcp.tool()
def get_color_of_the_year(year: int) -> Dict[str, Any]:
    """
    Get detailed information about a specific year's Color of the Year.
    
    Layer 1: Pure taxonomy retrieval (zero LLM cost).
    
    Args:
        year: The year to look up (2000-2024)
    
    Returns:
        Complete COTY entry including co-colors if applicable
    """
    if year not in COLOR_OF_THE_YEAR:
        return {"error": f"No Color of the Year data for {year}"}
    
    primary = COLOR_OF_THE_YEAR[year]
    result = {
        "year": year,
        "primary": primary
    }
    
    # Check for co-color (2016, 2021)
    secondary_key = f"{year}_secondary"
    if secondary_key in COLOR_OF_THE_YEAR:
        result["secondary"] = COLOR_OF_THE_YEAR[secondary_key]
        result["is_dual_color_year"] = True
    else:
        result["is_dual_color_year"] = False
    
    return result


@mcp.tool()
def list_classic_references(category: Optional[str] = None) -> Dict[str, Any]:
    """
    List classic Pantone reference colors, optionally filtered by category.
    
    Layer 1: Pure taxonomy retrieval (zero LLM cost).
    
    Args:
        category: Optional filter - "process", "metallic", "neutral", 
                  "heritage", "standard", or None for all
    
    Returns:
        Dictionary of classic Pantone references
    """
    if category:
        filtered = {k: v for k, v in CLASSIC_REFERENCES.items() 
                   if v.get("category") == category}
        return {
            "category": category,
            "references": filtered,
            "count": len(filtered)
        }
    
    # Group by category
    by_category = {}
    for key, ref in CLASSIC_REFERENCES.items():
        cat = ref.get("category", "other")
        if cat not in by_category:
            by_category[cat] = {}
        by_category[cat][key] = ref
    
    return {
        "by_category": by_category,
        "total_count": len(CLASSIC_REFERENCES),
        "categories": list(by_category.keys())
    }


@mcp.tool()
def get_era_palette(era: str, include_coty: bool = True) -> Dict[str, Any]:
    """
    Get era-appropriate Pantone palette for temporal matching.
    
    Layer 1: Pure taxonomy retrieval (zero LLM cost).
    
    Args:
        era: Decade string like "1970s", "1980s", "2010s"
        include_coty: Whether to include Colors of the Year from that era
    
    Returns:
        Era palette with mood, colors, and optional COTY accents
    """
    if era not in ERA_PALETTES:
        return {
            "error": f"Unknown era: {era}",
            "available_eras": list(ERA_PALETTES.keys())
        }
    
    result = {
        "era": era,
        "palette_data": ERA_PALETTES[era]
    }
    
    if include_coty:
        # Extract decade range
        decade_start = int(era.replace("s", ""))
        decade_end = decade_start + 9
        
        coty_accents = []
        for year, data in COLOR_OF_THE_YEAR.items():
            if isinstance(year, int) and decade_start <= year <= decade_end:
                coty_accents.append({
                    "year": year,
                    "name": data["name"],
                    "code": data["code"],
                    "hex": data["hex"],
                    "mood": data.get("era_mood")
                })
        
        result["coty_accents"] = coty_accents
    
    return result


@mcp.tool()
def list_heraldic_mappings() -> Dict[str, Any]:
    """
    List all heraldic tincture to Pantone mappings.
    
    Layer 1: Pure taxonomy retrieval (zero LLM cost).
    
    Returns:
        Complete heraldic tincture mapping table with intentionality
    """
    return {
        "mappings": HERALDIC_TO_PANTONE,
        "tincture_count": len(HERALDIC_TO_PANTONE),
        "metals": ["or", "argent"],
        "colors": ["azure", "gules", "vert", "purpure", "sable"],
        "stains": ["tenne", "sanguine"]
    }


@mcp.tool()
def list_cocktail_mappings() -> Dict[str, Any]:
    """
    List all cocktail atmosphere to Pantone mappings.
    
    Layer 1: Pure taxonomy retrieval (zero LLM cost).
    
    Returns:
        Complete cocktail atmosphere mapping table
    """
    return {
        "mappings": COCKTAIL_TO_PANTONE,
        "atmosphere_count": len(COCKTAIL_TO_PANTONE),
        "atmospheres": list(COCKTAIL_TO_PANTONE.keys())
    }


@mcp.tool()
def list_wine_mappings() -> Dict[str, Any]:
    """
    List all wine hue to Pantone mappings.
    
    Layer 1: Pure taxonomy retrieval (zero LLM cost).
    
    Returns:
        Complete wine color mapping table with age indications
    """
    return {
        "mappings": WINE_TO_PANTONE,
        "hue_count": len(WINE_TO_PANTONE),
        "red_wine_hues": ["ruby", "garnet", "brick", "tawny"],
        "white_wine_hues": ["straw", "gold", "amber"]
    }


# ==============================================================================
# LAYER 2 TOOLS - DETERMINISTIC BRIDGE MORPHISMS
# ==============================================================================

def _specify_pantone_from_heraldic_impl(
    tincture: str,
    variant: str = "primary",
    production_context: str = "print_coated"
) -> Dict[str, Any]:
    """Internal implementation of heraldic tincture to Pantone conversion."""
    tincture_lower = tincture.lower()
    
    if tincture_lower not in HERALDIC_TO_PANTONE:
        return {
            "error": f"Unknown tincture: {tincture}",
            "available_tinctures": list(HERALDIC_TO_PANTONE.keys())
        }
    
    mapping = HERALDIC_TO_PANTONE[tincture_lower]
    
    # Get requested variant or fall back to primary
    if variant in mapping:
        selected = mapping[variant]
    elif variant == "alternate" and "alternate" in mapping:
        selected = mapping["alternate"]
    else:
        selected = mapping["primary"]
    
    # Adjust code for production context
    code = selected["code"]
    if not code.endswith(" C") and not code.endswith(" U"):
        suffix = get_production_suffix(production_context)
        code = code + suffix
    elif production_context == "print_uncoated" and code.endswith(" C"):
        code = code.replace(" C", " U")
    
    result = {
        "source_tincture": tincture_lower,
        "variant_selected": variant,
        "pantone": {
            "code": code,
            "name": selected["name"],
            "hex": selected["hex"]
        },
        "production_context": production_context,
        "intentionality": mapping.get("intentionality", ""),
        "production_notes": mapping.get("production_notes", [])
    }
    
    # Add available variants for reference
    result["available_variants"] = [k for k in mapping.keys() 
                                    if k not in ["intentionality", "production_notes"]]
    
    return result


@mcp.tool()
def specify_pantone_from_heraldic(
    tincture: str,
    variant: str = "primary",
    production_context: str = "print_coated"
) -> Dict[str, Any]:
    """
    Convert heraldic tincture to Pantone specification.
    
    Layer 2: Deterministic bridge morphism (zero LLM cost).
    
    Args:
        tincture: Heraldic tincture (or, argent, azure, gules, vert, purpure, sable, tenne, sanguine)
        variant: "primary", "deep_variant", "bright_variant", "warm_variant", "alternate"
        production_context: "print_coated" or "print_uncoated"
    
    Returns:
        Pantone specification with production notes and intentionality
    """
    return _specify_pantone_from_heraldic_impl(tincture, variant, production_context)


def _specify_pantone_from_cocktail_impl(
    atmosphere: str,
    production_context: str = "print_coated"
) -> Dict[str, Any]:
    """Internal implementation of cocktail atmosphere to Pantone conversion."""
    atmosphere_lower = atmosphere.lower()
    
    if atmosphere_lower not in COCKTAIL_TO_PANTONE:
        return {
            "error": f"Unknown atmosphere: {atmosphere}",
            "available_atmospheres": list(COCKTAIL_TO_PANTONE.keys())
        }
    
    mapping = COCKTAIL_TO_PANTONE[atmosphere_lower]
    selected = mapping["primary"]
    
    # Adjust code for production context
    code = selected["code"]
    if not code.endswith(" C") and not code.endswith(" U"):
        suffix = get_production_suffix(production_context)
        code = code + suffix
    
    result = {
        "source_atmosphere": atmosphere_lower,
        "pantone": {
            "code": code,
            "name": selected["name"],
            "hex": selected["hex"]
        },
        "lighting_association": mapping.get("lighting_association"),
        "intentionality": mapping.get("intentionality"),
        "production_context": production_context
    }
    
    # Include era match if present (COTY connection)
    if "era_match" in mapping:
        era_year = mapping["era_match"]
        if era_year in COLOR_OF_THE_YEAR:
            coty = COLOR_OF_THE_YEAR[era_year]
            result["coty_connection"] = {
                "year": era_year,
                "name": coty["name"],
                "mood": coty.get("era_mood")
            }
    
    return result


@mcp.tool()
def specify_pantone_from_cocktail(
    atmosphere: str,
    production_context: str = "print_coated"
) -> Dict[str, Any]:
    """
    Convert cocktail atmosphere to Pantone specification.
    
    Layer 2: Deterministic bridge morphism (zero LLM cost).
    
    Args:
        atmosphere: Cocktail atmosphere (warm_amber, cool_clarity, tropical_vibrance, etc.)
        production_context: "print_coated" or "print_uncoated"
    
    Returns:
        Pantone specification with lighting association and intentionality
    """
    return _specify_pantone_from_cocktail_impl(atmosphere, production_context)


def _specify_pantone_from_wine_impl(
    hue: str,
    production_context: str = "print_coated"
) -> Dict[str, Any]:
    """Internal implementation of wine hue to Pantone conversion."""
    hue_lower = hue.lower()
    
    if hue_lower not in WINE_TO_PANTONE:
        return {
            "error": f"Unknown wine hue: {hue}",
            "available_hues": list(WINE_TO_PANTONE.keys())
        }
    
    mapping = WINE_TO_PANTONE[hue_lower]
    selected = mapping["primary"]
    
    # Adjust code for production context
    code = selected["code"]
    if not code.endswith(" C") and not code.endswith(" U"):
        suffix = get_production_suffix(production_context)
        code = code + suffix
    
    return {
        "source_hue": hue_lower,
        "pantone": {
            "code": code,
            "name": selected["name"],
            "hex": selected["hex"]
        },
        "age_indication": mapping.get("age_indication"),
        "grape_associations": mapping.get("grape_associations", []),
        "production_context": production_context
    }


@mcp.tool()
def specify_pantone_from_wine(
    hue: str,
    production_context: str = "print_coated"
) -> Dict[str, Any]:
    """
    Convert wine color descriptor to Pantone specification.
    
    Layer 2: Deterministic bridge morphism (zero LLM cost).
    
    Args:
        hue: Wine hue (ruby, garnet, brick, tawny, straw, gold, amber)
        production_context: "print_coated" or "print_uncoated"
    
    Returns:
        Pantone specification with age indication and grape associations
    """
    return _specify_pantone_from_wine_impl(hue, production_context)


def _specify_pantone_from_hex_impl(
    hex_color: str,
    production_context: str = "print_coated",
    prefer_coty: bool = False
) -> Dict[str, Any]:
    """Internal implementation of specify_pantone_from_hex."""
    # Normalize hex input
    hex_color = hex_color.strip()
    if not hex_color.startswith("#"):
        hex_color = "#" + hex_color
    
    nearest = find_nearest_pantone(hex_color)
    
    if nearest["reference"] is None:
        return {"error": "Could not find matching Pantone reference"}
    
    ref = nearest["reference"]
    
    result = {
        "input_hex": hex_color,
        "pantone": {
            "code": ref.get("code", "Unknown"),
            "name": ref.get("name", "Unknown"),
            "hex": ref.get("hex", "Unknown")
        },
        "match_key": nearest["key"],
        "match_quality": nearest["match_quality"],
        "color_distance": round(nearest["distance"], 2),
        "production_context": production_context
    }
    
    # Add COTY info if it's a Color of the Year match
    if nearest["key"] and nearest["key"].startswith("COTY_"):
        year_part = nearest["key"].replace("COTY_", "")
        result["is_coty"] = True
        result["coty_year"] = year_part
        if "era_mood" in ref:
            result["era_mood"] = ref["era_mood"]
    
    return result


@mcp.tool()
def specify_pantone_from_hex(
    hex_color: str,
    production_context: str = "print_coated",
    prefer_coty: bool = False
) -> Dict[str, Any]:
    """
    Find nearest Pantone match for a hex color.
    
    Layer 2: Deterministic nearest-neighbor matching (zero LLM cost).
    
    Args:
        hex_color: Hex color string (e.g., "#955251" or "955251")
        production_context: "print_coated" or "print_uncoated"
        prefer_coty: Boost Color of the Year matches in selection
    
    Returns:
        Nearest Pantone match with distance metric
    """
    return _specify_pantone_from_hex_impl(hex_color, production_context, prefer_coty)


@mcp.tool()
def match_coty_by_mood(
    mood: str,
    year_range: Optional[Tuple[int, int]] = None
) -> Dict[str, Any]:
    """
    Find Colors of the Year matching a mood descriptor.
    
    Layer 2: Deterministic keyword matching (zero LLM cost).
    
    Args:
        mood: Mood keyword (optimism, resilience, luxury, nature, warmth, etc.)
        year_range: Optional (start, end) tuple to limit search
    
    Returns:
        List of matching COTY entries ranked by relevance
    """
    if year_range is None:
        year_range = (2000, 2024)
    
    mood_lower = mood.lower()
    matches = []
    
    for year, data in COLOR_OF_THE_YEAR.items():
        # Filter by year range
        if isinstance(year, int):
            if not (year_range[0] <= year <= year_range[1]):
                continue
        elif isinstance(year, str) and "_secondary" in year:
            base_year = int(year.split("_")[0])
            if not (year_range[0] <= base_year <= year_range[1]):
                continue
        
        # Check mood match in era_mood
        era_mood = data.get("era_mood", "").lower()
        associations = [a.lower() for a in data.get("associations", [])]
        
        score = 0
        matched_in = []
        
        if mood_lower in era_mood:
            score += 2
            matched_in.append("era_mood")
        
        for assoc in associations:
            if mood_lower in assoc:
                score += 1
                matched_in.append(f"association:{assoc}")
        
        if score > 0:
            matches.append({
                "year": year,
                "name": data["name"],
                "code": data["code"],
                "hex": data["hex"],
                "era_mood": data.get("era_mood"),
                "relevance_score": score,
                "matched_in": matched_in
            })
    
    # Sort by relevance score
    matches.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    return {
        "search_mood": mood,
        "year_range": year_range,
        "matches": matches,
        "match_count": len(matches)
    }


def _bridge_domain_color_impl(
    source_domain: str,
    color_parameter: str,
    production_context: str = "print_coated",
    variant: str = "primary"
) -> Dict[str, Any]:
    """Internal implementation of bridge_domain_color."""
    source_lower = source_domain.lower()
    
    if source_lower == "heraldic":
        return _specify_pantone_from_heraldic_impl(color_parameter, variant, production_context)
    elif source_lower == "cocktail":
        return _specify_pantone_from_cocktail_impl(color_parameter, production_context)
    elif source_lower == "wine":
        return _specify_pantone_from_wine_impl(color_parameter, production_context)
    elif source_lower == "hex":
        return _specify_pantone_from_hex_impl(color_parameter, production_context)
    else:
        return {
            "error": f"Unknown source domain: {source_domain}",
            "supported_domains": ["heraldic", "cocktail", "wine", "hex"]
        }


@mcp.tool()
def bridge_domain_color(
    source_domain: str,
    color_parameter: str,
    production_context: str = "print_coated",
    variant: str = "primary"
) -> Dict[str, Any]:
    """
    Universal bridge: route color parameter from any upstream domain to Pantone.
    
    Layer 2: Deterministic routing and morphism application (zero LLM cost).
    
    Args:
        source_domain: Origin domain ("heraldic", "cocktail", "wine", "hex")
        color_parameter: The color value from that domain
        production_context: "print_coated" or "print_uncoated"
        variant: Variant selection for domains with multiple options
    
    Returns:
        Unified Pantone specification result
    """
    return _bridge_domain_color_impl(source_domain, color_parameter, production_context, variant)


@mcp.tool()
def compose_era_matched_palette(
    era: str,
    include_palette: bool = True,
    include_coty: bool = True,
    production_context: str = "print_coated"
) -> Dict[str, Any]:
    """
    Compose a complete era-matched Pantone palette for temporal domains.
    
    Layer 2: Deterministic composition (zero LLM cost).
    Designed for composition with game-show-aesthetics and other era-aware domains.
    
    Args:
        era: Decade string ("1950s", "1960s", "1970s", "1980s", "1990s", "2000s", "2010s")
        include_palette: Include the era's standard palette
        include_coty: Include Colors of the Year from that decade
        production_context: "print_coated" or "print_uncoated"
    
    Returns:
        Complete era palette ready for production specification
    """
    if era not in ERA_PALETTES:
        return {
            "error": f"Unknown era: {era}",
            "available_eras": list(ERA_PALETTES.keys())
        }
    
    era_data = ERA_PALETTES[era]
    suffix = get_production_suffix(production_context)
    
    result = {
        "era": era,
        "mood": era_data["mood"],
        "game_show_match": era_data.get("game_show_match"),
        "production_context": production_context,
        "palette": [],
        "coty_accents": []
    }
    
    # Process era palette
    if include_palette:
        for color in era_data["palette"]:
            code = color["code"]
            if not code.endswith(" C") and not code.endswith(" U"):
                code = code + suffix
            result["palette"].append({
                "name": color["name"],
                "code": code,
                "hex": color["hex"],
                "role": color["role"]
            })
    
    # Get COTY accents from era
    if include_coty:
        decade_start = int(era.replace("s", ""))
        decade_end = decade_start + 9
        
        for year, data in COLOR_OF_THE_YEAR.items():
            if isinstance(year, int) and decade_start <= year <= decade_end:
                code = data["code"]
                # COTY codes don't have suffix, they're Fashion/Home format
                result["coty_accents"].append({
                    "year": year,
                    "name": data["name"],
                    "code": code,
                    "hex": data["hex"],
                    "mood": data.get("era_mood"),
                    "note": "COTY codes are Pantone Fashion format; verify PMS equivalent for print"
                })
    
    return result


# ==============================================================================
# LAYER 3 TOOLS - SYNTHESIS SUPPORT
# ==============================================================================

@mcp.tool()
def prepare_synthesis_context(
    source_domain: str,
    source_parameters: Dict[str, Any],
    production_context: str = "print_coated",
    include_intentionality: bool = True
) -> Dict[str, Any]:
    """
    Prepare complete context for Claude synthesis of Pantone-specified output.
    
    Layer 3 Interface: Assembles deterministic parameters for creative synthesis.
    
    Args:
        source_domain: Origin domain name (heraldic, cocktail, wine, game_show, etc.)
        source_parameters: Color-related parameters from upstream domain
        production_context: "print_coated" or "print_uncoated"
        include_intentionality: Include reasoning for Pantone selections
    
    Returns:
        Complete synthesis context including specifications and intentionality
    """
    result = {
        "source_domain": source_domain,
        "source_parameters": source_parameters,
        "production_context": production_context,
        "pantone_specifications": {},
        "intentionality_notes": [] if include_intentionality else None,
        "production_warnings": []
    }
    
    # Process each color parameter from source
    for param_name, param_value in source_parameters.items():
        if param_value is None:
            continue
            
        # Try to bridge the parameter
        spec = None
        
        # Check if it's a known domain-specific term
        # Use internal implementations to avoid FunctionTool wrapper issues
        if source_domain.lower() == "heraldic" or param_name in ["tincture", "field_tincture", "charge_tincture"]:
            spec = _specify_pantone_from_heraldic_impl(str(param_value), "primary", production_context)
        elif source_domain.lower() == "cocktail" or param_name in ["atmosphere", "mood", "lighting"]:
            if str(param_value).lower() in COCKTAIL_TO_PANTONE:
                spec = _specify_pantone_from_cocktail_impl(str(param_value), production_context)
        elif source_domain.lower() == "wine" or param_name in ["hue", "color", "wine_color"]:
            if str(param_value).lower() in WINE_TO_PANTONE:
                spec = _specify_pantone_from_wine_impl(str(param_value), production_context)
        elif str(param_value).startswith("#") or (len(str(param_value)) == 6 and all(c in "0123456789ABCDEFabcdef" for c in str(param_value))):
            spec = _specify_pantone_from_hex_impl(str(param_value), production_context)
        
        if spec and "error" not in spec:
            result["pantone_specifications"][param_name] = spec.get("pantone", spec)
            
            if include_intentionality and "intentionality" in spec:
                result["intentionality_notes"].append({
                    "parameter": param_name,
                    "reasoning": spec["intentionality"]
                })
            
            if "production_notes" in spec and spec["production_notes"]:
                for note in spec["production_notes"]:
                    if note not in result["production_warnings"]:
                        result["production_warnings"].append(note)
    
    # Add synthesis instructions
    result["synthesis_instructions"] = {
        "task": "Integrate Pantone specifications into final output",
        "preserve": [
            "Production context requirements",
            "Metallic ink notes where applicable",
            "Intentionality reasoning for color choices"
        ],
        "format": "Include Pantone codes alongside hex values in final specification"
    }
    
    return result


# ==============================================================================
# PHASE 2.6: PANTONE MORPHOSPACE & RHYTHMIC PRESETS
# ==============================================================================
#
# 5D normalized morphospace for Pantone color specification aesthetics.
# Parameters capture production-meaningful dimensions of the Pantone system:
#
#   warmth:              0.0 = cool (azure, blue iris) → 1.0 = warm (coral, tigerlily)
#   saturation_intensity: 0.0 = muted (cool grays, taupe) → 1.0 = vivid (neon, process)
#   value_lightness:     0.0 = deep (navy, sable) → 1.0 = light (pastel, near-white)
#   metallicity:         0.0 = matte flat → 1.0 = full metallic (foil, reflective ink)
#   era_contemporaneity: 0.0 = heritage (1950s, traditional) → 1.0 = contemporary (COTY, trend)
#
# Canonical states anchored at culturally meaningful Pantone reference clusters.
# ==============================================================================

PANTONE_PARAMETER_NAMES = [
    "warmth",
    "saturation_intensity",
    "value_lightness",
    "metallicity",
    "era_contemporaneity"
]

PANTONE_CANONICAL_STATES: Dict[str, Dict[str, float]] = {
    # Deep traditional blues/greens — corporate, institutional, heritage printing
    "heritage_authority": {
        "warmth": 0.15,
        "saturation_intensity": 0.70,
        "value_lightness": 0.15,
        "metallicity": 0.0,
        "era_contemporaneity": 0.10
    },
    # Gold, silver, copper — luxury packaging, foil stamping territory
    "metallic_luxury": {
        "warmth": 0.55,
        "saturation_intensity": 0.45,
        "value_lightness": 0.45,
        "metallicity": 1.0,
        "era_contemporaneity": 0.40
    },
    # Rhodamine, electric blue, safety orange — high-energy saturated process
    "neon_vibrance": {
        "warmth": 0.60,
        "saturation_intensity": 1.0,
        "value_lightness": 0.50,
        "metallicity": 0.0,
        "era_contemporaneity": 0.85
    },
    # Millennial pink, sage, soft blue — wellness, Gen-Z, contemporary softness
    "pastel_wellness": {
        "warmth": 0.50,
        "saturation_intensity": 0.25,
        "value_lightness": 0.85,
        "metallicity": 0.0,
        "era_contemporaneity": 0.90
    },
    # Taupe, burnt orange, warm gray — organic, artisanal, natural material
    "earth_organic": {
        "warmth": 0.75,
        "saturation_intensity": 0.35,
        "value_lightness": 0.40,
        "metallicity": 0.05,
        "era_contemporaneity": 0.30
    },
    # Bold process primaries — reflex blue, warm red, yellow, green
    "process_primary": {
        "warmth": 0.45,
        "saturation_intensity": 0.95,
        "value_lightness": 0.45,
        "metallicity": 0.0,
        "era_contemporaneity": 0.50
    },
    # COTY-driven contemporary — Living Coral, Viva Magenta, Peach Fuzz cluster
    "zeitgeist_pop": {
        "warmth": 0.70,
        "saturation_intensity": 0.65,
        "value_lightness": 0.60,
        "metallicity": 0.0,
        "era_contemporaneity": 1.0
    }
}

# ==============================================================================
# PHASE 2.7: VISUAL VOCABULARY FOR PROMPT GENERATION
# ==============================================================================
#
# Each visual type carries image-generation-ready keywords.
# Nearest-neighbor matching in 5D space maps arbitrary parameter states
# to weighted keyword blends for ComfyUI / Stable Diffusion / DALL-E prompts.
# ==============================================================================

PANTONE_VISUAL_TYPES: Dict[str, Dict[str, Any]] = {
    "heritage_authority": {
        "coords": PANTONE_CANONICAL_STATES["heritage_authority"],
        "keywords": [
            "deep navy blue ink on coated stock",
            "traditional corporate letterpress",
            "rich saturated heritage colors",
            "institutional gravitas and depth",
            "Pantone spot color precision",
            "formal engraved stationery aesthetic"
        ]
    },
    "metallic_luxury": {
        "coords": PANTONE_CANONICAL_STATES["metallic_luxury"],
        "keywords": [
            "gold foil stamped on black stock",
            "reflective metallic ink sheen",
            "luxury packaging with embossed metallics",
            "warm gold and cool silver interplay",
            "opulent foil-blocked surface finish",
            "premium print production shimmer"
        ]
    },
    "neon_vibrance": {
        "coords": PANTONE_CANONICAL_STATES["neon_vibrance"],
        "keywords": [
            "electric saturated fluorescent hues",
            "high-chroma process color overprint",
            "bold graphic poster intensity",
            "vivid rhodamine and cyan clash",
            "attention-commanding signal color",
            "screen-printed day-glo vibrancy"
        ]
    },
    "pastel_wellness": {
        "coords": PANTONE_CANONICAL_STATES["pastel_wellness"],
        "keywords": [
            "soft muted pastel tonal range",
            "millennial pink and sage green wash",
            "gentle desaturated contemporary palette",
            "wellness-brand color harmony",
            "light airy tint on uncoated paper",
            "calming low-contrast color field"
        ]
    },
    "earth_organic": {
        "coords": PANTONE_CANONICAL_STATES["earth_organic"],
        "keywords": [
            "warm ochre and raw umber earth tones",
            "natural kraft paper color ground",
            "artisanal warm neutral palette",
            "terracotta and burnt sienna warmth",
            "organic matte finish texture",
            "handcrafted earthy material surface"
        ]
    },
    "process_primary": {
        "coords": PANTONE_CANONICAL_STATES["process_primary"],
        "keywords": [
            "bold primary color block composition",
            "clean sharp spot-color separation",
            "Bauhaus primary palette clarity",
            "saturated red yellow blue triad",
            "graphic design flat color precision",
            "high-fidelity color reproduction"
        ]
    },
    "zeitgeist_pop": {
        "coords": PANTONE_CANONICAL_STATES["zeitgeist_pop"],
        "keywords": [
            "Color of the Year trend palette",
            "culturally resonant warm contemporary",
            "Instagram-era color sensibility",
            "living coral to peach fuzz warmth",
            "editorial trend-driven color story",
            "zeitgeist-capturing modern palette"
        ]
    }
}

# ==============================================================================
# PHASE 2.6: RHYTHMIC PRESET DEFINITIONS
# ==============================================================================
#
# Period strategy for cross-domain resonance:
#   Period 14: Fills gap 12–15 (novel territory, LCM(14,12)=84)
#   Period 18: Overlaps nuclear + catastrophe + diatom (3-domain synchronization)
#   Period 22: Overlaps catastrophe + heraldic (2-domain synchronization)
#   Period 28: Reinforces the discovered composite beat attractor
#   Period 35: Fills gap above 30 (novel, LCM(35,30)=210, LCM(35,14)=70)
#   Period 40: Novel high-period attractor, Period 40 dominant in 16-domain catalog
# ==============================================================================

PANTONE_RHYTHMIC_PRESETS: Dict[str, Dict[str, Any]] = {
    "heritage_to_modern": {
        "state_a": "heritage_authority",
        "state_b": "zeitgeist_pop",
        "pattern": "sinusoidal",
        "num_cycles": 3,
        "steps_per_cycle": 14,
        "description": "Traditional formality dissolving into contemporary trend — "
                       "the tension between Pantone's institutional role and its "
                       "COTY cultural influence"
    },
    "warm_cool_tide": {
        "state_a": "earth_organic",
        "state_b": "pastel_wellness",
        "pattern": "sinusoidal",
        "num_cycles": 4,
        "steps_per_cycle": 18,
        "description": "Warm earth tones ebbing into cool pastels — "
                       "the seasonal rhythm of trend forecasting"
    },
    "saturation_breath": {
        "state_a": "pastel_wellness",
        "state_b": "neon_vibrance",
        "pattern": "triangular",
        "num_cycles": 3,
        "steps_per_cycle": 22,
        "description": "Soft whisper to vivid shout — intensity cycling "
                       "between wellness restraint and graphic energy"
    },
    "metallic_pulse": {
        "state_a": "process_primary",
        "state_b": "metallic_luxury",
        "pattern": "sinusoidal",
        "num_cycles": 2,
        "steps_per_cycle": 28,
        "description": "Flat matte primaries gaining metallic sheen — "
                       "the production upgrade from offset to foil-embellished"
    },
    "decade_drift": {
        "state_a": "heritage_authority",
        "state_b": "pastel_wellness",
        "pattern": "triangular",
        "num_cycles": 2,
        "steps_per_cycle": 35,
        "description": "Deep institutional heritage lightening into contemporary "
                       "softness — a half-century of Pantone's cultural trajectory"
    },
    "zeitgeist_cycle": {
        "state_a": "earth_organic",
        "state_b": "neon_vibrance",
        "pattern": "sinusoidal",
        "num_cycles": 2,
        "steps_per_cycle": 40,
        "description": "Grounded natural palette alternating with electric energy — "
                       "the macro-trend oscillation in color forecasting"
    }
}


# ==============================================================================
# PHASE 2.6: OSCILLATION & TRAJECTORY GENERATION (LAYER 2 — ZERO LLM COST)
# ==============================================================================

def _generate_pantone_oscillation(
    num_steps: int,
    num_cycles: float,
    pattern: str
) -> np.ndarray:
    """Generate oscillation envelope in [0, 1]."""
    t = np.linspace(0, 2 * np.pi * num_cycles, num_steps, endpoint=False)

    if pattern == "sinusoidal":
        return 0.5 * (1.0 + np.sin(t))
    elif pattern == "triangular":
        t_norm = (t / (2 * np.pi)) % 1.0
        return np.where(t_norm < 0.5, 2.0 * t_norm, 2.0 * (1.0 - t_norm))
    elif pattern == "square":
        t_norm = (t / (2 * np.pi)) % 1.0
        return np.where(t_norm < 0.5, 0.0, 1.0)
    else:
        raise ValueError(f"Unknown oscillation pattern: {pattern}")


def _generate_pantone_preset_trajectory(preset_name: str) -> Dict[str, Any]:
    """
    Generate a complete rhythmic trajectory for a given preset.

    Returns dict with 'steps' (list of parameter-state dicts),
    'period', and metadata.
    """
    if preset_name not in PANTONE_RHYTHMIC_PRESETS:
        return {"error": f"Unknown preset: {preset_name}",
                "available": list(PANTONE_RHYTHMIC_PRESETS.keys())}

    cfg = PANTONE_RHYTHMIC_PRESETS[preset_name]
    state_a = PANTONE_CANONICAL_STATES[cfg["state_a"]]
    state_b = PANTONE_CANONICAL_STATES[cfg["state_b"]]

    total_steps = cfg["num_cycles"] * cfg["steps_per_cycle"]
    alpha = _generate_pantone_oscillation(
        total_steps, cfg["num_cycles"], cfg["pattern"]
    )

    vec_a = np.array([state_a[p] for p in PANTONE_PARAMETER_NAMES])
    vec_b = np.array([state_b[p] for p in PANTONE_PARAMETER_NAMES])

    trajectory = np.outer(1.0 - alpha, vec_a) + np.outer(alpha, vec_b)

    steps = []
    for i in range(total_steps):
        step_dict = {p: round(float(trajectory[i, j]), 4)
                     for j, p in enumerate(PANTONE_PARAMETER_NAMES)}
        step_dict["step"] = i
        step_dict["cycle"] = i // cfg["steps_per_cycle"]
        step_dict["alpha"] = round(float(alpha[i]), 4)
        steps.append(step_dict)

    return {
        "preset": preset_name,
        "description": cfg["description"],
        "state_a": cfg["state_a"],
        "state_b": cfg["state_b"],
        "pattern": cfg["pattern"],
        "period": cfg["steps_per_cycle"],
        "num_cycles": cfg["num_cycles"],
        "total_steps": total_steps,
        "steps": steps
    }


def _interpolate_pantone_trajectory(
    state_a_id: str,
    state_b_id: str,
    num_steps: int = 60
) -> Dict[str, Any]:
    """
    Compute smooth interpolation between two canonical states.
    Uses cosine interpolation for natural easing.
    """
    if state_a_id not in PANTONE_CANONICAL_STATES:
        return {"error": f"Unknown state: {state_a_id}",
                "available": list(PANTONE_CANONICAL_STATES.keys())}
    if state_b_id not in PANTONE_CANONICAL_STATES:
        return {"error": f"Unknown state: {state_b_id}",
                "available": list(PANTONE_CANONICAL_STATES.keys())}

    vec_a = np.array([PANTONE_CANONICAL_STATES[state_a_id][p]
                       for p in PANTONE_PARAMETER_NAMES])
    vec_b = np.array([PANTONE_CANONICAL_STATES[state_b_id][p]
                       for p in PANTONE_PARAMETER_NAMES])

    t = np.linspace(0, 1, num_steps)
    alpha = 0.5 * (1.0 - np.cos(np.pi * t))  # cosine ease

    trajectory = np.outer(1.0 - alpha, vec_a) + np.outer(alpha, vec_b)

    steps = []
    for i in range(num_steps):
        step_dict = {p: round(float(trajectory[i, j]), 4)
                     for j, p in enumerate(PANTONE_PARAMETER_NAMES)}
        step_dict["step"] = i
        step_dict["alpha"] = round(float(alpha[i]), 4)
        steps.append(step_dict)

    distance = float(np.linalg.norm(vec_b - vec_a))

    return {
        "state_a": state_a_id,
        "state_b": state_b_id,
        "num_steps": num_steps,
        "euclidean_distance": round(distance, 4),
        "interpolation": "cosine_ease",
        "steps": steps
    }


# ==============================================================================
# PHASE 2.7: VISUAL VOCABULARY EXTRACTION & PROMPT GENERATION
# ==============================================================================

def _extract_pantone_visual_vocabulary(
    state: Dict[str, float],
    strength: float = 1.0
) -> Dict[str, Any]:
    """
    Find nearest visual type for an arbitrary parameter state via
    Euclidean distance in 5D normalized space.

    Returns nearest type, distance, and weighted keywords.
    """
    state_vec = np.array([state.get(p, 0.5) for p in PANTONE_PARAMETER_NAMES])

    min_dist = float("inf")
    nearest_type = None

    for vtype, vdata in PANTONE_VISUAL_TYPES.items():
        coords_vec = np.array([vdata["coords"][p] for p in PANTONE_PARAMETER_NAMES])
        dist = float(np.linalg.norm(state_vec - coords_vec))
        if dist < min_dist:
            min_dist = dist
            nearest_type = vtype

    keywords = PANTONE_VISUAL_TYPES[nearest_type]["keywords"]
    weight = max(0.0, 1.0 - min_dist) * strength

    return {
        "nearest_type": nearest_type,
        "distance": round(min_dist, 4),
        "weight": round(weight, 4),
        "keywords": keywords if weight > 0.15 else []
    }


def _generate_pantone_attractor_prompt(
    state: Dict[str, float],
    mode: str = "composite",
    strength: float = 1.0
) -> Dict[str, Any]:
    """
    Generate image-generation-ready prompt fragment from a Pantone
    morphospace state.

    Modes:
        composite:  Single blended prompt string
        keywords:   Raw keyword list with weights
    """
    vocab = _extract_pantone_visual_vocabulary(state, strength)

    if mode == "keywords":
        return {
            "domain": "pantone",
            "nearest_type": vocab["nearest_type"],
            "distance": vocab["distance"],
            "weight": vocab["weight"],
            "keywords": vocab["keywords"]
        }

    # Composite mode — join keywords weighted by proximity
    if not vocab["keywords"]:
        prompt_fragment = ""
    else:
        prompt_fragment = ", ".join(vocab["keywords"])

    return {
        "domain": "pantone",
        "mode": "composite",
        "nearest_type": vocab["nearest_type"],
        "distance": vocab["distance"],
        "weight": vocab["weight"],
        "prompt_fragment": prompt_fragment
    }


# ==============================================================================
# PHASE 2.6 TOOLS — LAYER 2 (ZERO LLM COST)
# ==============================================================================

@mcp.tool()
def get_pantone_coordinates(
    state_name: str
) -> Dict[str, Any]:
    """
    Get normalized 5D coordinates for a canonical Pantone aesthetic state.

    Layer 2: Pure lookup (zero LLM cost).

    Args:
        state_name: Canonical state ID (heritage_authority, metallic_luxury,
                    neon_vibrance, pastel_wellness, earth_organic,
                    process_primary, zeitgeist_pop)

    Returns:
        5D coordinates in [0,1] normalized morphospace
    """
    if state_name not in PANTONE_CANONICAL_STATES:
        return {
            "error": f"Unknown state: {state_name}",
            "available_states": list(PANTONE_CANONICAL_STATES.keys())
        }
    return {
        "state": state_name,
        "coordinates": PANTONE_CANONICAL_STATES[state_name],
        "parameter_names": PANTONE_PARAMETER_NAMES,
        "note": "All values normalized to [0.0, 1.0]"
    }


@mcp.tool()
def get_pantone_visual_types() -> Dict[str, Any]:
    """
    List all Pantone visual types with 5D coordinates and image-generation keywords.

    Layer 1: Pure taxonomy (zero LLM cost).

    Returns:
        Complete visual type catalog for prompt generation
    """
    types_out = {}
    for vtype, vdata in PANTONE_VISUAL_TYPES.items():
        types_out[vtype] = {
            "coordinates": vdata["coords"],
            "keywords": vdata["keywords"],
            "keyword_count": len(vdata["keywords"])
        }
    return {
        "visual_types": types_out,
        "total_types": len(types_out),
        "parameter_names": PANTONE_PARAMETER_NAMES
    }


@mcp.tool()
def list_pantone_presets() -> Dict[str, Any]:
    """
    List all Phase 2.6 rhythmic presets with period, pattern, and description.

    Layer 1: Pure taxonomy (zero LLM cost).

    Returns:
        Preset catalog with periods and cross-domain resonance notes
    """
    presets_out = {}
    all_periods = []
    for name, cfg in PANTONE_RHYTHMIC_PRESETS.items():
        presets_out[name] = {
            "state_a": cfg["state_a"],
            "state_b": cfg["state_b"],
            "pattern": cfg["pattern"],
            "period": cfg["steps_per_cycle"],
            "num_cycles": cfg["num_cycles"],
            "total_steps": cfg["num_cycles"] * cfg["steps_per_cycle"],
            "description": cfg["description"]
        }
        all_periods.append(cfg["steps_per_cycle"])

    return {
        "presets": presets_out,
        "total_presets": len(presets_out),
        "periods": sorted(set(all_periods)),
        "period_strategy": {
            "14": "Gap-filler 12–15 (novel territory)",
            "18": "Synchronizes with nuclear + catastrophe + diatom",
            "22": "Synchronizes with catastrophe + heraldic",
            "28": "Reinforces discovered composite beat attractor (60−2×16)",
            "35": "Fills gap above 30 (LCM(35,30)=210, LCM(35,14)=70)",
            "40": "Novel high-period — Period 40 dominant in 16-domain catalog"
        }
    }


@mcp.tool()
def apply_pantone_preset(
    preset_name: str,
    num_cycles: Optional[int] = None
) -> Dict[str, Any]:
    """
    Generate a complete rhythmic oscillation trajectory from a Phase 2.6 preset.

    Layer 2: Deterministic forced-orbit integration (zero LLM cost).
    Trajectory is mathematically guaranteed to be periodic — zero drift.

    Args:
        preset_name: Preset ID from list_pantone_presets()
        num_cycles: Override default cycle count (optional)

    Returns:
        Full trajectory with per-step 5D coordinates, alpha, cycle index
    """
    if preset_name not in PANTONE_RHYTHMIC_PRESETS:
        return {
            "error": f"Unknown preset: {preset_name}",
            "available": list(PANTONE_RHYTHMIC_PRESETS.keys())
        }

    if num_cycles is not None:
        original = PANTONE_RHYTHMIC_PRESETS[preset_name].copy()
        original["num_cycles"] = num_cycles
        # Temporarily patch and generate
        saved = PANTONE_RHYTHMIC_PRESETS[preset_name]
        PANTONE_RHYTHMIC_PRESETS[preset_name] = original
        result = _generate_pantone_preset_trajectory(preset_name)
        PANTONE_RHYTHMIC_PRESETS[preset_name] = saved
        return result

    return _generate_pantone_preset_trajectory(preset_name)


@mcp.tool()
def compute_pantone_trajectory(
    state_a: str,
    state_b: str,
    num_steps: int = 60
) -> Dict[str, Any]:
    """
    Compute smooth cosine-eased interpolation between two Pantone canonical states.

    Layer 2: Deterministic trajectory computation (zero LLM cost).

    Args:
        state_a: Starting canonical state ID
        state_b: Target canonical state ID
        num_steps: Number of interpolation steps (default 60)

    Returns:
        Interpolation trajectory with per-step 5D coordinates
    """
    return _interpolate_pantone_trajectory(state_a, state_b, num_steps)


@mcp.tool()
def generate_pantone_attractor_prompt(
    state: Dict[str, float],
    mode: str = "composite",
    strength: float = 1.0
) -> Dict[str, Any]:
    """
    Generate image-generation-ready prompt fragment from a Pantone morphospace state.

    Layer 2: Deterministic nearest-neighbor vocabulary extraction (zero LLM cost).

    Maps an arbitrary 5D parameter state to the nearest visual type and returns
    weighted keywords suitable for ComfyUI, Stable Diffusion, or DALL-E prompts.

    Args:
        state: Dict of parameter values, e.g. {"warmth": 0.6, "saturation_intensity": 0.8, ...}
               Missing parameters default to 0.5.
        mode:  "composite" (joined prompt string) or "keywords" (raw list)
        strength: Domain strength weight [0.0, 1.0] — controls keyword inclusion threshold

    Returns:
        Prompt fragment with nearest visual type, distance, and keywords
    """
    return _generate_pantone_attractor_prompt(state, mode, strength)


@mcp.tool()
def get_pantone_domain_registry_config() -> Dict[str, Any]:
    """
    Return Tier 4D integration configuration for compositional limit cycle discovery.

    Layer 2: Deterministic export (zero LLM cost).

    Returns domain registration data needed by the emergent attractor system:
    parameter names, canonical state coordinates, preset configurations,
    period list, and predicted emergent attractor interactions.
    """
    preset_configs = {}
    for name, cfg in PANTONE_RHYTHMIC_PRESETS.items():
        preset_configs[name] = {
            "period": cfg["steps_per_cycle"],
            "state_a": cfg["state_a"],
            "state_b": cfg["state_b"],
            "pattern": cfg["pattern"]
        }

    all_periods = sorted(set(
        cfg["steps_per_cycle"] for cfg in PANTONE_RHYTHMIC_PRESETS.values()
    ))

    return {
        "domain_id": "pantone",
        "display_name": "Pantone Specification",
        "mcp_server": "pantone-specification",
        "parameter_names": PANTONE_PARAMETER_NAMES,
        "state_coordinates": PANTONE_CANONICAL_STATES,
        "presets": preset_configs,
        "periods": all_periods,
        "visual_types": {
            vtype: {
                "coords": vdata["coords"],
                "keywords": vdata["keywords"]
            }
            for vtype, vdata in PANTONE_VISUAL_TYPES.items()
        },
        "predicted_emergent_attractors": [
            {
                "mechanism": "gap_filler",
                "predicted_period": 14,
                "gap": "12–15",
                "basin_estimate": 0.03,
                "note": "Novel period filling 12–15 gap; no existing domain uses 14"
            },
            {
                "mechanism": "lcm_sync",
                "predicted_period": 28,
                "interaction": "Reinforces composite beat (60−2×16=28)",
                "basin_estimate": 0.05,
                "note": "Pantone Period 28 + existing Period 28 attractor = mutual reinforcement"
            },
            {
                "mechanism": "lcm_sync",
                "predicted_period": 70,
                "interaction": "LCM(14, 35) = 70",
                "basin_estimate": 0.02,
                "note": "Novel high-period from Pantone's own gap-filler × drift preset"
            },
            {
                "mechanism": "gap_filler",
                "predicted_period": 35,
                "gap": "30–40",
                "basin_estimate": 0.03,
                "note": "Fills the large gap above Period 30 cluster"
            },
            {
                "mechanism": "harmonic",
                "predicted_period": 40,
                "interaction": "2×20, reinforces Period 40 dominance from 16-domain catalog",
                "basin_estimate": 0.04,
                "note": "Directly reinforces the globally dominant Period 40"
            }
        ],
        "phase_2_6_status": "complete",
        "phase_2_7_status": "complete"
    }


# ==============================================================================
# UPDATED SERVER INFO
# ==============================================================================

@mcp.tool()
def get_server_info() -> Dict[str, Any]:
    """
    Get information about the Pantone Specification MCP server.

    Returns:
        Server metadata, capabilities, and architecture overview
    """
    all_periods = sorted(set(
        cfg["steps_per_cycle"] for cfg in PANTONE_RHYTHMIC_PRESETS.values()
    ))

    return {
        "name": "pantone-specification",
        "version": "2.0.0",
        "role": "terminal_functor",
        "layer_type": "bridge",
        "description": (
            "Translates abstract color concepts from upstream domains into "
            "production-ready Pantone Graphics (PMS) specifications. "
            "Phase 2.6 adds rhythmic composition presets; Phase 2.7 adds "
            "attractor visualization prompt generation."
        ),

        "architecture": {
            "layer_1": "Pure taxonomy (COTY database, classic references, era palettes, visual types)",
            "layer_2": "Deterministic bridge morphisms (domain → Pantone) + "
                       "forced-orbit rhythmic composition + attractor prompt generation",
            "layer_3": "Synthesis context preparation for Claude"
        },

        "upstream_domains": [
            "heraldic_blazonry",
            "cocktail_aesthetics",
            "wine_tasting",
            "game_show_aesthetics",
            "japanese_garden_design",
            "any domain with color output"
        ],

        "system_scope": "Pantone Matching System (PMS) - Coated/Uncoated",

        "data_coverage": {
            "colors_of_the_year": f"{len([y for y in COLOR_OF_THE_YEAR.keys() if isinstance(y, int)])} years (2000-2024)",
            "classic_references": f"{len(CLASSIC_REFERENCES)} colors",
            "era_palettes": f"{len(ERA_PALETTES)} decades",
            "heraldic_mappings": f"{len(HERALDIC_TO_PANTONE)} tinctures",
            "cocktail_mappings": f"{len(COCKTAIL_TO_PANTONE)} atmospheres",
            "wine_mappings": f"{len(WINE_TO_PANTONE)} hues",
            "canonical_states": f"{len(PANTONE_CANONICAL_STATES)} states",
            "visual_types": f"{len(PANTONE_VISUAL_TYPES)} types",
            "rhythmic_presets": f"{len(PANTONE_RHYTHMIC_PRESETS)} presets"
        },

        "phase_2_6_enhancements": {
            "rhythmic_presets": True,
            "preset_count": len(PANTONE_RHYTHMIC_PRESETS),
            "periods": all_periods,
            "period_strategy": "Gap-filling (14, 35), synchronization (18, 22), "
                               "composite beat reinforcement (28), catalog dominant (40)",
            "forced_orbit_integration": True,
            "guaranteed_periodicity": True
        },

        "phase_2_7_enhancements": {
            "attractor_visualization": True,
            "visual_type_count": len(PANTONE_VISUAL_TYPES),
            "prompt_modes": ["composite", "keywords"],
            "nearest_neighbor_matching": True,
            "image_generation_targets": ["ComfyUI", "Stable Diffusion", "DALL-E"]
        },

        "morphospace": {
            "dimensions": 5,
            "parameters": PANTONE_PARAMETER_NAMES,
            "parameter_semantics": {
                "warmth": "cool (azure, blue iris) → warm (coral, tigerlily)",
                "saturation_intensity": "muted (cool grays) → vivid (neon, process)",
                "value_lightness": "deep (navy, sable) → light (pastel, near-white)",
                "metallicity": "matte flat → full metallic (foil, reflective ink)",
                "era_contemporaneity": "heritage (1950s) → contemporary (COTY, trend)"
            }
        },

        "intentionality_principles": [
            "Name over number: Pantone names carry cultural weight beyond color values",
            "Era authenticity: Historical accuracy requires period-appropriate references",
            "Production honesty: Acknowledge substrate dependency",
            "Symbolic preservation: Source domain symbolism guides selection over ΔE proximity"
        ],

        "tier_4d_integration": {
            "domain_registry_config": True,
            "predicted_emergent_attractors": 5,
            "cross_domain_periods": {
                "synchronization": [18, 22],
                "gap_fillers": [14, 35],
                "reinforcement": [28, 40]
            }
        },

        "author": "Dal Marsters / Lushy Project"
    }


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    mcp.run()
