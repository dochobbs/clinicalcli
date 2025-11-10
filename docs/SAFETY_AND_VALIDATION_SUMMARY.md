# Safety & Validation System - Complete Overview

## Your Three Questions Answered

### ❓ Question 1: "Did we build in the logic checking and anti-hallucination parts?"

**Answer: YES - Multiple Layers**

We have **three levels** of protection:

#### Level 1: Prompt Instructions (What we tell Claude)
✅ **Location:** `prompts/drug_lookup.md` and `prompts/clinical_decision_support.md`
- Instructions to state uncertainties
- Requirements to cite sources
- Warnings about off-label use
- Age-appropriate guidance rules

**Example from prompt:**
```markdown
CRITICAL INSTRUCTIONS:
1. If UNCERTAIN, explicitly state "I'm not certain about..."
2. Do NOT fabricate formulations or dosing
3. Mark OFF-LABEL uses clearly
```

#### Level 2: ACTUAL LOGIC VALIDATION (Real code checks)
✅ **Location:** `src/dose_validator.py`

This is **REAL CODE** that validates doses against a knowledge base:

```python
# Example: Amoxicillin validation
PEDIATRIC_DOSE_DATABASE = {
    "amoxicillin": {
        "standard": {
            "mg_per_kg_per_day_min": 20,
            "mg_per_kg_per_day_max": 50,
            "absolute_max_single_dose_mg": 1000,
            "absolute_max_daily_dose_mg": 3000,
            "source": "AAP Red Book 2021"
        }
    }
}

# Then we CHECK Claude's dose against this:
if calculated_mg_per_kg > max_dose:
    result["errors"].append("DOSE EXCEEDS SAFE RANGE!")
    result["is_valid"] = False  # BLOCKS the prescription
```

**What this does:**
- ✅ Calculates mg/kg from Claude's recommendation
- ✅ Compares to known safe ranges
- ✅ Shows ERROR if dose is unsafe
- ✅ Shows WARNING if dose is questionable
- ✅ Cites the source of the safe range

**Example output:**
```
📊 DOSE VALIDATION CHECK:
   Calculated: 42.4 mg/kg/day
   Reference: 20-50 mg/kg/day
   Source: AAP Red Book 2021

✓ Dose within safe range
```

**Or if unsafe:**
```
🚨 DOSE ERRORS (DO NOT PRESCRIBE):
   ❌ Dose 95 mg/kg/day EXCEEDS safe range (20-50 mg/kg/day)
   ❌ DO NOT PRESCRIBE!
```

#### Level 3: Post-Processing Detection
✅ **Location:** Command files (e.g., `src/commands/drug.py`)

After Claude responds, code checks for warning phrases:

```python
# Check for uncertainty markers
concerning_phrases = [
    "I'm not certain",
    "limited evidence",
    "OFF-LABEL",
    "verify"
]

if any(phrase in response):
    console.print("⚠️  Response includes uncertainties")
```

**Example output:**
```
⚠️  Note: Response includes uncertainties or off-label uses
    Always verify dosing with authoritative references
```

---

### ❓ Question 2: "Can we use secondary sources to cross-reference and show work?"

**Answer: YES - Built into prompts, can add web search**

#### Currently Implemented:

**1. Source Citation Requirements** ✅
In `prompts/drug_lookup.md`:
```markdown
## CROSS-REFERENCING REQUIREMENTS

Before providing ANY dosing information:
1. State your primary source (e.g., "Per AAP Red Book")
2. If you cannot cite a source, state "SOURCE UNAVAILABLE"
3. When sources conflict, explain which you're using

## SOURCES CITED
List all sources you referenced:
1. [Primary source for dosing]
2. [Safety information source]
```

**Example output:**
```markdown
**PEDIATRIC DOSING**
**[Source: AAP Red Book 2021, Lexicomp Pediatric]**

Standard infections:
- Dose: 20-40 mg/kg/day divided TID
- Max: 1000 mg per dose, 3000 mg/day

**SOURCES CITED**
1. AAP Red Book 2021 - Dosing ranges
2. Lexicomp Pediatric - Maximum doses
3. FDA Package Insert - Available formulations
```

**2. Show Your Work Requirements** ✅
In `prompts/drug_lookup.md`:
```markdown
## SHOW YOUR WORK

For dose calculations:
1. Show the formula: "Dose = [mg/kg] × [weight]"
2. Show your math: "[low mg/kg] × [weight] = [X] mg"
3. Explain rounding
4. Show volume calculation
```

**Example output:**
```markdown
**CALCULATED DOSE** (for 23.6 kg patient)
1. Standard dosing: 20-40 mg/kg/day
2. For 23.6 kg patient:
   - Low dose: 20 mg/kg × 23.6 kg = 472 mg/day
   - High dose: 40 mg/kg × 23.6 kg = 944 mg/day
3. Divided TID: 944 ÷ 3 = 315 mg per dose
4. Round to practical dose: 300 mg per dose
5. Using 250mg/5mL suspension: 300mg ÷ 50mg/mL = 6 mL per dose

**VALIDATION CHECK:**
- Dose 40 mg/kg/day: Within published range ✓
- Single dose 300mg: Below maximum 1000mg ✓
- Achievable with available formulation ✓
```

