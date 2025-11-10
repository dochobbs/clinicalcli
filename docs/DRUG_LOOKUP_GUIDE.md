# Drug Lookup Guide

## Overview

The `drug` command provides comprehensive medication information focused on practical prescribing needs:
- **Available dosing forms** - All formulations and strengths
- **Patient instructions** - How to take, what to expect, what to avoid
- **Cost information** - Generic vs brand pricing, cost-saving tips
- **Standard dosing** - Adult and pediatric doses
- **Safety information** - Warnings, interactions, side effects

## Basic Usage

### Simple Drug Lookup
```bash
./clinical drug lisinopril
```

**Output includes:**
- Generic and brand names
- All available forms (tablets, capsules, liquid, etc.)
- Standard adult dosing
- Pediatric dosing (if applicable)
- Patient instructions
- Cost comparison (generic vs brand)
- Key safety information
- Clinical pearls

### With Drug Name Argument
```bash
# Single word drug names
./clinical drug metformin

# Multi-word or specific forms (use quotes)
./clinical drug "amoxicillin suspension"
./clinical drug "albuterol inhaler"
```

### Without Argument (Interactive)
```bash
./clinical drug
# You'll be prompted: "Enter drug name(s):"
```

## Advanced Features

### 1. Compare Multiple Drugs

Compare drugs side-by-side (great for choosing between options):

```bash
# Compare SSRIs
./clinical drug sertraline fluoxetine escitalopram --compare

# Compare ACE inhibitors
./clinical drug lisinopril enalapril ramipril --compare

# Compare antibiotics
./clinical drug amoxicillin cephalexin --compare
```

**Comparison includes:**
- Forms and strengths side-by-side
- Dosing differences
- Cost comparison
- Key differentiating features
- When to choose one over another

### 2. Indication-Specific Information

Get dosing for specific conditions:

```bash
# Diabetes medication
./clinical drug metformin --indication "type 2 diabetes"

# Antihypertensive
./clinical drug lisinopril --indication "hypertension"

# Antibiotic for specific infection
./clinical drug azithromycin --indication "community-acquired pneumonia"
```

### 3. Pediatric Focus

Get pediatric dosing and formulations:

```bash
# Pediatric antibiotic dosing
./clinical drug amoxicillin --pediatric

# Pediatric asthma medication
./clinical drug albuterol --pediatric

# ADHD medication
./clinical drug methylphenidate --pediatric --indication "ADHD"
```

**Pediatric output emphasizes:**
- Age and weight-based dosing
- Available liquid formulations
- Taste considerations
- Administration tips for children

### 4. Generic-Only Options

Focus on generic availability and cost:

```bash
# Show only generic options
./clinical drug atorvastatin --generic-only

# Compare generic availability
./clinical drug nexium prilosec --generic-only
```

### 5. Specific Questions

Ask targeted questions:

```bash
# Cost questions
./clinical drug atorvastatin --question "What's the cheapest form?"

# Formulation questions
./clinical drug omeprazole --question "Is there a liquid form?"

# Dosing questions
./clinical drug gabapentin --question "What's the max dose for neuropathic pain?"

# Interaction questions
./clinical drug warfarin --question "What are the major drug interactions?"
```

## Clinical Use Cases

### Use Case 1: New Prescription Decision
**Scenario:** Need to prescribe an SSRI for depression

```bash
./clinical drug sertraline escitalopram paroxetine --compare --indication "depression"
```

**Use the output to:**
- Choose based on cost (important for patient access)
- Select appropriate starting dose
- Identify best formulation (tablet vs liquid)
- Review major interactions
- Get patient instructions ready

### Use Case 2: Cost-Conscious Prescribing
**Scenario:** Patient asks about cheaper alternatives

```bash
# Check if generic available
./clinical drug Lipitor --generic-only

# Compare generic options
./clinical drug atorvastatin simvastatin pravastatin --compare
```

**Use the output to:**
- Identify lowest cost option
- Find tablet-splitting opportunities
- Locate patient assistance programs
- Compare efficacy at various price points

### Use Case 3: Pediatric Dosing
**Scenario:** 5-year-old with strep throat

```bash
./clinical drug amoxicillin --pediatric --indication "strep pharyngitis"
```

**Use the output to:**
- Calculate weight-based dose
- Choose suspension concentration
- Get mixing and storage instructions
- Provide parent counseling points

### Use Case 4: Formulary Decision
**Scenario:** Hospital formulary choosing between options

```bash
./clinical drug enoxaparin fondaparinux --compare --indication "DVT prophylaxis"
```

