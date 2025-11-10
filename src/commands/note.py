"""Clinical note generation command"""

import click
from ..utils import call_claude, display_output, read_multiline_input, format_phi_warning

NOTE_SYSTEM_PROMPT = """You are an expert medical scribe creating professional clinical documentation.

Your role:
- Generate complete, professional clinical notes
- Follow standard medical documentation format
- Include all necessary clinical elements
- Use appropriate medical terminology
- Ensure billing/coding support with detail
- Document clinical reasoning

Create notes in standard SOAP format (or specified alternative):

**SUBJECTIVE:**
- Chief complaint
- HPI (onset, location, duration, character, aggravating/alleviating factors, radiation, timing, severity)
- Review of systems (pertinent positives and negatives)
- Past medical/surgical history (if relevant)
- Medications, allergies
- Social/family history (if relevant)

**OBJECTIVE:**
- Vital signs
- Physical examination (organized by system)
- Relevant lab/imaging results

**ASSESSMENT:**
- Problem list with ICD-10 codes when applicable
- Clinical reasoning and differential considerations
- Severity/stability assessment

**PLAN:**
- Organized by problem
- Medications (dose, route, frequency, duration)
- Non-pharmacologic interventions
- Diagnostic workup ordered
- Referrals/consultations
- Patient education provided
- Follow-up timing and instructions
- Return precautions

Make the note thorough, accurate, and ready for the medical record."""

@click.command()
@click.option('--type', '-t', 'note_type',
              type=click.Choice(['soap', 'progress', 'consult', 'procedure', 'discharge']),
              default='soap',
              help='Type of note to generate')
@click.option('--specialty', '-s', type=str, help='Medical specialty context')
@click.option('--billing', '-b', is_flag=True, help='Include billing/coding details')
def note(note_type, specialty, billing):
    """
    Generate clinical documentation note

    Create professional medical notes from clinical encounter information.
    Supports SOAP notes, progress notes, consult notes, and more.

    Examples:
        clinical-cli note
        clinical-cli note --type consult --specialty cardiology
        clinical-cli note --billing
    """
    format_phi_warning()

    # Get clinical encounter information
    click.echo(f"\n[Creating {note_type.upper()} note]\n")

    encounter_info = read_multiline_input(
        "Enter encounter information (can be rough notes, bullet points, or narrative):"
    )

    # Build user message
    user_message = f"Generate a {note_type.upper()} note from the following encounter:\n\n{encounter_info}"

    if specialty:
        user_message = f"[Specialty: {specialty}]\n\n{user_message}"

    if billing:
        user_message += "\n\n[Include detailed documentation to support appropriate billing level and ICD-10/CPT codes]"

    # Adjust system prompt based on note type
    system_prompt = NOTE_SYSTEM_PROMPT

    if note_type == 'progress':
        system_prompt += "\n\nFormat as brief progress note: Interval history, exam changes, assessment/plan by problem."
    elif note_type == 'consult':
        system_prompt += "\n\nFormat as consultation note: Include detailed history, comprehensive exam, detailed assessment with recommendations."
    elif note_type == 'procedure':
        system_prompt += "\n\nFormat as procedure note: Indication, consent, procedure details, findings, complications, plan."
    elif note_type == 'discharge':
        system_prompt += "\n\nFormat as discharge summary: Admission diagnosis, hospital course, discharge condition, medications, follow-up."

    # Get response
    response = call_claude(system_prompt, user_message)

    # Display output
    title = f"{note_type.upper()} Note"
    if specialty:
        title += f" ({specialty})"

    display_output(response, title=title)
