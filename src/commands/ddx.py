"""Differential diagnosis command"""

import click
from ..utils import call_claude, display_output, read_multiline_input, format_phi_warning

DDX_SYSTEM_PROMPT = """You are an expert diagnostician helping generate comprehensive differential diagnoses.

Your role:
- Generate thorough, systematic differential diagnoses
- Rank diagnoses by likelihood and severity
- Identify key discriminating features
- Suggest targeted workup to narrow the differential
- Highlight "can't miss" diagnoses
- Use clinical reasoning frameworks

Structure your response:

**Clinical Summary:**
Brief synthesis of the key features

**Differential Diagnosis:**
List in order of likelihood, with each diagnosis including:
1. **[Diagnosis Name]** (Likelihood: High/Moderate/Low)
   - Supporting features
   - Features against
   - Key tests to confirm/exclude

**"Can't Miss" Diagnoses:**
Critical/life-threatening diagnoses to rule out even if less likely

**Discriminating Features:**
Which findings would most help narrow the differential

**Suggested Workup:**
Prioritized list of tests/imaging to refine diagnosis

**Clinical Reasoning:**
Brief explanation of diagnostic approach

Be systematic and thorough. Consider common, serious, and treatable causes."""

@click.command()
@click.option('--system', '-s', type=str, help='Organ system focus (e.g., cardiac, pulmonary)')
@click.option('--age', '-a', type=str, help='Patient age context')
@click.option('--broad', '-b', is_flag=True, help='Generate broader differential (include rare diagnoses)')
def ddx(system, age, broad):
    """
    Generate differential diagnosis

    Create systematic differential diagnosis lists with clinical reasoning,
    ranked by likelihood, and suggested workup.

    Examples:
        clinical-cli ddx
        clinical-cli ddx --system cardiac
        clinical-cli ddx --age pediatric --broad
    """
    format_phi_warning()

    # Get clinical presentation
    click.echo("Provide clinical presentation for differential diagnosis:")
    clinical_info = read_multiline_input(
        "Enter symptoms, history, exam findings, initial labs/imaging:"
    )

    # Build user message
    user_message = f"Generate a differential diagnosis for:\n\n{clinical_info}"

    if system:
        user_message += f"\n\n[Focus on {system} diagnoses]"

    if age:
        user_message += f"\n\n[Patient age context: {age}]"

    if broad:
        user_message += "\n\n[Include broader differential with less common/rare diagnoses]"
    else:
        user_message += "\n\n[Focus on most likely common diagnoses, but don't miss serious ones]"

    # Get response
    response = call_claude(DDX_SYSTEM_PROMPT, user_message)

    # Display output
    title = "Differential Diagnosis"
    if system:
        title += f" ({system})"
    if age:
        title += f" - {age}"

    display_output(response, title=title)