**Use the output to:**
- Compare dosing complexity
- Evaluate cost differences
- Review safety profiles
- Assess monitoring requirements

### Use Case 5: Patient Education
**Scenario:** Patient has questions about their new medication

```bash
./clinical drug metformin --question "What are the common side effects and how to minimize them?"
```

**Use the output to:**
- Provide clear patient instructions
- Set expectations for side effects
- Offer practical tips (take with food, etc.)
- Identify when to call doctor

### Use Case 6: Medication Substitution
**Scenario:** Pharmacy is out of stock, need alternative

```bash
# Find alternatives in same class
./clinical drug cephalexin cefadroxil --compare

# Check if different formulation available
./clinical drug "lisinopril tablets" --question "Is there a liquid form?"
```

## Understanding Cost Information

### How Costs are Presented

```
COST INFORMATION (Approximate US pricing)
Generic:
- 10mg tablets: $4-10 per month (at 10mg daily)
- 20mg tablets: $8-15 per month (at 20mg daily)
- Available as generic: Yes

Brand:
- 10mg tablets: $200-300 per month
- 20mg tablets: $250-350 per month

Cost-saving tips:
- Generic is 95% cheaper
- Consider tablet splitting: 20mg tablets cut in half = 10mg dose
- Check GoodRx for coupons
- Ask about 90-day supply discount
```

### Cost Notes
- Costs are **approximate** US retail (2024-2025)
- Actual costs vary by:
  - Insurance coverage
  - Pharmacy (chains vs independent)
  - Location
  - Quantity purchased
- Generic costs are typically for commonly prescribed doses
- Brand costs reflect list prices without insurance

### Cost-Saving Strategies Provided
1. **Generic substitution** when available
2. **Tablet splitting** for appropriate medications
3. **Therapeutic alternatives** in same class
4. **Higher strength/lower frequency** when safe
5. **Patient assistance programs** for expensive drugs
6. **90-day supplies** for chronic medications
7. **Pharmacy price comparison** tools (GoodRx, etc.)

## Dosing Forms Explained

### Common Forms Listed

**Tablets:**
- Standard release
- Extended release (XR, ER, SR)
- Chewable
- Orally disintegrating (ODT)

**Capsules:**
- Immediate release
- Extended release
- Sprinkle capsules (can be opened)

**Liquids:**
- Solutions (dissolved drug)
- Suspensions (particles in liquid)
- Syrups (sweetened)
- Elixirs (alcohol-based)

**Injectables:**
- Intramuscular (IM)
- Intravenous (IV)
- Subcutaneous (SubQ)
- Prefilled syringes vs vials

**Other Forms:**
- Patches (transdermal)
- Inhalers (MDI, DPI)
- Nebulizer solutions
- Suppositories
- Topical creams/ointments

## Patient Instructions Included

### What You'll Get

**Administration:**
- Best time to take (morning, bedtime, with meals)
- With or without food
- How to take (swallow whole, chew, dissolve)

**Expectations:**
- When to expect effects (onset)
- How long effects last (duration)
- What improvement looks like

**Avoidance:**
- Drug interactions (major ones)
- Food/beverage interactions
- Activities to avoid (driving, alcohol)

**Monitoring:**
- What to watch for
- When to call doctor
- Signs of serious reactions

**Storage:**
- Room temperature vs refrigeration
- Light protection
- Expiration after opening

## Safety Information Depth

### Black Box Warnings
- Highest FDA safety warning
- Most serious risks
- Required monitoring or restrictions

### Contraindications
- When NOT to use the drug
- Absolute vs relative contraindications
- Patient factors that preclude use

### Major Interactions
- Drugs that should not be combined
- Drugs requiring dose adjustment
- Monitoring needed with certain combinations

### Pregnancy/Lactation
- FDA pregnancy category (if applicable)
- Safety in breastfeeding
- When to avoid or use cautiously

### Common Side Effects
- Most frequently reported (>10%)
- Usually mild and transient
- How to manage

### Serious Side Effects
- Rare but dangerous reactions
- Warning signs to watch for
- When to seek immediate care

## Clinical Pearls

Each drug lookup includes practical prescribing tips:

- **Efficacy considerations:** When this drug works best
- **Tolerability tips:** How to minimize side effects
- **Monitoring requirements:** What labs or checks needed
- **Adherence strategies:** How to improve compliance
- **Alternative options:** When to consider switching
- **Special populations:** Elderly, renal/hepatic impairment

## Tips for Best Results

