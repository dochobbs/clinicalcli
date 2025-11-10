"""
Drug information lookup command - Pediatric focused

This module provides comprehensive medication information with emphasis on:
- Pediatric dosing (weight-based calculations)
- Available formulations suitable for children
- Cost considerations for families
- Parent/caregiver instructions
- Safety information specific to pediatric use
"""

import click
import re
from ..utils import call_claude, display_output, format_phi_warning, console

# ============================================================================
# PEDIATRIC-FOCUSED SYSTEM PROMPT WITH ANTI-HALLUCINATION SAFEGUARDS
# ============================================================================

DRUG_SYSTEM_PROMPT = """You are an expert pediatric clinical pharmacist providing drug information for pediatric providers.

CRITICAL INSTRUCTIONS - ANTI-HALLUCINATION SAFEGUARDS:
1. If you are UNCERTAIN about ANY information, explicitly state "I'm not certain about [specific detail]"
2. For pediatric dosing, ONLY provide ranges that are well-established and evidence-based
3. If a medication is NOT commonly used in pediatrics, state this clearly upfront
4. Do NOT fabricate formulations, strengths, or dosing that you're unsure about
5. When dosing varies significantly by indication, present ONLY the specific indication requested
6. If asked about off-label pediatric use, clearly label it as "OFF-LABEL" and note evidence level
7. For weight-based dosing, always include "mg/kg/day" or "mg/kg/dose" - be precise
8. If maximum doses differ by age/weight, specify this clearly

Your role:
- Provide accurate, clinically relevant PEDIATRIC drug information
- Focus on practical prescribing guidance for children
- Emphasize child-friendly formulations (liquids, chewables, sprinkles)
- Include cost considerations for families
- Highlight pediatric-specific safety information
- Compare options when multiple drugs mentioned

Format your response as:

**DRUG NAME**
Generic: [name] | Brand: [name(s)]
**Pediatric Use:** Common / Less Common / Off-Label / Not Recommended

**AVAILABLE FORMS & STRENGTHS** (Pediatric-Friendly First)
List child-friendly forms first:
- Oral Suspension/Solution: [concentrations in mg/mL]
- Chewable Tablets: [strengths]
- Sprinkle Capsules: [strengths]
- Orally Disintegrating Tablets (ODT): [strengths]
- Standard Tablets/Capsules: [strengths] (for older children/adolescents)
- Injectable: [concentrations] (if applicable)

**PEDIATRIC DOSING**
[For EACH indication, provide:]
- Age/weight ranges
- Dose: X-Y mg/kg/day or mg/kg/dose
- Frequency: once daily, BID, TID, QID
- Maximum single dose: X mg
- Maximum daily dose: X mg/day
- Duration: [typical course length]

Special considerations:
- Renal dosing adjustments
- Hepatic dosing adjustments
- Age-specific dosing notes

**CALCULATED DOSE** (if weight provided)
[This section will be filled in by the tool based on patient weight]

**PARENT/CAREGIVER INSTRUCTIONS**
- How to give (with/without food, best time of day)
- How to measure (use oral syringe, not household spoon)
- What to expect (when to see improvement)
- What to avoid (interactions, activities)
- When to call doctor (warning signs)
- Storage (refrigerate vs room temp, discard after X days)
- Tips for administration (mix with food if needed, etc.)

**COST INFORMATION** (Approximate US pricing)
Generic:
- [Form/strength]: $X-Y (typical course or monthly for chronic meds)
- Available as generic: Yes/No

Brand:
- [Form/strength]: $X-Y (typical course or monthly)

Cost-saving tips for families:
- [e.g., generic alternatives, assistance programs, larger bottles if chronic use]

**PEDIATRIC SAFETY INFORMATION**
Black box warnings (if any): [specific to children]
Age restrictions: [minimum age, specific age group warnings]
Contraindications: [especially relevant to children]
Major interactions: [most important in pediatrics]
Common side effects: [in children specifically]
Serious side effects to watch for: [pediatric-specific concerns]

**CLINICAL PEARLS FOR PEDIATRIC PRESCRIBING**
- [Taste considerations - which formulations taste better]
- [Administration tips for different age groups]
- [Monitoring requirements specific to children]
- [When to use vs alternatives in pediatrics]
- [Growth/development considerations]

If comparing multiple drugs, create a comparison table focusing on:
- Pediatric dosing ease
- Available child-friendly forms
- Taste/palatability (when known)
- Cost for typical pediatric course
- Safety profile in children

IMPORTANT REMINDERS:
- Always state if evidence in children is limited
- Clearly mark off-label uses
- Include age restrictions prominently
- Emphasize liquid formulations when available
- Provide practical administration tips for parents
- Be explicit about uncertainties

Be accurate and evidence-based. If information is not well-established in pediatrics, say so.
Note that costs are approximate and vary by insurance, pharmacy, and location."""


# ============================================================================
# WEIGHT CONVERSION AND DOSE CALCULATION UTILITIES
# ============================================================================