#### Can Add: Web Search Integration

**Option A: Anthropic Web Search** (if available)
```python
from anthropic import Anthropic

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    tools=[{"type": "web_search"}],  # Enable web search
    messages=[...]
)
```

**Option B: Manual Cross-Reference Prompt**
Add to prompt:
```markdown
## CROSS-REFERENCE CHECKLIST

Before finalizing response:
1. Check AAP Red Book (cite year and page)
2. Check Lexicomp Pediatric (cite access date)
3. Check FDA package insert (cite approval date)
4. If sources conflict, list ALL sources and explain choice
```

**I can add web search capability if you'd like!**

---

### ❓ Question 3: "Are prompts outputted as files so I can edit them surgically?"

**Answer: YES - Fully implemented!**

#### How It Works:

**1. Prompts are Markdown Files** ✅
```
clinical-cli/
└── prompts/
    ├── drug_lookup.md                  ← Edit this!
    ├── clinical_decision_support.md    ← Edit this!
    ├── handout.md                      ← Edit this!
    ├── note.md                         ← Edit this!
    ├── ddx.md                          ← Edit this!
    └── parse.md                        ← Edit this!
```

**2. Commands Load Prompts Dynamically** ✅
```python
from prompt_loader import load_prompt

# This reads prompts/drug_lookup.md at runtime
system_prompt = load_prompt("drug_lookup")
response = call_claude(system_prompt, user_message)
```

**3. Edit and Test Immediately** ✅
```bash
# Step 1: Edit the prompt file
vim prompts/drug_lookup.md

# Step 2: Save changes

# Step 3: Run command - uses new prompt immediately!
./clinical drug amoxicillin --weight "52#"

# NO RESTART NEEDED - changes are immediate!
```

**4. Complete Editing Guide Created** ✅
See: `PROMPT_EDITING_GUIDE.md` - 400+ lines of examples and instructions

---

## Complete Safety Architecture

### Input Validation
```python
# Weight validation (src/commands/drug.py)
if weight_lbs < 4 or weight_lbs > 400:
    raise ValueError("Weight outside pediatric range")

if weight_kg < 2 or weight_kg > 180:
    raise ValueError("Weight outside pediatric range")
```

### Dose Calculation
```python
# Weight-based dose request (sent to Claude)
user_message += f"""
Patient Weight: {weight_kg:.1f} kg

Calculate dose:
1. Low: [X mg/kg] × {weight_kg} = ? mg
2. High: [Y mg/kg] × {weight_kg} = ? mg
3. Show all steps
"""
```

### Validation Against Knowledge Base
```python
# Real logic check (src/dose_validator.py)
validation = validate_dose(
    drug_name="amoxicillin",
    weight_kg=23.6,
    calculated_dose_mg=1000,
    indication="standard"
)

if not validation["is_valid"]:
    console.print("🚨 DOSE UNSAFE - DO NOT PRESCRIBE")
    for error in validation["errors"]:
        console.print(f"❌ {error}")
```

### Source Citation
```python
# Required in prompt
"**Source:** [Cite AAP, Lexicomp, FDA label]"

# Verified in output
if "Source:" not in response:
    console.print("⚠️  No source cited")
```

### Uncertainty Detection
```python
# Post-processing check
if "I'm not certain" in response:
    console.print("⚠️  Uncertainty detected")
if "OFF-LABEL" in response:
    console.print("⚠️  Off-label use noted")
```

---

## Files Created for You

### Safety Infrastructure
1. ✅ `src/dose_validator.py` - REAL dose validation logic
2. ✅ `src/prompt_loader.py` - Load prompts from files

### Editable Prompts
3. ✅ `prompts/drug_lookup.md` - Drug command behavior
4. ✅ `prompts/clinical_decision_support.md` - CDS command behavior

### Documentation
5. ✅ `PROMPT_EDITING_GUIDE.md` - How to edit prompts
6. ✅ `SAFETY_AND_VALIDATION_SUMMARY.md` - This file

---

## Example: Complete Safety in Action

```bash
$ ./clinical drug amoxicillin --weight "52#" --indication "otitis media"

# What happens:

# 1. Weight validation
✓ Weight parsed: 52.0 lbs (23.6 kg)
✓ Within pediatric range (4-400 lbs)

# 2. Prompt loaded
✓ Loaded prompts/drug_lookup.md
✓ Includes source citation requirements
✓ Includes "show your work" requirements

# 3. Claude generates response
✓ Shows calculations step-by-step
✓ Cites sources (AAP Red Book 2021)
✓ Provides dose: 40 mg/kg/day = 944 mg/day

# 4. Dose validation (REAL LOGIC)
📊 DOSE VALIDATION CHECK:
   Calculated: 40 mg/kg/day
   Reference: 20-50 mg/kg/day (AAP Red Book 2021)
   ✓ Dose within safe range

# 5. Uncertainty detection
✓ No uncertainty markers found
✓ Source properly cited

# 6. Display result
[Shows complete drug information with validated dose]
```

