"""Clinical image analysis for rashes, lesions, injuries, and other visual findings"""

import click
from pathlib import Path
from ..utils import call_claude_with_files, display_output, format_phi_warning, console

IMAGE_ANALYSIS_SYSTEM_PROMPT = """You are a pediatric clinical expert analyzing visual medical findings sent by parents or providers.

Your role:
- Provide detailed clinical assessment of visual findings (rashes, lesions, injuries, etc.)
- Identify key clinical features visible in the image
- Offer differential diagnosis based on visual appearance
- Suggest appropriate triage and management
- Flag concerning features requiring immediate evaluation
- Provide parent education when appropriate

## Analysis Framework

**Describe What You See:**
- Distribution and pattern
- Morphology (macules, papules, vesicles, etc.)
- Color, size, borders
- Associated findings (swelling, drainage, etc.)

**Differential Diagnosis:**
- Most likely diagnoses based on appearance
- Include common pediatric conditions
- Note any concerning features
- Consider age-appropriate differentials

**Clinical Assessment:**
- Severity assessment (mild, moderate, severe)
- RED FLAGS that require immediate evaluation
- Likelihood of different conditions
- Natural history/expected course

**Recommendations:**
- Triage decision (911, ED, urgent, routine, home care)
- Specific treatment suggestions (topical, oral, supportive)
- When to seek further care
- Home care instructions
- Follow-up timing

**Parent Education:**
- What this likely represents
- What to watch for (warning signs)
- Expected timeline for improvement
- When to call back

## Important Reminders

**Safety First:**
- Always err on the side of caution with concerning features
- Explicitly state if ER evaluation needed
- Note limitations of photo assessment vs in-person exam
- Recommend follow-up when diagnosis uncertain

**Be Specific:**
- Use precise clinical terminology but explain in parent-friendly terms
- Give actionable recommendations
- Include specific treatments (e.g., "hydrocortisone 1% cream twice daily")

**Common Pediatric Presentations:**
- Viral exanthems (roseola, hand-foot-mouth, fifth disease, etc.)
- Bacterial infections (impetigo, cellulitis, abscess)
- Allergic reactions (urticaria, contact dermatitis, drug reactions)
- Eczema/atopic dermatitis
- Insect bites
- Traumatic injuries
- Burns (thermal, chemical, sun)
- Birthmarks and benign lesions

Format your response with clear sections using markdown headings.
Make it immediately clinically actionable."""

@click.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True), required=True)
@click.option('--type', '-t', 'finding_type',
              type=click.Choice(['auto', 'rash', 'lesion', 'injury', 'throat', 'eye', 'skin']),
              default='auto',
              help='Type of clinical finding (auto-detect by default)')
@click.option('--context', '-c', type=str, help='Additional clinical context (age, duration, symptoms)')
@click.option('--question', '-q', type=str, help='Specific question about the image')
def image(files, finding_type, context, question):
    """
    Analyze clinical images (rashes, lesions, injuries, etc.)

    Accepts photos of clinical findings sent by parents or captured in clinic.
    Provides assessment, differential diagnosis, and management recommendations.

    Examples:
        clinical-cli image rash.jpg
        clinical-cli image lesion.png --context "5yo, present x3 days, itchy"
        clinical-cli image throat.jpg --type throat
        clinical-cli image bite.jpg --question "Is this infected?"
    """
    format_phi_warning()

    # Build user message
    user_message_parts = []

    if finding_type == 'auto':
        user_message_parts.append("Analyze this clinical image and provide assessment with differential diagnosis.")
    elif finding_type == 'rash':
        user_message_parts.append("This is an image of a rash. Provide detailed analysis including morphology, distribution, differential diagnosis, and management.")
    elif finding_type == 'lesion':
        user_message_parts.append("This is an image of a skin lesion. Describe morphology, concerning features, differential diagnosis, and recommendations.")
    elif finding_type == 'injury':
        user_message_parts.append("This is an image of an injury. Assess severity, need for further evaluation, wound care recommendations.")
    elif finding_type == 'throat':
        user_message_parts.append("This is a throat/pharynx image. Assess for signs of infection, exudate, swelling, and provide differential diagnosis.")
    elif finding_type == 'eye':
        user_message_parts.append("This is an eye image. Assess for conjunctivitis, injury, foreign body, and provide recommendations.")
    elif finding_type == 'skin':
        user_message_parts.append("This is a skin finding. Provide detailed dermatologic assessment and recommendations.")

    # Add clinical context if provided
    if context:
        user_message_parts.append(f"\n\nClinical context: {context}")

    # Add specific question if provided
    if question:
        user_message_parts.append(f"\n\nSpecific question: {question}")

    user_message = "\n".join(user_message_parts)

    # Process files
    file_list = list(files)

    if len(file_list) > 1:
        user_message += f"\n\n[Note: {len(file_list)} images provided - analyze all and provide comprehensive assessment]"

    # Get response
    response = call_claude_with_files(IMAGE_ANALYSIS_SYSTEM_PROMPT, user_message, file_list)

    # Display output
    if len(file_list) == 1:
        title = f"Clinical Image Analysis: {Path(file_list[0]).name}"
    else:
        title = f"Clinical Image Analysis: {len(file_list)} images"

    if finding_type != 'auto':
        title += f" ({finding_type})"

    display_output(response, title=title)
