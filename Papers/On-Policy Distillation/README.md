# On-Policy Distillation — Beamer Slides

This folder contains an English Beamer presentation (`on_policy_distillation_beamer.tex`) that:
- Briefly motivates on-policy distillation
- Details the algorithmic flow and practical tips
- Explains why reverse KL divergence is often preferable (with visuals)

Images are loaded from the locally saved webpages’ asset folders:
- `On-Policy Distillation - Thinking Machines Lab_files/`
- `KL&Reverse_KL.html/`

## How to build (Windows, PowerShell)

The `.tex` uses XeLaTeX (handles Unicode paths and fonts). If you have MiKTeX or TeX Live installed, run:

```powershell
# From the folder: c:\Users\31670\Desktop\Study-Material\Papers\On-Policy Distillation
xelatex -interaction=nonstopmode .\on_policy_distillation_beamer.tex
xelatex -interaction=nonstopmode .\on_policy_distillation_beamer.tex
```

Notes:
- Two runs ensure references and TOC are settled.
- If you don’t have `xelatex` in PATH, open MiKTeX Console or TeX Live Manager to install/update.
- SVGs are not required; the slides only include PNG/JPG to avoid external converters.

## Customize
- Edit the title/author/date in the preamble.
- Replace or add images with `\includegraphics{...}`; XeLaTeX supports the Unicode and spaces in the given folder names.
- If you prefer another theme, change `\usetheme{Madrid}`.

## References
- Thinking Machines Lab: On-Policy Distillation (local HTML)
- ML POD: Forward vs Reverse KL Divergence (本地保存)