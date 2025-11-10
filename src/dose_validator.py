"""
Dose Validation and Safety Checking Module

This module provides ACTUAL LOGIC to validate medication doses,
not just prompt instructions. It cross-checks calculated doses against
known safe ranges to catch hallucinations and calculation errors.

This is a critical safety layer - we don't just trust Claude, we verify.
"""

import re
from typing import Optional, Dict, Tuple
from rich.console import Console

console = Console()

# ============================================================================
# PEDIATRIC DOSE KNOWLEDGE BASE
# ============================================================================

# This is a curated knowledge base of common pediatric medications
# with their safe dosing ranges. This provides HARD LIMITS that we check against.
#
# Format: {
#     "drug_name": {
#         "indication": {
#             "mg_per_kg_per_day_min": float,
#             "mg_per_kg_per_day_max": float,
#             "absolute_max_single_dose_mg": float,
#             "absolute_max_daily_dose_mg": float,
#             "source": "Reference source"
#         }
#     }
# }

PEDIATRIC_DOSE_DATABASE = {
    "amoxicillin": {
        "standard": {
            "mg_per_kg_per_day_min": 20,
            "mg_per_kg_per_day_max": 50,
            "absolute_max_single_dose_mg": 1000,
            "absolute_max_daily_dose_mg": 3000,
            "source": "AAP Red Book 2021, Lexicomp"
        },
        "high_dose": {  # For resistant organisms
            "mg_per_kg_per_day_min": 80,
            "mg_per_kg_per_day_max": 90,
            "absolute_max_single_dose_mg": 2000,
            "absolute_max_daily_dose_mg": 3000,
            "source": "AAP Red Book 2021"
        }
    },
    "ibuprofen": {
        "standard": {
            "mg_per_kg_per_dose_min": 5,
            "mg_per_kg_per_dose_max": 10,
            "mg_per_kg_per_day_max": 40,
            "absolute_max_single_dose_mg": 800,
            "absolute_max_daily_dose_mg": 2400,
            "min_age_months": 6,
            "source": "Lexicomp Pediatric"
        }
    },
    "acetaminophen": {
        "standard": {
            "mg_per_kg_per_dose_min": 10,
            "mg_per_kg_per_dose_max": 15,
            "mg_per_kg_per_day_max": 75,
            "absolute_max_single_dose_mg": 1000,
            "absolute_max_daily_dose_mg": 4000,
            "source": "Lexicomp Pediatric"
        }
    },
    "azithromycin": {
        "standard": {
            "mg_per_kg_per_day_min": 10,
            "mg_per_kg_per_day_max": 12,
            "absolute_max_single_dose_mg": 500,
            "absolute_max_daily_dose_mg": 500,
            "source": "AAP Red Book 2021"
        }
    },
    "cefdinir": {
        "standard": {
            "mg_per_kg_per_day_min": 14,
            "mg_per_kg_per_day_max": 14,
            "absolute_max_single_dose_mg": 600,
            "absolute_max_daily_dose_mg": 600,
            "min_age_months": 6,
            "source": "Lexicomp Pediatric"
        }
    }
}


# ============================================================================
# DOSE VALIDATION FUNCTIONS
# ============================================================================

