# Output Formats: Quick vs Full

**Clinical CLI now supports two output formats for faster, more efficient clinical workflows.**

---

## Overview

All major clinical commands now support two output formats:
- **`q` (Quick)** - Concise, essential information only (~100-200 words)
- **`f` (Full)** - Comprehensive, detailed information (default)

This gives you control over response length and detail level depending on your needs.

---

## Syntax

### Drug Lookup
```bash
d <drug> [q|f] [--weight WT] [--age AGE] [--indication IND]

# Examples
d amoxicillin q --weight 52# --age 5yo
d amoxicillin f --indication "strep throat"
d amoxicillin --weight 52#     # Defaults to full
```

### Clinical Decision Support
```bash
cds [q|f] <clinical presentation>

# Examples
cds q 5yo with fever x3 days, ear pain
cds f 5yo with fever x3 days, ear pain, decreased hearing
cds 5yo with fever              # Defaults to full
```

### Differential Diagnosis
```bash
ddx [q|f] <clinical presentation>

# Examples
ddx q 5yo with fever, ear pain
ddx f 12yo with headache, photophobia, neck stiffness
ddx 5yo with fever              # Defaults to full
```

### Clinical Notes
```bash
note [q|f] [type] <encounter info>

# Examples
note q 5yo with AOM, starting amoxicillin
note f progress doing better, fever resolved
note q discharge resolved AOM
note 5yo with AOM               # Defaults to full
```

---

## When to Use Quick Format

### ✅ Use Quick (`q`) When:
- **Fast scanning** - Need to review info quickly during busy clinic
- **Basic lookups** - Just need the essential dose or key recommendation
- **Quick reference** - Refreshing memory on familiar topics
- **Mobile use** - Smaller screen, want concise output
- **Time pressure** - Patient waiting, need answer fast

### Examples:
```bash
# Quick dose check during patient visit
⚕️  clinical> d amox q --weight 52#

Response:

# Amoxicillin - Quick Info

**Standard Dose:**
- 80-90 mg/kg/day divided BID
- For 23.6 kg: 530 mg BID
- Use 400 mg/5 mL suspension: 6.5 mL BID

**Indications:**
- Acute otitis media, strep throat, pneumonia

**Key Warnings:**
- Check penicillin allergy
- Risk of rash (5-10%)

[Total: ~100 words, easy to scan]
```

```bash
# Quick CDS check
⚕️  clinical> cds q 5yo with fever, ear pain

Response:

# Clinical Assessment [Quick]

**Assessment:** Likely acute otitis media (AOM)

**Top 3 Diagnoses:**
1. AOM (most likely)
2. Otitis externa
3. Viral URI with referred pain

**Plan:**
- Start high-dose amoxicillin
- Follow up if no improvement in 48-72 hours
- Red flags: lethargy, neck stiffness, bulging fontanel

[Total: ~80 words, actionable]
```

---

## When to Use Full Format

### ✅ Use Full (`f` or default) When:
- **Complex cases** - Need comprehensive information
- **Unfamiliar topics** - Want detailed explanation
- **Documentation** - Generating notes for EHR
- **Teaching** - Want full context and reasoning
- **Safety-critical** - Need all warnings and precautions
- **First-time lookup** - Learning about new drug/condition

### Examples:
```bash
# Comprehensive drug information
⚕️  clinical> d amoxicillin f --indication "strep throat"

Response:

# Amoxicillin - Pediatric Dosing

**Patient Information:**
Indication: Strep throat (Group A Streptococcal pharyngitis)

## Dosing for Strep Throat

**Standard Regimen:**
- Dose: 50 mg/kg/day (max 1000 mg/day)
- Frequency: Once daily OR 25 mg/kg BID (max 500 mg/dose)
- Duration: 10 days (full course essential)

**For 23.6 kg patient:**
- Single daily dose: 1180 mg → give 1200 mg daily
- OR divided: 590 mg BID → give 600 mg BID
- Using 400 mg/5 mL suspension: 15 mL daily OR 7.5 mL BID

## Pharmacology
Amoxicillin is a beta-lactam antibiotic...
[Continues with detailed pharmacology]

## Clinical Considerations
- First-line treatment for Group A Strep pharyngitis
- Excellent oral bioavailability (>90%)
- Food does not affect absorption
...

## Safety & Warnings
- Penicillin allergy: ABSOLUTE CONTRAINDICATION
- History of mononucleosis: May develop rash...
...

## Monitoring
- Clinical improvement expected in 24-48 hours
- Complete full 10-day course even if improved
...

[Total: 500-800 words, comprehensive]
```

---

## Comparison

| Aspect | Quick (`q`) | Full (`f` or default) |
|--------|-------------|----------------------|
| **Length** | ~100-200 words | ~500-1000 words |
| **Reading time** | 30-60 seconds | 2-5 minutes |
| **Use case** | Fast reference | Comprehensive info |
| **Detail level** | Essential only | Complete details |
| **Format** | Bullet points | Sections + explanations |
| **Best for** | Busy clinic | Learning, complex cases |

---

## Output Format Details

### Quick Format Features

**Drug Lookup (`d ... q`):**
- Standard dose only
- Key indication(s)
- Critical warnings only
- ~200 words max

**CDS (`cds q ...`):**
- Brief assessment (1-2 sentences)
- Top 3 differential diagnoses
- Key plan/recommendations only
- Red flags if applicable
- ~150 words max

