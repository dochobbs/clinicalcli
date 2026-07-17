"""Shared utilities for Clinical CLI"""

import os
import base64
import mimetypes
from pathlib import Path
from typing import List, Dict, Any, Optional

import anthropic
import pyperclip
from PIL import Image
from pypdf import PdfReader
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Confirm

console = Console()

def get_anthropic_client():
    """Initialize and return Anthropic client"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        console.print("[red]Error: ANTHROPIC_API_KEY not set[/red]")
        raise ValueError("Missing API key")
    return anthropic.Anthropic(api_key=api_key)

def call_claude(system_prompt: str, user_message: str, model: str = "claude-sonnet-4-5-20250929") -> str:
    """
    Call current model (Claude or local) with system prompt and user message

    Args:
        system_prompt: System instructions for model
        user_message: User's clinical query/data
        model: Model to use (default: Sonnet 4.5) - DEPRECATED, uses model_manager instead

    Returns:
        Model's response as string
    """
    # Use model manager for routing
    from .model_manager import get_model_manager
    model_manager = get_model_manager()

    return model_manager.call_model(system_prompt, user_message)

def display_output(content: str, title: str = "Result"):
    """
    Display output in rich format

    Args:
        content: The text content to display
        title: Title for the panel
    """
    # Display in a panel
    console.print(Panel(Markdown(content), title=title, border_style="green"))
    console.print("\n[dim]Tip: Use 'copy' command to copy this to clipboard[/dim]")

def read_multiline_input(prompt: str = "Enter clinical information (Ctrl+D or Ctrl+Z when done):") -> str:
    """
    Read multiline input from user

    Args:
        prompt: Prompt message to display

    Returns:
        User's multiline input as string
    """
    console.print(f"[cyan]{prompt}[/cyan]")
    console.print("[dim](Type or paste your input, then press Ctrl+D on macOS/Linux or Ctrl+Z on Windows)[/dim]\n")

    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass

    return "\n".join(lines)

def format_phi_warning(mode: str = "full"):
    """
    Display PHI handling warning.

    Args:
        mode: "full" (detailed panel), "brief" (one-line), or "silent" (none)
    """
    if mode == "silent":
        return

    if mode == "brief":
        console.print("[yellow]⚠️  PHI Notice:[/yellow] Data sent to Anthropic under BAA")
        return

    # Default full warning
    warning = Panel(
        "[yellow]⚠️  PHI Warning[/yellow]\n\n"
        "This tool processes Protected Health Information (PHI).\n"
        "• Ensure you have proper authorization\n"
        "• Data is sent to Anthropic under BAA\n"
        "• Do not share outputs containing PHI insecurely",
        border_style="yellow",
        title="HIPAA Compliance"
    )
    console.print(warning)

def detect_file_type(file_path: str) -> str:
    """
    Detect file type from path

    Args:
        file_path: Path to file

    Returns:
        File type: 'image', 'pdf', or 'unknown'
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Get MIME type
    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type and mime_type.startswith('image/'):
        return 'image'
    elif path.suffix.lower() == '.pdf':
        return 'pdf'
    else:
        return 'unknown'

def process_image_file(file_path: str) -> Dict[str, Any]:
    """
    Process image file for Claude API

    Args:
        file_path: Path to image file

    Returns:
        Dictionary with image data formatted for Claude API
    """
    path = Path(file_path)

    # Verify it's an image
    try:
        img = Image.open(file_path)
        img.verify()
    except Exception as e:
        raise ValueError(f"Invalid image file: {e}")

    # Read and encode image
    with open(file_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    # Determine media type
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith('image/'):
        # Default to common types
        ext = path.suffix.lower()
        mime_map = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        mime_type = mime_map.get(ext, 'image/jpeg')

    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": mime_type,
            "data": image_data
        }
    }

def process_pdf_file(file_path: str) -> str:
    """
    Extract text from PDF file

    Args:
        file_path: Path to PDF file

    Returns:
        Extracted text content
    """
    try:
        reader = PdfReader(file_path)
        text_parts = []

        for i, page in enumerate(reader.pages, 1):
            page_text = page.extract_text()
            if page_text.strip():
                text_parts.append(f"--- Page {i} ---\n{page_text}")

        if not text_parts:
            raise ValueError(
                "No text could be extracted from PDF. This is likely a scanned/image-based PDF.\n"
                "Workaround: Convert the PDF to images (PNG/JPG) and use 'parse image.png' instead.\n"
                "Tools: Use Preview (macOS), Adobe Acrobat, or online converters to export as images."
            )

        return "\n\n".join(text_parts)

    except Exception as e:
        raise ValueError(f"Error processing PDF: {e}")

def call_claude_with_files(
    system_prompt: str,
    user_message: str,
    file_paths: Optional[List[str]] = None,
    model: str = "claude-sonnet-4-5-20250929"
) -> str:
    """
    Call Claude API with optional file attachments (images/PDFs)

    Args:
        system_prompt: System instructions for Claude
        user_message: User's clinical query/data
        file_paths: Optional list of file paths to include
        model: Claude model to use (default: Sonnet 4.5)

    Returns:
        Claude's response as string
    """
    from .model_manager import get_model_manager

    model_manager = get_model_manager()
    if model_manager.model_type != "anthropic":
        raise ValueError(
            "Image/file analysis is currently supported only with Anthropic "
            f"models, not {model_manager.get_current_model_info()}. "
            "No file data was sent. Switch to an Anthropic model before retrying."
        )

    client = get_anthropic_client()

    # Build content list
    content = []

    # Process files if provided
    if file_paths:
        for file_path in file_paths:
            console.print(f"[cyan]Processing file: {Path(file_path).name}[/cyan]")

            file_type = detect_file_type(file_path)

            if file_type == 'image':
                # Add image to content
                image_content = process_image_file(file_path)
                content.append(image_content)
                console.print(f"[green]✓ Image processed[/green]")

            elif file_type == 'pdf':
                # Extract text and prepend to message
                pdf_text = process_pdf_file(file_path)
                pdf_header = f"[PDF Content from {Path(file_path).name}]\n\n{pdf_text}\n\n---\n\n"
                user_message = pdf_header + user_message
                console.print(f"[green]✓ PDF text extracted ({len(pdf_text)} chars)[/green]")

            else:
                console.print(f"[yellow]⚠ Unsupported file type, skipping: {file_path}[/yellow]")

    # Add text message
    content.append({
        "type": "text",
        "text": user_message
    })

    # Call API with streaming
    console.print("\n[cyan]Response:[/cyan]\n")

    full_text = []
    with client.messages.stream(
        model=model,
        max_tokens=4096,
        system=system_prompt,
        messages=[
            {"role": "user", "content": content}
        ]
    ) as stream:
        for text in stream.text_stream:
            print(text, end='', flush=True)
            full_text.append(text)

    print()  # Add newline at end
    return ''.join(full_text)
