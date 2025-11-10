"""
Clinical Decision Support command - Pediatric focused

This module provides evidence-based clinical guidance for pediatric cases with:
- Age-appropriate differential diagnoses
- Pediatric-specific workup recommendations
- Red flag identification for children
- Family-centered management plans
- Growth/development considerations
"""

import click
from ..utils import (
    call_claude,
    call_claude_with_files,
    display_output,
    read_multiline_input,
    format_phi_warning,
    console
)

# ============================================================================
# PEDIATRIC CDS SYSTEM PROMPT WITH ANTI-HALLUCINATION SAFEGUARDS
# ============================================================================

CDS_SYSTEM_PROMPT = """You are an expert pediatric clinical decision support system for pediatricians and pediatric providers.

CRITICAL INSTRUCTIONS - ANTI-HALLUCINATION SAFEGUARDS:
1. If you are UNCERTAIN about ANY clinical recommendation, explicitly state "Further evaluation recommended" or "Consider specialist consultation"
2. For diagnoses, ONLY suggest conditions that fit the clinical picture - do not list every possible diagnosis
3. If information is insufficient for clinical guidance, clearly state what additional information is needed
4. Do NOT provide specific dosing - instead note "dose based on weight" and refer to drug references
5. When evidence in pediatrics is limited, explicitly state "Limited pediatric data available"
6. For urgent/emergent presentations, clearly highlight time-sensitive interventions
7. Always consider age-appropriate differentials (e.g., don't suggest adult conditions in young children)
8. If a presentation is atypical for the age group, note this explicitly

Your role:
- Provide evidence-based PEDIATRIC clinical guidance
- Consider age-appropriate differential diagnoses
- Suggest appropriate workup for children (minimally invasive when possible)
- Highlight red flags and safety concerns specific to pediatrics
- Reference current AAP, PIDS, and other pediatric guidelines when applicable
- Consider family/caregiver context
- Maintain clinical accuracy and safety

Format your response as:

1. **CLINICAL ASSESSMENT**
   - Brief summary of presentation with age context
   - Acuity level: Emergent / Urgent / Non-urgent
   - Red flags identified (if any)

2. **KEY CONSIDERATIONS**
   - Age-specific clinical points
   - Pertinent positives and negatives
   - Growth/development context (if relevant)
   - Risk factors or protective factors

3. **DIFFERENTIAL DIAGNOSIS** (Ranked by likelihood)
   For each diagnosis, list:
   - Diagnosis name with likelihood (High/Moderate/Low)
   - Supporting features from presentation
   - Features against this diagnosis
   - Key distinguishing features

   Start with "CAN'T MISS" diagnoses (serious/life-threatening) even if less likely

4. **RECOMMENDED WORKUP**
   Prioritize least invasive → more invasive:
   - Vital signs and physical exam findings to assess
   - Point-of-care testing (if applicable)
   - Laboratory tests (with rationale)
   - Imaging (with rationale and radiation considerations)
   - Consultations needed

5. **MANAGEMENT RECOMMENDATIONS** (Evidence-based)
   Immediate:
   - Stabilization if needed
   - Symptomatic management
   - Family counseling points

   Definitive:
   - Treatment plan (note "weight-based dosing" for medications)
   - Non-pharmacologic interventions
   - Anticipatory guidance for parents
   - When to escalate care

6. **SAFETY NET**
   - Return precautions (specific symptoms to watch for)
   - Red flags that require immediate return
   - Expected clinical course and timeline
   - Follow-up timing and plan
   - Parent education points

7. **REFERENCES/GUIDELINES** (when applicable)
   - Cite AAP, PIDS, CDC, or other pediatric-specific guidelines
   - Note strength of evidence (strong/moderate/weak/expert opinion)

IMPORTANT REMINDERS:
- Always consider the child's age and developmental stage
- Account for immunization status when relevant
- Consider social determinants and family resources
- Be explicit about uncertainties and when to seek specialist input
- Avoid adult-centric thinking
- Consider minimally invasive approaches first
- Think about family/caregiver education needs

Be concise but thorough. Focus on actionable clinical decision-making.
If critical information is missing, state what is needed for better guidance."""


# ============================================================================
# MAIN COMMAND FUNCTION
# ============================================================================

@click.command()
@click.option('--age', '-a', type=str,
              help='Patient age (e.g., "5yo", "18mo", "3 weeks") - RECOMMENDED for pediatric guidance')
@click.option('--urgent', '-u', is_flag=True,
              help='Flag case as urgent/emergent (prioritizes red flags)')
@click.option('--file', '-f', 'files', multiple=True, type=click.Path(exists=True),
              help='Attach files (labs, images, PDFs) for analysis')
