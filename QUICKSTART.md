# Clinical CLI - Quick Start Guide

## 5-Minute Setup

### Step 1: Run Setup Script
```bash
cd /Users/dochobbs/Downloads/Consult/Claude/clinical-cli
./setup.sh
```

This will:
- Create virtual environment
- Install all dependencies
- Verify your API key
- Make scripts executable

### Step 2: Test Installation
```bash
source .venv/bin/activate
python src/cli.py --help
```

You should see a list of available commands.

### Step 3: Run Your First Command
```bash
python src/cli.py cds --help
```

## Quick Command Reference

### Using Python Directly
```bash
# Always activate venv first
source .venv/bin/activate

# Run commands
python src/cli.py cds
python src/cli.py note
python src/cli.py handout --condition "diabetes"
```

### Using the Wrapper Script
```bash
# Run without activating venv manually
./clinical cds
./clinical note --type consult
./clinical prior-auth --urgent
```

### Using an Alias (Recommended)
Add to your `~/.zshrc`:
```bash
alias clinical='cd /Users/dochobbs/Downloads/Consult/Claude/clinical-cli && source .venv/bin/activate && python src/cli.py'
```

Then from anywhere:
```bash
clinical cds
clinical note
clinical handout --condition "asthma"
```

## Common Workflows

### 1. Get Clinical Decision Support
```bash
./clinical cds
# Enter your clinical case when prompted
# Press Ctrl+D when done
# Review recommendations
# Copy to clipboard (y/n)
```

### 2. Generate a SOAP Note
```bash
./clinical note
# Paste/type your encounter notes
# Press Ctrl+D
# Get formatted SOAP note
# Copy to EMR
```

### 3. Create Patient Handout
```bash
./clinical handout --condition "URI management"
# Add any specific points when prompted
# Get patient-friendly handout
# Print or send to patient
```

### 4. Write Prior Auth Letter
```bash
./clinical prior-auth --service "Physical therapy" --urgent
# Enter clinical justification
# Get compelling medical necessity letter
# Submit to insurance
```

### 5. Look Up Drug Information
```bash
./clinical drug lisinopril
# Get comprehensive drug info
# Forms, dosing, cost, instructions
# Ready for prescribing or patient counseling
```

### 6. Compare Medication Options
```bash
./clinical drug sertraline fluoxetine --compare
# See side-by-side comparison
# Dosing, cost, differences
# Make informed choice
```

## Tips

### Input Methods
- **Type directly**: Enter information line by line
- **Paste**: Copy from EMR and paste (Cmd+V)
- **Mix both**: Type some, paste some
- **Finish**: Ctrl+D (macOS/Linux) or Ctrl+Z (Windows)

### Output Options
- **View**: Results display in formatted panels
- **Copy**: Auto-offers to copy to clipboard
- **Save**: Redirect output to file: `./clinical note > note.txt`

### Specialty Contexts
Many commands support specialty flags:
```bash
./clinical cds --specialty pediatrics
./clinical note --specialty cardiology
./clinical referral --specialty orthopedics
```

### Urgency Flags
Mark urgent cases:
```bash
./clinical cds --urgent
./clinical prior-auth --urgent
./clinical referral --urgent
```

## Troubleshooting

### "Command not found: clinical"
- Make sure you're in the right directory
- Or use the full path: `/Users/dochobbs/Downloads/Consult/Claude/clinical-cli/clinical`
- Or set up the alias in ~/.zshrc

### "Module not found"
- Activate virtual environment: `source .venv/bin/activate`
- Or use the wrapper: `./clinical`

### "ANTHROPIC_API_KEY not found"
```bash
# Check if it's set
echo $ANTHROPIC_API_KEY

# If empty, verify in ~/.zshrc
cat ~/.zshrc | grep ANTHROPIC_API_KEY

# Reload shell config
source ~/.zshrc
```

### Clipboard not working
- Just select "n" when asked to copy
- Manually copy from terminal output
- Or pipe to pbcopy: `./clinical note | pbcopy`

## Next Steps

1. **Test each command** to understand capabilities
2. **Customize system prompts** in `src/commands/*.py` if needed
3. **Add to PATH** for system-wide access (optional)
4. **Create favorites** - save common command sequences

## Example Session

```bash
# Start in project directory
cd /Users/dochobbs/Downloads/Consult/Claude/clinical-cli

# Generate DDx for a case
./clinical ddx --system cardiac --age "65 year old"
# Enter: "Chest pain, SOB, diaphoresis, started 2 hours ago..."
# Ctrl+D
# Review differential and workup suggestions

# Create SOAP note
./clinical note --billing
# Enter encounter details
# Ctrl+D
# Copy formatted note to EMR

# Generate patient handout
./clinical handout --condition "chest pain" --reading-level simple
# Get patient education material
# Print for patient

# Done!
```

## All Available Commands

| Command | Purpose | Common Flags |
|---------|---------|--------------|
| `cds` | Clinical decision support | `--specialty`, `--urgent`, `--file` |
| `note` | Clinical documentation | `--type`, `--specialty`, `--billing` |
| `handout` | Patient education | `--condition`, `--reading-level`, `--language` |
| `prior-auth` | Prior authorization | `--service`, `--urgent`, `--appeal` |
| `referral` | Referral letters | `--specialty`, `--urgent` |
| `ddx` | Differential diagnosis | `--system`, `--age`, `--broad` |
| `parse` | Parse documents (PDF, images) | `--type`, `--question`, `--extract-only` |
| `drug` | **NEW** Drug information & cost | `--compare`, `--pediatric`, `--generic-only`, `--question` |

### File Attachment Support
Many commands now support `--file` or `-f` to attach screenshots or PDFs:
```bash
# Parse standalone document
./clinical parse labs.pdf

# Attach to CDS query
./clinical cds --file labs.pdf --file xray.png

# Parse multiple documents at once
./clinical parse report1.pdf report2.pdf --type imaging
```

For detailed help on any command:
```bash
./clinical <command> --help
```

---

**Ready to start?** Run `./setup.sh` and try your first command!
