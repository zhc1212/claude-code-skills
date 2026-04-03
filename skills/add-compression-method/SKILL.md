---
name: add-compression-method
description: Add a new compression strategy to SVD_LLM. Use when user says "添加压缩方法", "add compression method", "new method", "implement compression", or wants to add a new SVD/low-rank compression approach.
user_invocable: true
---

# Add Compression Method

Guide for implementing a new compression strategy in SVD_LLM.

## Steps

1. **Understand the method**: Clarify the compression approach with the user — what's the mathematical formulation? How does it differ from the existing `svd_llm_w` method?

2. **Implement the compression function**: Add `compress_model_<name>()` in `src/compress/`. Follow the pattern of existing methods in `src/compress/whitening.py` and `src/compress/compress_model.py`.

3. **Register the method**: Add the new method name to the CLI argument parser in `scripts/compress.py`.

4. **Add tests**: Create tests in `tests/` following the patterns in `test_whitening.py` and `test_replace.py`. Include:
   - Unit tests for the core math (CPU-only, no `@pytest.mark.integration`)
   - Integration tests for end-to-end compression (mark with `@pytest.mark.integration`)

5. **Run tests**:
```bash
pytest tests/ -m "not integration" -v
```

6. **Update docs**: Add the method description to `README.md` and `docs/technical_report.md`.

## Key files to reference
- `src/compress/whitening.py` — whitening + SVD logic
- `src/compress/compress_model.py` — compression pipeline
- `src/model/replace.py` — CompressedLinear layer
- `src/model/loader.py` — rank computation
