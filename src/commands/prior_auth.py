"""Prior authorization letter generation command"""

import click
from ..utils import call_claude, display_output, read_multiline_input, format_phi_warning

PRIOR_AUTH_SYSTEM_PROMPT = """You are an expert at writing prior authorization and appeal letters for medical services.

Your role:
- Create compelling, evidence-based prior authorization letters
- Document medical necessity clearly
- Address insurance criteria directly
- Include relevant clinical guidelines and evidence
- Anticipate and counter common denial reasons
- Use professional, persuasive tone

Structure your letter:

**[Letterhead format]**

To: [Insurance Company] Utilization Management
Re: Prior Authorization Request
Patient: [Name, DOB, Member ID]
Requested Service/Medication: [Specific item]
ICD-10 Diagnosis Codes: [Relevant codes]
CPT/HCPCS Codes: [If applicable]

**Introduction:**
Brief statement of request and clinical urgency

**Clinical History:**
- Relevant medical history
- Prior treatments attempted and failed
- Current clinical status
- Complications or progression

**Medical Necessity:**
- Why this specific intervention is necessary
- Why alternatives are inadequate or contraindicated
- Clinical guidelines supporting this approach
- Expected outcomes and benefits

**Evidence Base:**
- Cite relevant clinical guidelines (specialty society recommendations)
- Reference literature if applicable
- Address insurance coverage criteria directly

**Conclusion:**
Strong closing statement requesting approval

Be thorough, professional, and persuasive. Focus on medical necessity and patient safety."""

@click.command()
@click.option('--service', '-s', type=str, help='Service/medication requiring authorization')
@click.option('--urgent', '-u', is_flag=True, help='Mark as urgent/expedited request')
@click.option('--appeal', '-a', is_flag=True, help='This is an appeal of a denial')
def prior_auth(service, urgent, appeal):
    """
    Generate prior authorization letter

    Create detailed medical necessity letters for insurance prior authorizations
    or appeals. Includes clinical rationale and evidence-based support.

    Examples:
        clinical-cli prior-auth --service "MRI brain"
        clinical-cli prior-auth --urgent
        clinical-cli prior-auth --appeal
    """
    format_phi_warning()

    # Get service if not provided
    if not service:
        service = click.prompt("What service/medication needs authorization?", type=str)

    # Get clinical information
    click.echo("\nProvide clinical information supporting the request:")
    clinical_info = read_multiline_input(
        "Enter relevant history, diagnosis, prior treatments, medical necessity:"
    )

    # Build user message
    user_message = f"""Create a prior authorization {"appeal" if appeal else "request"} letter for:

Service/Medication: {service}

Clinical Information:
{clinical_info}
"""

    if urgent:
        user_message += "\n\n[Mark this as URGENT/EXPEDITED - explain time-sensitive medical necessity]"

    if appeal:
        denial_reason = click.prompt(
            "\nWhat was the reason for denial?",
            default="",
            show_default=False
        )
        if denial_reason:
            user_message += f"\n\nDenial Reason: {denial_reason}\n[Directly address and refute the denial reason]"

    # Get response
    response = call_claude(PRIOR_AUTH_SYSTEM_PROMPT, user_message)

    # Display output
    title = "Prior Authorization "
    title += "Appeal" if appeal else "Request"
    if urgent:
        title += " [URGENT]"
    title += f": {service}"

    display_output(response, title=title)
