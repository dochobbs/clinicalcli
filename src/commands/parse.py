"""Parse and analyze clinical documents (screenshots, PDFs)"""

import click
from pathlib import Path
from ..utils import call_claude_with_files, display_output, format_phi_warning, console

PARSE_SYSTEM_PROMPT = """You are an expert at analyzing and extracting information from clinical documents.

Your role:
- Extract all relevant clinical information from the provided document
- Organize information clearly and systematically
- Identify key findings, diagnoses, lab values, medications
- Flag abnormal results or critical findings
- Summarize in a clinically useful format

When analyzing documents:

**For Lab Results:**
- List all test results with reference ranges
- Highlight abnormal values
- Note critical values
- Provide brief clinical interpretation

**For Imaging/Radiology Reports:**
- Extract findings section
- Note impressions/conclusions
- Highlight critical or urgent findings
- Include comparison to prior studies if mentioned

**For Consultation Notes:**
- Extract key recommendations
- Note diagnosis and assessment
- List suggested workup or treatments
- Include follow-up plans

**For Medication Lists:**
- Extract all medications with doses
- Note any new prescriptions or changes
- Identify potential interactions or concerns

**For General Clinical Documents:**
- Summarize key clinical information
- Extract diagnoses, problems, allergies
- Note dates, providers, visit types
- Highlight action items or follow-up needs

Format your response clearly with markdown headings and bullet points.
Make it immediately useful for clinical decision-making."""

@click.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True), required=True)
@click.option('--type', '-t', 'doc_type',
              type=click.Choice(['auto', 'labs', 'imaging', 'consult', 'medication', 'general']),
              default='auto',
              help='Type of document (auto-detect by default)')
@click.option('--extract-only', '-e', is_flag=True, help='Just extract text, no interpretation')
@click.option('--question', '-q', type=str, help='Ask specific question about the document')
def parse(files, doc_type, extract_only, question):
    """
    Parse and analyze clinical documents (images, PDFs)

    Accepts screenshots, scanned documents, or PDF files and extracts
    relevant clinical information with interpretation.

    Examples:
        clinical-cli parse labs.pdf
        clinical-cli parse screenshot.png --type labs
        clinical-cli parse report1.pdf report2.pdf
        clinical-cli parse consult.pdf --question "What were the recommendations?"
    """
    format_phi_warning()

    # Build user message
    if extract_only:
        user_message = "Extract all text and information from this document. Present it in a clear, organized format."
    elif question:
        user_message = f"Answer this question about the document:\n\n{question}"
    else:
        if doc_type == 'auto':
            user_message = "Analyze this clinical document and extract all relevant information."
        elif doc_type == 'labs':
            user_message = "This is a lab results document. Extract all results, flag abnormal values, and provide clinical interpretation."
        elif doc_type == 'imaging':
            user_message = "This is an imaging/radiology report. Extract findings, impressions, and critical results."
        elif doc_type == 'consult':
            user_message = "This is a consultation note. Extract key recommendations, diagnosis, and follow-up plans."
        elif doc_type == 'medication':
            user_message = "This is a medication list. Extract all medications with doses and note any concerns."
        else:
            user_message = "Extract and summarize the clinical information from this document."

    # Process files
    file_list = list(files)
    console_msg = f"Analyzing {len(file_list)} file(s)..."

    if len(file_list) > 1:
        user_message += f"\n\n[Note: {len(file_list)} files provided - analyze all and combine information]"

    # Get response
    response = call_claude_with_files(PARSE_SYSTEM_PROMPT, user_message, file_list)

    # Display output
    if len(file_list) == 1:
        title = f"Document Analysis: {Path(file_list[0]).name}"
    else:
        title = f"Document Analysis: {len(file_list)} files"

    if doc_type != 'auto':
        title += f" ({doc_type})"

    display_output(response, title=title)
