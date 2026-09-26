# Clinical CLI - Quick Reference Card

## 🚀 Start the Shell

```bash
cd /Users/dochobbs/consult/Claude/clinical-cli
./clinical-shell
```

## 📋 All Commands

| Command | Shortcut | What it does |
|---------|----------|--------------|
| **Drug Tools** |||
| `drug <name>` | `d` | Look up pediatric drug info |
| `dose <drug> <wt>` | - | Quick dose calculation |
| `compare <d1> <d2>` | - | Compare medications |
| **Clinical Tools** |||
| `cds <presentation>` | `c` | Clinical decision support |
| `ddx <presentation>` | - | Differential diagnosis |
| `note <info>` | - | Generate clinical note |
| `parse <file>` | - | Parse PDF/image |
| **Session** |||
| `stats` | `s` | Show session statistics |
| `model [name]` | - | List or switch models |
| **Other** |||
| `help` | `?` or `h` | Show help |
| `quit` | `q` | Exit shell |

## 💊 Drug Examples

```bash
⚕️  clinical> d amoxicillin --weight 52#              # Drug lookup with weight
⚕️  clinical> d amoxicillin --weight 52# --age 5yo    # With weight and age
⚕️  clinical> dose ibuprofen 40#                      # Quick dose
⚕️  clinical> compare amox cef                        # Compare options
```

## 🩺 Clinical Examples

```bash
⚕️  clinical> cds 5yo with fever x3 days, ear pain    # Clinical decision
⚕️  clinical> ddx 5yo with fever, ear pain            # Differential diagnosis
⚕️  clinical> note 5yo with AOM, starting amoxicillin # SOAP note
⚕️  clinical> note progress doing better              # Progress note
⚕️  clinical> parse ~/labs.pdf                        # Parse document
```

## 🔧 Model Selection Examples

```bash
⚕️  clinical> model                                   # List available models
⚕️  clinical> model llama3.2                          # Switch to local Ollama model
⚕️  clinical> model claude-sonnet-4-5-20250929        # Switch back to Claude
```

## 🎯 Common Workflows

### Workflow 1: Quick Drug Lookup
```bash
./clinical-shell
⚕️  clinical> dose amox 52#
⚕️  clinical> q
```

### Workflow 2: Patient Encounter
```bash
./clinical-shell
⚕️  clinical> d amoxicillin --weight 52# --age 5yo
⚕️  clinical> cds 5yo with fever x3 days, ear pain, decreased hearing
⚕️  clinical> note 5yo with AOM, starting amoxicillin 400mg/5ml
⚕️  clinical> q
```

### Workflow 3: All Day Clinic
```bash
./clinical-shell

# Patient 1
⚕️  clinical> d amox --weight 52#

# Patient 2
⚕️  clinical> d cefdinir --weight 30# --age 3yo

# Patient 3 - complex
⚕️  clinical> cds 12yo with headache, photophobia, neck stiffness
⚕️  clinical> ddx 12yo with headache, photophobia, neck stiffness
⚕️  clinical> note 12yo with concerning headache, recommend urgent evaluation

# Evening
⚕️  clinical> stats
⚕️  clinical> q
```

## ⚡ Pro Tips

1. **Leave shell running all day** - No startup delay
2. **Specify weight/age explicitly** - Safer than session state
3. **Use arrow keys** - Command history
4. **Tab completion** - Start typing, hit tab
5. **Ctrl+C** - Cancel current command
6. **Model selector** - Use local models when offline
7. **Single-line commands** - Fast and efficient

## 🎨 Weight Formats

All these work:
```bash
sw 52#
sw 52 lbs
sw 52 pounds
sw 23.5kg
sw 23.5 kg
sw 23.5 kilograms
```

## 📝 Note Types

```bash
note              # SOAP (default)
note progress     # Progress note
note consult      # Consultation
note procedure    # Procedure note
note discharge    # Discharge summary
```

## 🚨 Red Flags

CDS command auto-detects emergent indicators:
```bash
⚕️  clinical> cds
[2mo with high fever, lethargy...]

🚨 ALERT: Response includes emergent/urgent indicators
```

## 🎓 Session Statistics Example

```bash
⚕️  clinical> stats
┌─────────────────────────────┐
│ Session Statistics          │
├─────────────┬───────────────┤
│ Session uptime │ 0:15:32   │
│ Commands run   │ 8         │
└─────────────┴───────────────┘

⚕️  clinical> s               # Shortcut for stats
```

## 📚 More Help

- Type `?` or `help` in the shell
- See `INTERACTIVE_MODE_GUIDE.md`
- See `COMMANDS_REFERENCE.md`
- See `COMPLETE_SYSTEM_OVERVIEW.md`

## 🎉 You're Ready!

```bash
./clinical-shell
⚕️  clinical> help
```

---

**Print this page and keep it handy!**
