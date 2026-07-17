# Clinical CLI - Pediatric Clinical Decision Support Tool

**Fast, interactive AI-powered clinical decision support for pediatric care.**

[![Version](https://img.shields.io/badge/version-1.3.0-blue.svg)](https://github.com/dochobbs/clinicalcli)
[![Python](https://img.shields.io/badge/python-3.9+-green.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Internal-red.svg)](LICENSE)

---

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/dochobbs/clinicalcli.git
cd clinicalcli
./setup.sh

# Start interactive shell
./clinical-shell

# Try it out!
⚕️  clinical> d amoxicillin --weight 52# --age 5yo
⚕️  clinical> cds 5yo with fever x3 days, ear pain
⚕️  clinical> help
```

**That's it!** Responses stream in real-time. ⚡

---

## ✨ Key Features

### 🎯 Interactive Shell Mode
- **Real-time streaming responses** - See results immediately (200-500ms)
- **Single-line commands** - Fast, natural workflow
- **Tab completion** - Quick command entry
- **Command history** - Arrow keys to recall
- **Copy on demand** - `copy` command when you need it

### 💊 Clinical Commands
- **`drug`** / **`d`** - Drug lookup with weight-based dosing
- **`dose`** - Quick dose calculation
- **`compare`** - Compare multiple medications
- **`cds`** / **`c`** - Clinical decision support with red flag detection
- **`ddx`** - Differential diagnosis generation
- **`note`** - Clinical notes (SOAP, progress, consult, discharge)
- **`parse`** - Analyze PDF/image documents

### 🤖 AI Model Support
- **Default:** Claude Haiku 4.5 (1-2 sec, optimized for speed) ⚡
- **Quality:** Claude Sonnet 4.5 (2-5 sec, best for complex cases)
- **OpenAI:** GPT-5.1 with streamed interactive text responses
- **Offline:** LM Studio and Ollama for local models
- **Easy switching:** `model gpt-5.1`, `model llama3.2`, or `model claude-sonnet-4-5-20250929`

### 🛡️ Safety Features
- **3-layer dosing validation** - Weight, age, and range checking
- **Red flag detection** - Emergent condition identification
- **Anti-hallucination prompts** - Source citation requirements
- **Session isolation** - No cross-patient data retention

---

## 📖 Documentation

**Start here:** [docs/README.md](docs/README.md)

### Quick Links
- **[Quick Start Guide](docs/QUICKSTART.md)** - 5 minutes to get running
- **[Interactive Shell Guide](docs/INTERACTIVE_MODE_GUIDE.md)** - Complete shell reference
- **[Command Reference](docs/COMMANDS_REFERENCE.md)** - All available commands
- **[Performance Guide](docs/PERFORMANCE_UPDATES.md)** - Speed optimization tips

See full documentation in [`docs/`](docs/) directory.

---

## 💡 Usage Examples

### Drug Lookup with Dosing
```bash
⚕️  clinical> d amoxicillin --weight 52# --age 5yo

Response:

# Amoxicillin - Pediatric Dosing
**Patient:** 52 lbs (23.6 kg), 5 years old

## Standard Dosing for Acute Otitis Media
- Dose: 80-90 mg/kg/day divided BID
- Calculation: 23.6 kg × 45 mg/kg = 1062 mg/day
- Give: 530 mg BID (use 400 mg/5 mL suspension)
- Volume: 6.5 mL BID

[Full response continues streaming...]

Tip: Use 'copy' command to copy this to clipboard
```

### Clinical Decision Support
```bash
⚕️  clinical> cds 5yo with fever x3 days, ear pain, decreased hearing

Response:

# Clinical Assessment: Acute Otitis Media (AOM)

## Key Features
This 5-year-old with fever, ear pain, and decreased hearing...
[Comprehensive assessment streams in real-time]

⚕️  clinical> copy
✓ Copied 2103 characters to clipboard
```

### Quick Dose Calculation
```bash
⚕️  clinical> dose ibuprofen 40#

Response:
# Ibuprofen - Quick Dose
- Weight: 40 lbs (18.2 kg)
- Dose: 10 mg/kg = 182 mg
- Give: 9 mL of 100 mg/5 mL suspension
- Frequency: Every 6-8 hours PRN
```

### Switch Models
```bash
⚕️  clinical> model
═══ Available Models ═══

Anthropic Claude (Cloud):
  [✓] claude-haiku-4-5-20251001    # Default, fast
  [ ] claude-sonnet-4-5-20250929   # Best quality

OpenAI (Cloud):
  [ ] gpt-5.1

⚕️  clinical> model claude-sonnet-4-5-20250929
✓ Switched to Anthropic model: claude-sonnet-4-5-20250929
```

---

## 🎨 Why This Tool?

### Speed
- ⚡ **Streaming responses** - Start reading in 200ms
- ⚡ **Claude Haiku 4.5 default** - 1-2 second responses
- ⚡ **Single-line commands** - No Ctrl+D needed

### User Experience
- ✅ **No interruptions** - Copy only when you want
- ✅ **Natural workflow** - Like talking to a colleague
- ✅ **Rich formatting** - Clear, readable output
- ✅ **Tab completion** - Fast command entry

### Clinical Focus
- 🎯 **Pediatric-optimized** - Weight-based dosing, age-appropriate guidance
- 🎯 **Safety-first** - Multiple validation layers
- 🎯 **Red flag detection** - Critical condition alerts
- 🎯 **Evidence-based** - Source citation requirements

---

## 📋 Requirements

- **Python:** 3.9 or higher
- **Cloud API key:** Set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` for the corresponding provider
- **Optional:** LM Studio or Ollama for offline local models without a cloud key
- **Platforms:** macOS, Linux, Windows

---

## 🔧 Installation

### Automated Setup (Recommended)
```bash
git clone https://github.com/dochobbs/clinicalcli.git
cd clinicalcli
./setup.sh
```

### Manual Setup
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Set the key for the cloud provider you intend to use
export ANTHROPIC_API_KEY="your-api-key-here"
# or: export OPENAI_API_KEY="your-api-key-here"
```

### Verify Installation
```bash
./clinical-shell
⚕️  clinical> help
```

---

## 🎯 Common Workflows

### Quick Drug Lookup
```bash
./clinical-shell
⚕️  clinical> dose amox 52#
⚕️  clinical> q
```
**Time:** ~10 seconds

### Complete Patient Assessment
```bash
./clinical-shell
⚕️  clinical> d amoxicillin --weight 52# --age 5yo
⚕️  clinical> cds 5yo with fever x3 days, ear pain, decreased hearing
⚕️  clinical> note 5yo with AOM, starting amoxicillin
⚕️  clinical> copy
⚕️  clinical> q
```
**Time:** ~2 minutes

### All-Day Clinic Session
```bash
./clinical-shell
# Leave running all day
⚕️  clinical> d amox --weight 52#      # Patient 1
⚕️  clinical> d cefdinir --weight 30#  # Patient 2
⚕️  clinical> cds 12yo with headache...
⚕️  clinical> stats                     # Check session stats
⚕️  clinical> q
```

---

## 🚨 HIPAA Compliance

⚠️ **Protected Health Information (PHI) Warning**

- ✅ **BAA Required** - Use PHI only with a selected cloud provider covered by an applicable Business Associate Agreement
- ✅ **Authorized Use** - Ensure proper authorization for PHI processing
- ✅ **Secure Handling** - Do not share outputs containing PHI insecurely
- ✅ **Audit Trail** - Session logs available via `stats` command
- ✅ **Session Isolation** - No data persists between sessions

**This tool does not make a deployment HIPAA compliant by itself. Use only in an organizationally approved environment with the selected provider, data controls, and applicable agreements reviewed.**

---

## 📊 Performance

### Response Times

| Model | Speed | Quality | Use Case |
|-------|-------|---------|----------|
| **Claude Haiku 4.5** (default) | 1-2 sec ⚡⚡⚡ | Excellent | Quick lookups, routine queries |
| **Claude Sonnet 4.5** | 2-5 sec ⚡⚡ | Outstanding | Complex cases, critical decisions |
| **OpenAI GPT-5.1** | Varies | Advanced | Interactive text workflows |
| **Local Models** (offline) | 30-60 sec ⚠️ | Good | Emergency offline reference |

**Streaming:** First words appear in ~200-500ms regardless of model!

---

## 🔄 Model Management

### Available Models

**Cloud (Anthropic) - Recommended:**
- `claude-haiku-4-5-20251001` - Default, optimized for speed
- `claude-sonnet-4-5-20250929` - Best quality for complex cases

**Cloud (OpenAI):**
- `gpt-5.1` - Streamed interactive text responses

**Local (Offline):**
- LM Studio - User-friendly GUI, any GGUF model
- Ollama - CLI-based, scriptable

### Switching Models
```bash
⚕️  clinical> model                            # List available
⚕️  clinical> model claude-sonnet-4-5-20250929 # Switch to Sonnet
⚕️  clinical> model gpt-5.1                    # Switch to OpenAI
⚕️  clinical> model llama3.2                   # Switch to Ollama (if running)
```

See [Model Selection Guide](docs/SINGLE_LINE_AND_MODEL_SELECTOR.md) for details.

---

## 🛠️ Development

### Project Structure
```
clinicalcli/
├── src/
│   ├── cli.py              # Single-command CLI
│   ├── interactive.py      # Interactive shell (main)
│   ├── model_manager.py    # Multi-model support
│   ├── utils.py            # Shared utilities
│   ├── dose_validator.py   # Safety validation
│   └── commands/           # Command modules
├── prompts/                # System prompts
├── docs/                   # Documentation
├── requirements.txt        # Dependencies
└── clinical-shell          # Interactive launcher
```

### Adding Features
See [Development Guide](docs/DEVELOPMENT.md) (coming soon)

---

## 🐛 Troubleshooting

### API Key Issues
```bash
# Check if set
echo $ANTHROPIC_API_KEY
echo $OPENAI_API_KEY

# If empty, add to ~/.zshrc
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.zshrc
# or: echo 'export OPENAI_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### Import Errors
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Slow Performance
- **Use Haiku** (default) - 2-3x faster than Sonnet
- **Local models are slow** - See [Performance Guide](docs/LOCAL_MODEL_PERFORMANCE.md)
- **Check internet connection** - Cloud models require connectivity

### Command Not Found
```bash
# Make shell executable
chmod +x clinical-shell

# Or run directly
python -m src.interactive
```

---

## 🗺️ Roadmap

### Current Version: 1.3.0
- ✅ Interactive shell mode
- ✅ Streaming responses
- ✅ Multi-model support (Claude, OpenAI, LM Studio, Ollama)
- ✅ Copy on demand
- ✅ Comprehensive documentation

### Planned Features
- [ ] Response caching for offline access
- [ ] Custom prompt templates
- [ ] Batch processing mode
- [ ] Integration with EHR systems
- [ ] Extended local model optimization
- [ ] Multi-language support

See [ROADMAP.md](docs/ROADMAP.md) for detailed plans (coming soon).

---

## 📝 License

**Internal Use Only** - PHI processing requires organizational approval and an applicable agreement with the selected cloud provider.

---

## 🙏 Acknowledgments

- **Anthropic** - Claude AI models and API
- **OpenAI** - GPT models through the OpenAI API
- **Rich** - Beautiful terminal formatting
- **Prompt Toolkit** - Interactive shell features

---

## 📞 Support

### Documentation
- **Quick Start:** [docs/QUICKSTART.md](docs/QUICKSTART.md)
- **Full Docs:** [docs/README.md](docs/README.md)
- **In-app Help:** `⚕️  clinical> help`

### Issues
Report issues at: https://github.com/dochobbs/clinicalcli/issues

---

**Version:** 1.3.0
**Last Updated:** November 9, 2025
**Default Model:** Claude Haiku 4.5 (fast!)
**Status:** Production Ready ✅

---

## ⭐ Quick Command Reference

```bash
# Interactive Shell
./clinical-shell           # Start shell

# Drug Commands
d <drug> --weight <wt>     # Drug lookup with dosing
dose <drug> <weight>       # Quick dose
compare <d1> <d2>          # Compare drugs

# Clinical Commands
cds <presentation>         # Clinical decision support
ddx <presentation>         # Differential diagnosis
note <info>                # Generate note
parse <file>               # Analyze document

# Utilities
copy                       # Copy last output
model                      # List/switch models
stats                      # Session statistics
help                       # Show help
quit                       # Exit

# Examples
d amoxicillin --weight 52# --age 5yo
cds 5yo with fever, ear pain
note 5yo with AOM, starting antibiotics
copy
```

**Get started in 5 minutes:** [Quick Start Guide](docs/QUICKSTART.md)
