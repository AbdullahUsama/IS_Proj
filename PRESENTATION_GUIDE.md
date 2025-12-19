# Presentation Guide

## 📊 LaTeX Beamer Presentation + Mermaid Diagrams

This guide helps you compile the presentation on Overleaf with diagrams from draw.io.

---

## 🚀 Quick Start

### Step 1: Upload to Overleaf

1. Go to [Overleaf](https://www.overleaf.com/)
2. Create new project → "Blank Project"
3. Upload `presentation.tex`
4. Compile (should work with placeholders)

### Step 2: Create Diagrams

1. Open `diagrams_mermaid.md` in this project
2. For each diagram (8 total):
   - Go to [draw.io](https://app.diagrams.net/)
   - Insert → Advanced → Mermaid
   - Copy mermaid code from `diagrams_mermaid.md`
   - Paste and click "Insert"
   - Export as PNG (File → Export as → PNG)
   - Use transparent background
   - High resolution (1920x1080 recommended)

### Step 3: Add Diagrams to Presentation

#### Option A: Replace Placeholders (Recommended)

In Overleaf, replace placeholder blocks with:

```latex
\begin{center}
    \includegraphics[width=0.8\textwidth]{algorithm_flowchart.png}
\end{center}
```

#### Option B: Keep Placeholders

If you present without diagrams, the red placeholders clearly indicate where visuals belong.

---

## 📋 Diagram Checklist

### Required Diagrams (8 total):

- [ ] **DIAGRAM 1**: algorithm_flowchart.png
  - **Mermaid Code**: Section "DIAGRAM 1" in diagrams_mermaid.md
  - **Slide**: Frame "Original Algorithm: Overview"
  - **Purpose**: Show algorithm flow from start to end

- [ ] **DIAGRAM 2**: security_layers.png
  - **Mermaid Code**: Section "DIAGRAM 2" in diagrams_mermaid.md
  - **Slide**: Frame "Enhancement Strategy"
  - **Purpose**: Show 3-layer security architecture

- [ ] **DIAGRAM 3**: system_architecture.png
  - **Mermaid Code**: Section "DIAGRAM 3" in diagrams_mermaid.md
  - **Slide**: Frame "System Architecture"
  - **Purpose**: Show component hierarchy and interactions

- [ ] **DIAGRAM 4**: embedding_flow.png
  - **Mermaid Code**: Section "DIAGRAM 4" in diagrams_mermaid.md
  - **Slide**: Frame "Embedding Process"
  - **Purpose**: Show data flow during embedding

- [ ] **DIAGRAM 5**: extraction_flow.png
  - **Mermaid Code**: Section "DIAGRAM 5" in diagrams_mermaid.md
  - **Slide**: Frame "Extraction Process"
  - **Purpose**: Show data flow during extraction

- [ ] **DIAGRAM 6**: quality_comparison.png
  - **Mermaid Code**: Section "DIAGRAM 6" in diagrams_mermaid.md
  - **Slide**: Frame "Results: Quality Metrics"
  - **Purpose**: Compare quality metrics across methods

- [ ] **DIAGRAM 7**: detection_comparison.png
  - **Mermaid Code**: Section "DIAGRAM 7" in diagrams_mermaid.md
  - **Slide**: Frame "Results: Steganalysis Resistance"
  - **Purpose**: Show detection rates for different methods

- [ ] **DIAGRAM 8**: visual_comparison.png
  - **Mermaid Code**: Section "DIAGRAM 8" in diagrams_mermaid.md (conceptual)
  - **Slide**: Frame "Visual Comparison"
  - **Purpose**: Side-by-side image comparison
  - **Note**: Replace with actual images from your experiments

---

## 🎨 Creating Diagrams in draw.io

### Method 1: Using Mermaid (Recommended)

1. Open [app.diagrams.net](https://app.diagrams.net/)
2. Click **Arrange** → **Insert** → **Advanced** → **Mermaid...**
3. Copy mermaid code from `diagrams_mermaid.md`
4. Paste into dialog box
5. Click **Insert**
6. Adjust styling:
   - Click diagram to select
   - Use **Format Panel** (right side) to change colors, fonts
   - Resize as needed
7. Export:
   - **File** → **Export as** → **PNG...**
   - Check **Transparent Background**
   - Set **Zoom**: 200-300% for high quality
   - **Border Width**: 5-10
   - Click **Export**
8. Save with correct filename (e.g., `algorithm_flowchart.png`)

### Method 2: Using Mermaid Live Editor

1. Go to [mermaid.live](https://mermaid.live/)
2. Paste mermaid code in left panel
3. View rendered diagram on right
4. Click **Download** → **PNG**
5. May need to edit in draw.io for better styling

---

## 📦 Uploading Diagrams to Overleaf

### Option 1: Direct Upload

1. In Overleaf project, click **Upload** icon (top left)
2. Select all PNG files
3. They'll appear in file list
4. Update `\includegraphics` commands with filenames

### Option 2: Organized Folder

1. In Overleaf, create new folder: "images"
2. Upload all PNG files to "images" folder
3. Update `\includegraphics` commands:
   ```latex
   \includegraphics[width=0.8\textwidth]{images/algorithm_flowchart.png}
   ```

---

## 🔧 Customizing the Presentation

### Change Theme

Replace in preamble:
```latex
\usetheme{Madrid}
\usecolortheme{default}
```

With other themes:
- `\usetheme{Berkeley}` - sidebar navigation
- `\usetheme{Copenhagen}` - clean and minimal
- `\usetheme{Warsaw}` - classic academic
- `\usecolortheme{dolphin}` - blue tones
- `\usecolortheme{crane}` - orange tones

### Adjust Aspect Ratio

Change from 16:9 to 4:3:
```latex
\documentclass[aspectratio=43]{beamer}
```

### Font Size

Change code font size:
```latex
\begin{lstlisting}[..., basicstyle=\scriptsize\ttfamily]
```

Options: `\tiny`, `\scriptsize`, `\footnotesize`, `\small`, `\normalsize`

---

## 📝 Editing Placeholders

### Find and Replace Placeholder

Search for:
```latex
\fbox{\parbox{0.8\textwidth}{\centering
    \textcolor{red}{[DIAGRAM PLACEHOLDER 1: Algorithm Flowchart]} \\
    \textit{Insert algorithm\_flowchart.png here}
}}
```

Replace with:
```latex
\includegraphics[width=0.85\textwidth]{algorithm_flowchart.png}
```

### Add Caption (Optional)

```latex
\begin{figure}
    \centering
    \includegraphics[width=0.8\textwidth]{algorithm_flowchart.png}
    \caption{Adaptive LSB-MSB Algorithm Flowchart}
\end{figure}
```

---

## 🎯 Presentation Tips

### Before the Presentation

1. **Compile Successfully**: Ensure no LaTeX errors
2. **Preview All Slides**: Check layout and text overflow
3. **Test Transitions**: Beamer has built-in navigation
4. **Print Handouts**: Generate PDF with notes
5. **Practice Timing**: 15-20 minutes recommended

### During the Presentation

1. **Use Arrow Keys**: Navigate slides
2. **Use Overview**: Press `Ctrl+Shift+O` (Overleaf) for slide overview
3. **Highlight Key Points**: Use laser pointer on diagrams
4. **Refer to Code**: Explain code snippet on demo slide
5. **Interactive Demo**: Consider live demo after slides

### Slide-by-Slide Guide

| Slide | Duration | Key Points |
|-------|----------|------------|
| Title | 30s | Introduce team and project |
| Outline | 30s | Quick overview |
| Motivation | 2min | Why steganography matters |
| Research Paper | 2min | Paper details and contributions |
| Problem | 1min | What we're solving |
| Original Algorithm | 3min | **IMPORTANT**: Explain with DIAGRAM 1 |
| MSB Cases | 2min | Show table, explain adaptive nature |
| Mean-of-Medians | 1.5min | Mathematical explanation |
| Enhancements | 2min | AES-CTR + Edge-adaptive (DIAGRAM 2) |
| Edge-Adaptive | 2min | Sobel, HVS explanation |
| System Architecture | 1.5min | Show DIAGRAM 3, explain modules |
| Embedding Process | 1.5min | Walk through DIAGRAM 4 |
| Extraction Process | 1.5min | Walk through DIAGRAM 5 |
| Evaluation Metrics | 1.5min | Define each metric |
| Results (Quality) | 2min | **IMPORTANT**: Discuss table + DIAGRAM 6 |
| Results (Steganalysis) | 2min | **IMPORTANT**: Show resistance (DIAGRAM 7) |
| Visual Comparison | 1min | Show actual images |
| Live Demo | 3min | Run main.py if possible |
| Code Snippet | 1min | Briefly explain key code |
| Achievements | 1.5min | Summarize what was done |
| Evaluation | 1min | Comprehensive framework |
| Impact | 1.5min | Academic + practical value |
| Limitations | 1.5min | Be honest about trade-offs |
| Conclusion | 1min | Strong closing |
| Q&A | 5min | Answer questions |

**Total**: ~18-20 minutes (+ Q&A)

---

## 🛠️ Troubleshooting

### LaTeX Compilation Errors

**Error**: `Package graphicx Error: File not found`
- **Fix**: Ensure PNG files are uploaded to Overleaf
- **Fix**: Check filename spelling (case-sensitive)

**Error**: `Undefined control sequence`
- **Fix**: Ensure all packages are in preamble
- **Fix**: Check for typos in commands

**Error**: `Overfull \hbox`
- **Fix**: Reduce text or use `\small` font
- **Fix**: Break long words with `\-` (hyphenation)

### Mermaid Rendering Issues

**Issue**: Diagram too large
- **Fix**: Reduce text in nodes
- **Fix**: Use shorter labels
- **Fix**: Split into multiple diagrams

**Issue**: Arrows overlap
- **Fix**: Add manual routing with `-->` vs `-.->` vs `==>`
- **Fix**: Adjust layout in draw.io after import

**Issue**: Colors don't match
- **Fix**: Edit in draw.io after Mermaid import
- **Fix**: Use consistent color scheme

### Overleaf Issues

**Issue**: Slow compilation
- **Fix**: Use fast compile mode (draft)
- **Fix**: Reduce image resolution
- **Fix**: Comment out unused slides during editing

**Issue**: Can't upload files
- **Fix**: Check file size (< 50MB per file)
- **Fix**: Use PNG instead of PDF for images
- **Fix**: Compress images if too large

---

## 📤 Exporting Final Presentation

### PDF Export

1. In Overleaf: **Download PDF**
2. Name: `IS_Project_Presentation.pdf`

### With Notes (for Practice)

Add notes to frames:
```latex
\begin{frame}{Title}
    Content here
    \note{These are my speaking notes}
\end{frame}
```

Compile with notes:
```latex
\documentclass[aspectratio=169,notes]{beamer}
```

### Handouts (for Audience)

```latex
\documentclass[aspectratio=169,handout]{beamer}
```

---

## ✅ Pre-Presentation Checklist

- [ ] All diagrams created and uploaded
- [ ] Presentation compiles without errors
- [ ] All placeholders replaced
- [ ] Tables formatted correctly
- [ ] Code snippets readable
- [ ] Team member names correct
- [ ] Institution name updated
- [ ] References complete
- [ ] PDF exported
- [ ] Practiced timing (15-20 min)
- [ ] Demo environment tested
- [ ] Backup plan prepared

---

## 🎓 Additional Resources

### Beamer Resources
- [Beamer User Guide](https://ctan.org/pkg/beamer)
- [Beamer Theme Gallery](https://mpetroff.net/files/beamer-theme-matrix/)
- [Overleaf Beamer Tutorial](https://www.overleaf.com/learn/latex/Beamer)

### Mermaid Resources
- [Mermaid Documentation](https://mermaid.js.org/)
- [Mermaid Live Editor](https://mermaid.live/)
- [Mermaid Examples](https://mermaid.js.org/ecosystem/integrations.html)

### Presentation Skills
- Keep slides concise (6-8 words per bullet)
- Use diagrams over text
- Practice smooth transitions
- Engage with audience
- Time for Q&A

---

## 🎉 You're Ready!

Your presentation package includes:
- ✅ Professional LaTeX Beamer presentation
- ✅ 8 Mermaid diagram codes ready to render
- ✅ Clear placeholders for easy insertion
- ✅ Comprehensive content covering all aspects
- ✅ This detailed guide

**Good luck with your presentation!** 🚀

---

**Need Help?**
- Overleaf has built-in chat support
- draw.io has extensive documentation
- Mermaid community on GitHub

**Last Updated**: December 19, 2025