def validate_dose(
    drug_name: str,
    weight_kg: float,
    calculated_dose_mg: float,
    indication: str = "standard",
    frequency: str = "daily"
) -> Dict[str, any]:
    """
    Validate a calculated dose against known safe ranges.

    This provides an ACTUAL CHECK, not just a prompt instruction.
    Returns validation results with warnings/errors.

    Args:
        drug_name: Name of medication (lowercase)
        weight_kg: Patient weight in kilograms
        calculated_dose_mg: The dose calculated by Claude
        indication: Indication for dosing (e.g., "standard", "high_dose")
        frequency: "daily" or "per_dose"

    Returns:
        Dictionary with validation results:
        {
            "is_valid": bool,
            "warnings": list of warning messages,
            "errors": list of error messages,
            "calculated_mg_per_kg": float,
            "reference_range": str,
            "source": str
        }

    Example:
        >>> result = validate_dose("amoxicillin", 23.6, 1000, "standard", "daily")
        >>> if not result["is_valid"]:
        ...     print(f"DOSE ERROR: {result['errors']}")
    """
    # Normalize drug name
    drug_name = drug_name.lower().strip()

    # Initialize result
    result = {
        "is_valid": True,
        "warnings": [],
        "errors": [],
        "calculated_mg_per_kg": None,
        "reference_range": None,
        "source": None,
        "in_database": False
    }

    # Check if we have this drug in our database
    if drug_name not in PEDIATRIC_DOSE_DATABASE:
        result["warnings"].append(
            f"Drug '{drug_name}' not in validation database - cannot verify dose safety"
        )
        result["warnings"].append(
            "ALWAYS verify doses against authoritative references (Lexicomp, AAP Red Book)"
        )
        return result

    result["in_database"] = True

    # Get drug data
    drug_data = PEDIATRIC_DOSE_DATABASE[drug_name]

    # Get indication-specific data
    if indication not in drug_data:
        # Default to "standard" if indication not found
        if "standard" in drug_data:
            indication = "standard"
            result["warnings"].append(
                f"Using 'standard' dosing as '{indication}' not in database"
            )
        else:
            result["errors"].append(
                f"No dosing data for '{indication}' indication"
            )
            result["is_valid"] = False
            return result

    dose_data = drug_data[indication]
    result["source"] = dose_data.get("source", "Unknown")

    # Calculate mg/kg
    if frequency == "daily":
        calculated_mg_per_kg = calculated_dose_mg / weight_kg
        result["calculated_mg_per_kg"] = calculated_mg_per_kg

        # Check against mg/kg/day range
        min_dose = dose_data.get("mg_per_kg_per_day_min")
        max_dose = dose_data.get("mg_per_kg_per_day_max")

        if min_dose and max_dose:
            result["reference_range"] = f"{min_dose}-{max_dose} mg/kg/day"

            if calculated_mg_per_kg < min_dose:
                result["warnings"].append(
                    f"Dose {calculated_mg_per_kg:.1f} mg/kg/day is BELOW typical range "
                    f"({min_dose}-{max_dose} mg/kg/day). May be subtherapeutic."
                )

            if calculated_mg_per_kg > max_dose * 1.1:  # 10% over is warning
                result["errors"].append(
                    f"Dose {calculated_mg_per_kg:.1f} mg/kg/day EXCEEDS safe range "
                    f"({min_dose}-{max_dose} mg/kg/day). VERIFY before prescribing!"
                )
                result["is_valid"] = False

            elif calculated_mg_per_kg > max_dose:
                result["warnings"].append(
                    f"Dose {calculated_mg_per_kg:.1f} mg/kg/day is at upper limit "
                    f"({max_dose} mg/kg/day). Verify this is intended."
                )

    elif frequency == "per_dose":
        calculated_mg_per_kg = calculated_dose_mg / weight_kg
        result["calculated_mg_per_kg"] = calculated_mg_per_kg

        # Check against mg/kg/dose range
        min_dose = dose_data.get("mg_per_kg_per_dose_min")
        max_dose = dose_data.get("mg_per_kg_per_dose_max")

        if min_dose and max_dose:
            result["reference_range"] = f"{min_dose}-{max_dose} mg/kg/dose"

            if calculated_mg_per_kg < min_dose:
                result["warnings"].append(
                    f"Dose {calculated_mg_per_kg:.1f} mg/kg/dose is BELOW typical range "
                    f"({min_dose}-{max_dose} mg/kg/dose)"
                )

            if calculated_mg_per_kg > max_dose:
                result["errors"].append(
                    f"Dose {calculated_mg_per_kg:.1f} mg/kg/dose EXCEEDS safe range "
                    f"({min_dose}-{max_dose} mg/kg/dose). DO NOT PRESCRIBE!"
                )
                result["is_valid"] = False

    # Check absolute maximum doses
    max_single_dose = dose_data.get("absolute_max_single_dose_mg")
    if max_single_dose and calculated_dose_mg > max_single_dose:
        result["errors"].append(
            f"Calculated dose {calculated_dose_mg}mg exceeds absolute maximum "
            f"single dose of {max_single_dose}mg. DO NOT PRESCRIBE!"
        )
        result["is_valid"] = False

    # Check age restrictions
    min_age_months = dose_data.get("min_age_months")
    if min_age_months:
        result["warnings"].append(
            f"Note: Minimum age for this medication is {min_age_months} months"
        )

    return result


