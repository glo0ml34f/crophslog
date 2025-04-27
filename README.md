# 🪣 **CrophSlog**  
_Cleansing the clogged arteries of ancient Lua code._

```
    ██████╗██████╗  ██████╗ ██████╗ ██╗  ██╗███████╗██╗      ██████╗  ██████╗  ██████╗ 
    ██╔════╝██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝██╔════╝██║     ██╔═══██╗██╔════╝ ██╔═══██╗
    ██║     ██████╔╝██║   ██║██████╔╝█████╔╝ █████╗  ██║     ██║   ██║██║  ███╗██║   ██║
    ██║     ██╔═══╝ ██║   ██║██╔═══╝ ██╔═██╗ ██╔══╝  ██║     ██║   ██║██║   ██║██║   ██║
    ╚██████╗██║     ╚██████╔╝██║     ██║  ██╗███████╗███████╗╚██████╔╝╚██████╔╝╚██████╔╝
     ╚═════╝╚═╝      ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝ 
                                
    CrophSlog: Taint Analysis for Lua — Clean the Code Sludge!
```

## 💡 What is CrophSlog?

**CrophSlog** is your trusty sewer diver for Lua codebases. It performs **taint analysis**, tracking the flow of untrusted data (**sources**) through your code to dangerous operations (**sinks**). Like draining sludge from ancient pipes, it clears out the hidden risks in your Lua projects.

🪤 **Catch** the taints.  
🪠 **Clear** the paths.  
🧹 **Clean** the sludge.

## 🧩 Features

- 📁 **Recursive Directory Analysis**: Scans all `.lua` files under a specified directory.
- 🕸️ **Taint Tracking Engine**: Follows data from **sources** to **sinks**, identifying dangerous paths.
- 🚿 **Cleansers Recognition**: Knows when data gets cleaned, avoiding false positives.
- 🪢 **Taint Chains Display**: Shows how tainted data moves through your code, step-by-step.
- 📝 **Markdown Reports**: Pretty-prints results, complete with file paths and line numbers.
- 🧩 **JSON Export**: Outputs machine-readable summaries of taint chains.
- 🎨 **ASCII Art and Emojis**: Because code analysis doesn't have to be boring.

## 🛠️ Setup

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Create your `config.yaml`

```yaml
sources:
  - get_input
  - os.getenv
sinks:
  - os.execute
  - io.popen
propagators:
  - string.format
  - table.insert
cleansers:
  - sanitize_input
```

## 🚦 Usage

```bash
python crophslog.py --base-dir /path/to/lua/project --config /path/to/config.yaml
```

### Arguments:

- `--base-dir`: Root directory to recursively analyze.
- `--config`: Path to the YAML config defining **sources**, **sinks**, **propagators**, and **cleansers**.

## 🪣 Output Example

```
🗂️ File: ./scripts/vulnerable.lua
⚠️  Taint Chain:
  - Source: get_input() at line 5
  - Propagation via variable 'user_cmd'
  - Sink: os.execute() at line 15

🔥 Danger Level: High
```

### JSON Export:  
`crophslog_summary.json` contains full taint chains and metadata for further analysis.

## ❓ Why *CrophSlog*?

In the clogged pipelines of legacy Lua code lies a festering sludge of insecure data flows. **CrophSlog** dives into the depths, dredging up the muck and leaving your codebase sparkling (or at least safe).

## 🤝 Contributing

Want to help dredge deeper or make the sludge flow smoother? Fork, tweak, and send a PR!

## 🪶 License

MIT License — Open, free, and sludge-friendly.

---