def parse_weight(weight_str: str) -> tuple:
    """
    Parse weight string and convert to kg.

    Accepts formats like:
    - "52#" or "52 #" or "52 lbs" or "52 pounds" (converts to kg)
    - "23.5kg" or "23.5 kg" or "23.5 kilograms" (uses as-is)

    Args:
        weight_str: Weight string from user input

    Returns:
        tuple: (weight_in_kg: float, original_unit: str)

    Raises:
        ValueError: If weight format is invalid or out of reasonable range
    """
    # Remove whitespace and convert to lowercase
    weight_str = weight_str.strip().lower()

    # Patterns for pounds: #, lb, lbs, pound, pounds
    lbs_pattern = r'^(\d+\.?\d*)\s*(?:#|lbs?|pounds?)$'
    # Patterns for kg: kg, kilogram, kilograms
    kg_pattern = r'^(\d+\.?\d*)\s*(?:kg|kilograms?)$'

    lbs_match = re.match(lbs_pattern, weight_str)
    kg_match = re.match(kg_pattern, weight_str)

    if lbs_match:
        # Convert pounds to kg
        weight_lbs = float(lbs_match.group(1))
        weight_kg = weight_lbs / 2.20462
        original_unit = "lbs"

        # Sanity check: reasonable pediatric weight in pounds (4-400 lbs)
        if weight_lbs < 4 or weight_lbs > 400:
            raise ValueError(f"Weight {weight_lbs} lbs seems outside reasonable pediatric range (4-400 lbs)")

    elif kg_match:
        # Use kg as-is
        weight_kg = float(kg_match.group(1))
        original_unit = "kg"

        # Sanity check: reasonable pediatric weight in kg (2-180 kg)
        if weight_kg < 2 or weight_kg > 180:
            raise ValueError(f"Weight {weight_kg} kg seems outside reasonable pediatric range (2-180 kg)")
    else:
        raise ValueError(
            "Invalid weight format. Use formats like: 52#, 52 lbs, 52 pounds, 23.5kg, 23.5 kilograms"
        )

    return weight_kg, original_unit


def format_weight_display(weight_kg: float, original_unit: str, original_value: str) -> str:
    """
    Format weight display showing both kg and lbs for clarity.

    Args:
        weight_kg: Weight in kilograms
        original_unit: Original unit from user input ("lbs" or "kg")
        original_value: Original weight string from user

    Returns:
        Formatted weight string for display
    """
    weight_lbs = weight_kg * 2.20462

    if original_unit == "lbs":
        return f"{weight_lbs:.1f} lbs ({weight_kg:.1f} kg)"
    else:
        return f"{weight_kg:.1f} kg ({weight_lbs:.1f} lbs)"


def calculate_dose_range(weight_kg: float, dose_range_str: str) -> str:
    """
    Calculate dose range based on weight and mg/kg dosing.

    This is a helper that will be included in the prompt to Claude,
    who will do the actual calculation. This function validates inputs.

    Args:
        weight_kg: Patient weight in kg
        dose_range_str: Dose range like "20-40 mg/kg/day" or "10 mg/kg/dose"

    Returns:
        Formatted calculation request for Claude
    """
    return f"""
PATIENT WEIGHT: {weight_kg:.1f} kg

Please calculate the dose range for this patient based on the standard mg/kg dosing above.
Show your calculation step-by-step:
1. Low dose: [low mg/kg] × {weight_kg:.1f} kg = X mg
2. High dose: [high mg/kg] × {weight_kg:.1f} kg = Y mg
3. Practical dosing: Round to achievable doses with available formulations
4. Volume needed: Calculate mL if using liquid formulation
5. Administration frequency: Divide daily dose by frequency

Format the final recommendation clearly for prescribing.
"""


# ============================================================================
# MAIN COMMAND FUNCTION
# ============================================================================

@click.command()
@click.argument('drug_name', nargs=-1, required=False)
@click.option('--weight', '-w', type=str,
              help='Patient weight (e.g., "52#" or "52 lbs" or "23.5kg")')
@click.option('--compare', '-c', is_flag=True,
              help='Compare multiple drugs')
@click.option('--indication', '-i', type=str,
              help='Specific indication/condition (recommended for accurate dosing)')
@click.option('--age', '-a', type=str,
              help='Patient age (e.g., "5yo" or "18mo") for age-specific guidance')
@click.option('--generic-only', '-g', is_flag=True,
              help='Show only generic options')
@click.option('--question', '-q', type=str,
              help='Ask specific question about the drug')