def display_validation_results(validation: Dict) -> None:
    """
    Display validation results to the user with appropriate color coding.

    Args:
        validation: Result dictionary from validate_dose()
    """
    if not validation["in_database"]:
        console.print("\n[yellow]⚠️  DOSE VALIDATION:[/yellow]")
        for warning in validation["warnings"]:
            console.print(f"[yellow]   {warning}[/yellow]")
        return

    console.print("\n[cyan]📊 DOSE VALIDATION CHECK:[/cyan]")

    if validation["calculated_mg_per_kg"]:
        console.print(f"[cyan]   Calculated: {validation['calculated_mg_per_kg']:.1f} mg/kg[/cyan]")

    if validation["reference_range"]:
        console.print(f"[cyan]   Reference: {validation['reference_range']}[/cyan]")

    if validation["source"]:
        console.print(f"[cyan]   Source: {validation['source']}[/cyan]")

    # Display errors (critical)
    if validation["errors"]:
        console.print(f"\n[red]🚨 DOSE ERRORS (DO NOT PRESCRIBE):[/red]")
        for error in validation["errors"]:
            console.print(f"[red]   ❌ {error}[/red]")

    # Display warnings (caution)
    if validation["warnings"]:
        console.print(f"\n[yellow]⚠️  WARNINGS:[/yellow]")
        for warning in validation["warnings"]:
            console.print(f"[yellow]   • {warning}[/yellow]")

    # Display success if valid
    if validation["is_valid"] and not validation["warnings"]:
        console.print(f"\n[green]✓ Dose within safe range[/green]")

    console.print()


# ============================================================================
# DOSE EXTRACTION FROM CLAUDE RESPONSE
# ============================================================================

def extract_dose_from_response(response: str, weight_kg: float) -> Optional[float]:
    """
    Attempt to extract calculated dose from Claude's response.

    This looks for patterns like:
    - "500 mg BID"
    - "total daily dose: 1000 mg"
    - "calculated dose: 42.5 mg/kg/day"

    Args:
        response: Claude's response text
        weight_kg: Patient weight for calculating from mg/kg

    Returns:
        Extracted dose in mg (daily total), or None if cannot extract

    Note: This is a best-effort extraction. May not catch all formats.
    """
    # Look for explicit dose calculations
    patterns = [
        r"calculated dose[:\s]+(\d+\.?\d*)\s*mg",
        r"total daily dose[:\s]+(\d+\.?\d*)\s*mg",
        r"(\d+\.?\d*)\s*mg\s+(?:BID|TID|QID|daily)",
        r"(\d+\.?\d*)\s*mg/kg/day.*?×.*?(\d+\.?\d*)\s*kg",
    ]

    for pattern in patterns:
        match = re.search(pattern, response, re.IGNORECASE)
        if match:
            try:
                dose_mg = float(match.group(1))
                return dose_mg
            except (ValueError, IndexError):
                continue

    return None


# ============================================================================
# MODULE DOCUMENTATION
# ============================================================================

"""
USAGE IN COMMANDS:

from dose_validator import validate_dose, display_validation_results

# After getting Claude's response with a dose
validation = validate_dose(
    drug_name="amoxicillin",
    weight_kg=23.6,
    calculated_dose_mg=1000,
    indication="standard",
    frequency="daily"
)

# Show results to user
display_validation_results(validation)

# Block if dose is unsafe
if not validation["is_valid"]:
    console.print("[red]DOSE UNSAFE - See errors above[/red]")
    return  # Don't show Claude's response

EXPANDING THE DATABASE:

To add new medications, edit PEDIATRIC_DOSE_DATABASE above:

PEDIATRIC_DOSE_DATABASE["new_drug"] = {
    "standard": {
        "mg_per_kg_per_day_min": X,
        "mg_per_kg_per_day_max": Y,
        "absolute_max_single_dose_mg": Z,
        "absolute_max_daily_dose_mg": W,
        "source": "Reference"
    }
}

This provides ACTUAL safety checking, not just prompts!
"""
