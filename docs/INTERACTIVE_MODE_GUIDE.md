# Interactive Mode - Fast, Persistent Clinical CLI

## Overview

The interactive shell keeps the CLI running persistently for rapid-fire queries. No startup time, session memory, command history, and tab completion.

## 🚀 Quick Start

### Launch Interactive Shell
```bash
cd /Users/dochobbs/consult/Claude/clinical-cli
./clinical-shell
```

You'll see:
```
┌─────────────────────────────────────────────┐
│ Clinical CLI - Interactive Mode             │
│ Pediatric-focused clinical decision support │
│                                             │
│ Quick Commands:                             │
│   d amoxicillin      - Drug lookup          │
│   dose amox 52#      - Quick dose for weight│
│   sw 52#             - Set session weight   │
│   sa 5yo             - Set session age      │
│   compare amox cef   - Compare drugs        │
│   state or s         - Show session state   │
│   help or ?          - Full help            │
│   quit or q          - Exit                 │
└─────────────────────────────────────────────┘

⚠️  PHI Notice: Data sent to Anthropic under BAA

⚕️  clinical> _
```

## 💡 Speed Features

### 1. Session Memory
Set patient info ONCE, reuse for all commands:

```bash
⚕️  clinical> sw 52#
✓ Session weight set: 52#

⚕️  clinical> sa 5yo
✓ Session age set: 5yo

⚕️  clinical> d amoxicillin
# Uses 52# automatically!

⚕️  clinical> d ibuprofen
# Still uses 52# and 5yo!

⚕️  clinical> clear
Session state cleared

⚕️  clinical> sw 30#
# New patient, new weight
```

### 2. Quick Shortcuts
| Shortcut | Full Command | Example |
|----------|-------------|---------|
| `d` | `drug` | `d amoxicillin` |
| `sw` | `set weight` | `sw 52#` |
| `sa` | `set age` | `sa 5yo` |
| `s` | `state` | `s` |
| `h` or `?` | `help` | `?` |
| `q` | `quit` | `q` |

### 3. One-Line Quick Dose
```bash
⚕️  clinical> dose amox 52#
# Instantly calculates dose for amoxicillin at 52 pounds
```

### 4. Command History
- **Up Arrow** - Previous command
- **Down Arrow** - Next command
- **Ctrl+R** - Search history

```bash
⚕️  clinical> d amoxicillin --weight 52#
[...output...]

⚕️  clinical> ↑    # Shows: d amoxicillin --weight 52#
⚕️  clinical> d cefdinir --weight 52#   # Edit and run
```

### 5. Tab Completion
```bash
⚕️  clinical> d am<TAB>
# Completes common commands

⚕️  clinical> set w<TAB>
# Completes to "set weight"
```

### 6. Compare Drugs Instantly
```bash
⚕️  clinical> compare amoxicillin cefdinir azithromycin
# Side-by-side comparison
```

## 📋 Typical Workflow

### Morning Clinic Session

```bash
# Start shell once
./clinical-shell

# First patient: 5yo, 52 pounds
⚕️  clinical> sw 52#
⚕️  clinical> sa 5yo
⚕️  clinical> d amoxicillin
# [Review dosing]
⚕️  clinical> d ibuprofen
# [Review fever dosing]

# Next patient: 18mo, 25 pounds
⚕️  clinical> clear
⚕️  clinical> sw 25#
⚕️  clinical> sa 18mo
⚕️  clinical> d amoxicillin
# [Different dose for different weight]

# Compare options for next patient
⚕️  clinical> compare amoxicillin augmentin
# [Review comparison]

# Quick dose check
⚕️  clinical> dose azithromycin 40#
# [Fast calculation]

# End of clinic
⚕️  clinical> q
```

## 🎯 Common Commands

### Drug Lookup
```bash
# Basic lookup (uses session weight/age if set)
d amoxicillin

# With specific weight (overrides session)
d amoxicillin --weight 30#

# With indication
d amoxicillin --indication "otitis media"

# Full options
d amoxicillin --weight 52# --age 5yo --indication "strep"
```

### Quick Dose
```bash
# Fastest way to get dose
dose amox 52#
dose ibuprofen 25#
dose azithromycin 40 lbs
```

### Compare Medications
```bash
compare amoxicillin cefdinir
compare amox augmentin cefdinir
compare ibuprofen acetaminophen
```

### Session Management
```bash
# Set patient info
sw 52#                    # Set weight (pounds)
sw 23.5kg                 # Set weight (kilograms)
sa 5yo                    # Set age (years)
sa 18mo                   # Set age (months)

# View current session
s                         # or 'state'

# Clear for next patient
clear
```

### Help
```bash
?                         # Quick help
help                      # Detailed help
h                         # Also works
```

### Exit
```bash
q                         # Quit
quit                      # Also works
exit                      # Also works
Ctrl+D                    # Also works
```

## 🔥 Pro Tips

### 1. Keep It Running All Day
```bash
# Start at beginning of clinic
./clinical-shell

# Leave it running between patients
# Much faster than restarting each time

# Only quit at end of day
```

### 2. Use Session State for Each Patient
```bash
# Set weight/age at start of encounter
sw 52#
sa 5yo

# Run multiple queries
d amoxicillin
d ibuprofen
compare amox cefdinir

# Clear before next patient
clear
```

### 3. Command History is Your Friend
```bash
# Query for first patient
d amoxicillin --weight 52#

# Second patient, similar query
↑    # Recalls: d amoxicillin --weight 52#
     # Edit weight: d amoxicillin --weight 30#
```

