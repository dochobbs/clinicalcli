#!/usr/bin/env python3
"""
Clinical CLI Tool - PHI-Safe Pediatric Clinical Decision Support

This tool provides pediatric-focused clinical decision support with:
- Age-appropriate guidance and dosing
- Anti-hallucination safeguards
- Weight-based medication dosing
- File parsing (labs, imaging, PDFs)
- Evidence-based recommendations

Requires BAA with Anthropic for PHI processing
"""

import os
import click
from rich.console import Console
from rich.markdown import Markdown

# Import active commands (all pediatric-focused)
from .commands.cds import cds
from .commands.handout import handout
from .commands.note import note
from .commands.ddx import ddx
from .commands.parse import parse
from .commands.drug import drug

# Temporarily disabled commands (files preserved, not deleted)
# from .commands.prior_auth import prior_auth
# from .commands.referral import referral

console = Console()

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    Clinical CLI - PHI-Safe Pediatric Clinical Decision Support Tool

    Pediatric-focused tools with anti-hallucination safeguards:
    - CDS: Age-appropriate clinical decision support
    - Drug: Weight-based dosing calculator (accepts lbs or kg)
    - Handout: Parent-friendly education materials
    - Note: Pediatric documentation
    - DDx: Age-appropriate differential diagnosis
    - Parse: Extract data from labs, imaging, PDFs

    Requires: ANTHROPIC_API_KEY environment variable
    BAA Required: This tool is designed for PHI processing under BAA
    """
    # Verify API key is present in environment
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[red]Error: ANTHROPIC_API_KEY not found in environment[/red]")
        console.print("[yellow]Set it in ~/.zshrc or export it in your shell[/yellow]")
        raise click.Abort()

# ============================================================================
# REGISTER ACTIVE COMMANDS
# ============================================================================

cli.add_command(cds)        # Pediatric clinical decision support
cli.add_command(handout)    # Parent education materials
cli.add_command(note)       # Pediatric documentation
cli.add_command(ddx)        # Age-appropriate differential diagnosis
cli.add_command(parse)      # Parse labs/imaging/documents
cli.add_command(drug)       # Weight-based drug dosing

# ============================================================================
# TEMPORARILY DISABLED COMMANDS
# ============================================================================
# These commands are commented out but files are preserved for future use
# Uncomment the imports above and add_command lines below to re-enable

# cli.add_command(prior_auth)  # Prior authorization letters
# cli.add_command(referral)    # Referral letters

if __name__ == "__main__":
    cli()
