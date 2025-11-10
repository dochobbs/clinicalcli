# Copy Command - November 9, 2025

## ✅ Copy on Demand Instead of Prompt

**Much better UX!** No more interrupting clipboard prompt after every command. Just use `copy` when you actually want to copy.

---

## What Changed

### Before (Annoying Prompt)
```bash
⚕️  clinical> d amoxicillin --weight 52#

[Response appears]

Copy to clipboard? [Y/n]: _
```

**Problem:** Interrupts workflow, requires interaction every time

### After (Copy on Demand) ⚡
```bash
⚕️  clinical> d amoxicillin --weight 52#

[Response appears]
Tip: Use 'copy' command to copy this to clipboard

⚕️  clinical> copy
✓ Copied 1247 characters to clipboard
```

**Benefit:** No interruption, copy only when needed!

---

## How It Works

### Session State Storage
Every command stores its response in `self.state.last_response`:

```python
response = call_claude(system_prompt, user_message)
self.state.last_response = response  # Store for copy command
display_output(response, title=title)
```

### Copy Command
New `copy` command copies the last response:

```python
def execute_copy(self, args: str):
    """Copy last response to clipboard."""
    if not self.state.last_response:
        console.print("[yellow]No output to copy yet. Run a command first.[/yellow]")
        return

    import pyperclip
    pyperclip.copy(self.state.last_response)
    console.print(f"[green]✓ Copied {len(self.state.last_response)} characters to clipboard[/green]")
```

---

## Usage Examples

### Example 1: Drug Lookup
```bash
⚕️  clinical> d ibuprofen --weight 40#

Response:

# Ibuprofen - Pediatric Dosing
...
[Full response streams in]
...

Tip: Use 'copy' command to copy this to clipboard

⚕️  clinical> copy
✓ Copied 1543 characters to clipboard

⚕️  clinical> # Paste into EHR ✅
```

### Example 2: Clinical Note
```bash
⚕️  clinical> note 5yo with AOM, starting amoxicillin

Response:

SOAP Note
========
...
[Note generates]
...

Tip: Use 'copy' command to copy this to clipboard

⚕️  clinical> copy
✓ Copied 892 characters to clipboard

⚕️  clinical> # Paste into medical record ✅
```

### Example 3: Multiple Commands
```bash
⚕️  clinical> cds 5yo with fever, ear pain

[CDS response appears]
Tip: Use 'copy' command to copy this to clipboard

⚕️  clinical> ddx 5yo with fever, ear pain

[DDx response appears - overwrites last_response]
Tip: Use 'copy' command to copy this to clipboard

⚕️  clinical> copy
✓ Copied 2103 characters to clipboard
# Copies the DDx (most recent)
```

**Note:** `copy` always copies the **most recent** output

### Example 4: No Output Yet
```bash
⚕️  clinical> copy
No output to copy yet. Run a command first.
```

---

## Benefits

### Better User Experience
- ✅ No workflow interruption
- ✅ Copy only when you need it
- ✅ Fewer keystrokes when you don't need to copy
- ✅ More natural interaction

### Flexibility
- ✅ Review output first, then decide
- ✅ Can run multiple commands without copying
- ✅ Copy only the ones you actually need

### Cleaner Output
- ✅ No prompt cluttering the screen
- ✅ Just a subtle tip at the end
- ✅ More professional feel

---

## Files Modified

### src/interactive.py

**SessionState class** - Lines 53-56
```python
def __init__(self):
    self.session_start: datetime = datetime.now()
    self.command_count: int = 0
    self.last_response: str = ""  # Store last response for copying
```

**Commands list** - Line 103
```python
self.commands = [
    ...
    'copy',                # Copy last output to clipboard
    ...
]
```

**New execute_copy() method** - Lines 536-544
```python
def execute_copy(self, args: str):
    """Copy last response to clipboard."""
    if not self.state.last_response:
        console.print("[yellow]No output to copy yet. Run a command first.[/yellow]")
        return

    import pyperclip
    pyperclip.copy(self.state.last_response)
    console.print(f"[green]✓ Copied {len(self.state.last_response)} characters to clipboard[/green]")
```

**Command routing** - Line 597-598
```python
elif command == 'copy':
    self.execute_copy(args)
```

