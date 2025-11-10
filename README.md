# Clinical CLI - PHI-Safe Clinical Decision Support

A command-line tool for physicians to use Claude AI for clinical decision support, documentation, and patient education while handling Protected Health Information (PHI) under a Business Associate Agreement with Anthropic.

## Features

### Core Commands

1. **`cds`** - Clinical Decision Support
   - Evidence-based clinical guidance
   - Differential diagnosis consideration
   - Workup and management recommendations
   - Red flag identification

2. **`handout`** - Patient Education Materials
   - Plain-language patient handouts
   - Customizable reading level
   - Condition-specific information
   - Multi-language support

3. **`note`** - Clinical Documentation
   - SOAP notes
   - Progress notes
   - Consultation notes
   - Procedure notes
   - Discharge summaries

4. **`prior-auth`** - Prior Authorization Letters
   - Medical necessity documentation
   - Evidence-based justification
   - Appeal letter generation
   - Urgent/expedited requests

5. **`referral`** - Specialist Referral Letters
   - Professional colleague communications
   - Clinical context and workup summary
   - Specific consultation requests

6. **`ddx`** - Differential Diagnosis
   - Systematic differential generation
   - Likelihood ranking
   - "Can't miss" diagnosis highlighting
   - Targeted workup suggestions

7. **`parse`** - Document Analysis
   - Parse screenshots and PDF files
   - Extract lab results, imaging reports, consultation notes
   - OCR and text extraction with interpretation
   - Support for multiple file formats (PNG, JPG, PDF)

8. **`drug`** - Drug Information Lookup (NEW)
   - Comprehensive medication information
   - Available dosing forms and strengths
   - Cost comparison (generic vs brand)
   - Patient instructions and safety information
   - Compare multiple medications
   - Pediatric dosing

### File Attachment Support

Most commands now support attaching files (screenshots, PDFs):
- Use `--file` or `-f` flag to attach documents
- Support for lab results, imaging, consultation notes
- Automatic text extraction from PDFs
- Vision API for screenshots and scanned documents

## Requirements

- Python 3.9+
- Anthropic API key with BAA for PHI processing
- macOS, Linux, or Windows

## Installation

### 1. Navigate to the directory
```bash
cd /Users/dochobbs/Downloads/Consult/Claude/clinical-cli
```

### 2. Create and activate virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify API key
The tool uses the `ANTHROPIC_API_KEY` from your environment (already configured in `~/.zshrc`).

To verify:
```bash
echo $ANTHROPIC_API_KEY
```

### 5. Make CLI executable (optional)
```bash
chmod +x src/cli.py
```

## Usage

### Basic Usage

Activate the virtual environment first:
```bash
source .venv/bin/activate
```

Run commands:
```bash
python src/cli.py <command> [options]
```

### Command Examples

#### Clinical Decision Support
```bash
# Basic CDS query
python src/cli.py cds

# Pediatric case
python src/cli.py cds --specialty pediatrics

# Urgent case
python src/cli.py cds --urgent
```

#### Patient Handouts
```bash
# Create handout for a condition
python src/cli.py handout --condition "asthma management"

# Simple language version
python src/cli.py handout --condition "diabetes" --reading-level simple

# Spanish language
python src/cli.py handout --condition "hypertension" --language Spanish
```

#### Clinical Notes
```bash
# Generate SOAP note
python src/cli.py note

# Consultation note
python src/cli.py note --type consult --specialty cardiology

# Note with billing detail
python src/cli.py note --billing
```

#### Prior Authorization
```bash
# Request for service
python src/cli.py prior-auth --service "MRI lumbar spine"

# Urgent request
python src/cli.py prior-auth --urgent

# Appeal a denial
python src/cli.py prior-auth --appeal
```

#### Referral Letters
```bash
# Referral to specialist
python src/cli.py referral --specialty neurology

# Urgent referral
python src/cli.py referral --specialty cardiology --urgent
```

#### Differential Diagnosis
```bash
# Generate differential
python src/cli.py ddx

# Focus on specific system
python src/cli.py ddx --system respiratory

# Include rare diagnoses
python src/cli.py ddx --broad

# Pediatric case
python src/cli.py ddx --age pediatric
```

