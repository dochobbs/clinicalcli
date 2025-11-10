#!/usr/bin/env python3
"""
Interactive Clinical CLI Shell

A persistent, terminal-based interface for rapid clinical decision support.
Stays running for quick access to drug dosing, CDS, and clinical tools.

Features:
- Session memory (remembers patient weight, age)
- Command history (arrow keys)
- Tab completion
- Quick shortcuts
- One-time HIPAA notice per session
"""

import os
import sys
from datetime import datetime
from typing import Optional, Dict

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown

# Import command functions
from .commands.drug import drug
from .commands.cds import cds
from .utils import call_claude, call_claude_with_files, display_output, read_multiline_input
from .prompt_loader import load_prompt
from .model_manager import get_model_manager

# Import system prompts from command modules
from .commands.cds import CDS_SYSTEM_PROMPT
from .commands.ddx import DDX_SYSTEM_PROMPT
from .commands.note import NOTE_SYSTEM_PROMPT
from .commands.parse import PARSE_SYSTEM_PROMPT

console = Console()

# ============================================================================
# SESSION STATE - Remembers patient info between commands
# ============================================================================

class SessionState:
    """
    Maintains basic session statistics and last response.
    """
    def __init__(self):
        self.session_start: datetime = datetime.now()
        self.command_count: int = 0
        self.last_response: str = ""  # Store last response for copying

    def show(self):
        """Display current session stats."""
        table = Table(title="Session Statistics", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        uptime = datetime.now() - self.session_start
        table.add_row("Session uptime", str(uptime).split('.')[0])
        table.add_row("Commands run", str(self.command_count))

        console.print(table)


# ============================================================================
# INTERACTIVE SHELL
# ============================================================================

class ClinicalShell:
    """
    Interactive shell for clinical CLI tools.

    Provides a persistent terminal interface with command history,
    tab completion, and session state management.
    """

    def __init__(self):
        # Session state
        self.state = SessionState()

        # Command history file
        history_file = os.path.expanduser("~/.clinical_cli_history")
        self.session = PromptSession(history=FileHistory(history_file))

        # Model manager
        self.model_manager = get_model_manager()

        # Define available commands for tab completion
        self.commands = [
            'drug', 'd',           # Drug lookup (d is shortcut)
            'cds', 'c',            # Clinical decision support
            'ddx',                 # Differential diagnosis
            'note',                # Clinical note
            'parse',               # Parse documents
            'dose',                # Quick dose calculation
            'compare',             # Compare medications
            'copy',                # Copy last output to clipboard
            'model',               # Model selector
            'stats', 's',          # Show session statistics
            'help', 'h', '?',      # Help
            'quit', 'exit', 'q',   # Exit
        ]

        # Tab completer
        self.completer = WordCompleter(
            self.commands,
            ignore_case=True,
            sentence=True
        )

        # Custom prompt style
        self.prompt_style = Style.from_dict({
            'prompt': '#00aa00 bold',
        })

        # HIPAA warning shown flag
        self.hipaa_shown = False

    def show_welcome(self):
        """Display welcome banner with one-time HIPAA notice."""
        model_info = self.model_manager.get_current_model_info()
        welcome = f"""
[bold cyan]Clinical CLI - Interactive Mode[/bold cyan]
[dim]Pediatric-focused clinical decision support[/dim]
[dim]Current model: {model_info}[/dim]

[yellow]Quick Commands:[/yellow]
  [cyan]d amoxicillin --weight 52#[/cyan] - Drug lookup
  [cyan]cds <presentation>[/cyan]         - Clinical decision support
  [cyan]ddx <symptoms>[/cyan]             - Differential diagnosis
  [cyan]note <encounter>[/cyan]           - Generate clinical note
  [cyan]parse labs.pdf[/cyan]             - Parse document/image
  [cyan]model[/cyan]                      - Switch model (cloud/local)
  [cyan]stats[/cyan] or [cyan]s[/cyan]                  - Show session stats
  [cyan]help[/cyan] or [cyan]?[/cyan]                   - Full help
  [cyan]quit[/cyan] or [cyan]q[/cyan]                   - Exit

[dim]Type commands and press Enter. Use arrow keys for history.[/dim]
"""
        console.print(Panel(welcome, border_style="cyan"))

        # Show HIPAA notice once per session
        if not self.hipaa_shown:
            console.print("\n[yellow]⚠️  PHI Notice:[/yellow] Data sent to Anthropic under BAA. Handle PHI appropriately.\n")
            self.hipaa_shown = True

    def show_help(self):
        """Display detailed help information."""
        help_text = """
# Clinical CLI - Command Reference

## Output Formats
```
Most commands support quick (q) or full (f) output formats:
  q = Quick: Concise but complete, clinically useful (250-400 words)
  f = Full:  Comprehensive, detailed info (default)
```

## Drug Lookup
```
drug <name> [q|f] [--weight WT] [--age AGE] [--indication IND]
d <name>                    # Shortcut
dose <name> <weight>        # Quick dose calc
compare <drug1> <drug2>     # Compare medications

Examples:
  d amoxicillin q --weight 52# --age 5yo
  d amoxicillin f --indication "strep throat"
  d amoxicillin --weight 52#  # Defaults to full
  dose amox 52#               # Quick calculation
  compare amoxicillin cefdinir
```

## Clinical Decision Support
```
cds [q|f] <clinical presentation>
c <clinical presentation>   # Shortcut

Examples:
  cds q 5yo with fever x3 days, ear pain
  cds f 3yo with cough, wheezing, tachypnea
  cds 5yo with fever    # Defaults to full
```

## Differential Diagnosis
```
ddx [q|f] <clinical presentation>

Examples:
  ddx q 5yo with fever, ear pain
  ddx f 12yo with headache, photophobia
  ddx 5yo with fever    # Defaults to full
```

## Clinical Notes
```
note [q|f] [type] <encounter info>

Examples:
  note q 5yo with AOM, starting amoxicillin
  note f progress doing better, fever resolved
  note q discharge resolved AOM
  note 5yo with AOM     # Defaults to full
```

## Parse Documents
```
parse <filename>            # Analyze PDF or image

Examples:
  parse labs.pdf
  parse ~/Desktop/cbc.png
  parse xray.pdf
```

## Model Selection
```
model                       # List available models
model list                  # List available models
model <name>                # Switch to model
model set <name>            # Switch to model

Examples:
  model                     # Show available models
  model llama3.2            # Switch to local Ollama model
  model claude-sonnet-4-5-20250929  # Switch to Claude
```

## Session Statistics
```
stats             or   s            # Show session statistics
```

## Utilities
```
copy                                 # Copy last output to clipboard
```

## Other Commands
```
help   or   h   or   ?     # This help
quit   or   exit   or   q  # Exit shell
```

## Tips
- Use arrow keys for command history
- Tab completion for commands
- Ctrl+C to cancel current command
- Use 'copy' command to copy last output to clipboard
- Specify weight/age with each drug command as needed
- Use 'q' for quick output (concise), 'f' or omit for full (detailed)
- Use local models (Ollama/LM Studio) for offline work
"""
        console.print(Markdown(help_text))

    def parse_command(self, cmd: str) -> tuple:
        """
        Parse user command into action and arguments.

        Returns:
            (command, args) tuple
        """
        parts = cmd.strip().split(maxsplit=1)
        if not parts:
            return None, None

        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        return command, args

    def execute_drug_lookup(self, args: str):
        """Execute drug lookup command."""
        # Parse arguments
        parts = args.split()
        if not parts:
            console.print("[yellow]Usage: drug <medication> [q|f] [--weight WT] [--age AGE] [--indication IND][/yellow]")
            console.print("[dim]Example: d amoxicillin q --weight 52# --age 5yo[/dim]")
            console.print("[dim]         d amoxicillin f --indication 'strep throat'[/dim]")
            console.print("[dim]         q = quick (concise), f = full (detailed, default)[/dim]")
            return

        drug_name = parts[0]

        # Parse output format flag (q or f)
        output_format = "full"  # default
        if len(parts) > 1 and parts[1] in ['q', 'f']:
            output_format = "quick" if parts[1] == 'q' else "full"
            parts.pop(1)  # Remove format flag from parts

        # Parse other flags
        weight = None
        age = None
        indication = None

        # Simple arg parsing
        i = 1
        while i < len(parts):
            if parts[i] in ['--weight', '-w'] and i + 1 < len(parts):
                weight = parts[i + 1]
                i += 2
            elif parts[i] in ['--age', '-a'] and i + 1 < len(parts):
                age = parts[i + 1]
                i += 2
            elif parts[i] in ['--indication', '-i'] and i + 1 < len(parts):
                indication = parts[i + 1]
                i += 2
            else:
                i += 1

        # Build prompt
        system_prompt = load_prompt("drug_lookup")

        # Set output format instruction
        if output_format == "quick":
            user_message = f"""Provide QUICK pediatric drug information for: {drug_name}

OUTPUT FORMAT: QUICK (concise but complete)
- Keep response under 300-400 words
- Use clear sections with bullet points
- Include: standard dose with calculation, key indications, dosing frequency, common formulations, critical warnings, monitoring
- Provide enough detail to be clinically useful
- Skip only: extensive pharmacology, drug interactions, rare side effects"""
        else:
            user_message = f"Provide comprehensive PEDIATRIC drug information for: {drug_name}"

        if indication:
            user_message += f"\n\nSpecific indication: {indication}"
            user_message += "\nProvide dosing specific to this indication only."

        if age:
            user_message += f"\n\nPatient age: {age}"

        if weight:
            user_message += f"\n\nPatient weight: {weight}"
            user_message += "\n\nCalculate dose for this weight. Show step-by-step calculation."

        # Add anti-hallucination reminder
        user_message += """

IMPORTANT:
- Only provide information you are confident about
- Clearly state if evidence in children is limited
- Mark any off-label uses as "OFF-LABEL"
- If unsure about specific details, say so
- CITE YOUR SOURCES
"""

        # Call Claude
        console.print(f"[dim]Looking up {drug_name}...[/dim]\n")
        console.print("[cyan]Response:[/cyan]\n")
        response = call_claude(system_prompt, user_message)

        # Check for uncertainties
        concerning_phrases = ["I'm not certain", "limited evidence", "OFF-LABEL", "verify"]
        has_uncertainty = any(phrase.lower() in response.lower() for phrase in concerning_phrases)

        if has_uncertainty:
            console.print("\n[yellow]⚠️  Note: Response includes uncertainties or off-label uses[/yellow]\n")

        # Display
        format_label = "Quick" if output_format == "quick" else "Full"
        title = f"Pediatric Drug Info [{format_label}]: {drug_name.title()}"
        if weight:
            title += f" - {weight}"

        self.state.last_response = response  # Store for copy command
        display_output(response, title=title)

        self.state.command_count += 1

    def execute_quick_dose(self, args: str):
        """Execute quick dose calculation: dose amox 52#"""
        parts = args.split()
        if len(parts) < 2:
            console.print("[yellow]Usage: dose <medication> <weight>[/yellow]")
            console.print("[dim]Example: dose amoxicillin 52#[/dim]")
            return

        drug_name = parts[0]
        weight = parts[1]

        # Use execute_drug_lookup with weight
        self.execute_drug_lookup(f"{drug_name} --weight {weight}")

    def execute_compare(self, args: str):
        """Compare multiple medications."""
        drugs = args.split()
        if len(drugs) < 2:
            console.print("[yellow]Usage: compare <drug1> <drug2> [drug3][/yellow]")
            return

        # Build prompt
        system_prompt = load_prompt("drug_lookup")
        user_message = f"""Compare these medications FOR PEDIATRIC USE: {', '.join(drugs)}

Focus on:
- Pediatric dosing differences
- Available child-friendly formulations
- Taste/palatability (when known)
- Cost for typical pediatric course
- Safety profile in children
- Ease of use for parents/caregivers

CITE YOUR SOURCES and note if evidence is limited.
"""

        console.print(f"[dim]Comparing {', '.join(drugs)}...[/dim]\n")
        console.print("[cyan]Response:[/cyan]\n")
        response = call_claude(system_prompt, user_message)

        self.state.last_response = response  # Store for copy command
        display_output(response, title=f"Drug Comparison: {', '.join(drugs)}")
        self.state.command_count += 1

    def execute_cds(self, args: str):
        """Execute clinical decision support."""
        if not args.strip():
            console.print("[yellow]Usage: cds [q|f] <clinical presentation>[/yellow]")
            console.print("[dim]Example: cds q 5yo with fever x3 days, ear pain[/dim]")
            console.print("[dim]         cds f 5yo with fever x3 days, ear pain[/dim]")
            console.print("[dim]         q = quick (brief), f = full (detailed, default)[/dim]")
            return

        # Parse output format
        parts = args.split(maxsplit=1)
        output_format = "full"  # default
        clinical_presentation = args

        if len(parts) > 1 and parts[0] in ['q', 'f']:
            output_format = "quick" if parts[0] == 'q' else "full"
            clinical_presentation = parts[1]

        # Build user message with format instruction
        if output_format == "quick":
            user_message = f"""Provide QUICK clinical decision support for:

{clinical_presentation}

OUTPUT FORMAT: QUICK (concise but complete)
- Keep under 250-300 words
- Assessment (2-3 sentences with key features)
- Top 5 differential diagnoses with brief likelihood
- Management plan with specific recommendations
- Red flags and when to escalate care
- Follow-up guidance"""
        else:
            user_message = f"Provide pediatric clinical decision support for:\n\n{clinical_presentation}"

        console.print(f"\n[dim]Analyzing: {clinical_presentation[:60]}...[/dim]\n")
        console.print("[cyan]Response:[/cyan]\n")

        response = call_claude(CDS_SYSTEM_PROMPT, user_message)

        # Check for red flags
        red_flag_phrases = ["emergent", "immediate", "911", "ED", "emergency"]
        has_red_flags = any(phrase.lower() in response.lower() for phrase in red_flag_phrases)

        if has_red_flags:
            console.print("\n[red]🚨 ALERT: Response includes emergent/urgent indicators[/red]\n")

        format_label = "Quick" if output_format == "quick" else "Full"
        self.state.last_response = response  # Store for copy command
        display_output(response, title=f"Clinical Decision Support [{format_label}]")
        self.state.command_count += 1

    def execute_ddx(self, args: str):
        """Execute differential diagnosis."""
        if not args.strip():
            console.print("[yellow]Usage: ddx [q|f] <clinical presentation>[/yellow]")
            console.print("[dim]Example: ddx q 5yo with fever, ear pain[/dim]")
            console.print("[dim]         ddx f 5yo with fever, ear pain[/dim]")
            console.print("[dim]         q = quick (top 5), f = full (comprehensive, default)[/dim]")
            return

        # Parse output format
        parts = args.split(maxsplit=1)
        output_format = "full"  # default
        clinical_presentation = args

        if len(parts) > 1 and parts[0] in ['q', 'f']:
            output_format = "quick" if parts[0] == 'q' else "full"
            clinical_presentation = parts[1]

        # Build user message with format instruction
        if output_format == "quick":
            user_message = f"""Generate a QUICK differential diagnosis for:

{clinical_presentation}

OUTPUT FORMAT: QUICK (concise but complete)
- List top 7 diagnoses
- Each diagnosis: likelihood + 1-2 key distinguishing features
- Keep under 200-250 words total
- Most likely diagnoses first
- Include any "can't miss" diagnoses"""
        else:
            user_message = f"Generate a differential diagnosis for:\n\n{clinical_presentation}"
            user_message += "\n\n[Focus on most likely common diagnoses, but don't miss serious ones]"

        console.print(f"\n[dim]Analyzing: {clinical_presentation[:60]}...[/dim]\n")
        console.print("[cyan]Response:[/cyan]\n")

        response = call_claude(DDX_SYSTEM_PROMPT, user_message)

        format_label = "Quick" if output_format == "quick" else "Full"
        self.state.last_response = response  # Store for copy command
        display_output(response, title=f"Differential Diagnosis [{format_label}]")
        self.state.command_count += 1

    def execute_note(self, args: str):
        """Execute clinical note generation."""
        note_types = ['soap', 'progress', 'consult', 'procedure', 'discharge']
        parts = args.strip().split()

        if not parts:
            console.print("[yellow]Usage: note [q|f] [type] <encounter info>[/yellow]")
            console.print("[dim]Example: note q 5yo with AOM, starting amoxicillin[/dim]")
            console.print("[dim]Example: note f progress doing better, fever resolved[/dim]")
            console.print("[dim]         q = quick (brief), f = full (detailed, default)[/dim]")
            return

        # Parse output format (q or f)
        output_format = "full"  # default
        start_idx = 0

        if parts[0] in ['q', 'f']:
            output_format = "quick" if parts[0] == 'q' else "full"
            start_idx = 1

        if start_idx >= len(parts):
            console.print("[yellow]No encounter information provided[/yellow]")
            return

        # Check if next word is a note type
        note_type = "soap"  # Default
        encounter_start_idx = start_idx

        if parts[start_idx].lower() in note_types:
            note_type = parts[start_idx].lower()
            encounter_start_idx = start_idx + 1

        if encounter_start_idx >= len(parts):
            console.print("[yellow]No encounter information provided[/yellow]")
            return

        # Get encounter info
        encounter_info = ' '.join(parts[encounter_start_idx:])

        # Build user message with format instruction
        if output_format == "quick":
            user_message = f"""Generate a CONCISE {note_type.upper()} note from the following encounter:

{encounter_info}

OUTPUT FORMAT: QUICK (concise but complete)
- Keep under 250-300 words
- Include all essential clinical elements
- Use bullets for efficiency but maintain professional format
- Cover: chief complaint, key findings, assessment, plan
- Suitable for medical documentation"""
        else:
            user_message = f"Generate a {note_type.upper()} note from the following encounter:\n\n{encounter_info}"

        # Adjust system prompt based on note type
        system_prompt = NOTE_SYSTEM_PROMPT

        if note_type == 'progress':
            system_prompt += "\n\nFormat as brief progress note: Interval history, exam changes, assessment/plan by problem."
        elif note_type == 'consult':
            system_prompt += "\n\nFormat as consultation note: Include detailed history, comprehensive exam, detailed assessment with recommendations."
        elif note_type == 'procedure':
            system_prompt += "\n\nFormat as procedure note: Indication, consent, procedure details, findings, complications, plan."
        elif note_type == 'discharge':
            system_prompt += "\n\nFormat as discharge summary: Admission diagnosis, hospital course, discharge condition, medications, follow-up."

        console.print(f"\n[dim]Generating {note_type} note from: {encounter_info[:50]}...[/dim]\n")
        console.print("[cyan]Response:[/cyan]\n")

        response = call_claude(system_prompt, user_message)

        format_label = "Quick" if output_format == "quick" else "Full"
        self.state.last_response = response  # Store for copy command
        display_output(response, title=f"{note_type.upper()} Note [{format_label}]")
        self.state.command_count += 1

    def execute_parse(self, args: str):
        """Execute document parsing."""
        if not args.strip():
            console.print("[yellow]Usage: parse <filename>[/yellow]")
            console.print("[dim]Example: parse labs.pdf[/dim]")
            return

        # Get file path from args
        file_path = args.strip()

        # Expand home directory if needed
        if file_path.startswith('~'):
            file_path = os.path.expanduser(file_path)

        # Check if file exists
        if not os.path.exists(file_path):
            console.print(f"[red]Error: File not found: {file_path}[/red]")
            return

        # Build user message
        user_message = "Analyze this clinical document and extract all relevant information."

        console.print(f"\n[dim]Analyzing {os.path.basename(file_path)}...[/dim]\n")

        try:
            response = call_claude_with_files(PARSE_SYSTEM_PROMPT, user_message, [file_path])

            self.state.last_response = response  # Store for copy command
            title = f"Document Analysis: {os.path.basename(file_path)}"
            display_output(response, title=title)
            self.state.command_count += 1
        except Exception as e:
            console.print(f"[red]Error parsing file: {e}[/red]")

    def execute_model(self, args: str):
        """Execute model management command."""
        args = args.strip()

        if not args or args == 'list' or args == 'ls':
            # List available models
            self.model_manager.list_available_models()
            current = self.model_manager.get_current_model_info()
            console.print(f"[green]Current model: {current}[/green]\n")

        elif args.startswith('set ') or args.startswith('use '):
            # Set model
            model_name = args.split(maxsplit=1)[1].strip()
            success = self.model_manager.set_model(model_name)
            if success:
                # Update welcome to reflect change
                console.print(f"[dim]Use 'help' to see usage with this model[/dim]")

        else:
            # Treat as model name directly
            success = self.model_manager.set_model(args)
            if success:
                console.print(f"[dim]Use 'help' to see usage with this model[/dim]")

    def execute_copy(self, args: str):
        """Copy last response to clipboard."""
        if not self.state.last_response:
            console.print("[yellow]No output to copy yet. Run a command first.[/yellow]")
            return

        import pyperclip
        pyperclip.copy(self.state.last_response)
        console.print(f"[green]✓ Copied {len(self.state.last_response)} characters to clipboard[/green]")

    def run(self):
        """Main interactive loop."""
        self.show_welcome()

        while True:
            try:
                # Get user input with styled prompt
                user_input = self.session.prompt(
                    [('class:prompt', '⚕️  clinical> ')],
                    completer=self.completer,
                    style=self.prompt_style
                )

                if not user_input.strip():
                    continue

                # Parse command
                command, args = self.parse_command(user_input)

                # Execute command
                if command in ['quit', 'exit', 'q']:
                    console.print("\n[cyan]Goodbye! Stay safe.[/cyan]")
                    break

                elif command in ['help', 'h', '?']:
                    self.show_help()

                elif command in ['drug', 'd']:
                    self.execute_drug_lookup(args)

                elif command == 'dose':
                    self.execute_quick_dose(args)

                elif command == 'compare':
                    self.execute_compare(args)

                elif command in ['cds', 'c']:
                    self.execute_cds(args)

                elif command == 'ddx':
                    self.execute_ddx(args)

                elif command == 'note':
                    self.execute_note(args)

                elif command == 'parse':
                    self.execute_parse(args)

                elif command == 'model':
                    self.execute_model(args)

                elif command == 'copy':
                    self.execute_copy(args)

                elif command in ['stats', 's']:
                    self.state.show()

                else:
                    console.print(f"[red]Unknown command: {command}[/red]")
                    console.print("[dim]Type 'help' for available commands[/dim]")

            except KeyboardInterrupt:
                console.print("\n[dim]Press Ctrl+D or type 'quit' to exit[/dim]")
                continue

            except EOFError:
                console.print("\n[cyan]Goodbye![/cyan]")
                break

            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                console.print("[dim]Type 'help' for usage information[/dim]")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point for interactive shell."""
    # Verify API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[red]Error: ANTHROPIC_API_KEY not found in environment[/red]")
        console.print("[yellow]Set it in ~/.zshrc or export it in your shell[/yellow]")
        sys.exit(1)

    # Start interactive shell
    shell = ClinicalShell()
    shell.run()


if __name__ == "__main__":
    main()


# ============================================================================
# MODULE DOCUMENTATION
# ============================================================================

"""
USAGE:

1. Start interactive shell:
   python src/interactive.py

   Or with wrapper:
   ./clinical-shell

2. Run commands with explicit parameters:
   > d amoxicillin --weight 52# --age 5yo
   > dose amox 52#
   > cds
   > ddx
   > note
   > compare amox cefdinir

BENEFITS:

- Stays running - no startup time between queries
- Command history - arrow keys recall previous commands
- Tab completion - faster typing
- Quick shortcuts - 'd' instead of 'drug'
- One HIPAA warning - not every command

SHORTCUTS:

d      = drug
c      = cds
s      = state
sw     = set weight
sa     = set age
h, ?   = help
q      = quit

SPEED TIPS:

1. Set weight/age at start of patient encounter
2. Use shortcuts (d, c, s)
3. Use tab completion
4. Use command history (up arrow)
5. Leave shell running all day
"""
