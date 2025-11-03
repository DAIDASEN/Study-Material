# On-Policy Distillation — Beamer Slides

This folder contains an English Beamer presentation (`on_policy_distillation_beamer.tex`) that:
- Briefly motivates on-policy distillation
- Details the algorithmic flow and practical tips
- Explains why reverse KL divergence is often preferable (with visuals)

Images are loaded from the locally saved webpages’ asset folders:
- `On-Policy Distillation - Thinking Machines Lab_files/`
- `反向 KL 散度与正向 KL 散度 - 机器学习POD_files/`

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

## How to compile on Overleaf

1. Upload the following to your Overleaf project:
	 - `on_policy_distillation_beamer.tex`
	 - The two asset folders:
		 - `On-Policy Distillation - Thinking Machines Lab_files/`
		 - `反向 KL 散度与正向 KL 散度 - 机器学习POD_files/`
2. In Overleaf, open Menu → Compiler → choose “XeLaTeX” (or “LuaLaTeX”).
3. Click “Recompile” (run twice if needed).

Notes:
- The `.tex` uses `\graphicspath{...}` to find images in both folders; `\includegraphics{20240112163924.png}` will resolve automatically.
- If you hit issues with Unicode/space-containing folder names in Overleaf, a simple workaround is:
	- Create a new folder (e.g., `images/`) with ASCII name
	- Move the PNGs you use into it (on Overleaf) and update `\graphicspath{{images/}}`
	- Or change the `\includegraphics{...}` paths accordingly.

### Option B (most robust): pdfLaTeX-safe project

If you prefer to keep Overleaf’s default pdfLaTeX compiler, use the provided alternative file:

- `on_policy_distillation_beamer_overleaf_pdflatex.tex`

Steps:
1. Create an `images/` folder in Overleaf.
2. Upload these PNGs into `images/`:
	 - `20240112163924.png` (KL visual)
	 - `20240112163931.png` (KL intuition)
	 - `chess.png` (RL context)
3. Set Compiler to `pdfLaTeX` (default) and compile `on_policy_distillation_beamer_overleaf_pdflatex.tex`.

This version avoids Unicode paths and special fonts, making it compile without extra settings.

### If compile still produces no PDF

- Ensure the main TeX file is not empty and has `\begin{document} ... \end{document}` (it does).
- Delete or rename any existing `output.pdf` in the Overleaf project root (Overleaf won’t overwrite it).
- Open the full log and check for one of the common errors:
	- “Package fontspec Error” or “unicode-math” related → switch compiler to XeLaTeX (Option A) or use Option B.
	- “File not found” for PNGs → verify you uploaded images to the right folder name and that `\graphicspath` matches.

## Customize
- Edit the title/author/date in the preamble.
- Replace or add images with `\includegraphics{...}`; XeLaTeX supports the Unicode and spaces in the given folder names.
- If you prefer another theme, change `\usetheme{Madrid}`.

## References
- Thinking Machines Lab: On-Policy Distillation (local HTML)
- ML POD: Forward vs Reverse KL Divergence (本地保存)