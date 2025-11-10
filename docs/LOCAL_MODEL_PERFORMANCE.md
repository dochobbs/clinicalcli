# Local Model Performance Guide

## ⚠️ Performance Reality Check

**Local models are significantly slower than Claude.** This is expected and unavoidable. Here's why and what you can do about it.

---

## Why Local Models Are Slow

### Hardware Limitations
- **Claude:** Runs on Anthropic's optimized GPU clusters
- **Local:** Runs on your laptop CPU/GPU with limited RAM

### Model Size
- **Larger models** = Better quality but MUCH slower
- **Smaller models** = Faster but lower quality

### Example Response Times (Approximate)

| Model | Size | Response Time | Quality |
|-------|------|---------------|---------|
| **Claude Sonnet 4.5** | Cloud | 2-5 seconds | Excellent |
| **Claude Haiku** | Cloud | 1-2 seconds | Good |
| Llama 3.2 3B (Q4) | 3B | 10-30 seconds | Fair |
| Llama 3.1 8B (Q4) | 8B | 30-60 seconds | Good |
| Mistral 7B (Q4) | 7B | 30-60 seconds | Good |
| Llama 3.1 70B (Q4) | 70B | 2-5+ minutes | Very Good |

**⚠️ Local models take 5-10x longer than Claude minimum.**

---

## Recommendations for Clinical CLI

### ❌ **NOT Recommended for Clinical CLI**

Local models are generally **too slow for interactive clinical use**. The Clinical CLI is designed for quick lookups during patient care, and waiting 30-60 seconds per query defeats the purpose.

**Instead, use local models for:**
- Offline emergency reference (when nothing else is available)
- Learning/practicing when not time-sensitive
- Testing the CLI functionality
- Privacy-sensitive non-urgent scenarios

### ✅ **Recommended: Stick with Claude**

For actual clinical use:
```bash
./clinical-shell
⚕️  clinical> model claude-sonnet-4-5-20250929  # Best quality
⚕️  clinical> model claude-haiku-4-5-20251001   # Faster when needed
```

**Claude Haiku 4.5** is your best option when you need speed - it's:
- Still faster than ANY local model
- Better quality than local models
- Optimized for quick responses

---

## If You Must Use Local Models

### Choose the Smallest Model Possible

**For speed, use 3B models:**
```bash
# LM Studio
⚕️  clinical> model llama-3.2-3b-instruct

# Ollama
ollama pull llama3.2:3b
⚕️  clinical> model llama3.2:3b
```

**Avoid:**
- ❌ 70B+ models (too slow for interactive use)
- ❌ Q8 quantization (higher quality but very slow)
- ❌ Multiple models running simultaneously

### Quantization Levels

Models come in different quantization levels (compression):

| Quantization | Speed | Quality | Recommendation |
|--------------|-------|---------|----------------|
| Q2 | Very Fast | Poor | Too low quality |
| **Q4** | Fast | Good | **Best balance** ✅ |
| Q5 | Medium | Better | Acceptable |
| Q8 | Slow | Best | Too slow ❌ |
| F16 (full) | Very Slow | Excellent | Way too slow ❌ |

**Use Q4 quantization** for the best speed/quality tradeoff.

### LM Studio Performance Tips

1. **Use GPU acceleration** (if you have a dedicated GPU)
   - Go to Settings → Hardware
   - Enable GPU offloading
   - Set to use your GPU if available

2. **Limit context length**
   - Shorter context = faster responses
   - Set max tokens to 2048 instead of 4096

3. **Use smaller models**
   - Download Llama 3.2 3B (Q4 version)
   - Avoid 70B models on laptops

4. **Close other apps**
   - Free up RAM
   - Stop other local models

### Ollama Performance Tips

```bash
# Pull the smallest quantized version
ollama pull llama3.2:3b-instruct-q4_K_M

# Use in CLI
⚕️  clinical> model llama3.2:3b-instruct-q4_K_M
```

---

## Hardware Requirements for "Fast" Local Models

To get reasonable performance (< 15 seconds per response):

**Minimum:**
- **RAM:** 16GB
- **Model:** 3B parameters, Q4 quantization
- **Expected speed:** 10-20 seconds

