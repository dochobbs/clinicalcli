# Clinical CLI - Commands Reference

## Two Modes of Operation

### 🚀 Interactive Shell (`./clinical-shell`) ⭐ RECOMMENDED
**Best for:** Daily clinic use, all clinical tasks

**Implements ALL commands:**
- ✅ Drug lookups with weight-based dosing
- ✅ Clinical decision support (CDS)
- ✅ Differential diagnosis (DDx)
- ✅ Clinical notes (SOAP, progress, consult, discharge)
- ✅ Document parsing (PDFs, images)
- ✅ Session state (remember weight/age)
- ✅ Quick dose calculations
- ✅ Drug comparisons

### 📋 Single Command Mode (`./clinical <command>`)
**Best for:** Scripting, one-off queries, handouts

**Also implements all 6 commands:**
- ✅ Drug, CDS, Handout, Note, DDx, Parse

---

## Interactive Shell Commands

When you run `./clinical-shell`, you have these commands available:

### Drug Lookup Commands

#### `drug <name>` or `d <name>`
Look up pediatric drug information
```bash
⚕️  clinical> d amoxicillin
⚕️  clinical> drug ibuprofen --weight 52#
⚕️  clinical> d amoxicillin --age 5yo --indication "otitis media"
```

#### `dose <drug> <weight>`
Quick dose calculation (fastest way!)
```bash
⚕️  clinical> dose amoxicillin 52#
⚕️  clinical> dose ibuprofen 25 lbs
⚕️  clinical> dose cefdinir 18kg
```

#### `compare <drug1> <drug2> [drug3]`
Side-by-side comparison
```bash
⚕️  clinical> compare amoxicillin cefdinir
⚕️  clinical> compare amoxicillin augmentin azithromycin
```

### Session Management Commands

#### `sw <weight>` or `set weight <weight>`
Set patient weight (remember for all queries)
```bash
⚕️  clinical> sw 52#
⚕️  clinical> sw 52 lbs
⚕️  clinical> sw 23.5kg
⚕️  clinical> set weight 40#
```

#### `sa <age>` or `set age <age>`
Set patient age
```bash
⚕️  clinical> sa 5yo
⚕️  clinical> sa 18mo
⚕️  clinical> set age 3yo
```

#### `state` or `s`
Show current session state
```bash
⚕️  clinical> s

┌─────────────────────────────────┐
│ Current Session State           │
├──────────────┬──────────────────┤
│ Weight       │ 52#              │
│ Age          │ 5yo              │
│ Last drug    │ amoxicillin      │
│ Session time │ 0:15:32          │
│ Commands run │ 8                │
└──────────────┴──────────────────┘
```

#### `clear`
Clear session state (for next patient)
```bash
⚕️  clinical> clear
Session state cleared
```

### Utility Commands

#### `help`, `h`, or `?`
Show help
```bash
⚕️  clinical> ?
⚕️  clinical> help
```

#### `quit`, `exit`, or `q`
Exit shell
```bash
⚕️  clinical> q
Goodbye! Stay safe.
```

### ✅ All Commands Now in Interactive Mode!

All commands are fully functional in the interactive shell. Commands that need longer input (CDS, DDx, note) use multiline mode:

```bash
⚕️  clinical> cds

═══ Clinical Decision Support ═══

Enter clinical presentation (Ctrl+D when done):

[Type your clinical information]
[Press Ctrl+D when done]
```

---

## Single Command Mode

For commands not in interactive shell, use single-command mode:

### Clinical Decision Support
```bash
./clinical cds --age "5yo" --urgent
./clinical cds --age "18mo"
```

### Patient Handouts
```bash
./clinical handout
# Then paste/type clinical information
```

### Clinical Notes
```bash
./clinical note
# Then paste/type encounter information
```

### Differential Diagnosis
```bash
./clinical ddx
# Then describe clinical presentation
```

### Parse Documents
```bash
./clinical parse labs.pdf
./clinical parse xray-screenshot.png
```

### Drug (also available)
```bash
./clinical drug amoxicillin --weight "52#" --age "5yo"
```

---

## Typical Workflow Examples