def cds(age, urgent, files):
    """
    Pediatric Clinical Decision Support - Evidence-based guidance

    Provides structured pediatric clinical decision support including age-appropriate
    differential diagnosis, workup recommendations, and family-centered management.

    Examples:
        # Basic pediatric case
        clinical cds --age "5yo"

        # Urgent/emergent presentation
        clinical cds --age "18mo" --urgent

        # With attached lab results
        clinical cds --age "3yo" --file labs.pdf

        # With multiple attachments
        clinical cds --age "7yo" --file labs.pdf --file xray.png --urgent
    """
    # Display PHI warning
    format_phi_warning()

    # ========================================================================
    # GET CLINICAL PRESENTATION
    # ========================================================================

    # Prompt for clinical information
    prompt_text = "Enter clinical presentation (history, exam, vitals, etc.):"
    if age:
        prompt_text = f"Enter clinical presentation for {age} patient:"

    clinical_info = read_multiline_input(prompt_text)

    # ========================================================================
    # BUILD QUERY WITH PEDIATRIC CONTEXT
    # ========================================================================

    # Start with clinical information
    user_message = clinical_info

    # Add age context (critical for pediatric care)
    if age:
        user_message = f"[Patient Age: {age}]\n\n{user_message}"
        user_message += "\n\nProvide age-appropriate clinical guidance for this child."
    else:
        # Warn if age not provided
        console.print("[yellow]⚠️  Age not specified - providing general pediatric guidance.[/yellow]")
        console.print("[yellow]   Add --age flag for age-specific recommendations.[/yellow]\n")

    # Mark as urgent/emergent if flagged
    if urgent:
        user_message = f"[URGENT/EMERGENT CASE]\n\n{user_message}"
        user_message += "\n\nPrioritize red flags, time-sensitive interventions, and immediate stabilization."

    # Add anti-hallucination reminder for pediatric safety
    user_message += """

IMPORTANT:
- Only suggest diagnoses that fit the clinical picture
- Clearly state if you need more information for better guidance
- Note when evidence in children is limited
- Be explicit about uncertainties
- Consider age-appropriate differentials only
"""

    # ========================================================================
    # CALL CLAUDE API (with files if provided)
    # ========================================================================

    console.print("[dim]Analyzing pediatric case...[/dim]")

    # Use file-aware function if files provided, otherwise standard call
    if files:
        response = call_claude_with_files(CDS_SYSTEM_PROMPT, user_message, list(files))
    else:
        response = call_claude(CDS_SYSTEM_PROMPT, user_message)

    # ========================================================================
    # POST-PROCESSING: CHECK FOR CRITICAL INDICATORS
    # ========================================================================

    # Check for red flag indicators in response
    red_flag_phrases = [
        "emergent",
        "immediate",
        "urgent",
        "911",
        "ED",
        "emergency department",
        "life-threatening",
        "critical"
    ]

    has_red_flags = any(phrase.lower() in response.lower() for phrase in red_flag_phrases)

    if has_red_flags:
        console.print("\n[red]🚨 ALERT: Response contains emergent/urgent indicators[/red]")
        console.print("[red]   Review time-sensitive recommendations carefully[/red]\n")

    # Check for uncertainty indicators
    uncertainty_phrases = [
        "uncertain",
        "unclear",
        "limited information",
        "need more",
        "consider specialist",
        "further evaluation"
    ]

    has_uncertainty = any(phrase.lower() in response.lower() for phrase in uncertainty_phrases)

    if has_uncertainty:
        console.print("\n[yellow]⚠️  Note: Response indicates need for additional information or specialist input[/yellow]\n")

    # ========================================================================
    # DISPLAY OUTPUT
    # ========================================================================

    # Build display title
    title = "Pediatric Clinical Decision Support"

    if age:
        title += f" - Age: {age}"

    if urgent:
        title += " [URGENT]"

    display_output(response, title=title)


# ============================================================================
# MODULE DOCUMENTATION
# ============================================================================

"""
USAGE EXAMPLES:

1. Basic pediatric case:
   ./clinical cds --age "5yo"
   [Enter presentation when prompted]

2. Urgent presentation:
   ./clinical cds --age "18mo" --urgent
   [Enter presentation when prompted]

3. With lab results:
   ./clinical cds --age "3yo" --file labs.pdf
   [Enter clinical context when prompted]

4. Complete case with multiple files:
   ./clinical cds --age "7yo" --file labs.pdf --file chest-xray.png
   [Enter presentation when prompted]

ANTI-HALLUCINATION FEATURES:
- System prompt explicitly limits to age-appropriate conditions
- Requires uncertainty to be stated when evidence limited
- Post-processing detects red flags and uncertainties
- User warnings for emergent conditions
- Prompts for age (critical for pediatric care)

PEDIATRIC FOCUS:
- Age-appropriate differential diagnoses
- Minimally invasive workup prioritized
- Family/caregiver education emphasized
- Growth/development context included
- Pediatric guideline references (AAP, PIDS, CDC)

FILE SUPPORT:
- Can attach lab results, imaging, consultation notes
- Automatic processing of PDFs and images
- Integrated into clinical decision support
"""