### Be Specific
```bash
# Instead of:
./clinical drug metformin

# Try:
./clinical drug metformin --indication "type 2 diabetes" --question "What's the best starting dose?"
```

### Use Comparison for Choices
```bash
# When deciding between options:
./clinical drug drug1 drug2 drug3 --compare
```

### Focus on Patient Needs
```bash
# Cost-conscious patient:
./clinical drug simvastatin --generic-only --question "Cheapest option?"

# Pediatric patient:
./clinical drug ibuprofen --pediatric

# Trouble swallowing pills:
./clinical drug levothyroxine --question "Is there a liquid form?"
```

### Combine Flags
```bash
# Multiple flags work together:
./clinical drug amoxicillin --pediatric --indication "otitis media" --question "What suspension concentration is easiest for dosing?"
```

## Limitations

### What This Tool Can Do
✅ Provide general drug information
✅ Compare standard dosing and costs
✅ List available formulations
✅ Highlight major safety concerns
✅ Offer clinical pearls

### What This Tool Cannot Do
❌ Replace package insert or prescribing information
❌ Provide exact local pharmacy pricing
❌ Account for all drug interactions
❌ Replace clinical judgment
❌ Substitute for pharmacist consultation

### Important Notes
- Always verify dosing in authoritative sources
- Check patient-specific factors (allergies, interactions, conditions)
- Consult pharmacist for complex cases
- Use clinical judgment for individual patients
- Costs are estimates only - verify with pharmacy

## Examples in Practice

### Example 1: Quick Drug Info
```bash
./clinical drug lisinopril
```

**Output snippet:**
```
DRUG NAME
Generic: Lisinopril | Brand: Prinivil, Zestril

AVAILABLE FORMS & STRENGTHS
- Tablets: 2.5mg, 5mg, 10mg, 20mg, 30mg, 40mg

STANDARD DOSING
Adult:
- Hypertension: Start 10mg once daily, max 40mg daily
- Heart failure: Start 5mg once daily, max 40mg daily

COST INFORMATION
Generic:
- 10mg tablets: $4-8 per month (30-day supply)
- Available as generic: Yes

Brand:
- 10mg tablets: $100-150 per month

Cost-saving tips:
- Generic is 95% cheaper - always use generic
- 90-day supply often cheaper per month
```

### Example 2: Comparing Options
```bash
./clinical drug lisinopril losartan --compare --indication "hypertension"
```

**Output includes comparison table:**
```
| Feature | Lisinopril (ACE-I) | Losartan (ARB) |
|---------|-------------------|----------------|
| Forms | Tablets only | Tablets only |
| Starting dose | 10mg daily | 50mg daily |
| Max dose | 40mg daily | 100mg daily |
| Generic cost | $4-8/month | $10-20/month |
| Main advantage | Lower cost | Less cough |
| Consideration | Can cause cough | Higher cost |
```

### Example 3: Pediatric Query
```bash
./clinical drug amoxicillin --pediatric
```

**Output emphasizes pediatric use:**
```
AVAILABLE FORMS & STRENGTHS
Pediatric-Friendly:
- Oral suspension: 125mg/5mL, 250mg/5mL
- Chewable tablets: 125mg, 250mg
- Capsules: 250mg, 500mg (older children)

PEDIATRIC DOSING
Standard infections:
- 20-40 mg/kg/day divided TID
- Max: 500mg per dose

Otitis media (high-dose):
- 80-90 mg/kg/day divided BID
- Max: 3000mg/day

PATIENT INSTRUCTIONS (for parents)
- Shake suspension well before each use
- Can mix with milk, formula, or juice if child refuses
- Refrigerate suspension, good for 14 days
- Complete full course even if child feels better
```

## Quick Reference Table

| Task | Command | Example |
|------|---------|---------|
| Basic lookup | `drug <name>` | `drug metformin` |
| Compare drugs | `drug <name1> <name2> --compare` | `drug sertraline fluoxetine --compare` |
| Pediatric info | `drug <name> --pediatric` | `drug amoxicillin --pediatric` |
| For indication | `drug <name> --indication "<condition>"` | `drug lisinopril --indication "hypertension"` |
| Generic only | `drug <name> --generic-only` | `drug lipitor --generic-only` |
| Specific question | `drug <name> --question "<question>"` | `drug warfarin --question "major interactions?"` |
| Combined flags | Multiple flags | `drug amoxicillin --pediatric --indication "strep"` |

---

**Remember:** This tool provides general information. Always use clinical judgment and verify with authoritative sources for patient-specific prescribing.
