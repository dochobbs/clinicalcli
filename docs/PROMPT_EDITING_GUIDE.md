# Prompt Editing Guide - Surgical Prompt Modifications

## Overview

All AI behavior is now controlled by **editable markdown files** in the `prompts/` directory. You can modify these files directly to change how the tool behaves - no code changes needed!

## 📁 Prompt Files Location

```
clinical-cli/
└── prompts/
    ├── drug_lookup.md                    ← Edit drug command behavior
    ├── clinical_decision_support.md      ← Edit CDS command behavior
    ├── handout.md                        ← Edit handout generation
    ├── note.md                           ← Edit note generation
    ├── ddx.md                            ← Edit differential diagnosis
    └── parse.md                          ← Edit document parsing
```

## ✏️ How to Edit Prompts

### Step 1: Locate the File

```bash
cd /Users/dochobbs/consult/Claude/clinical-cli/prompts
ls -la
```

### Step 2: Open in Your Editor

```bash
# Use your preferred editor
code drug_lookup.md          # VS Code
vim drug_lookup.md           # Vim
nano drug_lookup.md          # Nano
open -a TextEdit drug_lookup.md  # TextEdit (macOS)
```

### Step 3: Make Changes

The prompts are structured markdown. Edit any section:

```markdown
## CRITICAL INSTRUCTIONS - ANTI-HALLUCINATION SAFEGUARDS

1. If you are UNCERTAIN about ANY information, explicitly state it
2. For pediatric dosing, ONLY provide ranges that are well-established
3. [ADD YOUR OWN INSTRUCTION HERE]
```

### Step 4: Save and Test

Changes take effect **immediately** on next command run:

```bash
# No restart needed - just run the command
./clinical drug amoxicillin --weight "52#"

# Your changes are now active!
```

## 🎯 Common Edits

### Add More Anti-Hallucination Checks

**File:** `prompts/drug_lookup.md`

**Find this section:**
```markdown
## CRITICAL INSTRUCTIONS - ANTI-HALLUCINATION SAFEGUARDS

1. If you are UNCERTAIN about ANY information, explicitly state it
2. For pediatric dosing, ONLY provide ranges that are well-established
```

**Add your own:**
```markdown
9. Never suggest a dose if you haven't cited a source
10. If conflicting sources exist, list ALL sources and explain the conflict
11. For any dose over X mg/kg/day, require explicit source citation
```

### Change Output Format

**File:** `prompts/drug_lookup.md`

**Find this section:**
```markdown
## Response Format

**DRUG NAME**
Generic: [name] | Brand: [name(s)]
```

**Modify to your preference:**
```markdown
**DRUG NAME**
- Generic: [name]
- Brand: [name(s)]
- FDA Approval Year: [year]
- Your custom field: [data]
```

### Add New Requirements

**File:** `prompts/clinical_decision_support.md`

**Find this section:**
```markdown
## CROSS-REFERENCING REQUIREMENTS

For all clinical recommendations:
1. **Cite specific guidelines:** Reference AAP, PIDS, CDC
```

**Add your requirements:**
```markdown
5. **Check UpToDate:** Verify recommendations match UpToDate (as of [date])
6. **Consider costs:** Note if recommended test/treatment is high-cost
7. **Your custom requirement:** [description]
```

### Adjust Tone or Style

**File:** Any prompt file

**Find descriptive sections and modify:**

Before:
```markdown
Be concise but thorough.
```

After:
```markdown
Be EXTREMELY detailed and explicit. Explain every recommendation.
Assume the provider is unfamiliar with pediatric dosing.
```

## 📊 Example: Adding Citation Requirements

### Goal
Make drug lookup require specific sources for every claim.

### Steps

1. **Open the file:**
   ```bash
   vim prompts/drug_lookup.md
   ```

2. **Find the section:**
   ```markdown
   ## CROSS-REFERENCING REQUIREMENTS
   ```

