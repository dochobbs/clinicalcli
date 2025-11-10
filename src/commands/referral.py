"""Referral letter generation command"""

import click
from ..utils import call_claude, display_output, read_multiline_input, format_phi_warning

REFERRAL_SYSTEM_PROMPT = """You are an expert at writing professional referral letters to specialist colleagues.

Your role:
- Create clear, concise referral letters
- Provide relevant clinical context
- Specify the clinical question/request
- Include pertinent findings and workup to date
- Professional colleague-to-colleague tone

Structure your referral letter:

**[Professional letterhead format]**

Date: [Current date]
To: [Specialist name/practice]
From: [Referring provider]
Re: [Patient name, DOB]

Dear Dr. [Specialist]:

**Reason for Referral:**
Clear statement of clinical question and what you're asking the specialist to do

**Clinical Summary:**
- Brief relevant history
- Pertinent physical exam findings
- Workup completed to date (labs, imaging, prior treatments)
- Current medications relevant to the condition
- Response to treatments tried

**Specific Request:**
What you'd like the specialist to evaluate, advise on, or manage

**Additional Context:**
Any relevant psychosocial factors, patient concerns, urgency, or special considerations

Thank you for seeing this patient. Please let me know your recommendations.

Sincerely,
[Provider signature block]

Keep it concise but complete. Respect the specialist's time while providing necessary context."""

@click.command()
@click.option('--specialty', '-s', type=str, help='Specialist type (e.g., cardiology, orthopedics)')
@click.option('--urgent', '-u', is_flag=True, help='Mark as urgent referral')
def referral(specialty, urgent):
    """
    Generate specialist referral letter

    Create professional referral letters with clinical context and
    specific consultation requests.

    Examples:
        clinical-cli referral --specialty cardiology
        clinical-cli referral --urgent
    """
    format_phi_warning()

    # Get specialty if not provided
    if not specialty:
        specialty = click.prompt("What specialty are you referring to?", type=str)

    # Get reason for referral
    reason = click.prompt("Brief reason for referral", type=str)

    # Get clinical information
    click.echo("\nProvide relevant clinical information:")
    clinical_info = read_multiline_input(
        "Enter history, exam, workup, treatments tried, etc.:"
    )

    # Get specific request
    specific_request = click.prompt(
        "\nWhat specifically do you want the specialist to do? (evaluate, treat, advise, etc.)",
        type=str
    )

    # Build user message
    user_message = f"""Create a referral letter to {specialty}:

Reason for Referral: {reason}

Specific Request: {specific_request}

Clinical Information:
{clinical_info}
"""

    if urgent:
        user_message += "\n\n[Mark as URGENT - explain time-sensitive nature]"

    # Get response
    response = call_claude(REFERRAL_SYSTEM_PROMPT, user_message)

    # Display output
    title = f"Referral to {specialty.title()}"
    if urgent:
        title += " [URGENT]"

    display_output(response, title=title)
