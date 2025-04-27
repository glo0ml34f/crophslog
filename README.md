# 🛠️ VeinTap & CrophSlog

_Uncover the sludge, trace the veins — Lua code hygiene tools._

---

## 🩸 **VeinTap**

**VeinTap** extracts embedded Lua code from template files (ending in `.lua`) containing Lua code blocks wrapped in `<? ?>`. Each template compiles into a clean Lua file.

### 🚀 Usage
```bash
./utils/veintap.py --input-dir templates/ --output-dir compiled/
```

### 🔍 Features
- Extracts multi-line Lua code blocks from templates.
- Outputs one Lua file per template (`*_compiled.lua`).
- Emoji-filled logs & ASCII art.

---

## 🪣 **CrophSlog**

**CrophSlog** performs taint analysis on Lua codebases. It tracks data from **sources** to **sinks**, flagging insecure flows across `.lua` files.

### 🚀 Usage
```bash
./crophslog.py --base-dir lua_project/ --config config.yaml
```

### 🔍 Features
- Recursive taint analysis across `.lua` files.
- Configurable **sources**, **sinks**, **propagators**, **cleansers**.
- Markdown & JSON summaries with emoji logs & ASCII art.

---

## 🧰 Setup

```bash
make  # Builds dependencies for both tools
```

---

## 📖 Example Workflow
1. **VeinTap**: Extract Lua from templates.
2. **CrophSlog**: Analyze the extracted Lua files for taint flows.

Stay sludge-free. Trace the veins.

---

🖤 MIT License — Open, free, and friendly.