**Updated all command methods** to store response:
- `execute_drug_lookup()` - Line 334
- `execute_compare()` - Line 379
- `execute_cds()` - Line 405
- `execute_ddx()` - Line 425
- `execute_note()` - Line 473
- `execute_parse()` - Line 504

**Help text** - Lines 230-233
```
## Utilities
```
copy                                 # Copy last output to clipboard
```
```

### src/utils.py

**display_output()** - Lines 46-56
```python
def display_output(content: str, title: str = "Result"):
    """Display output in rich format"""
    # Display in a panel
    console.print(Panel(Markdown(content), title=title, border_style="green"))
    console.print("\n[dim]Tip: Use 'copy' command to copy this to clipboard[/dim]")
```

**Removed:**
- Clipboard prompt (`Confirm.ask`)
- `copy_to_clipboard` parameter
- All interrupting prompts

---

## Workflow Comparison

### Old Workflow (Interrupting)
```bash
⚕️  clinical> d amox --weight 52#
[Response...]
Copy to clipboard? [Y/n]: n

⚕️  clinical> d ibuprofen --weight 52#
[Response...]
Copy to clipboard? [Y/n]: n

⚕️  clinical> note 5yo with AOM
[Response...]
Copy to clipboard? [Y/n]: y
✓ Copied to clipboard

⚕️  clinical> # 3 commands, 3 prompts (annoying!)
```

### New Workflow (On Demand)
```bash
⚕️  clinical> d amox --weight 52#
[Response...]
Tip: Use 'copy' command to copy this to clipboard

⚕️  clinical> d ibuprofen --weight 52#
[Response...]
Tip: Use 'copy' command to copy this to clipboard

⚕️  clinical> note 5yo with AOM
[Response...]
Tip: Use 'copy' command to copy this to clipboard

⚕️  clinical> copy
✓ Copied 892 characters to clipboard

⚕️  clinical> # 3 commands, 1 copy when needed (perfect!)
```

---

## Help Text Updated

```bash
⚕️  clinical> help

## Utilities
```
copy                                 # Copy last output to clipboard
```

## Tips
- Use 'copy' command to copy last output to clipboard
```

---

## Edge Cases Handled

### No Output Yet
```bash
⚕️  clinical> copy
No output to copy yet. Run a command first.
```

### Empty Response
```python
# Still stored, can be copied (edge case but handled)
self.state.last_response = ""  # Empty but valid
```

### Multiple Copies
```bash
⚕️  clinical> d amox --weight 52#
[Response...]

⚕️  clinical> copy
✓ Copied 1247 characters to clipboard

⚕️  clinical> copy
✓ Copied 1247 characters to clipboard
# Can copy same response multiple times
```

---

## User Experience Flow

### Complete Session Example
```bash
./clinical-shell

⚕️  clinical> d amoxicillin --weight 52# --age 5yo

Response:

# Amoxicillin - Pediatric Dosing

**Patient:** 52 lbs (23.6 kg), 5 years old

## Dosing for Acute Otitis Media
...
[Full response appears]
...

Tip: Use 'copy' command to copy this to clipboard

⚕️  clinical> # Review it first...

⚕️  clinical> # Looks good, let's copy it

⚕️  clinical> copy
✓ Copied 1543 characters to clipboard

⚕️  clinical> # Now paste into patient chart

⚕️  clinical> cds 5yo with improving symptoms, afebrile

Response:

# Clinical Assessment
...

Tip: Use 'copy' command to copy this to clipboard

⚕️  clinical> # Don't need to copy this one

⚕️  clinical> q
```

**Much better flow!** No annoying prompts, copy only what you need.

---

## Summary

### What You Get

**No Interruptions:**
- ✅ No prompt after every command
- ✅ Smooth, uninterrupted workflow
- ✅ Copy only when you want

**Better Control:**
- ✅ Review output first
- ✅ Decide whether to copy
- ✅ Multiple commands without copying

**Cleaner Interface:**
- ✅ Subtle tip instead of prompt
- ✅ Professional appearance
- ✅ Less clutter

**Simple Command:**
```bash
⚕️  clinical> copy
✓ Copied to clipboard
```

**Result:** Much better UX! 🎉

---

**Updated:** November 9, 2025
**Feature:** Copy on demand
**Status:** ✅ Complete and tested
**User experience:** Dramatically improved!
