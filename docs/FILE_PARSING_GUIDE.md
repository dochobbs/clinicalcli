# File Parsing Guide

## Overview

The Clinical CLI now supports parsing and analyzing clinical documents including:
- **Screenshots** (PNG, JPG, WebP, GIF)
- **PDF documents** (lab results, imaging reports, consultation notes)
- **Scanned documents** (via OCR through Claude's vision capabilities)

## How It Works

### Images/Screenshots
- Images are encoded in base64 and sent to Claude's vision API
- Claude can read text, interpret graphs, charts, and visual data
- Supports common formats: PNG, JPG, JPEG, WebP, GIF

### PDF Documents
- Text is automatically extracted from PDFs
- Multi-page support with page markers
- Extracted text is analyzed by Claude

## Commands

### 1. Standalone Document Parsing

Use the `parse` command to analyze documents directly:

```bash
# Basic usage - auto-detect document type
./clinical parse labs.pdf

# Specify document type for better context
./clinical parse labs.pdf --type labs
./clinical parse xray-report.pdf --type imaging
./clinical parse consult-note.pdf --type consult

# Just extract text without interpretation
./clinical parse document.pdf --extract-only

# Ask specific questions
./clinical parse discharge-summary.pdf --question "What medications were prescribed?"
```

### 2. File Attachments with Other Commands

Attach files to any command that supports `--file` flag:

```bash
# CDS with lab results
./clinical cds --file labs.pdf
# Then enter clinical context when prompted

# Multiple files
./clinical cds --file labs.pdf --file chest-xray.png

# Note generation with attached documents
./clinical note --file consult-note.pdf --file labs.pdf
```

## Document Types

### Lab Results (`--type labs`)
Best for:
- Complete blood counts (CBC)
- Metabolic panels
- Urinalysis results
- Culture reports
- Any laboratory test results

Output includes:
- All test results with reference ranges
- Highlighted abnormal values
- Critical value flags
- Brief clinical interpretation

Example:
```bash
./clinical parse cbc-results.pdf --type labs
```

### Imaging Reports (`--type imaging`)
Best for:
- X-ray reports
- CT scan results
- MRI reports
- Ultrasound findings
- Any radiology/imaging reports

Output includes:
- Key findings section
- Impressions/conclusions
- Critical findings highlighted
- Comparison to prior studies

Example:
```bash
./clinical parse chest-xray.pdf --type imaging
```

### Consultation Notes (`--type consult`)
Best for:
- Specialist consultation reports
- Second opinion letters
- Interdisciplinary notes
- Referral responses

Output includes:
- Key recommendations
- Diagnosis and assessment
- Suggested workup/treatments
- Follow-up plans

Example:
```bash
./clinical parse cardiology-consult.pdf --type consult
```

### Medication Lists (`--type medication`)
Best for:
- Medication reconciliation lists
- Pharmacy printouts
- Medication administration records
- Prescription lists

Output includes:
- All medications with doses/frequencies
- New prescriptions or changes noted
- Potential interaction flags
- Concerns identified

Example:
```bash
./clinical parse med-list.pdf --type medication
```

### General Documents (`--type general`)
Best for:
- Discharge summaries
- Progress notes
- Mixed documents
- Any clinical document

Output includes:
- Key clinical information summary
- Diagnoses, problems, allergies
- Important dates and providers
- Action items and follow-up needs

Example:
```bash
./clinical parse discharge-summary.pdf --type general
```

## Use Cases

### 1. Quick Lab Review
```bash
# Patient texts you a photo of their lab results
./clinical parse ~/Downloads/lab-photo.jpg --type labs

# Get instant interpretation with abnormal values highlighted
```

### 2. Preparing for Patient Visit
```bash
# Parse consultation note before follow-up
./clinical parse specialist-note.pdf --type consult

# Extract key recommendations to discuss
```

### 3. Clinical Decision Support with Context
```bash
# Patient presents with chest pain, you have their recent ECG
./clinical cds --file ecg-screenshot.png --urgent

# Enter clinical presentation when prompted
# Claude analyzes both your description and the ECG
```

### 4. Multi-Document Analysis
```bash
# Analyze multiple test results together
./clinical parse labs.pdf imaging-report.pdf consult.pdf

# Get comprehensive summary of all documents
```

### 5. Specific Questions About Documents
```bash
# Quick queries about documents
./clinical parse discharge.pdf --question "What was the discharge diagnosis?"
./clinical parse labs.pdf --question "What was the hemoglobin level?"
./clinical parse imaging.pdf --question "Were there any critical findings?"
```

### 6. Text Extraction Only
```bash
# Just need the raw text from a PDF
./clinical parse document.pdf --extract-only > extracted.txt

# Useful for copying into EMR or other systems
```

## Tips and Best Practices

### Image Quality
- Use high-resolution screenshots (clear text)
- Ensure good lighting for photos of paper documents
- Crop to relevant content when possible
- Portrait orientation often works best

### PDF Files
- Searchable PDFs work best (not scanned images as PDF)
- For scanned PDFs, consider extracting pages as images
- Multi-page documents are fully supported

### File Naming
- Use descriptive filenames: `cbc-2025-01-09.pdf` not `file.pdf`
- Include dates when relevant
- Helps with organization and reference

### Privacy/Security
- Files are processed via Anthropic API under BAA
- No files are stored by the CLI tool
- Files remain on your local system
- Follow HIPAA guidelines for file storage

### Performance
- Large files may take longer to process
- Multiple small files faster than one large file
- PDFs with many pages: consider splitting if slow

### Combining with Text Input
All file commands still prompt for text input:
```bash
./clinical cds --file labs.pdf
# You'll still be prompted to enter clinical context
# Files supplement your description, not replace it
```

## Troubleshooting

### "File not found"
- Check file path is correct
- Use absolute path: `/Users/username/Downloads/file.pdf`
- Or relative path from CLI directory: `../../Downloads/file.pdf`

### "Invalid image file"
- Verify file is actually an image
- Try converting to PNG or JPG
- Check file isn't corrupted

### "No text could be extracted from PDF"
- PDF might be a scanned image
- Try using as image instead: convert PDF → PNG
- Or use `--extract-only` to see what's there

### "Unsupported file type"
Supported formats:
- Images: PNG, JPG, JPEG, WebP, GIF
- Documents: PDF only
- For other formats, convert first

### Poor OCR Results
- Improve image quality/resolution
- Ensure good contrast
- Try re-scanning or re-photographing
- Use original digital document when available

## Examples in Practice

### Scenario 1: Lab Results Review
```bash
# Patient emails you their lab results PDF
./clinical parse ~/Downloads/patient-labs-2025-01-09.pdf --type labs

# Output shows:
# - All values with reference ranges
# - Elevated WBC flagged
# - Low hemoglobin highlighted
# - Interpretation: "Possible anemia with leukocytosis..."
```

### Scenario 2: Imaging Interpretation Help
```bash
# Reviewing chest X-ray with clinical question
./clinical parse chest-xray.png --type imaging --question "Are there infiltrates?"

# Output focuses on infiltrates and provides interpretation
```

### Scenario 3: Comprehensive Case Review
```bash
# Complex patient with multiple recent tests
./clinical parse labs.pdf ecg.png chest-xray-report.pdf --type general

# Gets comprehensive synthesis of all documents
# Can then use for CDS or documentation
```

### Scenario 4: Prior Auth Documentation
```bash
# Need to write prior auth with supporting documentation
./clinical parse mri-report.pdf pt-notes.pdf

# Extract key findings
# Then use output to inform:
./clinical prior-auth --service "Physical therapy"
# Reference the extracted findings in your justification
```

## Advanced Usage

### Piping Output
```bash
# Extract and save to file
./clinical parse document.pdf --extract-only > extracted.txt

# Parse and copy directly to clipboard
./clinical parse labs.pdf | pbcopy
```

### Batch Processing (Future)
Currently you can process multiple files in one command:
```bash
./clinical parse file1.pdf file2.pdf file3.pdf
```

Future enhancement: process entire directories

### Integration with Workflow
```bash
# Example workflow script
#!/bin/bash
# Process today's lab results

LAB_FILE="$HOME/Documents/Labs/$(date +%Y-%m-%d)-labs.pdf"

if [ -f "$LAB_FILE" ]; then
    ~/clinical-cli/clinical parse "$LAB_FILE" --type labs > ~/Documents/Lab-Interpretations/$(date +%Y-%m-%d)-interpretation.md
fi
```

---

**Questions or Issues?**
- Check `./clinical parse --help` for options
- Review examples above
- Ensure files are in supported formats
- Verify ANTHROPIC_API_KEY is set correctly