### Example 1: Quick Dose Check (Interactive)
```bash
./clinical-shell

⚕️  clinical> dose amox 52#
[Gets instant dose calculation]

⚕️  clinical> q
```

### Example 2: Full Patient Encounter (Interactive)
```bash
./clinical-shell

⚕️  clinical> sw 52#
✓ Session weight set: 52#

⚕️  clinical> sa 5yo
✓ Session age set: 5yo

⚕️  clinical> d amoxicillin
[Drug info with calculated dose]

⚕️  clinical> d ibuprofen
[Another drug, still using same weight]

⚕️  clinical> compare amoxicillin cefdinir
[Comparison of options]

⚕️  clinical> clear
Session state cleared

⚕️  clinical> q
```

### Example 3: All-Day Clinic (Interactive)
```bash
# Morning: Start once
./clinical-shell

# Patient 1: 5yo, 52 lbs
⚕️  clinical> sw 52#
⚕️  clinical> d amoxicillin
⚕️  clinical> clear

# Patient 2: 3yo, 30 lbs
⚕️  clinical> sw 30#
⚕️  clinical> d cefdinir
⚕️  clinical> clear

# Patient 3: Compare options
⚕️  clinical> dose ibuprofen 40#

# ... continue all day ...

# Evening
⚕️  clinical> q
```

### Example 4: CDS for Complex Case (Single Command)
```bash
./clinical cds --age "18mo" --urgent
# Then type symptoms/findings
# Press Ctrl+D when done
```

### Example 5: Parse Labs (Single Command)
```bash
./clinical parse ~/Desktop/cbc-results.pdf
```

---

## Command Shortcuts Reference

| Full Command | Shortcut | What it does |
|--------------|----------|--------------|
| `drug` | `d` | Drug lookup |
| `cds` | `c` | Clinical decision support (not in shell yet) |
| `dose` | - | Quick dose calc |
| `compare` | - | Compare drugs |
| `set weight` | `sw` | Set session weight |
| `set age` | `sa` | Set session age |
| `state` | `s` | Show session info |
| `help` | `h` or `?` | Show help |
| `quit` | `exit` or `q` | Exit |
| `clear` | - | Clear session |

---

## Pro Tips

### 1. Leave Shell Running All Day
```bash
# Start once in morning
./clinical-shell

# Keep it in a dedicated terminal tab
# Switch to it whenever you need dosing
```

### 2. Use Session State for Speed
```bash
# Set once per patient
sw 52#
sa 5yo

# Then rapid-fire queries
d amoxicillin
d ibuprofen
compare amox cef

# Clear for next patient
clear
```

### 3. Use History for Similar Patients
```bash
⚕️  clinical> d amoxicillin --weight 52#
[output]

# Next patient, press ↑ to recall
⚕️  clinical> d amoxicillin --weight 30#  # Just edit weight
```

### 4. Verify State Before Prescribing
```bash
⚕️  clinical> s          # Quick check
⚕️  clinical> d amox     # Make sure weight is correct!
```

### 5. Mix and Match Modes
```bash
# In one terminal: Interactive shell for drugs
./clinical-shell

# In another terminal: Single commands for other tasks
./clinical cds --age "5yo"
./clinical parse labs.pdf
```

---

## Summary

**Interactive Shell (`./clinical-shell`):** ⭐ **RECOMMENDED**
- ✅ Best for: ALL clinical tasks during clinic
- ✅ Fast: No startup delay, remembers weight/age
- ✅ Available: ALL commands (drug, cds, ddx, note, parse, dose, compare)
- ✅ Session memory: Set weight/age once
- ✅ Multiline input: Natural for clinical presentations

**Single Command Mode (`./clinical <cmd>`):**
- ✅ Best for: Scripting, automation, handouts
- ✅ Available: All 6 commands (drug, cds, handout, note, ddx, parse)
- ❌ Slower: Startup time per command
- ❌ No session memory: Must specify weight each time

**Recommendation:**
- **Use interactive shell** for 95% of clinical work
- **Use single commands** for scripting or generating handouts

---

**Ready to start?**
```bash
./clinical-shell

⚕️  clinical> help
```