**DDx (`ddx q ...`):**
- Top 5 diagnoses only
- Each with likelihood (common/uncommon/rare)
- ~100 words max

**Notes (`note q ...`):**
- Essential elements only
- Concise bullet points acceptable
- ~150 words max

### Full Format Features

**Drug Lookup (`d ... f`):**
- Comprehensive dosing for all indications
- Detailed pharmacology
- Complete safety profile
- Extensive precautions
- Drug interactions
- Monitoring parameters

**CDS (`cds f ...`):**
- Detailed assessment
- Complete differential diagnosis
- Comprehensive management plan
- Patient education points
- Follow-up recommendations
- Red flag discussion

**DDx (`ddx f ...`):**
- Extensive differential list
- Clinical features of each
- Diagnostic approach
- Risk stratification

**Notes (`note f ...`):**
- Complete SOAP or chosen format
- Full documentation
- All relevant details

---

## Tips for Efficient Use

### Start Quick, Go Full If Needed
```bash
# Quick check first
⚕️  clinical> cds q 5yo with fever, ear pain
[Review quick response]

# If you need more detail
⚕️  clinical> cds f 5yo with fever x3 days, ear pain, decreased hearing
[Get comprehensive assessment]
```

### Use Quick During Patient Visits
```bash
# In exam room with patient
⚕️  clinical> d amox q --weight 40#
[Quick scan: 530 mg BID, done in 30 seconds]
```

### Use Full for Documentation
```bash
# After patient leaves
⚕️  clinical> note f 5yo with AOM, starting high-dose amoxicillin
[Generate complete note for EHR]
⚕️  clinical> copy
[Paste into medical record]
```

### Default Behavior
```bash
# These are equivalent (both use full format)
⚕️  clinical> d amoxicillin --weight 52#
⚕️  clinical> d amoxicillin f --weight 52#
```

**Omitting the format flag defaults to full/comprehensive output.**

---

## Benefits

### Time Savings
- **Quick format:** Get essential info in 30-60 seconds
- **Full format:** Get comprehensive info in 2-5 minutes
- **Choose based on urgency:** Quick during patient care, full for complex cases

### Better Workflow
- **Scan quickly** during busy clinic hours
- **Deep dive** when you have time for learning
- **Copy exactly what you need** - not too much, not too little

### Reduced Cognitive Load
- **Quick format:** Easy to scan, key points only
- **Less scrolling** on small screens
- **Faster decision-making** with concise recommendations

---

## Real-World Examples

### Scenario 1: Busy Afternoon Clinic

**Patient 1** - 5yo with ear pain
```bash
⚕️  clinical> cds q 5yo with fever, ear pain
# Quick: AOM likely, start amoxicillin → 30 seconds
```

**Patient 2** - 8yo with cough
```bash
⚕️  clinical> d albuterol q --weight 60#
# Quick: 2 puffs q4-6h PRN → 20 seconds
```

**Patient 3** - Complex case with multiple complaints
```bash
⚕️  clinical> cds f 12yo with headache, fever, photophobia, neck pain
# Full: Need comprehensive assessment → 3 minutes, worth it
```

**Time saved:** ~5 minutes per simple patient × 10 patients = 50 minutes

### Scenario 2: Learning New Drug

**First time prescribing:**
```bash
⚕️  clinical> d cefdinir f --weight 45# --age 6yo
# Full: Learn everything about dosing, safety, monitoring
```

**Subsequent times:**
```bash
⚕️  clinical> d cefdinir q --weight 45#
# Quick: Just need the dose → much faster
```

### Scenario 3: Mobile/Small Screen

**On phone/tablet:**
```bash
⚕️  clinical> ddx q 5yo with fever, cough
# Quick: Top 5 diagnoses fit on one screen
# Full: Would require lots of scrolling
```

---

## Future Enhancements

Planned improvements:
- [ ] User preference to set default format (quick vs full)
- [ ] Ultra-quick format (single line output)
- [ ] Format persistence within session
- [ ] Custom format templates

---

## Summary

### Quick Format (`q`)
- ✅ Concise (100-200 words)
- ✅ Essential info only
- ✅ Fast to scan (30-60 seconds)
- ✅ Perfect for busy clinic
- ✅ Bullet points, key facts only

### Full Format (`f` or default)
- ✅ Comprehensive (500-1000 words)
- ✅ Complete details
- ✅ Thorough explanations (2-5 minutes)
- ✅ Perfect for learning, complex cases
- ✅ Organized sections with context

### Key Takeaway
**Use `q` for speed, use `f` (or omit) for depth.** The choice is yours based on your immediate needs.

---

## Commands Summary

| Command | Quick | Full | Default |
|---------|-------|------|---------|
| `d <drug> ...` | `d amox q --weight 52#` | `d amox f --weight 52#` | Full |
| `cds <presentation>` | `cds q 5yo fever` | `cds f 5yo fever` | Full |
| `ddx <presentation>` | `ddx q 5yo fever` | `ddx f 5yo fever` | Full |
| `note <info>` | `note q 5yo with AOM` | `note f 5yo with AOM` | Full |

**All commands default to full format if `q` or `f` is not specified.**

---

**Updated:** November 10, 2025
**Feature:** Quick/Full output formats
**Status:** ✅ Production ready
**Commands affected:** drug, cds, ddx, note