3. **Add strict rules:**
   ```markdown
   ## CROSS-REFERENCING REQUIREMENTS

   **MANDATORY CITATIONS:**
   - Every dosing range MUST cite: AAP Red Book, Lexicomp, OR package insert
   - Every safety warning MUST cite: FDA label OR pediatric guideline
   - Every formulation MUST be verified against: package insert OR pharmacy reference

   **FORMAT:**
   - Use [Source Year]: format
   - Example: "[AAP Red Book 2021]: 20-40 mg/kg/day for standard infections"

   **PENALTIES FOR MISSING CITATIONS:**
   - If you cannot cite a specific source, state: "SOURCE UNAVAILABLE - VERIFY INDEPENDENTLY"
   - Do NOT provide dosing without a source
   ```

4. **Save and test:**
   ```bash
   ./clinical drug amoxicillin --weight "52#"
   ```

5. **Verify it's working:**
   - Look for source citations in the output
   - Check if doses include source references
   - Confirm "SOURCE UNAVAILABLE" appears when appropriate

## 🔬 Example: Strengthening Anti-Hallucination

### Goal
Make CDS command more conservative and explicit about uncertainties.

### Steps

1. **Edit:**
   ```bash
   vim prompts/clinical_decision_support.md
   ```

2. **Find anti-hallucination section and enhance:**

   Before:
   ```markdown
   1. If you are UNCERTAIN about ANY clinical recommendation, explicitly state it
   ```

   After:
   ```markdown
   1. If you are UNCERTAIN about ANY clinical recommendation, you MUST:
      - State: "UNCERTAINTY: [specific area of uncertainty]"
      - Explain: "Limited because [reason]"
      - Recommend: "Consult [specific resource or specialist]"
      - NEVER guess or fill in gaps with assumptions

   2. For ANY recommendation, ask yourself:
      - Do I have a specific guideline supporting this? [If no → flag uncertainty]
      - Is this based on adult data applied to kids? [If yes → flag clearly]
      - Would I bet my license on this advice? [If no → don't give it]
   ```

3. **Add verification prompts:**
   ```markdown
   ## BEFORE FINALIZING YOUR RESPONSE - SELF-CHECK:

   1. Have I cited sources for every major recommendation? [ ]
   2. Have I flagged all uncertainties explicitly? [ ]
   3. Have I avoided "cookbook" advice without considering patient specifics? [ ]
   4. Have I noted when evidence is from adult populations? [ ]
   5. Have I avoided dosing specific enough to cause harm if wrong? [ ]

   If ANY checkbox is unchecked, revise your response.
   ```

## 📋 Prompt Sections Explained

### Section: CRITICAL INSTRUCTIONS
**Purpose:** Core rules the AI must follow
**Edit to:** Add/remove rules, change strictness
**Impact:** Changes fundamental AI behavior

### Section: CROSS-REFERENCING REQUIREMENTS
**Purpose:** What sources must be cited
**Edit to:** Require specific sources, add new sources
**Impact:** Changes what gets cited and how

### Section: SHOW YOUR WORK
**Purpose:** How to display calculations
**Edit to:** Change calculation format, add verification steps
**Impact:** Changes how doses/reasoning are shown

### Section: Response Format
**Purpose:** Structure of the output
**Edit to:** Reorder sections, add/remove fields
**Impact:** Changes what information appears and where

## 🎨 Advanced: Multiple Prompt Versions

You can maintain multiple versions of prompts:

```bash
# Save current version
cp prompts/drug_lookup.md prompts/drug_lookup_v1.md

# Create experimental version
cp prompts/drug_lookup.md prompts/drug_lookup_experimental.md
# Edit experimental version...

# Use experimental version by renaming
mv prompts/drug_lookup.md prompts/drug_lookup_production.md
mv prompts/drug_lookup_experimental.md prompts/drug_lookup.md

# Test experimental version
./clinical drug amoxicillin --weight "52#"

# Revert if needed
mv prompts/drug_lookup.md prompts/drug_lookup_experimental.md
mv prompts/drug_lookup_production.md prompts/drug_lookup.md
```

## 📝 Best Practices

