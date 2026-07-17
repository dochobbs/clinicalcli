"""
Model Manager - Support for Anthropic Claude, OpenAI GPT, and local models

Allows switching between cloud-based models (Claude, GPT) and local models for offline use.
Supports: Anthropic Claude, OpenAI GPT-5.1, Ollama, and LM Studio.
"""

import os
import requests
from typing import Optional, Dict, Any
from rich.console import Console

console = Console()

class ModelManager:
    """Manage model selection and API calls."""

    # Available models
    ANTHROPIC_MODELS = [
        "claude-sonnet-4-5-20250929",  # Latest Sonnet (best quality, default)
        "claude-haiku-4-5-20251001",   # Latest Haiku (faster)
    ]

    OPENAI_MODELS = [
        "gpt-5.1",
    ]

    def __init__(self):
        self.current_model = "claude-sonnet-4-5-20250929"  # Default to Sonnet (best quality)
        self.model_type = "anthropic"  # or "openai" or "ollama" or "lmstudio"
        self.ollama_base_url = "http://localhost:11434"  # Default Ollama URL
        self.lmstudio_base_url = "http://localhost:1234/v1"  # Default LM Studio URL

    def set_model(self, model_name: str):
        """Set the current model."""
        # Check if it's an Anthropic model
        if model_name in self.ANTHROPIC_MODELS:
            self.current_model = model_name
            self.model_type = "anthropic"
            console.print(f"[green]✓ Switched to Anthropic model: {model_name}[/green]")
            return True

        # Check if it's an OpenAI model
        if model_name in self.OPENAI_MODELS:
            # Verify API key is set
            if not os.getenv("OPENAI_API_KEY"):
                console.print("[red]✗ OPENAI_API_KEY not set[/red]")
                console.print("[dim]Set with: export OPENAI_API_KEY='sk-...'[/dim]")
                return False
            self.current_model = model_name
            self.model_type = "openai"
            console.print(f"[green]✓ Switched to OpenAI model: {model_name}[/green]")
            return True

        # Try LM Studio first (faster to check)
        if self.check_lmstudio_available():
            if self.check_lmstudio_model_exists(model_name):
                self.current_model = model_name
                self.model_type = "lmstudio"
                console.print(f"[green]✓ Switched to LM Studio model: {model_name}[/green]")
                console.print("[yellow]⚠️  Local models may be slower than Claude[/yellow]")
                console.print("[dim]Tip: Use smaller/quantized models (3B-8B) for better speed[/dim]")
                return True

        # Try Ollama
        if self.check_ollama_available():
            if self.check_ollama_model_exists(model_name):
                self.current_model = model_name
                self.model_type = "ollama"
                console.print(f"[green]✓ Switched to Ollama model: {model_name}[/green]")
                console.print("[yellow]⚠️  Local models may be slower than Claude[/yellow]")
                console.print("[dim]Tip: Use smaller/quantized models (3B-8B) for better speed[/dim]")
                return True

        # Model not found in any provider
        console.print(f"[yellow]⚠️  Model '{model_name}' not found[/yellow]")
        console.print("[dim]Check available models with: model list[/dim]")
        if not self.check_lmstudio_available() and not self.check_ollama_available():
            console.print("[dim]Neither LM Studio nor Ollama appears to be running[/dim]")
        return False

    def check_ollama_available(self) -> bool:
        """Check if Ollama is running."""
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False

    def check_ollama_model_exists(self, model_name: str) -> bool:
        """Check if an Ollama model is available locally."""
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                data = response.json()
                models = [m['name'].replace(':latest', '') for m in data.get('models', [])]
                # Check with and without :latest suffix
                return model_name in models or f"{model_name}:latest" in [m['name'] for m in data.get('models', [])]
            return False
        except:
            return False

    def check_lmstudio_available(self) -> bool:
        """Check if LM Studio is running."""
        try:
            response = requests.get(f"{self.lmstudio_base_url}/models", timeout=2)
            return response.status_code == 200
        except:
            return False

    def check_lmstudio_model_exists(self, model_name: str) -> bool:
        """Check if an LM Studio model is loaded."""
        try:
            response = requests.get(f"{self.lmstudio_base_url}/models", timeout=2)
            if response.status_code == 200:
                data = response.json()
                models = [m['id'] for m in data.get('data', [])]
                return model_name in models
            return False
        except:
            return False

    def list_available_models(self):
        """List all available models."""
        console.print("\n[cyan]═══ Available Models ═══[/cyan]\n")

        # Anthropic models
        console.print("[yellow]Anthropic Claude (Cloud):[/yellow]")
        for model in self.ANTHROPIC_MODELS:
            marker = "✓" if model == self.current_model and self.model_type == "anthropic" else " "
            console.print(f"  [{marker}] {model}")

        # OpenAI models
        console.print("\n[yellow]OpenAI (Cloud):[/yellow]")
        if os.getenv("OPENAI_API_KEY"):
            for model in self.OPENAI_MODELS:
                marker = "✓" if model == self.current_model and self.model_type == "openai" else " "
                console.print(f"  [{marker}] {model}")
        else:
            console.print("  [dim]OPENAI_API_KEY not set[/dim]")
            console.print("  [dim]Set with: export OPENAI_API_KEY='sk-...'[/dim]")

        # LM Studio models
        console.print("\n[yellow]LM Studio (Local):[/yellow]")
        if self.check_lmstudio_available():
            try:
                response = requests.get(f"{self.lmstudio_base_url}/models", timeout=2)
                if response.status_code == 200:
                    data = response.json()
                    models = data.get('data', [])
                    if models:
                        for model in models:
                            model_id = model['id']
                            marker = "✓" if model_id == self.current_model and self.model_type == "lmstudio" else " "
                            console.print(f"  [{marker}] {model_id}")
                    else:
                        console.print("  [dim]No models loaded[/dim]")
                        console.print("  [dim]Load a model in LM Studio UI[/dim]")
            except Exception as e:
                console.print(f"  [red]Error listing models: {e}[/red]")
        else:
            console.print("  [dim]LM Studio not running[/dim]")
            console.print("  [dim]Start LM Studio and load a model[/dim]")

        # Ollama models
        console.print("\n[yellow]Ollama (Local):[/yellow]")
        if self.check_ollama_available():
            try:
                response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=2)
                if response.status_code == 200:
                    data = response.json()
                    models = data.get('models', [])
                    if models:
                        for model in models:
                            model_name = model['name'].replace(':latest', '')
                            marker = "✓" if model_name == self.current_model and self.model_type == "ollama" else " "
                            size = model.get('size', 0) / (1024**3)  # Convert to GB
                            console.print(f"  [{marker}] {model_name} ({size:.1f} GB)")
                    else:
                        console.print("  [dim]No models installed[/dim]")
                        console.print("  [dim]Install with: ollama pull llama3.2[/dim]")
            except Exception as e:
                console.print(f"  [red]Error listing models: {e}[/red]")
        else:
            console.print("  [dim]Ollama not running[/dim]")
            console.print("  [dim]Start with: ollama serve[/dim]")

        console.print()

    def get_current_model_info(self) -> str:
        """Get current model info string."""
        if self.model_type == "anthropic":
            return f"Claude ({self.current_model})"
        elif self.model_type == "openai":
            return f"OpenAI ({self.current_model})"
        elif self.model_type == "lmstudio":
            return f"LM Studio ({self.current_model})"
        else:
            return f"Ollama ({self.current_model})"

    def call_model(self, system_prompt: str, user_message: str, max_tokens: int = 4096) -> str:
        """
        Call the currently selected model.

        Routes to Anthropic, OpenAI, LM Studio, or Ollama based on current selection.
        """
        if self.model_type == "anthropic":
            return self._call_anthropic(system_prompt, user_message, max_tokens)
        elif self.model_type == "openai":
            return self._call_openai(system_prompt, user_message, max_tokens)
        elif self.model_type == "lmstudio":
            return self._call_lmstudio(system_prompt, user_message, max_tokens)
        else:
            return self._call_ollama(system_prompt, user_message, max_tokens)

    def _call_anthropic(self, system_prompt: str, user_message: str, max_tokens: int) -> str:
        """Call Anthropic Claude API with streaming."""
        import anthropic

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")

        client = anthropic.Anthropic(api_key=api_key)

        # Stream the response for better UX
        full_text = []

        with client.messages.stream(
            model=self.current_model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        ) as stream:
            for text in stream.text_stream:
                print(text, end='', flush=True)
                full_text.append(text)

        print()  # Add newline at end
        return ''.join(full_text)

    def _call_openai(self, system_prompt: str, user_message: str, max_tokens: int) -> str:
        """Call OpenAI API with streaming."""
        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")

        client = OpenAI(api_key=api_key)

        # Stream the response for better UX
        full_text = []

        stream = client.chat.completions.create(
            model=self.current_model,
            max_completion_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                text = chunk.choices[0].delta.content
                print(text, end='', flush=True)
                full_text.append(text)

        print()  # Add newline at end
        return ''.join(full_text)

    def _call_lmstudio(self, system_prompt: str, user_message: str, max_tokens: int) -> str:
        """Call LM Studio API with streaming (OpenAI-compatible)."""
        try:
            response = requests.post(
                f"{self.lmstudio_base_url}/chat/completions",
                json={
                    "model": self.current_model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    "max_tokens": max_tokens,
                    "temperature": 0.7,
                    "stream": True,  # Enable streaming
                },
                timeout=120,
                stream=True  # Enable response streaming
            )

            if response.status_code == 200:
                full_text = []
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            data_str = line[6:]  # Remove 'data: ' prefix
                            if data_str.strip() == '[DONE]':
                                break
                            try:
                                import json
                                data = json.loads(data_str)
                                if 'choices' in data and len(data['choices']) > 0:
                                    delta = data['choices'][0].get('delta', {})
                                    content = delta.get('content', '')
                                    if content:
                                        print(content, end='', flush=True)
                                        full_text.append(content)
                            except json.JSONDecodeError:
                                pass

                print()  # Add newline at end
                return ''.join(full_text)
            else:
                raise Exception(f"LM Studio API error: {response.status_code}")

        except requests.exceptions.Timeout:
            raise Exception("LM Studio request timed out - model may be too slow")
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to LM Studio - is it running?")
        except Exception as e:
            raise Exception(f"LM Studio error: {e}")

    def _call_ollama(self, system_prompt: str, user_message: str, max_tokens: int) -> str:
        """Call Ollama API with streaming."""
        try:
            # Combine system and user message for Ollama
            combined_message = f"{system_prompt}\n\n{user_message}"

            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json={
                    "model": self.current_model,
                    "prompt": combined_message,
                    "stream": True,  # Enable streaming
                    "options": {
                        "num_predict": max_tokens,
                    }
                },
                timeout=120,
                stream=True  # Enable response streaming
            )

            if response.status_code == 200:
                full_text = []
                for line in response.iter_lines():
                    if line:
                        try:
                            import json
                            data = json.loads(line)
                            text_chunk = data.get('response', '')
                            if text_chunk:
                                print(text_chunk, end='', flush=True)
                                full_text.append(text_chunk)
                        except json.JSONDecodeError:
                            pass

                print()  # Add newline at end
                return ''.join(full_text)
            else:
                raise Exception(f"Ollama API error: {response.status_code}")

        except requests.exceptions.Timeout:
            raise Exception("Ollama request timed out - model may be too slow")
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to Ollama - is it running?")
        except Exception as e:
            raise Exception(f"Ollama error: {e}")


# Global model manager instance
_model_manager = None

def get_model_manager() -> ModelManager:
    """Get or create the global model manager instance."""
    global _model_manager
    if _model_manager is None:
        _model_manager = ModelManager()
    return _model_manager