def drug(drug_name, weight, compare, indication, age, generic_only, question):
    """
    Pediatric drug information lookup - dosing, forms, cost

    Provides pediatric-focused medication information with weight-based
    dosing calculations and child-friendly formulation guidance.

    Examples:
        # Basic lookup (pediatric-focused by default)
        clinical drug amoxicillin

        # With weight for dose calculation
        clinical drug amoxicillin --weight "52#"
        clinical drug amoxicillin --weight "23.5kg"

        # With indication for specific dosing
        clinical drug amoxicillin --indication "otitis media" --weight "52 lbs"

        # Compare options
        clinical drug amoxicillin cefdinir azithromycin --compare

        # With age for age-specific guidance
        clinical drug ibuprofen --age "6mo" --weight "8kg"

        # Specific question
        clinical drug ondansetron --question "What's the best formulation for a 4yo?"
    """
    # Display PHI warning
    format_phi_warning()

    # ========================================================================
    # INPUT VALIDATION AND PARSING
    # ========================================================================

    # Get drug name if not provided as argument
    if not drug_name:
        drug_input = click.prompt("Enter medication name(s)", type=str)
        drug_names = [drug_input]
    else:
        drug_names = list(drug_name)

    # Parse and validate weight if provided
    weight_kg = None
    weight_display = None
    if weight:
        try:
            weight_kg, original_unit = parse_weight(weight)
            weight_display = format_weight_display(weight_kg, original_unit, weight)
            console.print(f"[cyan]Patient weight: {weight_display}[/cyan]")
        except ValueError as e:
            console.print(f"[red]Error parsing weight: {e}[/red]")
            console.print("[yellow]Continuing without weight-based calculation...[/yellow]")
            weight_kg = None

    # ========================================================================
    # BUILD QUERY WITH CLINICAL CONTEXT
    # ========================================================================

    # Start with base query
    if len(drug_names) > 1 or compare:
        user_message = f"""Compare these medications FOR PEDIATRIC USE: {', '.join(drug_names)}

Focus on:
- Pediatric dosing differences
- Available child-friendly formulations
- Taste/palatability (when known)
- Cost for typical pediatric course or month
- Safety profile in children
- Ease of use for parents/caregivers"""
    else:
        user_message = f"Provide comprehensive PEDIATRIC drug information for: {drug_names[0]}"

    # Add clinical context to improve accuracy
    if indication:
        user_message += f"\n\nSpecific indication: {indication}"
        user_message += "\nProvide dosing specific to this indication only."

    if age:
        user_message += f"\n\nPatient age: {age}"
        user_message += "\nInclude any age-specific considerations or restrictions."

    if weight_kg:
        user_message += f"\n\nPatient weight: {weight_display}"
        user_message += calculate_dose_range(weight_kg, "standard mg/kg dosing")

    if generic_only:
        user_message += "\n\n[Focus on generic options only, include all generic manufacturers if relevant]"

    if question:
        user_message += f"\n\nSpecific question: {question}"

    # Add anti-hallucination reminder
    user_message += """

IMPORTANT:
- Only provide information you are confident about
- Clearly state if evidence in children is limited
- Mark any off-label uses as "OFF-LABEL"
- If unsure about specific details, say so rather than guessing
"""

    # ========================================================================
    # CALL CLAUDE API WITH SAFETY CHECKS
    # ========================================================================

    console.print("[dim]Querying pediatric drug information...[/dim]")
    response = call_claude(DRUG_SYSTEM_PROMPT, user_message)

    # ========================================================================
    # POST-PROCESSING: CHECK FOR HALLUCINATION INDICATORS
    # ========================================================================

    # Check for concerning phrases that might indicate hallucination
    concerning_phrases = [
        "I'm not certain",
        "I'm unsure",
        "limited evidence",
        "OFF-LABEL",
        "not well-established",
        "consult",
        "verify"
    ]

    has_uncertainty = any(phrase.lower() in response.lower() for phrase in concerning_phrases)

    if has_uncertainty:
        console.print("\n[yellow]⚠️  Note: Response includes uncertainties or off-label uses.[/yellow]")
        console.print("[yellow]   Always verify dosing with authoritative references.[/yellow]\n")

    # ========================================================================
    # DISPLAY OUTPUT
    # ========================================================================

    # Build display title
    if len(drug_names) > 1 or compare:
        title = f"Pediatric Drug Comparison: {', '.join(drug_names)}"
    else:
        title = f"Pediatric Drug Info: {drug_names[0].title()}"

    if indication:
        title += f" (for {indication})"

    if weight_display:
        title += f" - Patient: {weight_display}"

    display_output(response, title=title)


# ============================================================================
# MODULE DOCUMENTATION
# ============================================================================

"""
USAGE EXAMPLES:

1. Basic pediatric lookup:
   ./clinical drug amoxicillin

2. Weight-based dosing:
   ./clinical drug amoxicillin --weight "52#"
   ./clinical drug amoxicillin --weight "23.5kg"

3. Complete clinical context:
   ./clinical drug amoxicillin --indication "otitis media" --weight "52 lbs" --age "5yo"

4. Compare options:
   ./clinical drug amoxicillin cefdinir --compare

5. Specific question:
   ./clinical drug ondansetron --question "ODT vs liquid for 4yo?"

ANTI-HALLUCINATION FEATURES:
- System prompt explicitly instructs to state uncertainties
- Weight validation with reasonable pediatric ranges
- Post-processing checks for uncertainty markers
- User warnings when off-label or uncertain info detected

WEIGHT PARSING:
- Accepts: 52#, 52 lbs, 52 pounds, 23.5kg, 23.5 kilograms
- Converts lbs to kg automatically
- Validates reasonable pediatric ranges
- Displays both units for clarity

PEDIATRIC FOCUS:
- All responses emphasize child-friendly formulations
- Weight-based dosing prioritized
- Parent/caregiver instructions included
- Age-specific safety information highlighted
"""
