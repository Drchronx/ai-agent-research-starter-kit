---
name: paper-writing-assistant-typesetting
description: Automatically consolidate literature metadata, generate a paper outline, normalize citation keys, and output LaTeX, Word, and PDF manuscript drafts.
---

# Paper Writing Assistant Typesetting

Use this skill from `F:\Python\课程\OpenClaw\cnki\skills\paper-writing-assistant-typesetting`.

## Workflow

1. Install dependencies:

```powershell
python -m pip install -r scripts/requirements.txt
```

2. Build the manuscript package:

```powershell
python scripts/build_paper_package.py assets/sample_references.csv --title "数字化转型与企业创新效率" --author "OpenClaw" --outline-json assets/sample_outline.json --output-dir reports/paper-package-demo
```

3. Read the generated files:
- `generated_outline.json`
- `reference_catalog.csv`
- `references.bib`
- `manuscript.tex`
- `manuscript.docx`
- `manuscript.pdf`

## Behavior

- The script accepts literature metadata from `csv/xlsx/xls`.
- Required columns are `authors`, `title`, `year`, and `journal`.
- `doi` and `abstract` are optional but improve generated section guidance.
- Citation keys are normalized automatically to stable BibTeX identifiers.
- If no custom outline is passed, the script falls back to a standard empirical-paper structure.
- PDF export is generated directly by Python and does not depend on local Word or LaTeX compilation.

## Parameters

Use the default section structure:

```powershell
python scripts/build_paper_package.py path\to\references.xlsx --title "论文标题"
```

Specify a custom author and output path:

```powershell
python scripts/build_paper_package.py path\to\refs.csv --title "论文标题" --author "张三" --output-dir reports\paper-final
```

Use a custom outline JSON:

```powershell
python scripts/build_paper_package.py path\to\refs.csv --title "论文标题" --outline-json path\to\outline.json
```
