"""
Prompt Loader and Management Utility

This module handles loading system prompts from editable markdown files,
allowing easy surgical editing of AI behavior without touching code.

Benefits:
- Prompts are version-controlled markdown files
- Easy to edit, review, and update
- No code changes needed for prompt iterations
- Clear separation of AI instructions from application logic
"""

import os
from pathlib import Path
from typing import Optional
from rich.console import Console

console = Console()

# ============================================================================
# PROMPT FILE LOCATIONS
# ============================================================================

# Get the project root directory (parent of src/)
PROJECT_ROOT = Path(__file__).parent.parent

# Prompts directory
PROMPTS_DIR = PROJECT_ROOT / "prompts"

# Individual prompt files
PROMPT_FILES = {
    "drug_lookup": PROMPTS_DIR / "drug_lookup.md",
    "clinical_decision_support": PROMPTS_DIR / "clinical_decision_support.md",
    "handout": PROMPTS_DIR / "handout.md",
    "note": PROMPTS_DIR / "note.md",
    "ddx": PROMPTS_DIR / "ddx.md",
    "parse": PROMPTS_DIR / "parse.md",
}


# ============================================================================
# PROMPT LOADING FUNCTIONS
# ============================================================================

def load_prompt(prompt_name: str) -> str:
    """
    Load a system prompt from its markdown file.

    This function reads the prompt from the prompts/ directory, allowing
    easy editing of AI behavior without modifying code.

    Args:
        prompt_name: Name of the prompt to load (e.g., "drug_lookup")

    Returns:
        The prompt text as a string

    Raises:
        FileNotFoundError: If the prompt file doesn't exist
        ValueError: If prompt_name is not recognized

    Example:
        >>> prompt = load_prompt("drug_lookup")
        >>> # Now use prompt with Claude API
    """
    # Validate prompt name
    if prompt_name not in PROMPT_FILES:
        available = ", ".join(PROMPT_FILES.keys())
        raise ValueError(
            f"Unknown prompt name: '{prompt_name}'. "
            f"Available prompts: {available}"
        )

    # Get file path
    prompt_file = PROMPT_FILES[prompt_name]

    # Check if file exists
    if not prompt_file.exists():
        raise FileNotFoundError(
            f"Prompt file not found: {prompt_file}\n"
            f"Expected location: {prompt_file.absolute()}"
        )

    # Load and return the prompt
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt_text = f.read()

        # Log successful load (optional, can be disabled)
        # console.print(f"[dim]Loaded prompt: {prompt_name} ({len(prompt_text)} chars)[/dim]")

        return prompt_text

    except Exception as e:
        console.print(f"[red]Error loading prompt '{prompt_name}': {e}[/red]")
        raise


def get_prompt_file_path(prompt_name: str) -> Path:
    """
    Get the file path for a prompt (useful for telling user where to edit).

    Args:
        prompt_name: Name of the prompt

    Returns:
        Path object pointing to the prompt file

    Example:
        >>> path = get_prompt_file_path("drug_lookup")
        >>> print(f"Edit this file: {path}")
    """
    if prompt_name not in PROMPT_FILES:
        available = ", ".join(PROMPT_FILES.keys())
        raise ValueError(f"Unknown prompt: {prompt_name}. Available: {available}")

    return PROMPT_FILES[prompt_name]


def list_available_prompts() -> dict:
    """
    List all available prompts and their file paths.

    Returns:
        Dictionary mapping prompt names to file paths

    Example:
        >>> prompts = list_available_prompts()
        >>> for name, path in prompts.items():
        ...     print(f"{name}: {path}")
    """
    return {name: str(path) for name, path in PROMPT_FILES.items()}


def verify_all_prompts() -> tuple[list, list]:
    """
    Verify that all prompt files exist and are readable.

    Returns:
        Tuple of (existing_prompts, missing_prompts)

    Example:
        >>> existing, missing = verify_all_prompts()
        >>> if missing:
        ...     print(f"Missing prompts: {missing}")
    """
    existing = []
    missing = []

    for name, path in PROMPT_FILES.items():
        if path.exists():
            try:
                with open(path, 'r') as f:
                    f.read()
                existing.append(name)
            except Exception as e:
                console.print(f"[yellow]Warning: Can't read {name}: {e}[/yellow]")
                missing.append(name)
        else:
            missing.append(name)

    return existing, missing


# ============================================================================
# PROMPT EDITING HELPERS
# ============================================================================

def show_prompt_location(prompt_name: str) -> None:
    """
    Display the file location for a prompt, making it easy to edit.

    Args:
        prompt_name: Name of the prompt to locate

    Example:
        >>> show_prompt_location("drug_lookup")
        To edit the drug_lookup prompt:
        File: /path/to/prompts/drug_lookup.md
    """
    try:
        path = get_prompt_file_path(prompt_name)
        console.print(f"\n[cyan]To edit the {prompt_name} prompt:[/cyan]")
        console.print(f"[yellow]File: {path.absolute()}[/yellow]")
        console.print("[dim]Changes take effect on next command run[/dim]\n")
    except ValueError as e:
        console.print(f"[red]{e}[/red]")


def export_prompt_to_file(prompt_name: str, output_path: str) -> None:
    """
    Export a prompt to a specific file location (for sharing/backup).

    Args:
        prompt_name: Name of the prompt to export
        output_path: Where to save the exported prompt

    Example:
        >>> export_prompt_to_file("drug_lookup", "backup_drug_prompt.md")
    """
    prompt = load_prompt(prompt_name)
    output = Path(output_path)

    with open(output, 'w', encoding='utf-8') as f:
        f.write(prompt)

    console.print(f"[green]✓ Exported {prompt_name} to {output.absolute()}[/green]")


# ============================================================================
# MODULE DOCUMENTATION
# ============================================================================

"""
USAGE:

1. Load a prompt in your command:
   from prompt_loader import load_prompt

   system_prompt = load_prompt("drug_lookup")
   response = call_claude(system_prompt, user_message)

2. Edit prompts surgically:
   - Open prompts/drug_lookup.md in your editor
   - Make changes (add instructions, modify format, etc.)
   - Save file
   - Next command run uses updated prompt automatically

3. Show user where to edit:
   from prompt_loader import show_prompt_location

   show_prompt_location("drug_lookup")
   # Displays file path for easy editing

4. Verify prompts on startup:
   from prompt_loader import verify_all_prompts

   existing, missing = verify_all_prompts()
   if missing:
       print(f"Warning: Missing prompts: {missing}")

BENEFITS:

- No code changes needed for prompt iteration
- Easy diff/version control of prompts
- Can share prompts as standalone files
- Clear separation of concerns
- Surgical editing of AI behavior

PROMPT FILE FORMAT:

- Markdown files (.md)
- First-level heading: Prompt title
- Rest of file: Prompt content
- Can include formatting, lists, examples
- Loaded as-is (markdown formatting included in prompt)
"""