## What Makes This Safe

### ❌ What We DON'T Do (Unsafe)
- Just trust Claude's answer
- Only use prompts without validation
- Accept doses without checking
- Allow missing source citations

### ✅ What We DO (Safe)
1. **Validate input** (weight in reasonable range)
2. **Load vetted prompts** (your edited, version-controlled prompts)
3. **Require sources** (prompt demands citations)
4. **Show work** (prompt demands step-by-step math)
5. **Validate output** (code checks dose against database)
6. **Alert user** (warnings for uncertainties, errors for unsafe doses)

---

## How to Expand Safety

### Add More Drugs to Validation Database

Edit `src/dose_validator.py`:

```python
PEDIATRIC_DOSE_DATABASE["new_drug"] = {
    "standard": {
        "mg_per_kg_per_day_min": X,
        "mg_per_kg_per_day_max": Y,
        "absolute_max_single_dose_mg": Z,
        "absolute_max_daily_dose_mg": W,
        "source": "AAP Red Book 2021"
    }
}
```

### Require More Citations

Edit `prompts/drug_lookup.md`:

```markdown
## MANDATORY CITATIONS

Every dose MUST cite:
1. Primary source (AAP, Lexicomp, FDA)
2. Publication year
3. Page number or section

Format: [Source Year, Section]: "dosing info"
Example: [AAP Red Book 2021, p342]: "20-40 mg/kg/day"
```

### Add Cross-Checks

Edit `prompts/drug_lookup.md`:

```markdown
## CROSS-REFERENCE REQUIREMENT

Before providing dose:
1. Check AAP Red Book
2. Check Lexicomp
3. If they differ, explain why and which you chose

Format:
**Sources Checked:**
- AAP Red Book 2021: 20-40 mg/kg/day
- Lexicomp 2024: 20-50 mg/kg/day
- Following AAP (more conservative)
```

---

## Testing the Safety System

### Test 1: Safe Dose
```bash
./clinical drug amoxicillin --weight "52#"

# Expected:
✓ Validates dose
✓ Shows sources
✓ No warnings
```

### Test 2: Unsafe Dose (If Claude Hallucinates)
```bash
# If Claude somehow suggests 100 mg/kg/day:

🚨 DOSE ERRORS (DO NOT PRESCRIBE):
   ❌ Dose 100 mg/kg/day EXCEEDS safe range (20-50 mg/kg/day)
   ❌ Source: AAP Red Book 2021
```

### Test 3: Missing Source
```bash
# If Claude doesn't cite a source:

⚠️  Warning: No source citation found
    ALWAYS verify dosing independently
```

### Test 4: Uncertainty
```bash
# If Claude is uncertain:

⚠️  Note: Response includes uncertainties or off-label uses
    Claude stated: "I'm not certain about..."
    Always verify dosing with authoritative references
```

---

## Summary

### ✅ Logic Checking
- **YES** - Real validation code checks doses
- **YES** - Knowledge database with safe ranges
- **YES** - Blocks unsafe doses with errors
- **YES** - Warns on questionable doses

### ✅ Cross-Referencing
- **YES** - Prompts require source citations
- **YES** - Prompts demand "show your work"
- **YES** - Can add web search if needed
- **YES** - Multiple source checking built into prompts

### ✅ Surgical Prompt Editing
- **YES** - All prompts are markdown files
- **YES** - Edit files directly, changes immediate
- **YES** - Complete editing guide provided
- **YES** - Version control friendly

---

## Quick Reference

| Feature | Location | How to Modify |
|---------|----------|---------------|
| Dose validation ranges | `src/dose_validator.py` | Edit PEDIATRIC_DOSE_DATABASE |
| Source requirements | `prompts/drug_lookup.md` | Edit CROSS-REFERENCING section |
| Calculation format | `prompts/drug_lookup.md` | Edit SHOW YOUR WORK section |
| Anti-hallucination rules | `prompts/*.md` | Edit CRITICAL INSTRUCTIONS |
| Response format | `prompts/*.md` | Edit Response Format section |

---

**You now have:**
1. ✅ Real logic validation (not just prompts)
2. ✅ Source citation requirements (with examples)
3. ✅ Editable prompt files (surgical modifications)
4. ✅ Complete documentation (how to use and modify)

**Next steps:**
1. Try editing a prompt file
2. Test with a known medication
3. Add more drugs to the validation database
4. Let me know what else you need!