#### Document Parsing (NEW)
```bash
# Parse a lab result PDF
python src/cli.py parse labs.pdf

# Parse multiple files at once
python src/cli.py parse labs.pdf xray.png

# Parse with document type hint
python src/cli.py parse report.pdf --type imaging

# Just extract text without interpretation
python src/cli.py parse consult.pdf --extract-only

# Ask specific question about document
python src/cli.py parse discharge.pdf --question "What medications were prescribed?"
```

#### Drug Information Lookup (NEW)
```bash
# Look up a medication
python src/cli.py drug lisinopril

# Compare multiple drugs
python src/cli.py drug sertraline fluoxetine paroxetine --compare

# Pediatric dosing
python src/cli.py drug amoxicillin --pediatric

# For specific indication
python src/cli.py drug metformin --indication "type 2 diabetes"

# Generic options only
python src/cli.py drug atorvastatin --generic-only

# Ask specific question
python src/cli.py drug warfarin --question "What are the major interactions?"

# Combined options
python src/cli.py drug amoxicillin --pediatric --indication "otitis media"
```

#### Using Files with Other Commands
```bash
# CDS with attached lab results
python src/cli.py cds --file labs.pdf --file xray.png

# You'll be prompted to enter clinical context
# The files will be automatically analyzed with your input

# Note generation with attached documents
python src/cli.py note --file consult.pdf --file labs.pdf
```

### Getting Help
```bash
# General help
python src/cli.py --help

# Command-specific help
python src/cli.py cds --help
python src/cli.py note --help
```

## Input Methods

Most commands support multiline input:
- Type or paste your clinical information
- Press **Ctrl+D** (macOS/Linux) or **Ctrl+Z** (Windows) when done
- The tool will process and display results

## Output

- Results display in formatted markdown panels
- Automatic clipboard copy option (configurable per command)
- All outputs ready to paste into EMR, letters, or documents

## HIPAA Compliance

⚠️ **PHI Warning**: This tool processes Protected Health Information.

- **BAA Required**: Only use with Anthropic API under signed BAA
- **Authorized Use**: Ensure proper authorization for PHI processing
- **Secure Handling**: Do not share outputs containing PHI insecurely
- **Audit Trail**: Consider logging usage for compliance

## Model Information

- Default model: **Claude Sonnet 4.5** (`claude-sonnet-4-5-20250929`)
- Max tokens: 4096 per response
- Optimized for medical accuracy and clinical reasoning

## Development

### Project Structure
```
clinical-cli/
├── src/
│   ├── cli.py              # Main CLI entry point
│   ├── utils.py            # Shared utilities
│   └── commands/           # Individual command modules
│       ├── __init__.py
│       ├── cds.py
│       ├── handout.py
│       ├── note.py
│       ├── prior_auth.py
│       ├── referral.py
│       └── ddx.py
├── requirements.txt
└── README.md
```

### Adding New Commands

1. Create new command file in `src/commands/`
2. Define system prompt and command function
3. Import and register in `src/cli.py`
4. Test with `python src/cli.py <new-command> --help`

### Future Enhancements

Potential additions:
- Lab interpretation command
- ICD-10/CPT code lookup
- Drug interaction checker
- Evidence-based medicine queries
- Literature search integration
- Template management system
- Batch processing mode
- Output format options (PDF, DOCX)

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
- Verify: `echo $ANTHROPIC_API_KEY`
- If empty, add to `~/.zshrc`: `export ANTHROPIC_API_KEY="your-key-here"`
- Restart terminal or run: `source ~/.zshrc`

### Import errors
- Ensure virtual environment is activated
- Reinstall: `pip install -r requirements.txt`

### Clipboard not working
- Install clipboard utilities: `brew install pbcopy` (macOS)
- Or decline clipboard option when prompted

## License

Internal use only. Requires valid Anthropic API credentials and BAA for PHI processing.

## Support

For issues or questions:
- Check command help: `python src/cli.py <command> --help`
- Review this README
- Consult Anthropic API documentation

---

**Version:** 1.0.0
**Last Updated:** November 9, 2025
**Model:** Claude Sonnet 4.5