### 4. Tab Completion for Speed
```bash
# Type partial command
d am<TAB>      # Completes or shows options
sw<TAB>        # Completes to "sw "
```

### 5. Quick Dose for Common Scenarios
```bash
# Just need a dose fast?
dose amox 52#
dose tylenol 40#
dose motrin 25#
```

### 6. State Command to Verify
```bash
# Did I set the weight?
s
# Shows current weight, age, session info
```

## 🆚 Interactive vs Single Commands

### Interactive Shell (Recommended for Clinic)
**Pros:**
- Stays running (no startup time)
- Session memory (set weight once)
- Command history
- Tab completion
- Faster workflow

**When to use:**
- During clinic sessions
- Multiple queries for same patient
- Comparing multiple options
- Rapid-fire queries

### Single Commands (Script/Quick Lookups)
**Pros:**
- One-off queries
- Scriptable
- Can redirect output

**When to use:**
- Single query needed
- Scripting workflows
- Saving output to files

```bash
# Single command mode
./clinical drug amoxicillin --weight "52#" > result.txt

# Interactive mode (preferred for clinic)
./clinical-shell
```

## 🛠️ Setup for Daily Use

### Option 1: Alias (Fastest Access)
Add to `~/.zshrc`:
```bash
alias clinic='cd /Users/dochobbs/consult/Claude/clinical-cli && ./clinical-shell'
```

Then from anywhere:
```bash
clinic
# Instantly starts interactive shell
```

### Option 2: Path (Run from Anywhere)
Add to `~/.zshrc`:
```bash
export PATH="$PATH:/Users/dochobbs/consult/Claude/clinical-cli"
```

Then from anywhere:
```bash
clinical-shell
```

### Option 3: Dedicated Terminal Tab
Keep a terminal tab open with the shell running all day:
- Tab 1: EMR
- Tab 2: Clinical shell (running)
- Tab 3: Other work

## 📊 Session State Details

The shell remembers:
- **Weight**: Patient weight in lbs or kg
- **Age**: Patient age (e.g., 5yo, 18mo)
- **Last drug**: Last medication queried
- **Session uptime**: How long shell has been running
- **Command count**: Number of commands run this session

View anytime with:
```bash
⚕️  clinical> s

┌─────────────────────────────────┐
│ Current Session State           │
├──────────────┬──────────────────┤
│ Weight       │ 52#              │
│ Age          │ 5yo              │
│ Last drug    │ amoxicillin      │
│ Session time │ 2:34:15          │
│ Commands run │ 47               │
└──────────────┴──────────────────┘
```

## 🎓 Learning Path

### Day 1: Basic Usage
```bash
./clinical-shell
sw 52#
d amoxicillin
q
```

### Day 2: Session State
```bash
./clinical-shell
sw 52#
sa 5yo
d amoxicillin
d ibuprofen
clear
sw 30#
```

### Day 3: Shortcuts
```bash
./clinical-shell
sw 52#
d amox        # Shortcut for drug
s             # Shortcut for state
?             # Shortcut for help
```

### Day 4: Full Workflow
```bash
# Keep running all clinic
./clinical-shell

# Use for every patient
# Set weight → Query → Clear → Repeat
```

## 🐛 Troubleshooting

### Shell Won't Start
```bash
# Check API key
echo $ANTHROPIC_API_KEY

# Activate venv manually
cd /Users/dochobbs/consult/Claude/clinical-cli
source .venv/bin/activate
python src/interactive.py
```

### Commands Not Working
```bash
# Type 'help' to see available commands
help

# Make sure you're in interactive mode
# (Prompt should show: ⚕️  clinical>)
```

### Want to Cancel Current Command
```bash
# Press Ctrl+C
# Returns to prompt
```

### Tab Completion Not Working
```bash
# Make sure prompt_toolkit is installed
pip install prompt-toolkit

# Or reinstall requirements
pip install -r requirements.txt
```

### History Not Saving
```bash
# History saves to ~/.clinical_cli_history
# Check if file exists and is writable
ls -la ~/.clinical_cli_history
```

## 📝 Comparison: Before & After

### Before (Single Command Mode)
```bash
$ ./clinical drug amoxicillin --weight "52#"
[...startup time...]
[...HIPAA warning...]
[...output...]

$ ./clinical drug ibuprofen --weight "52#"
[...startup time again...]
[...HIPAA warning again...]
[...output...]

# Slow: Startup + warning every time
# Tedious: Type weight every time
```

### After (Interactive Mode)
```bash
$ ./clinical-shell
[...one-time startup...]
[...one-time HIPAA warning...]

⚕️  clinical> sw 52#
✓ Session weight set

⚕️  clinical> d amoxicillin
[...instant output...]

⚕️  clinical> d ibuprofen
[...instant output...]

# Fast: No repeated startup
# Easy: Weight remembered
# Efficient: One warning per session
```

## 🎉 Benefits Summary

✅ **Faster**: No startup time between queries
✅ **Smarter**: Remembers patient info
✅ **Easier**: Shortcuts and tab completion
✅ **Better**: Command history and recall
✅ **Cleaner**: One HIPAA notice per session
✅ **Professional**: Persistent tool like a medical calculator

---

**Ready to try it?**
```bash
cd /Users/dochobbs/consult/Claude/clinical-cli
./clinical-shell

# Your first command:
⚕️  clinical> help
```

**Add to daily workflow:**
```bash
# Add to ~/.zshrc:
alias clinic='cd /path/to/clinical-cli && ./clinical-shell'

# Then just type:
clinic
```

Enjoy your fast, persistent clinical assistant!
