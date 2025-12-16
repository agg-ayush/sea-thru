# Sea-thru: Underwater Image Enhancement

Remove water color and restore underwater photos to look like they were taken on land.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download the Model

You need to download a depth estimation model (it helps figure out what's near and far in the photo):

```bash
mkdir -p models
cd models
wget https://storage.googleapis.com/niantic-lon-static/research/monodepth2/mono_1024x320.zip
unzip mono_1024x320.zip
cd ..
```

Your `models/` folder should look like this:
```
models/
└── mono_1024x320/
    ├── encoder.pth
    ├── depth.pth
    ├── pose_encoder.pth
    └── pose.pth
```

## Quick Start

Just point it at your underwater photo:

```bash
python seathru-mono-e2e.py --image my_photo.jpg --output fixed_photo.png
```

## Adjusting the Results

If your photo comes out too dark or too bright, here's what to change:

### Making it Brighter or Darker

**Use the `--f` flag** (default is 2.0):

```bash
# Too dark? Make it brighter by lowering --f
python seathru-mono-e2e.py --image photo.jpg --f 1.0 --output brighter.png

# Too bright? Make it darker by raising --f
python seathru-mono-e2e.py --image photo.jpg --f 3.5 --output darker.png
```

**Remember:** Bigger number = darker photo, smaller number = brighter photo

### All Available Settings

Here's every setting you can change (with their default values):

```bash
python seathru-mono-e2e.py \
  --image input/photo.jpg \              # Your underwater photo (REQUIRED)
  --output output/result.png \           # Where to save result (default: output.png)
  --f 2.0 \                              # Brightness: lower = brighter, higher = darker
  --l 0.5 \                              # Color correction strength (0.0 to 1.0)
  --p 0.01 \                             # Detail vs smoothness (0.001 = sharp, 0.1 = smooth)
  --size 2048 \                          # Output size in pixels
  --min-depth 0.0 \                      # Ignore closest objects (0.0 to 1.0)
  --spread-data-fraction 0.05 \          # Processing precision (lower = more detail)
  --monodepth-add-depth 2.0 \            # Depth adjustment (advanced)
  --monodepth-multiply-depth 10.0        # Depth scaling (advanced)
```

## What Each Setting Does

### Basic Settings (You'll Use These)

**`--f`** (default: 2.0) - Brightness control
- Lower values (1.0, 0.5): Makes photo brighter
- Higher values (3.0, 4.0): Makes photo darker
- Start here if your photo looks wrong!

**`--l`** (default: 0.5) - How much to restore colors
- Lower (0.3): Gentle color correction
- Higher (0.8): Aggressive color restoration
- Use if reds and yellows look off

**`--p`** (default: 0.01) - Detail vs smooth look
- Lower (0.005): Keeps more detail, may look grainy
- Higher (0.05): Smoother look, may blur details

**`--size`** (default: 2048) - Output image size
- 1024: Fast processing, lower quality
- 2048: Good balance (recommended)
- 4096: High quality, slower processing

### Advanced Settings (Usually Don't Need to Change)

**`--min-depth`** (default: 0.0) - Exclude very close objects
- Range: 0.0 to 1.0
- Example: 0.1 ignores the closest 10% of the scene

**`--spread-data-fraction`** (default: 0.05) - Processing detail level
- Lower values: More detailed processing
- Higher values: Faster but less precise

**`--monodepth-add-depth`** (default: 2.0) - Baseline depth offset
**`--monodepth-multiply-depth`** (default: 10.0) - Depth range scaling
- Only change these if colors look really weird
- Try values between 8.0 and 15.0 for multiply

### Other Flags

**`--no-cuda`** - Use CPU instead of GPU (slower but works on any computer)
**`--raw`** - If your input is a RAW camera file (.NEF, .CR2, etc.)
**`--output-graphs`** - Save diagnostic images showing how the algorithm works

## Example Commands

### Basic usage (usually good enough)
```bash
python seathru-mono-e2e.py --image underwater.jpg --output result.png
```

### Photo came out too dark
```bash
python seathru-mono-e2e.py --image underwater.jpg --f 1.2 --output result.png
```

### Photo came out too bright
```bash
python seathru-mono-e2e.py --image underwater.jpg --f 3.0 --output result.png
```

### Shallow, clear water (needs less correction)
```bash
python seathru-mono-e2e.py --image shallow.jpg --f 1.5 --l 0.4 --output result.png
```

### Deep, murky water (needs more correction)
```bash
python seathru-mono-e2e.py --image deep.jpg --f 3.0 --l 0.7 --output result.png
```

### Quick test (lower resolution = faster)
```bash
python seathru-mono-e2e.py --image test.jpg --size 1024 --output quick_test.png
```

## Troubleshooting

**Photo is too dark**
→ Lower the `--f` value: try `--f 1.5` or `--f 1.0`

**Photo is too bright or washed out**
→ Raise the `--f` value: try `--f 2.5` or `--f 3.0`

**Colors look weird or unnatural**
→ Adjust `--l`: try `--l 0.3` (less) or `--l 0.7` (more)
→ Or adjust depth: try `--monodepth-multiply-depth 8.0` or `12.0`

**Image looks blotchy or uneven**
→ Increase `--p`: try `--p 0.05` for smoother results

**Processing is too slow**
→ Reduce size: use `--size 1024` or `--size 512`
→ Or use CPU mode if you think GPU is causing issues: add `--no-cuda`

