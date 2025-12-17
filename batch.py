#!/usr/bin/env python3
import os
import sys
import argparse
import glob
import subprocess

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(THIS_DIR, "input")
OUTPUT_DIR = os.path.join(THIS_DIR, "output")


def list_images(folder: str):
    patterns = [
        "*.jpg", "*.jpeg", "*.png", "*.bmp",
        "*.tiff", "*.tif", "*.webp",
        "*.cr2", "*.nef", "*.arw", "*.raf", "*.rw2"
    ]
    files = []
    for p in patterns:
        files.extend(glob.glob(os.path.join(folder, p)))
    return sorted(files)


def main():
    parser = argparse.ArgumentParser(description="Run Sea-Thru on first N images from input/ to output/. Only pass flags if explicitly provided.")
    parser.add_argument("N", type=int, help="Number of images to process")
    # Optional flags to forward to seathru-mono-e2e.py when explicitly provided
    parser.add_argument("--size", type=int, default=None)
    parser.add_argument("--model-name", type=str, default=None)
    parser.add_argument("--f", type=float, default=None)
    parser.add_argument("--l", type=float, default=None)
    parser.add_argument("--p", type=float, default=None)
    parser.add_argument("--min-depth", type=float, default=None)
    parser.add_argument("--max-depth", type=float, default=None)
    parser.add_argument("--spread-data-fraction", type=float, default=None)
    parser.add_argument("--raw", action="store_true")
    parser.add_argument("--no-cuda", action="store_true")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    images = list_images(INPUT_DIR)
    if not images:
        print(f"No images found in {INPUT_DIR}")
        sys.exit(1)

    to_process = images[: args.N]
    print(f"Processing {len(to_process)} image(s) from {INPUT_DIR} -> {OUTPUT_DIR}")

    script = os.path.join(THIS_DIR, "run.py")
    for idx, img_path in enumerate(to_process, 1):
        base = os.path.splitext(os.path.basename(img_path))[0]
        out_path = os.path.join(OUTPUT_DIR, f"{base}.png")
        cmd = [sys.executable, script, "--input", img_path, "--output", out_path]
        # Append only explicitly provided flags (None means not provided)
        if args.size is not None:
            cmd.extend(["--size", str(args.size)])
        if args.model_name is not None:
            cmd.extend(["--model-name", args.model_name])
        if args.f is not None:
            cmd.extend(["--f", str(args.f)])
        if args.l is not None:
            cmd.extend(["--l", str(args.l)])
        if args.p is not None:
            cmd.extend(["--p", str(args.p)])
        if args.min_depth is not None:
            cmd.extend(["--min-depth", str(args.min_depth)])
        if args.max_depth is not None:
            cmd.extend(["--max-depth", str(args.max_depth)])
        if args.spread_data_fraction is not None:
            cmd.extend(["--spread-data-fraction", str(args.spread_data_fraction)])
        if args.raw:
            cmd.append("--raw")
        if args.no_cuda:
            cmd.append("--no-cuda")

        print(f"[{idx}/{len(to_process)}] Running: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed on {img_path}: {e}")

    print("Done.")


if __name__ == "__main__":
    main()
