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

### Single Image Processing

Process one underwater photo (automatically saves to `output/` folder):

```bash
python run.py --input my_photo.jpg
```

Or specify a custom output location:

```bash
python run.py --input my_photo.jpg --output fixed_photo.png
```

### Batch Processing

Process multiple images from the `input/` folder:

```bash
# Process first 5 images from input/ folder
python batch.py 5
```

## Adjusting the Results

If your photo comes out too dark or too bright, here's what to change:

### Making it Brighter or Darker

**Use the `--f` flag** (default is 2.0):

```bash
# Too dark? Make it brighter by lowering --f
python run.py --input photo.jpg --f 1.0

# Too bright? Make it darker by raising --f
python run.py --input photo.jpg --f 3.5
```

**Remember:** Bigger number = darker photo, smaller number = brighter photo

### All Available Settings

Here's every setting you can change (with their default values):

```bash
python run.py \
  --input photo.jpg \                    # Your underwater photo (REQUIRED)
  --output result.png \                  # Where to save result (default: output/{input_name}.png)
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
python run.py --input underwater.jpg
```

### Photo came out too dark
```bash
python run.py --input underwater.jpg --f 1.2
```

### Photo came out too bright
```bash
python run.py --input underwater.jpg --f 3.0
```

### Shallow, clear water (needs less correction)
```bash
python run.py --input shallow.jpg --f 1.5 --l 0.4
```

### Deep, murky water (needs more correction)
```bash
python run.py --input deep.jpg --f 3.0 --l 0.7
```

### Quick test (lower resolution = faster)
```bash
python run.py --input test.jpg --size 1024
```

### Batch process multiple images
```bash
# Process first 10 images from input/ folder
python batch.py 10

# Batch process with custom settings
python batch.py 5 --f 2.5 --size 1024
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