### 1. Version Control Your Changes
```bash
# Before editing
git commit -am "Backup before prompt changes"

# After editing and testing
git commit -am "Updated drug prompt: added stricter source requirements"
```

### 2. Test Incrementally
- Make ONE change at a time
- Test with a known case
- Verify the change worked as expected
- Then make the next change

### 3. Document Your Intentions
Add comments in the markdown:
```markdown
<!-- EDITED 2025-01-09: Added requirement for explicit uncertainty flagging -->
<!-- REASON: Had cases where AI was overconfident about off-label uses -->

## CRITICAL INSTRUCTIONS
...
```

### 4. Keep a Change Log
Create `prompts/CHANGELOG.md`:
```markdown
# Prompt Change Log

## 2025-01-09
- **drug_lookup.md**: Added requirement for source citation on every dose
- **Reason**: Noticed occasional doses without clear sources
- **Test**: Verified with amoxicillin query - now shows "[AAP Red Book 2021]"

## 2025-01-08
- **clinical_decision_support.md**: Strengthened age-appropriateness checking
- **Reason**: Had one case suggesting adult condition in pediatric patient
- **Test**: Tested with various age groups - now correctly limits DDx by age
```

## 🔍 Troubleshooting

### "Changes don't seem to apply"
- Check you edited the right file in `prompts/`
- Check file was saved (look at timestamp)
- Try clearing any caching: just run command again
- Verify syntax is still valid markdown

### "Getting errors after editing"
- Check you didn't break markdown formatting
- Make sure you didn't delete required sections
- Look for unclosed code blocks or quotes
- Restore from git if needed: `git checkout prompts/drug_lookup.md`

### "Want to see what prompt is being used"
```python
# Add this to see loaded prompt
from prompt_loader import load_prompt
prompt = load_prompt("drug_lookup")
print(prompt[:500])  # First 500 chars
```

## 🚀 Quick Reference

| Task | Command |
|------|---------|
| List all prompts | `ls prompts/` |
| Edit drug prompt | `vim prompts/drug_lookup.md` |
| Edit CDS prompt | `vim prompts/clinical_decision_support.md` |
| Backup prompts | `cp -r prompts prompts_backup` |
| Test changes | `./clinical drug amoxicillin --weight "52#"` |
| Restore prompt | `git checkout prompts/drug_lookup.md` |

## 💡 Pro Tips

1. **Make prompts conversational**: Claude responds better to natural language
2. **Use examples**: Show what you want with examples in the prompt
3. **Be specific**: "Cite AAP Red Book" > "cite sources"
4. **Use formatting**: Bold, bullets, and headers make prompts clearer
5. **Test edge cases**: Try unusual inputs after prompt changes

## 📚 Examples of Effective Edits

### Example 1: Require Evidence Grading

Add to `clinical_decision_support.md`:
```markdown
**EVIDENCE GRADING REQUIRED:**
For every recommendation, append:
- [A] Strong evidence (RCTs, meta-analyses)
- [B] Moderate evidence (cohort studies)
- [C] Expert opinion only

Example: "Start amoxicillin 40mg/kg/day [A - AAP CPG 2022]"
```

### Example 2: Add Safety Checks

Add to `drug_lookup.md`:
```markdown
**PRE-OUTPUT SAFETY CHECK:**
Before providing dosing, ask yourself:
1. Is this dose higher than package insert max? [STOP if yes]
2. Is this based on adult dosing? [FLAG clearly if yes]
3. Am I 95%+ confident in this dose? [State uncertainty if no]
```

### Example 3: Simplify for Specific Use

If you mostly use for common infections:
```markdown
**STREAMLINED FOR COMMON INFECTIONS:**
- Focus on: amoxicillin, azithromycin, cefdinir
- Skip rare formulations
- Emphasize taste and adherence
- Highlight 10-day vs 5-day courses
```

---

**Remember:** The prompts are YOUR tool. Edit them to match YOUR practice style and safety requirements!

**Questions?** Check the loaded prompt:
```bash
./clinical drug --help  # See current behavior
cat prompts/drug_lookup.md  # See current prompt
```
