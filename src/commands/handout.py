"""Patient handout generation command"""

import click
from ..utils import call_claude, display_output, read_multiline_input, format_phi_warning

HANDOUT_SYSTEM_PROMPT = """You are an expert at creating patient education materials.

Your role:
- Write clear, compassionate patient handouts
- Use 6th-8th grade reading level
- Avoid medical jargon; explain terms when necessary
- Include actionable advice and clear instructions
- Address common patient questions
- Provide appropriate reassurance and safety information

Structure your handout with:
1. **What You Need to Know**: Brief overview in plain language
2. **What to Expect**: Timeline, symptoms, recovery
3. **What You Should Do**: Clear action items, medications, lifestyle
4. **Warning Signs**: When to call or seek emergency care
5. **Common Questions**: Address typical concerns
6. **Follow-Up**: When to return, what to monitor

Tone: Professional, warm, reassuring but realistic. Empower patients with knowledge."""

@click.command()
@click.option('--condition', '-c', type=str, help='Specific condition/diagnosis for handout')
@click.option('--reading-level', '-r', type=click.Choice(['simple', 'standard', 'detailed']),
              default='standard', help='Adjust complexity')
@click.option('--language', '-l', type=str, default='English', help='Target language (default: English)')
def handout(condition, reading_level, language):
    """
    Generate patient education handout

    Create patient-friendly educational materials for specific conditions,
    post-visit instructions, or preventive care topics.

    Examples:
        clinical-cli handout --condition "asthma management"
        clinical-cli handout --reading-level simple
        clinical-cli handout --condition "URI" --language Spanish
    """
    format_phi_warning()

    # Get handout details
    if not condition:
        condition = click.prompt("What condition/topic for the handout?", type=str)

    additional_info = click.prompt(
        "Any specific points to cover? (optional, press Enter to skip)",
        default="",
        show_default=False
    )

    # Build user message
    user_message = f"Create a patient handout for: {condition}"

    if additional_info:
        user_message += f"\n\nSpecific points to address:\n{additional_info}"

    # Adjust for reading level
    if reading_level == 'simple':
        user_message += "\n\n[Use very simple language, 5th-6th grade level, short sentences]"
    elif reading_level == 'detailed':
        user_message += "\n\n[Provide more detailed explanations for engaged patients]"

    if language != 'English':
        user_message += f"\n\n[Write the entire handout in {language}]"

    # Get response
    response = call_claude(HANDOUT_SYSTEM_PROMPT, user_message)

    # Display output
    display_output(response, title=f"Patient Handout: {condition}")
