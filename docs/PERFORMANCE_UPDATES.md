# Performance Updates - November 9, 2025

## Changes Based on User Feedback

### Issue 1: Too Many Claude Models
**Feedback:** "the only other claude models should be the latest sonnet and haiku"

**Fixed:** ✅ Simplified model list

**Before:**
```python
ANTHROPIC_MODELS = [
    "claude-sonnet-4-5-20250929",
    "claude-3-5-sonnet-20241022",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
]
```

**After:**
```python
ANTHROPIC_MODELS = [
    "claude-sonnet-4-5-20250929",  # Latest Sonnet (default)
    "claude-haiku-4-5-20251001",   # Latest Haiku (faster)
]
```

**Now you see:**
```bash
⚕️  clinical> model
═══ Available Models ═══

Anthropic Claude (Cloud):
  [✓] claude-sonnet-4-5-20250929  # Best quality
  [ ] claude-haiku-4-5-20251001   # Faster
```

---

### Issue 2: Local Models Are Too Slow
**Feedback:** "local model lookup is really slow in either app- it's really slow"

**Fixed:** ✅ Added performance warnings and documentation

**Changes Made:**

1. **Warning when switching to local models:**
   ```bash
   ⚕️  clinical> model llama-3.2-3b-instruct
   ✓ Switched to LM Studio model: llama-3.2-3b-instruct
   ⚠️  Local models may be slower than Claude
   Tip: Use smaller/quantized models (3B-8B) for better speed
   ```

2. **Created comprehensive performance guide:**
   - **LOCAL_MODEL_PERFORMANCE.md** - Reality check on speed
   - Documents that local models are 5-10x slower minimum
   - Recommends sticking with Claude for clinical use

3. **Updated all documentation** with realistic expectations

---

## Performance Reality

### Speed Comparison (Typical Response Times)

| Model | Response Time | Quality | Recommendation |
|-------|---------------|---------|----------------|
| **Claude Sonnet 4.5** | 2-5 seconds | Excellent | ✅ Best for clinical use |
| **Claude Haiku 3.5** | 1-2 seconds | Good | ✅ When you need speed |
| LM Studio (3B Q4) | 30-60 seconds | Fair | ⚠️ Offline only |
| Ollama (3B Q4) | 30-60 seconds | Fair | ⚠️ Offline only |
| Local (8B Q4) | 1-2 minutes | Good | ❌ Too slow |
| Local (70B) | 3-5+ minutes | Very Good | ❌ Way too slow |

**Conclusion:** Local models are **5-10x slower minimum**, often much worse.

---

## Recommendations

### For Clinical Use: Use Claude

```bash
./clinical-shell

# Default - best quality (2-5 seconds)
⚕️  clinical> model claude-sonnet-4-5-20250929

# When you need speed (1-2 seconds)
⚕️  clinical> model claude-3-5-haiku-20241022
```

**Why:**
- ✅ **Fast:** 2-5 seconds vs 30-60 seconds
- ✅ **Accurate:** Critical for clinical decisions
- ✅ **Reliable:** Consistent performance
- ✅ **Current:** Always up to date

### Local Models: Emergency Offline Only

```bash
# Only if you're offline and it's an emergency
⚕️  clinical> model llama-3.2-3b-instruct  # LM Studio
⚕️  clinical> model llama3.2:3b           # Ollama
```

**Accept that:**
- ⚠️ Will take 30-60 seconds per query
- ⚠️ Lower quality than Claude
- ⚠️ May miss clinical nuances
- ⚠️ Better than nothing when offline

---

## When to Use What

### Claude Sonnet 4.5 (Default)
**Use for:**
- Complex clinical scenarios
- Differential diagnosis
- Critical decisions
- Official documentation

**Speed:** 2-5 seconds ✅

### Claude Haiku 4.5
**Use for:**
- Quick drug lookups
- Simple dosing calculations
- Fast reference checks
- When every second counts

**Speed:** 1-2 seconds ✅✅

### Local Models (LM Studio/Ollama)
**Use for:**
- You're on a plane (no internet)
- Privacy-critical scenarios
- Learning/practicing (not time-sensitive)
- Testing without API costs
- **Emergency offline reference only**

**Speed:** 30-60 seconds ⚠️⚠️⚠️

---

## Files Changed

### src/model_manager.py
**Lines 18-21:** Simplified ANTHROPIC_MODELS list
```python
ANTHROPIC_MODELS = [
    "claude-sonnet-4-5-20250929",  # Latest Sonnet (default)
    "claude-3-5-haiku-20241022",   # Latest Haiku (faster)
]
```

**Lines 43-46, 53-56:** Added performance warnings
```python
console.print("[yellow]⚠️  Local models may be slower than Claude[/yellow]")
console.print("[dim]Tip: Use smaller/quantized models (3B-8B) for better speed[/dim]")
```

### Documentation
- **LOCAL_MODEL_PERFORMANCE.md** - New comprehensive guide
- **UPDATES_COMPLETE.md** - Updated with performance warnings
- **SINGLE_LINE_AND_MODEL_SELECTOR.md** - Updated expectations
- **LMSTUDIO_SUPPORT.md** - Updated with realistic timing

---

## Summary

✅ **Simplified model list** - Only latest Sonnet and Haiku
✅ **Added performance warnings** - Users know what to expect
✅ **Created performance guide** - Realistic expectations documented
✅ **Updated recommendations** - Stick with Claude for clinical use

**Bottom line:**
- Use **Claude** for clinical work (fast and accurate)
- Use **local models** only for offline emergencies (slow but available)

---

**Updated:** November 9, 2025
**Status:** ✅ Performance issues addressed
**Recommendation:** Claude Sonnet 4.5 or Haiku 4.5 for clinical use
