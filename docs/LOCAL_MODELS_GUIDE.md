# How to Use Local Models with Clinical CLI

**Complete guide to running Clinical CLI offline with LM Studio or Ollama**

This guide covers everything you need to know about using local AI models with Clinical CLI, including setup, usage, and performance expectations.

---

## 📋 Table of Contents

1. [Why Use Local Models?](#why-use-local-models)
2. [Before You Start: Important Considerations](#before-you-start-important-considerations)
3. [Option 1: LM Studio (Recommended for Beginners)](#option-1-lm-studio-recommended-for-beginners)
4. [Option 2: Ollama (For Command Line Users)](#option-2-ollama-for-command-line-users)
5. [Using Local Models in Clinical CLI](#using-local-models-in-clinical-cli)
6. [Recommended Models](#recommended-models)
7. [Performance Tips](#performance-tips)
8. [Troubleshooting](#troubleshooting)
9. [When to Use What](#when-to-use-what)

---

## Why Use Local Models?

### ✅ **Benefits**
- **Works offline** - No internet required
- **Privacy** - Data stays on your computer
- **Free** - No API costs
- **Control** - Choose exactly which model to use
- **Learning** - Practice without using API credits

### ⚠️ **Tradeoffs**
- **Slower** - 5-10x slower than Claude (30-60 seconds per query)
- **Lower quality** - Less accurate, may miss clinical nuances
- **Resource intensive** - Uses RAM, CPU, battery
- **Disk space** - Models are 2-70+ GB each

---

## Before You Start: Important Considerations

### ⚠️ Performance Reality Check

**Local models are SIGNIFICANTLY slower than Claude:**

| Model | Response Time | Quality | Use Case |
|-------|---------------|---------|----------|
| Claude Haiku 4.5 | 1-2 sec ⚡⚡⚡ | Excellent | Recommended for clinical use |
| Claude Sonnet 4.5 | 2-5 sec ⚡⚡ | Outstanding | Complex cases |
| Local 3B (Q4) | 10-30 sec ⚠️ | Fair | Offline emergency only |
| Local 7B (Q4) | 30-60 sec ⚠️ | Good | Offline emergency only |

**⚠️ For actual clinical use, we strongly recommend using Claude Haiku 4.5 (the default).** Local models are best reserved for:
- Offline emergencies (plane, remote areas)
- Learning and practice sessions
- Privacy-critical situations
- Testing without API costs

### Hardware Requirements

**Minimum (for usable performance):**
- **RAM:** 16GB
- **Storage:** 10GB free
- **Model size:** 3B parameters, Q4 quantization
- **Expected speed:** 10-20 seconds per response

**Recommended:**
- **RAM:** 32GB+
- **Storage:** 50GB+ free
- **GPU:** Apple Silicon M1/M2/M3 or NVIDIA RTX 3060+
- **Model size:** 3B-8B parameters, Q4 quantization
- **Expected speed:** 5-15 seconds per response

---

## Option 1: LM Studio (Recommended for Beginners)

**LM Studio** provides a user-friendly GUI for running local models. Perfect if you prefer clicking over typing.

### Step 1: Install LM Studio

1. Download from: **https://lmstudio.ai**
2. Install the application (macOS, Windows, or Linux)
3. Open LM Studio

### Step 2: Download a Model

1. Click the **"Search"** tab (🔍 icon)
2. Search for a recommended model:
   - `llama-3.2-3b-instruct` (fastest, 3GB)
   - `mistral-7b-instruct` (balanced, 7GB)
   - `llama-3.1-8b-instruct` (higher quality, 8GB)

3. Look for **Q4 quantization** versions:
   - `llama-3.2-3b-instruct-q4_K_M.gguf` ✅ (fastest)
   - Avoid F16 or Q8 (too slow) ❌

4. Click **Download** button
5. Wait for download to complete (may take 5-20 minutes)

### Step 3: Load the Model

1. Click the **"Chat"** tab (💬 icon)
2. At the top, click **"Select a model to load"**
3. Choose your downloaded model
4. Click **"Load model"**
5. Wait for status to show **"Server started"** (bottom right)

### Step 4: Use in Clinical CLI

```bash
cd /path/to/clinicalcli
./clinical-shell

⚕️  clinical> model
═══ Available Models ═══

Anthropic Claude (Cloud):
  [✓] claude-haiku-4-5-20251001    # Default, fast
  [ ] claude-sonnet-4-5-20250929   # Best quality

LM Studio (Local):
  [ ] llama-3.2-3b-instruct        # Your loaded model!

⚕️  clinical> model llama-3.2-3b-instruct
✓ Switched to LM Studio model: llama-3.2-3b-instruct
⚠️  Local models may be slower than Claude
Tip: Use smaller/quantized models (3B-8B) for better speed

⚕️  clinical> d amoxicillin --weight 52#
# Now using local model offline!
```

### LM Studio Configuration Tips

1. **GPU Acceleration** (Settings → Hardware)
   - Enable GPU offloading if you have a dedicated GPU
   - Set GPU layers to max for faster performance

2. **Context Length** (Chat Settings)
   - Set to 2048 tokens instead of 4096 for faster responses
   - Clinical queries rarely need more than 2048 tokens

3. **Keep Model Loaded**
   - Leave LM Studio running when using Clinical CLI
   - Model stays in memory for faster subsequent queries

---

## Option 2: Ollama (For Command Line Users)

**Ollama** is a command-line tool for running local models. Great for automation and scripting.

### Step 1: Install Ollama

**macOS/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download from: https://ollama.com/download

**Verify installation:**
```bash
ollama --version
```

### Step 2: Download a Model

**Quick start (3B model, fastest):**
```bash
ollama pull llama3.2:3b
```

**Other options:**
```bash
# Balanced (7B)
ollama pull mistral:7b-instruct-q4_K_M

# Higher quality (8B)
ollama pull llama3.1:8b-instruct-q4_K_M

# Medical-focused (if available)
ollama pull biomistral:7b-q4_K_M
```

**List installed models:**
```bash
ollama list
```

### Step 3: Run Ollama Server

**Start server:**
```bash
ollama serve
```

**Or run in background (macOS/Linux):**
```bash
ollama serve &
```

### Step 4: Use in Clinical CLI

```bash
cd /path/to/clinicalcli
./clinical-shell

⚕️  clinical> model
═══ Available Models ═══

Anthropic Claude (Cloud):
  [✓] claude-haiku-4-5-20251001    # Default, fast
  [ ] claude-sonnet-4-5-20250929   # Best quality

Ollama (Local):
  [ ] llama3.2:3b (2.0 GB)         # Fast
  [ ] mistral:7b-instruct (4.1 GB) # Balanced

⚕️  clinical> model llama3.2:3b
✓ Switched to Ollama model: llama3.2:3b
⚠️  Local models may be slower than Claude

⚕️  clinical> cds 5yo with fever, ear pain
# Using local Ollama model offline!
```

### Ollama Configuration Tips

**Customize performance:**
```bash
# Set environment variables
export OLLAMA_NUM_PARALLEL=1        # Number of concurrent requests
export OLLAMA_MAX_LOADED_MODELS=1   # Keep only 1 model in memory
export OLLAMA_FLASH_ATTENTION=1     # Enable flash attention (faster)
```

**Manage models:**
```bash
ollama list              # Show installed models
ollama rm llama3.2       # Remove a model
ollama ps                # Show running models
ollama stop llama3.2     # Unload a model from memory
```

---

## Using Local Models in Clinical CLI

### Switching Between Models

**Check available models:**
```bash
⚕️  clinical> model
```

**Switch to local model:**
```bash
⚕️  clinical> model llama-3.2-3b-instruct     # LM Studio
⚕️  clinical> model llama3.2:3b               # Ollama
```

**Switch back to Claude:**
```bash
⚕️  clinical> model claude-haiku-4-5-20251001
```

### All Commands Work Offline

Once you've switched to a local model, **all Clinical CLI commands work offline:**

```bash
# Drug lookup
⚕️  clinical> d amoxicillin --weight 52# --age 5yo

# Quick dose
⚕️  clinical> dose ibuprofen 40#

# Clinical decision support
⚕️  clinical> cds 5yo with fever, ear pain, decreased hearing

# Differential diagnosis
⚕️  clinical> ddx 5yo with fever, ear pain

# Clinical note
⚕️  clinical> note 5yo with AOM, starting amoxicillin

# Drug comparison
⚕️  clinical> compare amoxicillin cefdinir

# All work completely offline!
```

### Hybrid Workflow (Recommended)

Use local models for drafts, then verify with Claude for critical decisions:

```bash
./clinical-shell

# Start with local model for quick draft
⚕️  clinical> model llama-3.2-3b-instruct
⚕️  clinical> cds 5yo with fever, ear pain
[Review local response - takes 20 seconds]

# Verify with Claude for accuracy
⚕️  clinical> model claude-sonnet-4-5-20250929
⚕️  clinical> cds 5yo with fever, ear pain
[Get authoritative answer - takes 3 seconds]

# Use whichever response is better
⚕️  clinical> copy
```

---

## Recommended Models

### For Speed (3B Parameters)

**Best choice if you want the fastest local model:**

| Model | Size | Speed | Quality | Download |
|-------|------|-------|---------|----------|
| Llama 3.2 3B (Q4) | ~2GB | 10-20s | Fair | **Best option** ✅ |
| Phi-3 Mini 4K (Q4) | ~2GB | 10-20s | Fair | Medical knowledge |

**LM Studio:**
- Search: `llama-3.2-3b-instruct-q4`
- Download Q4_K_M version

**Ollama:**
```bash
ollama pull llama3.2:3b
```

### For Balance (7-8B Parameters)

**Better quality, still reasonable speed:**

| Model | Size | Speed | Quality | Download |
|-------|------|-------|---------|----------|
| Llama 3.1 8B (Q4) | ~5GB | 30-60s | Good | General purpose |
| Mistral 7B (Q4) | ~4GB | 30-60s | Good | Excellent reasoning |
| BioMistral 7B (Q4) | ~4GB | 30-60s | Good | Medical-focused |

**LM Studio:**
- Search: `llama-3.1-8b-instruct-q4` or `mistral-7b-instruct-q4`

**Ollama:**
```bash
ollama pull llama3.1:8b
ollama pull mistral:7b-instruct
```

### For Quality (70B+ Parameters)

**⚠️ NOT RECOMMENDED** - Too slow for interactive clinical use (2-5+ minutes per response)

Only consider if:
- You have a powerful GPU
- You're doing non-time-sensitive batch work
- You need offline capability and can wait

---

## Performance Tips

### 1. Choose the Right Quantization

**What is quantization?**
Models are compressed to run faster with less memory. Lower numbers = faster but lower quality.

| Quantization | Speed | Quality | Recommendation |
|--------------|-------|---------|----------------|
| Q2 | Very Fast | Poor | Too low quality ❌ |
| **Q4_K_M** | Fast | Good | **Best balance** ✅ |
| Q5 | Medium | Better | Acceptable |
| Q8 | Slow | Best | Too slow for interactive use ❌ |

**Always choose Q4_K_M versions** for Clinical CLI.

### 2. Reduce Context Length

**LM Studio:**
- Chat Settings → Max Response Length → Set to 2048

**Ollama:**
- Use smaller `num_predict` in environment config
- Clinical queries rarely need more than 2048 tokens

### 3. Close Other Apps

- Free up RAM by closing browsers, IDEs, etc.
- Stop other local AI tools
- Quit background applications

### 4. Use GPU Acceleration (If Available)

**LM Studio:**
- Settings → Hardware → Enable GPU offloading
- Set GPU layers to maximum

**Ollama:**
- Automatically uses GPU if detected
- Check with: `ollama ps` (shows GPU usage)

### 5. Keep Models Loaded

- Leave LM Studio or Ollama running
- Models stay in memory for subsequent queries
- First query is slow (loading), next queries are faster

---

## Troubleshooting

### "Model not found" Error

**LM Studio:**
1. Make sure model is **loaded** in the Chat tab (not just downloaded)
2. Check model name matches exactly
3. Use `model` command to see available models

**Ollama:**
```bash
# List installed models
ollama list

# If model not installed, pull it
ollama pull llama3.2:3b
```

### "Cannot connect" Error

**LM Studio:**
1. Check LM Studio is running
2. Make sure model is loaded (Chat tab)
3. Look for "Server started" message at bottom
4. Default URL: http://localhost:1234

**Ollama:**
```bash
# Check if Ollama is running
ollama list

# If not running, start it
ollama serve
```

### Slow Performance

**If responses take 60+ seconds:**

1. **Use smaller model**
   - Switch to 3B model: `ollama pull llama3.2:3b`

2. **Check quantization**
   - Make sure you have Q4 version (not Q8 or F16)

3. **Close other apps**
   - Free up RAM and CPU

4. **Check hardware**
   - Minimum 16GB RAM recommended
   - GPU acceleration helps significantly

5. **Consider using Claude instead**
   - If time matters, Claude is always faster (1-2 seconds)

### Model Takes Forever to Load

**First-time loading is slow (30-60 seconds):**
- This is normal for large models
- Subsequent queries are faster
- Leave model loaded between queries

**If loading fails:**
- Check available RAM (`Activity Monitor` on Mac, `Task Manager` on Windows)
- Try smaller model (3B instead of 7B)
- Close memory-intensive applications

### Low Quality Responses

**If responses are poor quality:**

1. **Try larger model**
   - 7B or 8B models are better than 3B

2. **Check quantization**
   - Q4 or Q5 are better than Q2

3. **Verify with Claude**
   - Use Claude for critical clinical decisions

4. **Remember limitations**
   - Local models are not as accurate as Claude
   - Use for drafts, not final medical advice

---

## When to Use What

### Use Claude Haiku 4.5 (Default) When:
- ✅ You have internet connection
- ✅ Time matters (1-2 second responses)
- ✅ Working with actual patients
- ✅ Need accurate clinical information
- ✅ Quality is important
- ✅ **This should be your default choice**

### Use Claude Sonnet 4.5 When:
- ✅ Complex medical cases
- ✅ Need highest accuracy
- ✅ Critical clinical decisions
- ✅ Official documentation
- ✅ When you can wait 2-5 seconds for best quality

### Use Local Models (LM Studio/Ollama) When:
- ✅ Completely offline (airplane, remote location)
- ✅ Learning and practice (no API costs)
- ✅ Privacy-critical situations
- ✅ Testing CLI functionality
- ✅ Non-time-sensitive queries
- ✅ **You can wait 30-60 seconds per response**
- ⚠️ **NOT for actual clinical care** (too slow, lower quality)

---

## Comparison Chart

### Response Time Comparison

```
Claude Haiku 4.5:    ⚡ [====] 1-2 seconds
Claude Sonnet 4.5:   ⚡⚡ [========] 2-5 seconds
Local 3B (Q4):       ⏳ [================================] 10-30 seconds
Local 7B (Q4):       ⏳⏳ [================================================================] 30-60 seconds
```

### Quality Comparison

```
Claude Sonnet 4.5:   ★★★★★ Excellent (best)
Claude Haiku 4.5:    ★★★★☆ Very Good
Local 7B (Q4):       ★★★☆☆ Good (acceptable)
Local 3B (Q4):       ★★☆☆☆ Fair (basic)
```

### Recommended Use Cases

| Scenario | Recommended Model | Alternative |
|----------|------------------|-------------|
| Quick drug lookup | Claude Haiku 4.5 | Local 3B (if offline) |
| Complex CDS | Claude Sonnet 4.5 | Claude Haiku 4.5 |
| On airplane | Local 3B (Q4) | None (offline) |
| Learning/practice | Local 3B (Q4) | Claude Haiku 4.5 |
| Actual patient care | Claude Haiku/Sonnet | Never use local |
| Privacy-critical | Local 7B (Q4) | Local 3B (Q4) |

---

## Quick Start Cheat Sheet

### LM Studio Quick Start
```bash
# 1. Download LM Studio from lmstudio.ai
# 2. Open LM Studio → Search → Download "llama-3.2-3b-instruct-q4"
# 3. Chat tab → Load model → Wait for "Server started"
# 4. Use in Clinical CLI:

./clinical-shell
⚕️  clinical> model llama-3.2-3b-instruct
⚕️  clinical> d amoxicillin --weight 52#
```

### Ollama Quick Start
```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Download model
ollama pull llama3.2:3b

# 3. Start server
ollama serve

# 4. Use in Clinical CLI
./clinical-shell
⚕️  clinical> model llama3.2:3b
⚕️  clinical> cds 5yo with fever
```

### Switch Back to Claude
```bash
⚕️  clinical> model claude-haiku-4-5-20251001
✓ Switched to Anthropic model
# Back to fast, high-quality responses!
```

---

## Summary

### Key Takeaways

1. **Local models are much slower than Claude** (5-10x)
2. **Local models have lower quality** than Claude
3. **Use local models for offline emergencies only**
4. **Claude Haiku 4.5 is the recommended default** (fast + accurate)
5. **LM Studio is easier for beginners** (GUI)
6. **Ollama is better for automation** (CLI)
7. **Q4 quantization is the best balance** (speed vs quality)
8. **3B models are fastest** (10-20 seconds)
9. **Always verify critical decisions with Claude**
10. **For clinical use, stick with Claude**

### Bottom Line

**Local models are a nice option for offline scenarios, but Clinical CLI is designed for fast, accurate clinical support. For best results, use the default Claude Haiku 4.5 model.**

If you absolutely must work offline, local models will work but expect:
- 10-30 second responses (3B models)
- 30-60 second responses (7B models)
- Lower accuracy than Claude
- Occasional mistakes or omissions

**For actual patient care, always use Claude.**

---

## Additional Resources

- **LM Studio:** https://lmstudio.ai
- **Ollama:** https://ollama.com
- **Model Hub:** https://huggingface.co/models?library=gguf
- **Performance Guide:** [LOCAL_MODEL_PERFORMANCE.md](LOCAL_MODEL_PERFORMANCE.md)
- **LM Studio Details:** [LMSTUDIO_SUPPORT.md](LMSTUDIO_SUPPORT.md)

---

**Updated:** November 10, 2025
**Status:** Complete guide for local model usage
**Recommendation:** Use Claude for clinical work, local models for offline emergencies only