**Recommended:**
- **RAM:** 32GB+
- **GPU:** Apple Silicon M1/M2/M3 or NVIDIA RTX 3060+
- **Model:** 3B-8B parameters, Q4 quantization
- **Expected speed:** 5-15 seconds

**Still 3-5x slower than Claude Haiku.**

---

## Reality Check: When to Use What

### Use Claude Sonnet When:
- ✅ You need accurate clinical information
- ✅ Working with actual patients
- ✅ Time matters (it's always faster)
- ✅ Quality matters (it's always better)

### Use Claude Haiku When:
- ✅ You need FAST responses
- ✅ Simple drug lookups
- ✅ Quick reference checks
- ✅ Still want good quality

### Use Local Models (LM Studio/Ollama) When:
- ✅ You're on a plane with no internet
- ✅ You're learning/practicing (not time-sensitive)
- ✅ You're in a privacy-critical situation
- ✅ You're testing the CLI without using API credits
- ✅ **You can wait 30-60 seconds per query**

---

## Example Session (Realistic Timing)

### With Claude Sonnet (Recommended)
```bash
⚕️  clinical> d amoxicillin --weight 52#
[2 seconds]
[Excellent response appears]

⚕️  clinical> cds 5yo with fever, ear pain
[3 seconds]
[Comprehensive clinical decision support]

Total time: 5 seconds ✅
```

### With Local Model (3B Q4)
```bash
⚕️  clinical> model llama-3.2-3b-instruct
✓ Switched to LM Studio model
⚠️  Local models may be slower than Claude

⚕️  clinical> d amoxicillin --weight 52#
[20 seconds...]
[Fair quality response]

⚕️  clinical> cds 5yo with fever, ear pain
[30 seconds...]
[Basic clinical guidance, may miss nuances]

Total time: 50 seconds ⚠️
```

**10x slower, lower quality.**

---

## The Bottom Line

### For Clinical CLI: Use Claude

The Clinical CLI is designed for **fast, accurate clinical decision support**. Local models undermine both goals:

- **Too slow:** Defeats the "quick reference" purpose
- **Lower quality:** Risk missing important clinical details
- **Not worth it:** Even in offline scenarios, it's frustratingly slow

### Recommendation

```bash
./clinical-shell

# Default (best quality)
⚕️  clinical> model claude-sonnet-4-5-20250929

# When you need speed
⚕️  clinical> model claude-haiku-4-5-20251001

# Avoid local models for clinical use
```

---

## Alternative: Offline-First Design

If you truly need offline capability, consider:

1. **Pre-fetch common queries** to a local database
2. **Cache Claude responses** for repeated questions
3. **Download reference PDFs** for offline access
4. **Use specialized medical databases** designed for offline use

**Don't rely on local LLMs for time-sensitive clinical queries.**

---

## Updated Model List

We've simplified the Claude model list to the essentials:

```bash
⚕️  clinical> model
═══ Available Models ═══

Anthropic Claude (Cloud):
  [✓] claude-sonnet-4-5-20250929  # Best quality
  [ ] claude-haiku-4-5-20251001   # Faster

LM Studio (Local):
  [ ] llama-3.2-3b-instruct       # Slow but available offline

Ollama (Local):
  [ ] llama3.2:3b                 # Slow but available offline
```

**Only two Claude models now:**
- **Sonnet 4.5** - Best quality (default)
- **Haiku 3.5** - Fast when you need speed

Both are **always faster than local models.**

---

## Summary

- ⚠️ **Local models are slow** (5-10x slower than Claude minimum)
- ⚠️ **Local models have lower quality** (miss clinical nuances)
- ✅ **Use Claude Sonnet** for best quality (2-5 seconds)
- ✅ **Use Claude Haiku** when you need speed (1-2 seconds)
- 🆘 **Use local models** only as emergency offline fallback
- 💡 **Expectation:** Local = 30-60 seconds per query vs Claude = 2-5 seconds

**The local model option is there for offline emergencies, not regular use.**

---

**Updated:** November 9, 2025
**Status:** Performance expectations documented
**Recommendation:** Stick with Claude for clinical work
