# Trigram Stimulus Generator

Generate unique, non-repeating letter trigrams, render them as image stimuli in multiple fonts with fixation markers, and export a stimulus manifest for use in psychophysics or readability experiments. Includes a small utility to split MNREAD-style sentences into fixed-length lines.

## Features

- **Trigram list generation** with no repeated letters per trigram and no duplicate trigrams across the list.  
- **Image rendering** for each trigram across screen positions with green fixation ellipses (plus optional blank “red/green” marker images). Exports both PNGs and a consolidated CSV stimulus sheet.
- **Font metrics aware**: computes x-height from the font’s glyph data via `fontTools` to scale images and metadata consistently.
- **Config-driven**: pixel size, x-height, output dir, positions, and schema are set in `config_triagram.json`.
- **Sentence splitter**: quick helper to break sentences into three fixed-length lines for spreadsheets.

## Repository Structure

```
.
├─ config_triagram.json         # Global settings (render size, x-height, positions, output paths)
├─ generate_triagram.py         # Builds unique trigram CSVs (per-font if desired)
├─ generate_triagram_images.py  # Renders PNGs and writes stimulus CSV using config
├─ getFilesInDir.py             # Helper to list files in a folder
├─ divide_sentences.py          # Utility to split sentences into 3 fixed-length lines
└─ fonts/                       # (You add) .ttf/.otf files used for rendering
```

## Requirements

- Python 3.10+ (recommended)
- Packages:
  - `pillow`
  - `fonttools`
  - `pandas`

Install:

```bash
pip install pillow fonttools pandas
```

## Configuration

Edit `config_triagram.json` to set:

- `RENDER_PIXEL`: base font pixel size used for rendering
- `X_HEIGHT_CM`, `X_HEIGHT_DEGREE`, `X_HEIGHT_LOGMAR`: physical/visual metrics written into the stimulus sheet
- `DATA_OUT`: output directory for CSVs (default `.\\output\\`)
- `POS_COOR`: integer screen positions (1–11) along the x-axis
- `STIM_SHEET`: column schema for the output CSV

> **Note:** Paths currently use backslashes; adjust if running on macOS/Linux.

## How It Works

1. **Place fonts** (`.ttf`/`.otf`) in `./fonts/`.
2. **Generate trigram CSVs**:
   ```bash
   python generate_triagram.py
   ```
   Creates `triagram_list_<FONTNAME>.csv` for each font.
3. **Render images and manifest**:
   ```bash
   python generate_triagram_images.py
   ```
   Generates trigram images in `images/stim_list/<FONTNAME>/` and a metadata CSV in the output folder.
4. **(Optional)** Split MNREAD sentences:
   ```bash
   python divide_sentences.py
   ```
   Produces `output_with_lines.xlsx` with `line1`, `line2`, `line3`.

## Output

- `output/triagram_list_<FONTNAME>.csv` — trigram list per font
- `images/stim_list/<FONTNAME>/stim_<TRI>_<POS>.PNG` — rendered images
- `output/stimulus_list_<FONTNAME>.csv` — CSV manifest with metadata
- `images/blank_red.PNG`, `images/blank_green.PNG` — blank markers

## Notes

- Alphabet omits “i” by default (`abcdefghjklmnopqrstuvwxyz`)
- No repeating letters within or across trigrams
- Positions determine orientation and visual angle
- Green fixation ellipses mark center points
- Ensure fonts expose a `glyf`, `CFF`, or `CFF2` table for x-height computation

## Troubleshooting

- **Font not found**: ensure fonts exist in `./fonts/`
- **No `glyf` table**: try another font
- **Missing CSV**: run `generate_triagram.py` before rendering

## License

Add your preferred license (e.g., MIT) here.